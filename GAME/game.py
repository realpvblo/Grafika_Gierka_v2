import pygame as pg
import random
import settings
import player
# import player, coin, playerLife, coinCapture
# import wall, rock, axe, fireball, ninja, ninjaGirl
# import levels

vec = pg.math.Vector2


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()

        self.screen = pg.display.set_mode((settings.SCREENWIDTH, settings.SCREENHEIGHT))
        self.stage = pg.Surface((settings.STAGEWIDTH, settings.STAGEHEIGHT))
        # self.stageBkGrd = pg.Surface((settings.STAGEWIDTH,settings.STAGEHEIGHT))
        pg.display.set_caption(settings.TITLE)

        self.clock = pg.time.Clock()
        self.running = True

        self.chapter = ""
        self.mapData = []
        # self.mapBkGrdData = []
        self.frameCounter = 0
        self.animatedFrameNo = 0
        self.TickCounter = 0
        self.showHitBoxes = False
        self.scroll = vec(0, 0)
        # self.scrollBkGrd = vec(0,0)
        self.allEnemies = []
        self.status = ''
        self.dead = False
        self.bonusLife = False

        # LoadImgTiles
        self.tileSet = {}
        for tileNo in range(1, 266):
            fileName = 'Assets/Tiles/medievalTile_{:03d}.png'.format(tileNo)
            tileImage = pg.image.load(fileName)  # .convert()
            # tileImage.set_colorkey(settings.WHITE)
            self.tileSet['{:03d}'.format(tileNo)] = tileImage

    def new(self):
        self.NoOfLives = 4
        self.score = 0
        self.TotalNumberOfCoinsAquired = 0

    def nextChapter(self, chapter):
        # Starts a new game
        self.setUpSpriteGroups()
        self.chapter = chapter

        self.clearOutSpriteGroups()

        self.setUpLivesRemaining()

        self.setUpCoinsAquired()

        leveling = levels.Level(self.chapter)
        leveling.loadCurrentLevel()
        self.allEnemies = leveling.allEnemies
        self.mapData = self.load_map(leveling.levelMap)

        self.generateScreenMap()

        for ninjaGirls in leveling.allNinjaGirls:
            ninjaGirl1 = ninjaGirl.NinjaGirl(self, ninjaGirls['WallPosition'], ninjaGirls['DelayStart'],
                                             ninjaGirls['FreqSecs'], ninjaGirls['Direction'])
            self.enemies.add(ninjaGirl1)
            self.allSprites.add(ninjaGirl1)

        # self.mapBkGrdData = self.load_map('MapBack')

        # # Generate Screen Map
        # tileY = 0
        # for layer in self.mapBkGrdData:
        #     tileX = 0
        #     for tile in layer:
        #         if tile != '000':
        #                 background = wall.Platform(tileX*70, tileY*70, 70, 70, tileSet[tile])
        #                 #self.allSprites.add(background)
        #                 self.background.add(background)
        #         tileX += 1
        #     tileY +=1

        # Create Sprites
        # Add Player
        self.goal = coin.Coin(self, 2180, 110, 70)
        self.allSprites.add(self.goal)

        self.player = player.Player(self)
        self.allSprites.add(self.player)

        self.addEnemiesSpritePools()

        ninja1 = ninja.Ninja(self)
        self.allSprites.add(ninja1)
        self.enemies.add(ninja1)

        # Add any other sprites
        self.status = settings.STATUS_RUNNING
        self.run()

    def run(self):
        self.playing = True

        while self.playing:
            self.clock.tick(settings.FPS)
            self.frameCounter += 1
            if self.frameCounter == 40:
                self.frameCounter = 0
            self.animatedFrameNo = (self.frameCounter // 4)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop Events Handler
        for event in pg.event.get():
            # print (event)

            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.showHitBoxes = not self.showHitBoxes

    def update(self):
        # Game Lopp Updates
        # sprite.update

        if self.status == settings.STATUS_RUNNING:
            self.ActivateSprites()
            self.DidWeReachGoal()
        elif self.status == settings.STATUS_DYING:
            self.ActivateSprites()
            if self.player.dead:
                self.TickCounter = 0
        elif self.status == settings.STATUS_DEAD:
            self.TickCounter += 1
            if self.TickCounter > 60:
                self.playing = False
                self.dead = True
                self.TotalNumberOfCoinsAquired = 0
                self.NoOfLives -= 1
        # elif self.status == settings.STATUS_OUTOFLIVES:
        #     self.ActivateSprites()
        # elif self.status == settings.STATUS_GOALGOT:
        #     self.ActivateSprites()

        self.allSprites.update()

    def draw(self):
        # Game Lopp Drawing routine
        self.stage.fill(settings.BLACK)
        # self.screen.fill(settings.BLACK)
        self.allSprites.draw(self.stage)
        self.enemies.draw(self.stage)
        # self.background.draw(self.stageBkGrd)

        if self.showHitBoxes:
            for sprite in self.enemies:
                pg.draw.rect(self.stage, settings.RED, sprite.rect, 1)
                pg.draw.circle(self.stage, settings.RED, sprite.rect.center, sprite.radius, 1)

            pg.draw.rect(self.stage, settings.BLUE, self.player.rect, 1)
            pg.draw.rect(self.stage, settings.BLUE, (self.player.rect.center, (4, 4)), 0)
            pg.draw.circle(self.stage, settings.BLUE, self.player.rect.center, self.player.radius, 1)
            pg.draw.rect(self.stage, settings.BLUE, self.goal.rect, 1)
            pg.draw.circle(self.stage, settings.BLUE, self.goal.rect.center, self.goal.radius, 1)

        self.scroll.x += -(self.player.position.x + self.scroll.x - (settings.SCREENWIDTH / 2)) / 20
        self.scroll.y += -(self.player.position.y + self.scroll.y - (settings.SCREENHEIGHT / 2)) / 20

        self.drawText(self.stage, settings.TEXT_FONT, "Lives:", 18, -self.scroll.x + 10, 0)
        self.drawText(self.stage, settings.TEXT_FONT, ":SuperBonus", 18, -self.scroll.x + settings.SCREENWIDTH - 110, 0)

        self.screen.blit(self.stage, self.scroll)

        pg.display.flip()

    def showStartScreen(self):
        # Start Splash Screen of the game
        pass

    def showGameOverScreen(self):
        self.screen = pg.display.set_mode((settings.SCREENWIDTH, settings.SCREENHEIGHT))
        self.drawText(self.screen, settings.TEXT_FONT, "THATS IT", 42, settings.SCREENWIDTH * .4,
                      settings.SCREENHEIGHT * .45)
        self.drawText(self.screen, settings.TEXT_FONT, "Your DEAD!!", 30, settings.SCREENWIDTH * .45,
                      settings.SCREENHEIGHT * .65)
        pg.display.flip()
        pg.time.wait(1000)

    def showLevelStartScreen(self, level):
        self.screen = pg.display.set_mode((settings.SCREENWIDTH, settings.SCREENHEIGHT))
        self.drawText(self.screen, settings.TEXT_FONT, "GET READY", 42, settings.SCREENWIDTH * .4,
                      settings.SCREENHEIGHT * .45)
        self.drawText(self.screen, settings.TEXT_FONT, "Level {:02d}".format(level), 30, settings.SCREENWIDTH * .45,
                      settings.SCREENHEIGHT * .65)
        pg.display.flip()
        pg.time.wait(1000)

    def showBonusLife(self):
        self.screen = pg.display.set_mode((settings.SCREENWIDTH, settings.SCREENHEIGHT))
        self.drawText(self.screen, settings.TEXT_FONT, "EXTRA LIFE", 42, settings.SCREENWIDTH * .4,
                      settings.SCREENHEIGHT * .45)
        pg.display.flip()
        pg.time.wait(1000)

    def load_map(self, path):
        # loads a screen map from file
        mapData = []
        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        for row in data:
            mapData.append(row.split('|'))
        return mapData

    def ActivateSprites(self):
        for enemy in self.allEnemies:
            enemy.update()
            if enemy.newSpriteNeeded:
                enemy.newSpriteNeeded = False
                if enemy.type == "Rocks":
                    for rock in self.rocks:
                        if not rock.active and rock.size == enemy.size:
                            rock.reactivateSprite(enemy.height, enemy.direction, enemy.speed)
                            break
                elif enemy.type == "FireBalls":
                    for fireball in self.fireballs:
                        if not fireball.active:
                            fireball.reactivateSprite(enemy.height, enemy.direction, enemy.speed, enemy.set)
                            break
                elif enemy.type == "Axes":
                    for axe in self.axes:
                        if not axe.active:
                            axe.reactivateSprite(enemy.height, enemy.direction, enemy.speed, enemy.set)
                            break

    def DidWeReachGoal(self):
        if pg.sprite.collide_circle(self.player, self.goal):
            self.playing = False
            self.dead = False
            self.TotalNumberOfCoinsAquired += 1
            if self.TotalNumberOfCoinsAquired == 5:
                self.bonusLife = True
                self.NoOfLives += 1
                self.TotalNumberOfCoinsAquired = 0

    def setUpSpriteGroups(self):
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.artifacts = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.fireballs = pg.sprite.Group()
        self.axes = pg.sprite.Group()
        self.background = pg.sprite.Group()

    def clearOutSpriteGroups(self):
        self.allSprites.empty()
        self.walls.empty()
        self.artifacts.empty()
        self.allEnemies.clear()
        self.rocks.empty()
        self.enemies.empty()
        self.fireballs.empty()
        self.axes.empty()

    def setUpLivesRemaining(self):
        for lives in range(1, self.NoOfLives + 1):
            life = playerLife.PlayerLife(self, lives * 40, 40)
            self.allSprites.add(life)

    def setUpCoinsAquired(self):
        for coins in range(1, self.TotalNumberOfCoinsAquired + 1):
            coin1 = coinCapture.CoinCapture(self, (coins * 40) + 10, 40, 35)
            self.allSprites.add(coin1)

    def generateScreenMap(self):
        # Generate Screen Map
        tileY = 0
        for layer in self.mapData:
            tileX = 0
            for tile in layer:
                if tile != '000':
                    if tile == '064' or tile == '065' or tile == '066' or tile == '067' or tile == '068':
                        platformTile = wall.Platform(tileX * 70, tileY * 70, 70, 70, self.tileSet[tile])
                        self.allSprites.add(platformTile)
                        self.walls.add(platformTile)
                    else:
                        artifact = wall.Platform(tileX * 70, tileY * 70, 70, 70, self.tileSet[tile])
                        self.allSprites.add(artifact)
                        self.artifacts.add(artifact)
                tileX += 1
            tileY += 1

    def addEnemiesSpritePools(self):
        # Add Enimies
        for i in range(1, 10):
            rock1 = rock.Rock(self, 30)
            self.allSprites.add(rock1)
            self.enemies.add(rock1)
            self.rocks.add(rock1)

        for i in range(1, 5):
            rock1 = rock.Rock(self, 70)
            self.allSprites.add(rock1)
            self.enemies.add(rock1)
            self.rocks.add(rock1)

        for i in range(1, 15):
            axe1 = axe.Axe(self)
            self.allSprites.add(axe1)
            self.enemies.add(axe1)
            self.axes.add(axe1)

        for i in range(1, 15):
            fireball1 = fireball.FireBall(self)
            self.allSprites.add(fireball1)
            self.enemies.add(fireball1)
            self.fireballs.add(fireball1)

    def drawText(self, surf, fontname, text, size, x, y):
        pgfont = pg.font.match_font(fontname)
        font = pg.font.Font(pgfont, size)
        text_surface = font.render(text, True, settings.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surf.blit(text_surface, text_rect)