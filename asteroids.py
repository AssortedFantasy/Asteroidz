import pygame as pg
from pathlib import Path
import random
import math
import algorithms

# It would be nice to be able to circularly import things.
# but because of code order and imports happening first, that crashes things horribly.
WIDTH, HEIGHT = 1280, 720

# Where the assets should come from
assets_folder = Path("./assets/")

# Sprite images
asteroid_art = []
for image in (assets_folder / "asteroids").glob("*.png"):
    asteroid_art.append(image.as_posix())


class Game:
    def __init__(self):
        # Some state machine variables
        self.is_running = True
        self.is_ended = False
        self.won = False
        self.time_to_next = 180
        self.score = 0

        # Sprite groups used in the game
        self.asteroid_sprites = pg.sprite.Group()
        self.missile_sprites = pg.sprite.Group()
        self.power_up_sprites = pg.sprite.Group()
        self.line_sprites = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()

        # You spawn in the center of the map
        self.player_sprite = Player(WIDTH // 2, HEIGHT // 2)
        self.player.add(self.player_sprite)
        self.health_bar = HealthBar(self.player_sprite.health, (30, 30))
        self.space_pressed = False

        # Loading up some assets used.
        self.level_cleared = pg.image.load((assets_folder / "level_cleared.png").as_posix()).convert()
        self.level_cleared.set_colorkey((0, 0, 0))
        lx, ly = self.level_cleared.get_rect().center
        self.level_cleared_anchor = WIDTH//2 - lx, HEIGHT//2 - ly

    def add_random_asteroid(self):
        # The first array is the sizes, the second array is the probabilities.
        size = random.choices([5, 6, 7, 8, 9, 10, 11],
                              [8, 8, 5, 3, 2, 1, 1])[0]

        posx = random.randrange(0, WIDTH)
        posy = random.randrange(0, HEIGHT)

        vx = random.randint(size - 13, 13 - size)
        vy = random.randint(size - 13, 13 - size)

        angular_velocity = random.random() * 2 - 1

        self.asteroid_sprites.add(Asteroid(size, posx, posy, vx, vy, angular_velocity))

    def update(self):
        # Main update loop.
        self.asteroid_sprites.update()
        self.missile_sprites.update()
        self.line_sprites.update()
        self.power_up_sprites.update()
        self.player.update()

        self.spawn_missiles()
        self.check_asteroid_missile_collision()
        self.check_player_collision()
        self.check_power_up_collisions()

        if self.player_sprite.health < 0:  # If we die.
            self.is_ended = True
            self.player_sprite.kill()
        if not self.asteroid_sprites:  # If there aren't any asteroids left.
            self.won = True
            self.is_ended = True
        if self.is_ended:  # This delays the game ending a little bit.
            self.time_to_next -= 1
            if self.time_to_next < 0:
                self.is_running = False

    def roll_for_powerup(self, location):
        # Really generous in this case, makes the game fairly unbalanced. But is fun to play with.
        if random.randint(1, 6) >= 4:
            power = random.choice(ALL_POWER_UPS)
            self.power_up_sprites.add(power(location))

    def check_asteroid_missile_collision(self):
        collided_missiles = pg.sprite.groupcollide(self.asteroid_sprites, self.missile_sprites, False, True,
                                                   collided=pg.sprite.collide_circle)

        for asteroid, missiles in collided_missiles.items():
            for _ in missiles:
                if asteroid.get_hit():
                    # Sometimes asteroids drop powerups!
                    self.roll_for_powerup(asteroid.rect.center)
                    self.asteroid_sprites.add(asteroid.split())
                    self.score += 1
                    break

    def check_player_collision(self):
        player = self.player_sprite
        collided_asteroids = pg.sprite.groupcollide(self.player, self.asteroid_sprites, False, False,
                                                    collided=pg.sprite.collide_circle)

        for key, value in collided_asteroids.items():
            # I used a KMAP to solve this, no joke!
            if (not (player.invunticks > 0)) or player.impervious:
                player = key
                asteroids = value
                for asteroid in asteroids:
                    while not asteroid.get_hit():
                        pass

                    if player.impervious:  # You only get points if the player is impervious.
                        self.roll_for_powerup(asteroid.rect.center)
                        self.score += 1
                    self.asteroid_sprites.add(asteroid.split())

            if not (player.invunticks > 0):
                player.health -= 1
                player.invunticks = 120

    def check_power_up_collisions(self):
        collided_powerups = pg.sprite.groupcollide(self.player, self.power_up_sprites, False, True,
                                                   collided=pg.sprite.collide_circle)

        for value in collided_powerups.values():

            # All the code for the powerups is done right here instead of in the powerup
            # mainly because the powerups have effects which need data from the game.
            for power_up in value:
                if power_up.effect == "HealthUp":
                    self.player_sprite.health += 1

                elif power_up.effect == "Impervious":
                    self.player_sprite.impervious = 1
                    self.player_sprite.invunticks = 300

                elif power_up.effect == "Score":
                    self.score += 10

                elif power_up.effect == "Circle":
                    # Summon a circle of missiles around the player.
                    x, y = self.player_sprite.rect.center
                    missile_locations = algorithms.circle(x, y, 30)
                    missile_velocities = algorithms.circle(0, 0, 30)
                    angle_missiles = math.pi * 2 / len(missile_velocities)
                    degrees_90 = math.pi / 2

                    new_missiles = []
                    for i, loc, vel in zip(range(len(missile_velocities)), missile_locations, missile_velocities):
                        x, y = loc
                        vx, vy = vel

                        # By dividing by 3 we give them 10 velocity.
                        # Also the angles are 90 degrees out of phase and backwards because of reasons
                        new_missiles.append(Missile(x, y, -angle_missiles*i - degrees_90, vx/3, vy/3))
                    self.missile_sprites.add(new_missiles)

                elif power_up.effect == "Span":
                    # Rather complicated, Create a spanning tree over the map which shoots every asteroid at once.
                    points_to_hit = []
                    new_shards = []
                    for asteroid in self.asteroid_sprites:
                        points_to_hit.append(asteroid.rect.center)
                        if asteroid.get_hit():
                            self.score += 1
                            new_shards.extend(asteroid.split())
                    self.asteroid_sprites.add(new_shards)
                    points_to_hit.append(power_up.rect.center)

                    spanning_tree = algorithms.prims_algorithm(points_to_hit)
                    lines = []
                    for point in spanning_tree[1:]:
                        lines.append(Line(point.x, point.y, point.nearest.x, point.nearest.y))
                    self.line_sprites.add(lines)

    def spawn_missiles(self):
        keys = pg.key.get_pressed()
        if not keys[pg.K_SPACE]:
            if self.space_pressed:
                self.space_pressed = False
                player = self.player_sprite

                posx, posy = player.rect.center
                angle = player.angle

                # These might seem strange, but its because straight up and down is the negative y axis. Which is
                # what we chose as the reference angle (0). ( With Counterclockwise being positive ).
                hx = -math.sin(angle)
                hy = -math.cos(angle)

                new_missile = Missile(posx + 12*hx, posy + 12*hy, angle,
                                      player.vx + 4*hx, player.vy + 4*hy)
                self.missile_sprites.add(new_missile)
        else:
            self.space_pressed = True

    def draw(self, screen):
        self.asteroid_sprites.draw(screen)
        self.missile_sprites.draw(screen)
        self.power_up_sprites.draw(screen)
        self.player.draw(screen)
        screen.blit(self.health_bar.health_bar, (0, 0))
        for line in self.line_sprites:
            # Flashes, looks fairly lightning esque.
            if line.life & 16:
                pg.draw.line(screen, (255, 200, 0), line.p0, line.p1, line.life//10)
        if not self.asteroid_sprites:
            screen.blit(self.level_cleared, self.level_cleared_anchor)


class Missile(pg.sprite.Sprite):
    def __init__(self, xpos, ypos, angle, vx_i, vy_i):
        pg.sprite.Sprite.__init__(self)
        fixed_missile_image = pg.image.load((assets_folder / "missile.png").as_posix()).convert()
        self.image = pg.transform.rotate(fixed_missile_image, math.degrees(angle))
        self.image.set_colorkey((0, 0, 0))
        self.radius = 3
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.vx = vx_i
        self.vy = vy_i

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Missiles don't roll over edges!
        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()


class Player(pg.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pg.sprite.Sprite.__init__(self)

        # You only have 5 health! You spawn with some invulnerability though.
        self.health = 5
        self.invunticks = 210
        self.impervious = False

        self.fixed_image = pg.image.load((assets_folder / "ship.png").as_posix()).convert()
        self.impervious_image = pg.image.load((assets_folder / "ship_invunrable.png").as_posix()).convert()
        self.impervious_image.set_colorkey((0, 0, 0))
        self.fixed_image.set_colorkey((0, 0, 0))
        self.radius = 10

        self.image = pg.transform.rotate(self.fixed_image, 0)
        self.rect = self.image.get_rect()

        self.rect.x = xpos
        self.rect.y = ypos
        self.angle = 0
        self.vx = 0
        self.vy = 0

    def fix_angles(self):
        old_rect = self.rect
        if self.impervious:
            self.image = pg.transform.rotate(self.impervious_image, math.degrees(self.angle))
        else:
            self.image = pg.transform.rotate(self.fixed_image, math.degrees(self.angle))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = old_rect.center

    def make_blank(self):
        self.image.fill((0, 0, 0))

    def update(self):
        self.invunticks -= 1
        self.fix_angles()

        if self.invunticks > 0:
            if (not self.impervious) and (self.invunticks & 16):
                self.make_blank()
        else:
            self.impervious = False

        self.rect.x += self.vx
        self.rect.y += self.vy

        # Slow reduction in velocity over time.
        # This actually caps our speed as well.
        # When deltavx = 0.97*vx
        self.vx *= 0.97
        self.vy *= 0.97

        # Roll over the edges code
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT

        # Player controls for the missile.
        # Missile spawning is done in the game though.
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:  # Accelerate
            self.vx -= math.sin(self.angle) * 0.3
            self.vy -= math.cos(self.angle) * 0.3
        if keys[pg.K_s] or keys[pg.K_DOWN]:  # Accelerate in reverse
            self.vx += math.sin(self.angle) * 0.3
            self.vy += math.cos(self.angle) * 0.3
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.angle += 0.1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.angle -= 0.1


class Asteroid(pg.sprite.Sprite):
    def __init__(self, size, xpos, ypos, xvel, yvel, angular_velocity):
        pg.sprite.Sprite.__init__(self)

        # Size is essentially width + 1, times 10px
        # The plus one is because too small asteroids make the game unfun to play.
        self.fixed_image = pg.transform.smoothscale(
            pg.image.load(random.choice(asteroid_art)).convert(), (int(30 * (size+1)), int(30 * (size+1))))
        self.fixed_image.set_colorkey((0, 0, 0))

        self.image = pg.transform.rotate(self.fixed_image, 0)
        self.rect = self.image.get_rect()
        self.radius = int(15 * (size+1))

        if size < 4:
            self.health = 1
        elif size < 9:
            self.health = 2
        else:
            self.health = 3

        self.angv = math.atan(angular_velocity / 5) * 5
        self.angle = 0
        self.rect.x = xpos
        self.rect.y = ypos

        # The Atan is used to smush the velocities down a bit if they are too fast.
        # so velocities actually will be between -8 and 8.
        self.vx = math.atan(xvel / 8) * 8
        self.vy = math.atan(yvel / 8) * 8

        self.size = size

    def split(self):
        shards = []
        # Small asteroids don't split
        if self.size <= 2:
            return shards
        else:
            # We will split into one, two or three new asteroids.
            # They are our size / 1.3 in size.
            split_into = random.choices([1, 2, 3], [2, 10, 2])[0]
            for i in range(split_into):
                # The new asteroids are somewhere between 1.5 to 1.75 times smaller.
                new_size = self.size / (1.5 + random.random() / 4)
                x, y = self.rect.center
                shards.append(
                    Asteroid(new_size, x, y,
                             self.vx + random.random()*6 - 3, self.vy + random.random()*6 - 3,
                             self.angv + random.random()*6 - 3)
                )
            return shards

    def get_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        else:
            return False

    def rotate_image(self):
        old_rect = self.rect
        self.image = pg.transform.rotate(self.fixed_image, math.degrees(self.angle))
        self.rect = self.image.get_rect()
        self.rect.center = old_rect.center

    def update(self):
        self.angle += 0.02 * self.angv
        self.rotate_image()

        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT


# Base PowerUp class, other powerups are subclasses of this.
class PowerUp(pg.sprite.Sprite):
    def __init__(self, size, lifetime, image_name, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.smoothscale(
            pg.image.load((assets_folder / image_name).as_posix()).convert(), size
        )
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.effect = ""

    def update(self, *args):
        if self.lifetime < 0:
            self.kill()
        else:
            self.lifetime -= 1


class HealthUp(PowerUp):
    def __init__(self, location):
        super().__init__((46, 30), 600, "health.png", location)
        self.effect = "HealthUp"


class CircleMissiles(PowerUp):
    def __init__(self, location):
        super().__init__((46, 30), 600, "circle_missile.png", location)
        self.effect = "Circle"


class SpanningDestruction(PowerUp):
    def __init__(self, location):
        super().__init__((46, 30), 600, "bolt.png", location)
        self.effect = "Span"


class Impervious(PowerUp):
    def __init__(self, location):
        super().__init__((46, 30), 600, "invuln.png", location)
        self.effect = "Impervious"


class ScorePoints(PowerUp):
    def __init__(self, location):
        super().__init__((46, 30), 600, "score.png", location)
        self.effect = "Score"


class HealthBar:
    def __init__(self, health, size):
        self.fixed_image = pg.transform.smoothscale(
            pg.image.load((assets_folder / "heart.png").as_posix()).convert(), size
        )
        self.fixed_image.set_colorkey((0, 0, 0))
        self.health_bar = pg.Surface((size[0] * (health + 1), size[1]))
        self.health_bar.fill((0, 0, 0))
        for i in range(health + 1):
            self.health_bar.blit(self.fixed_image, (size[0] * i, 0))

    def update_health(self, health):
        self.health_bar.fill((0, 0, 0))
        for i in range(health + 1):
            self.health_bar.blit(self.fixed_image, (self.fixed_image.get_rect().size[0] * i, 0))


# This exists to be used by the lightning powerup
class Line(pg.sprite.Sprite):
    def __init__(self, x0, y0, x1, y1):
        pg.sprite.Sprite.__init__(self)
        self.life = 64
        self.p0 = x0, y0
        self.p1 = x1, y1

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()


# ALL_POWER_UPS = [CircleMissiles]
# This list is used to create powerups
ALL_POWER_UPS = [HealthUp, SpanningDestruction, Impervious, ScorePoints, CircleMissiles]
