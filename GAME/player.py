import pygame as pg
import settings

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        # Set animation modes
        self.action = "Idle"
        self.direction = "Right"

        # Load animation sets
        self.animationSets = {}
        self.animationSets['Idle'] = {}
        self.animationSets['Idle']['Right'] = self.loadAnimationFrames('Knight', 'Idle', 'Right')
        self.animationSets['Idle']['Left'] = self.loadAnimationFrames('Knight', 'Idle', 'Left')
        self.animationSets['Walk'] = {}
        self.animationSets['Walk']['Right'] = self.loadAnimationFrames('Knight', 'Walk', 'Right')
        self.animationSets['Walk']['Left'] = self.loadAnimationFrames('Knight', 'Walk', 'Left')
        self.animationSets['Jump'] = {}
        self.animationSets['Jump']['Right'] = self.loadAnimationFrames('Knight', 'Jump', 'Right')
        self.animationSets['Jump']['Left'] = self.loadAnimationFrames('Knight', 'Jump', 'Left')
        self.animationSets['Dead'] = {}
        self.animationSets['Dead']['Right'] = self.loadAnimationFrames('Knight', 'Dead', 'Right')
        self.animationSets['Dead']['Left'] = self.loadAnimationFrames('Knight', 'Dead', 'Left')

        self.image = self.animationSets[self.action][self.direction][0]
        self.rect = self.image.get_rect()
        self.radius = 0
        self.rect.center = (480, settings.SCREENHEIGHT / 4)
        self.position = vec(480, settings.SCREENHEIGHT / 4)

        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.frameCounter = 0
        self.jumping = False
        self.dead = False

    def update(self):
        self.rect.centerx = int(self.position.x)

        if self.game.status == settings.STATUS_RUNNING:
            self.enemyHit()
            if self.game.status == settings.STATUS_RUNNING:
                self.performRun()
        else:
            self.velocity.x = 0
            self.acceleration = vec(0, 0)
            self.performDying()

        if not self.dead:
            if self.game.status == settings.STATUS_DYING:
                self.frameCounter += 0.5
            else:
                self.frameCounter += 1

            if self.frameCounter >= 40:
                if self.action == 'Dead':
                    self.dead = True
                    self.game.status = settings.STATUS_DEAD
                    self.frameCounter = 39
                else:
                    self.frameCounter = 0

    def jump(self):
        if not self.jumping:
            # Check if we are standing on a platform, if so.... Jump
            self.rect.y += 5
            platformHits = pg.sprite.spritecollide(self, self.game.walls, False)
            self.rect.y -= 5
            if platformHits:
                if self.rect.bottom >= platformHits[0].rect.top:
                    self.velocity.y = -settings.JUMP_HEIGHT
                    self.jumping = True
                    self.action = "Jump"
                    self.game.frameCounter = 0
                    # platformHits[0].image.fill(settings.GREEN)

    def loadAnimationFrames(self, asset, mode, direction):
        animatedSet = []
        for frameNo in range(1, 11):
            fileName = 'Assets/{0}/{1} ({2}).png'.format(asset, mode, frameNo)
            animatedImage = pg.image.load(fileName)  # .convert()
            if direction == 'Left':
                animatedImage = pg.transform.flip(animatedImage, True, False)
            # tileImage.set_colorkey(settings.WHITE)
            animatedSet.append(animatedImage)
        return animatedSet

    def performRun(self):
        wallHits = pg.sprite.spritecollide(self, self.game.walls, False)
        if wallHits:
            for wall in wallHits:
                if wall.rect.top < self.rect.bottom:
                    # wall.image.fill(settings.BLUE)
                    self.acceleration.x = 0
                    if self.velocity.x < 0:
                        self.rect.left = wall.rect.right
                        self.velocity.x = 0
                    elif self.velocity.x > 0:
                        self.rect.right = wall.rect.left
                        self.velocity.x = 0

        self.gravityCheck()
        self.getNextAnimation()
        self.acceleration = vec(0, settings.GRAVITY)

        keys = pg.key.get_pressed()
        if not self.jumping:
            self.action = "Idle"

        if keys[pg.K_LEFT]:
            self.acceleration.x = -settings.PLAYER_ACCELERATION
            self.direction = "Left"
            if not self.jumping:
                self.action = "Walk"

        if keys[pg.K_RIGHT]:
            self.acceleration.x = settings.PLAYER_ACCELERATION
            self.direction = "Right"
            if not self.jumping:
                self.action = "Walk"

        if keys[pg.K_SPACE]:
            self.jump()

        self.calculateNewPosition()

    def getNextAnimation(self):
        animatedFrameNo = int(self.frameCounter // 4)
        self.image = self.animationSets[self.action][self.direction][animatedFrameNo]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.center = self.position
        # self.rect.inflate_ip(-30,-30)

    def performDying(self):
        self.gravityCheck()
        self.getNextAnimation()
        self.calculateNewPosition()

    def calculateNewPosition(self):
        # Apply Friction
        self.velocity.x += self.velocity.x * settings.PLAYER_FRICTION

        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

        # Equation of Motion
        self.velocity += self.acceleration
        self.position += self.velocity  # + 0.5 * self.acceleration

    def gravityCheck(self):
        self.rect.centery = int(self.position.y)

        if self.velocity.y > 0:
            platformHits = pg.sprite.spritecollide(self, self.game.walls, False)
            if platformHits:
                if self.rect.bottom < (platformHits[0].rect.top + (self.velocity.y * 1.1)):
                    # platformHits[0].image.fill(settings.RED)
                    self.rect.bottom = platformHits[0].rect.top
                    self.velocity.y = 0
                    self.jumping = False

        self.position = self.rect.center

    def enemyHit(self):
        enemyHits = pg.sprite.spritecollide(self, self.game.enemies, False, pg.sprite.collide_circle)
        if enemyHits:
            self.game.status = settings.STATUS_DYING
            self.action = "Dead"
            self.velocity = vec(0, 0)
            self.frameCounter = 0

