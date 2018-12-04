import pygame as pg
from pathlib import Path
import random
import math

WIDTH, HEIGHT = 1280, 720


class Game:
    def __init__(self):
        self.is_running = True
        self.won = False
        self.score = 0
        self.asteroid_sprites = pg.sprite.Group()
        self.missile_sprites = pg.sprite.Group()
        self.power_up_sprites = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()

        self.player_sprite = Player(WIDTH // 2, HEIGHT // 2)
        self.player.add(self.player_sprite)
        self.health_bar = HealthBar(self.player_sprite.health, (30, 30))
        self.space_pressed = False

    def add_random_asteroid(self):
        size = random.choices([5, 6, 7, 8, 9, 10, 11],
                              [8, 8, 5, 3, 2, 1, 1])[0]

        posx = random.randrange(0, WIDTH)
        posy = random.randrange(0, HEIGHT)

        vx = random.randint(size - 13, 13 - size)
        vy = random.randint(size - 13, 13 - size)

        angular_velocity = random.random() * 2 - 1

        self.asteroid_sprites.add(Asteroid(size, posx, posy, vx, vy, angular_velocity))

    def update(self):
        self.asteroid_sprites.update()
        self.missile_sprites.update()
        self.player.update()
        self.spawn_missiles()
        self.check_collisions()
        self.check_player_collision()
        self.check_power_up_collisions()
        if self.player_sprite.health < 0:
            self.is_running = False
        if not self.asteroid_sprites: # If there aren't any asteroids
            self.won = True
            self.is_running = False

    def check_collisions(self):
        collided_missiles = pg.sprite.groupcollide(self.missile_sprites, self.asteroid_sprites, True, False,
                                                   collided=pg.sprite.collide_circle)

        for value in collided_missiles.values():
            for asteroid in value:
                if asteroid.get_hit():
                    self.asteroid_sprites.add(asteroid.split())
                    self.score += 1

    def check_player_collision(self):
        player = self.player.sprites()[0]

        if player.invunticks > 0:
            return

        collided_asteroids = pg.sprite.groupcollide(self.player, self.asteroid_sprites, False, False,
                                                    collided=pg.sprite.collide_circle)

        for key, value in collided_asteroids.items():
            player = key
            asteroids = value
            for asteroid in asteroids:
                while not asteroid.get_hit():
                    pass
                self.asteroid_sprites.add(asteroid.split())

            player.health -= 1
            player.invunticks = 180

    def check_power_up_collisions(self):
        collided_powerups = pg.sprite.groupcollide(self.power_up_sprites, self.player, True, False,
                                                   collided=pg.sprite.collide_circle)

        for value in collided_powerups.values():
            for power_up in value:
                if power_up.effect == "HealthUp":
                    self.player_sprite.health += 1

    def spawn_missiles(self):
        keys = pg.key.get_pressed()
        if not keys[pg.K_SPACE]:
            if self.space_pressed:
                self.space_pressed = False
                player = self.player.sprites()[0]

                posx, posy = player.rect.center
                angle = player.angle
                new_missile = Missile(posx - 12 * math.sin(angle), posy - 12 * math.cos(angle), angle, 4,
                                      player.vx, player.vy)
                self.missile_sprites.add(new_missile)
        else:
            self.space_pressed = True

    def draw(self, screen):
        self.asteroid_sprites.draw(screen)
        self.missile_sprites.draw(screen)
        self.player.draw(screen)


# Where the assets should come from
assets_folder = Path("./assets/")

# Sprite images
asteroid_art = []
for image in (assets_folder / "asteroids").glob("*.png"):
    asteroid_art.append(image.as_posix())


class Missile(pg.sprite.Sprite):
    def __init__(self, xpos, ypos, angle, velocity, vx_i, vy_i):
        pg.sprite.Sprite.__init__(self)
        fixed_missile_image = pg.image.load((assets_folder / "missile.png").as_posix()).convert()
        self.image = pg.transform.rotate(fixed_missile_image, math.degrees(angle))
        self.image.set_colorkey((0, 0, 0))
        self.radius = 3
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.vx = -math.sin(angle) * velocity + vx_i
        self.vy = -math.cos(angle) * velocity + vy_i

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()


class Player(pg.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pg.sprite.Sprite.__init__(self)

        # TEMPORARY HEALTH CHANGE
        self.health = 5
        self.invunticks = 300

        self.fixed_image = pg.image.load((assets_folder / "ship.png").as_posix()).convert()
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
        self.image = pg.transform.rotate(self.fixed_image, math.degrees(self.angle))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = old_rect.center

    def make_blank(self):
        self.image.fill((0,0,0))

    def update(self):
        self.invunticks -= 1
        self.fix_angles()

        if self.invunticks > 0:
            if self.invunticks & 16:
                self.make_blank()

        self.rect.x += self.vx
        self.rect.y += self.vy

        # Slow reduction in acceleration over time.
        self.vx *= 0.97
        self.vy *= 0.97

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:  # Accelerate
            self.vx -= math.sin(self.angle) * 0.3
            self.vy -= math.cos(self.angle) * 0.3
        if keys[pg.K_s]:  # Decelerate
            self.vx += math.sin(self.angle) * 0.3
            self.vy += math.cos(self.angle) * 0.3
        if keys[pg.K_a]:
            self.angle += 0.1
        if keys[pg.K_d]:
            self.angle -= 0.1


class Asteroid(pg.sprite.Sprite):
    def __init__(self, size, xpos, ypos, xvel, yvel, rotation):
        pg.sprite.Sprite.__init__(self)
        # Size is essentially the width, times 10px
        self.fixed_image = pg.transform.smoothscale(
            pg.image.load(random.choice(asteroid_art)).convert(), (30 * size, 30 * size))
        self.fixed_image.set_colorkey((0, 0, 0))

        self.image = pg.transform.rotate(self.fixed_image, 0)
        self.rect = self.image.get_rect()
        self.radius = 15 * size

        if size < 4:
            self.health = 1
        elif size < 9:
            self.health = 2
        else:
            self.health = 3

        self.angv = math.atan(rotation / 5) * 5
        self.angle = 0
        self.rect.x = xpos
        self.rect.y = ypos

        # The Atan is used to smush the velocities down a bit if they are too fast.
        self.vx = math.atan(xvel / 8) * 8
        self.vy = math.atan(yvel / 8) * 8

        self.size = size

    def split(self):
        shards = []
        if self.size <= 2:
            return shards
        else:
            split_into = random.choices([1, 2, 3], [2, 10, 2])[0]
            for i in range(split_into):
                shards.append(
                    Asteroid(int(self.size / 1.3), self.rect.x, self.rect.y,
                             self.vx + random.randint(-3, 3), self.vy + random.randint(-3, 3),
                             self.angv + random.randint(-3, 3))
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


class PowerUp(pg.sprite.Sprite):

    def __init__(self, size, lifetime, image_name):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.smoothscale(
            pg.image.load((assets_folder / image_name).as_posix()).convert(), size
        )
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.lifetime = lifetime
        self.effect = ""

    def update(self, *args):
        if self.lifetime < 0:
            self.kill()
        else:
            self.lifetime -= 1


class HealthUp(PowerUp):

    def __init__(self, size=(30,30), lifetime=10):
        super().__init__(size, lifetime, "heart.png")
        self.effect = "HealthUp"
        self.rect.center = (300, 300)


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
