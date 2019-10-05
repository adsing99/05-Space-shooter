import sys, logging, os, random, math, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Space Shooter"

NUM_ENEMIES = 10
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 50
HIT_SCORE = 10
KILL_SCORE = 100
PLAYER_HEALTH = 100


class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
     
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/ship.png", 0.5)
        

        self.hp = PLAYER_HEALTH
       
        (self.center_x, self.center_y) = STARTING_LOCATION
   
      
            
     

       

class Enemy(arcade.Sprite):
    def __init__(self, position):
       
        super().__init__("assets/alien.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position


        


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        self.background = None
        self.rock_list = None
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.ammo = 100
        self.shiphp = 100
        self.end = 10
        self.dead = False

    def setup(self):
        
        self.background = arcade.load_texture("assets/source.gif")
        self.rock_list = arcade.SpriteList()


        for i in range(NUM_ENEMIES):
            x = random.randint(0, 400) * 2 #120 * (i+1) + 40
            y = random.randint(300, 500)
            enemy = Enemy((x,y))

            self.enemy_list.append(enemy)  

        
                                                                
            

    def update(self, delta_time):

        for e in self.enemy_list:
            e.center_x += 2
            if e.center_x == 800:
                e.center_x = 0
                
     
        self.bullet_list.update()
        
        for e in self.enemy_list:
            damage = arcade.check_for_collision_with_list(e, self.bullet_list)
            for d in damage:
                e.hp = e.hp - d.damage
                d.kill()
                if e.hp <= 0:
                    self.score += KILL_SCORE
                    e.kill()
                    self.end -= 1
                else:
                    self.score += HIT_SCORE

        for enemy in self.enemy_list:

            # Have a random 1 in 200 change of shooting each frame
            if random.randrange(200) == 0:
                bullet = arcade.Sprite("assets/rock.png", 0.5)
                bullet.center_x = enemy.center_x
                bullet.angle = -90
                bullet.top = enemy.bottom
                bullet.change_y = -2
                self.rock_list.append(bullet)

        for rock in self.rock_list:
            if rock.top < 0:
                rock.kill()

        self.rock_list.update()
        for b in self.rock_list:
            hit = arcade.check_for_collision(b, self.player)
            if hit == True:
                b.kill()
                if self.player.hp == 0:
                    
                    self.dead = True
                else:
                    self.player.hp -= 10
                    self.shiphp -= 10


    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        if self.dead == True or self.ammo == 0:
            arcade.draw_text("GAME OVER", 240, 300, arcade.color.WHITE, 40)
        if self.end == 0:
            arcade.draw_text("Great Job Captain!", 220, 300, arcade.color.WHITE, 40)
        arcade.draw_text("SCORE: " + str(self.score), 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 16)
        arcade.draw_text("HP: " + str(self.shiphp), 20, SCREEN_HEIGHT - 60, arcade.color.WHITE, 16)
        arcade.draw_text("AMMO: " + str(self.ammo), 20, SCREEN_HEIGHT - 80, arcade.color.WHITE, 16)

        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.rock_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
      
        self.player.center_x = x
    


    def on_mouse_press(self, x, y, button, modifiers):
        if self.dead == False:
            if self.ammo > 0:
                if button == arcade.MOUSE_BUTTON_LEFT:
                    x = self.player.center_x
                    y = self.player.center_y + 15
                    bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
                    self.bullet_list.append(bullet)
                    if self.end > 0:
                        self.ammo -= 1
        else:
            pass
           

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()