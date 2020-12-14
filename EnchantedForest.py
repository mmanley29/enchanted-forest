import arcade
import random
import math


CHARACTER_SCALING = 0.03
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_SCALING_COIN = .25
TREE_SCALING = 0.05
PLAYER_MOVEMENT_SPEED = 5
ENEMY_SPEED = 2
BULLET_COOLDOWN_TICKS = 10
BULLET_SPEED = 15



class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title, monsters, magicTree, wand, hud, coinTracker):
        super().__init__(width, height, title)
        self.set_location(100, 100)
        arcade.set_background_color(arcade.color.BROWN_NOSE)
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None

        self.monsters = monsters
        self.tree = magicTree
        self.wand = wand
        self.hud = hud
        self.coinTracker = coinTracker

        self.angle_in_deg = 0
        

        

    def setup(self):
        
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.angle_in_deg = 0

        #setting up the player
        image_source = "wizard.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 600
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)

        #create border of trees
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("tree.png", TREE_SCALING)
            wall.center_x = x
            difference = random.randint(-15, 15)
            wall.center_y = 15 + difference
            self.wall_list.append(wall)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite("tree.png", TREE_SCALING)
            wall.center_x = x
            difference = random.randint(-15, 15)
            wall.center_y = 715 + difference
            self.wall_list.append(wall)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite("tree.png", TREE_SCALING)
            wall.center_x = 15 + difference
            difference = random.randint(-15, 15)
            wall.center_y = x
            self.wall_list.append(wall)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite("tree.png", TREE_SCALING)
            wall.center_x = 1235 + difference
            difference = random.randint(-15, 15)
            wall.center_y = x
            self.wall_list.append(wall)

        #create some more walls
        coordinate_list = [[492, 248],
                           [492, 472],
                           [716, 248],
                           [716, 472]]
                           

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        #create physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        

        

    def on_draw(self):
        arcade.start_render()
        
        self.tree.tree.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.monsters.enemy_list.draw()
        self.wand.bullet_list.draw()
        self.coinTracker.coin_list.draw()
        self.coinTracker.smallCoin_list.draw()
        self.hud.drawHUD()

        if self.hud.isGameOver():
            arcade.draw_text("Game Over", 1280/2, 720/2, arcade.color.RED, 100, width=1280,
                             align="center", anchor_x="center", anchor_y="center")
        
            arcade.draw_text("press y to try again", 1280/2, 720/4, arcade.color.RED, 40, width=1280,
                             align="center", anchor_x="center", anchor_y="center")


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            self.angle_in_deg = 90
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
            self.angle_in_deg = 270
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            self.angle_in_deg = 180
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            self.angle_in_deg = 0
            
        if key == arcade.key.W:
            self.angle_in_deg = 90
            self.wand.spawn_bullet(self.angle_in_deg)
        elif key == arcade.key.S:
            self.angle_in_deg = 270
            self.wand.spawn_bullet(self.angle_in_deg)
        elif key == arcade.key.A:
            self.angle_in_deg = 180
            self.wand.spawn_bullet(self.angle_in_deg)
        elif key == arcade.key.D:
            self.angle_in_deg = 0
            self.wand.spawn_bullet(self.angle_in_deg)

        if key == arcade.key.SPACE or key == arcade.key.B:
            self.wand.spawn_bullet(self.angle_in_deg)

        if key == arcade.key.Y:
            self.resetGame()
            
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        if self.hud.isGameOver():
            return
        # Move the player with the physics engine
        self.physics_engine.update()
        
        self.wand.update()
        self.wand.bullet_list.update()
        self.monsters.spawnMonsters()
        self.monsters.enemy_list.update()
        self.monsters.checkScoreToIncreaseEnemies()
        self.monsters.brain.moveTowardCenter(self.tree.tree)
        self.monsters.brain.attackObjective(self.tree.tree, self.tree)
        self.monsters.brain.attackObjective(self.player_sprite, self.hud)

        self.coinTracker.spawnPowerUps()
        self.coinTracker.managePowerups()

    def resetGame(self):
        

        self.hud.score = 1
        self.monsters.numberofEnemies = 1
       
        self.monsters.removeAllMonsters()
        
        self.hud.healthPoints = 30
        self.tree.healthPoints = 300
        self.hud.ammoPoints = 10
        self.hud.isGameOver()
        


class PlayerWeapon:
    def __init__(self):
        self.player = None
        self.bullet_list = None
        self.bullet_cooldown = None
        self.score = 1
        
    
    def setup(self, player, enemies, scoreKeeper, coinTracker):
        self.player = player
        self.bullet_list = arcade.SpriteList()
        self.bullet_cooldown = 0
        self.enemy_list = enemies
        self.scoreKeeper = scoreKeeper
        self.coinTracker = coinTracker

    def update(self):
        self.bullet_cooldown += 1
        
        for bullet in self.bullet_list:
            bullet_killed = False
            enemy_shot_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            # Loop through each colliding sprite, remove it, and add to the score.
            for enemy in enemy_shot_list:
                self.coinTracker.addSmallCoin(enemy.center_x, enemy.center_y)
                enemy.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()
                bullet_killed = True
                self.scoreKeeper.score += 1
            if bullet_killed:
                continue

    def spawn_bullet(self, angle_in_deg):
        # only allow bullet to spawn on an interval
        if self.bullet_cooldown < BULLET_COOLDOWN_TICKS or self.scoreKeeper.ammoPoints == 0:
            return
        self.bullet_cooldown = 0

        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.75)

        # Position the bullet at the player's current location
        start_x = self.player.center_x
        start_y = self.player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # angle the bullet visually
        bullet.angle = angle_in_deg
        angle_in_rad = math.radians(angle_in_deg)

        # set bullet's movement direction
        bullet.change_x = math.cos(angle_in_rad) * BULLET_SPEED
        bullet.change_y = math.sin(angle_in_rad) * BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)
        self.scoreKeeper.ammoPoints -= 1

class PowerUps:
    def __init__(self, hud):
        self.coin_list = arcade.SpriteList()
        self.smallCoin_list = arcade.SpriteList()
        self.coin = arcade.Sprite(":resources:images/items/coinGold.png",
                                 SPRITE_SCALING_COIN)
        
        self.ammoWorth = 4
        self.hud = hud
        self.numberOfCoins = 2
    
    def setup(self, player_sprite):
        self.player = player_sprite

    def spawnPowerUps(self):
        while len(self.coin_list) < self.numberOfCoins:

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(":resources:images/items/coinGold.png",
                                 SPRITE_SCALING_COIN * 2)

            # Position the coin
            coin.center_x = random.randrange(45,1230)
            coin.center_y = random.randrange(45, 670)

            # Add the coin to the lists
            self.coin_list.append(coin)    

    def addSmallCoin(self, x, y):
        coin = arcade.Sprite(":resources:images/items/coinGold.png",
                                 SPRITE_SCALING_COIN)
        coin.center_x = x
        coin.center_y = y
         
        self.smallCoin_list.append(coin)    

    def managePowerups(self):
        for coin in self.coin_list:
            if coin.collides_with_sprite(self.player):
                coin.remove_from_sprite_lists()
                self.hud.ammoPoints += self.ammoWorth
        
        for coin in self.smallCoin_list:
            if coin.collides_with_sprite(self.player):
                coin.remove_from_sprite_lists()
                self.hud.ammoPoints += 1


##Enemies
class EnemyAI:
    def __init__(self, enemies):
        self.enemies = enemies
        self.attackValue = 1
        self.speed = 2

    def moveTowardCenter(self, objective):
        for enemy in self.enemies:
            if not(enemy.collides_with_sprite(objective)):
                x_distance = objective.center_x - enemy.center_x
                y_distance = objective.center_y - enemy.center_y

                if abs(x_distance) != 0:
                    divisor = abs(x_distance) 
                else:
                    divisor = abs(x_distance) + 1
                    

                speedFactor = 0.7
                enemy.change_x = min(1, (x_distance / divisor * speedFactor))
                 
                    
                enemy.change_y = min(1, (y_distance / divisor * speedFactor))
            else:
                enemy.change_x = 0
                enemy.change_y = 0

    def moveTowardCenterTest(self, objective):
        ENEMY_SPEED = 2
        for enemy in self.enemies:
            if enemy.center_y < objective.center_y:
                enemy.center_y += min(ENEMY_SPEED, objective.center_y - enemy.center_y)
            elif enemy.center_y > objective.center_y:
                enemy.center_y -= min(ENEMY_SPEED, enemy.center_y - objective.center_y)

            if enemy.center_x < objective.center_x:
                enemy.center_x += min(ENEMY_SPEED, objective.center_x - enemy.center_x)
            elif enemy.center_x > objective.center_x:
                enemy.center_x -= min(ENEMY_SPEED, enemy.center_x - objective.center_x)

    def moveTowardCenterNew(self, objective):
        for enemy in self.enemies:
            if not(enemy.collides_with_sprite(objective)):
                x_distance = objective.center_x - enemy.center_x
                y_distance = objective.center_y - enemy.center_y
                
                if objective.center_x > enemy.center_x:
                    negX = 1
                else:
                    negX = -1

                if objective.center_y > enemy.center_y:
                    negY = 1
                else:
                    negY = -1

                if abs(x_distance) > 5:   
                    enemy.change_x = self.speed * negX
                    enemy.change_y = 0
                else:
                    enemy.change_y = self.speed * negY
                    enemy.change_x = 0

                    
            else:
                enemy.change_x = 0
                enemy.change_y = 0


    def attackObjective(self, objective, objectiveClass):
        enemies_that_attacked_list = arcade.check_for_collision_with_list(objective, self.enemies)

        for enemy in enemies_that_attacked_list:
            if objective.center_x > enemy.center_x:
                enemy.center_x -= 15
            else:
                enemy.center_x += 15

            if objective.center_y > enemy.center_y:
                enemy.center_y -= 15
            else:
                enemy.center_y += 15
            objectiveClass.healthPoints -= self.attackValue



class MonsterSpawner:
    def __init__(self):
        self.enemy_list = None
        self.numberOfEnemies = 1
        self.beenIncreased = False
    
    def setup(self, window, hud):
        self.enemy_list = arcade.SpriteList()
        self.scoreKeeper = hud

        while len(self.enemy_list) < self.numberOfEnemies:
            
            enemy = arcade.Sprite("ghost.png", 0.2)
            coordinate = [random.randint(0, 1280), random.randint(0, 720),]
            right = [random.randint(1280, 1310), random.randint(0, 720),]
            left = [random.randint(-30, 0), random.randint(0, 720),]
            top = [random.randint(0, 1280), random.randint(720, 750),]
            bottom = [random.randint(0, 1280), random.randint(-30, 0),]
            oneOffourSides = random.choice([right, left, top, bottom])
            enemy.position = oneOffourSides
            self.enemy_list.append(enemy)

        self.brain = EnemyAI(self.enemy_list)
        self.brain.moveTowardCenter(window.player_sprite)

        
    def spawnMonsters(self):
        if self.scoreKeeper.score == 1:
            self.numberOfEnemies = 1
        while len(self.enemy_list) < self.numberOfEnemies:
            enemy = arcade.Sprite("ghost.png", 0.2)
            
            coordinate = [random.randint(0, 1280), random.randint(0, 720),]

            right = [random.randint(1280, 1310), random.randint(0, 720),]
            left = [random.randint(-30, 0), random.randint(0, 720),]
            top = [random.randint(0, 1280), random.randint(720, 750),]
            bottom = [random.randint(0, 1280), random.randint(-30, 0),]
            oneOffourSides = random.choice([right, left, top, bottom])
            enemy.position = oneOffourSides
            self.enemy_list.append(enemy)

    def checkScoreToIncreaseEnemies(self):
        if not self.scoreKeeper.score % 10 and self.scoreKeeper.score != 0:
            if not self.beenIncreased:
                self.numberOfEnemies += 1 
                
                self.beenIncreased = True
        else:
            self.beenIncreased = False
    
    def removeAllMonsters(self):
        while len(self.enemy_list)  > 1:
            for enemy in self.enemy_list:
                enemy.remove_from_sprite_lists()
   

    def on_draw(self):
        arcade.start_render()

        ##self.enemy_list.draw()
       
class TreeHealth:
    def __init__(self):
        self.healthPoints = 300
        self.tree = None

    def setup(self, window):
        self.tree = arcade.Sprite("Tree.png", TREE_SCALING)
        self.tree.center_x = 604
        self.tree.center_y = 360

class HUD:
    def __init__(self, treeHP):
        self.treeHP = treeHP
        self.score = 0
        self.healthPoints = 30
        self.ammoPoints = 10

    def drawHUD(self):
        output = f"Tree Health: {self.treeHP.healthPoints} "
        arcade.draw_text(output, 10, 670, arcade.color.WHITE, 14)

        scoreOutput = f"Score: {self.score} "
        arcade.draw_text(scoreOutput, 150, 670, arcade.color.WHITE, 14)

        healthOutput = f"Health Points: {self.healthPoints} "
        arcade.draw_text(healthOutput, 310, 670, arcade.color.WHITE, 14)

        ammoOutput = f"Magic Bolts: {self.ammoPoints} "
        arcade.draw_text(ammoOutput, 710, 670, arcade.color.WHITE, 14)
    
    def isGameOver(self):
        if self.healthPoints <= 0:
            return True
        
        if self.treeHP.healthPoints <= 0:
            return True

def main():
    
    monsters =  MonsterSpawner()
    magicTree = TreeHealth()
    wand = PlayerWeapon()
    hud = HUD(magicTree)
    coinTracker = PowerUps(hud)

    window = MyGameWindow(1280,  720, 'New Try', monsters, magicTree, wand, hud, coinTracker)
    window.setup()
    coinTracker.setup(window.player_sprite)
    magicTree.setup(window)
    monsters.setup(window, hud)
    wand.setup(window.player_sprite, monsters.enemy_list, hud, coinTracker)
    
    
    arcade.run()
    

if __name__ == "__main__":
    main()






