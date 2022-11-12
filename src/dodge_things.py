import pyxel
import random

class App():
    def __init__(self) -> None:
        pyxel.init(256,256)
        pyxel.load("res.pyxres")

        self.reset()

        pyxel.playm(0, loop=True)
        pyxel.run(self.update,self.draw)
    def update(self):
        if self.is_gameover:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset()
            return
        self.update_player()
        self.spawn()
        self.update_things()
        self.score += 1

    def update_player(self):
        dx = 0
        dy = 0
        if pyxel.btn(pyxel.KEY_W):
            dy -= 1
        if pyxel.btn(pyxel.KEY_S):
            dy += 1
        if pyxel.btn(pyxel.KEY_A):
            dx -= 1
        if pyxel.btn(pyxel.KEY_D):
            dx += 1

        if self.player_y + dy < 0:
            self.player_y = 0
        elif pyxel.height-self.player_h < self.player_y + dy:
            self.player_y = pyxel.height-self.player_h
        else:
            self.player_y += dy
        if self.player_x + dx < 0:
            self.player_x = 0
        elif pyxel.width-self.player_w < self.player_x + dx:
            self.player_x = pyxel.width-self.player_w
        else:
            self.player_x += dx

    def spawn(self):
        if pyxel.frame_count % 10 == 0:
            self.things.append((pyxel.width,random.randint(0,pyxel.height-4),4,4))

    def update_things(self):
        indexes = []
        for i, value in enumerate(self.things):
            x,y,w,h = value
            x -= 2
            if self.collision_detection(x,y,w,h):
                self.is_gameover = True
            if x < -w:
                indexes.append(i)
            self.things[i] = (x,y,w,h,)
        for value in indexes:
            self.things.pop(value)

    def collision_detection(self,x,y,w,h):
        if (x < self.player_x + self.player_w) and \
            (self.player_x < x + w) and \
            (y < self.player_y + self.player_h) and \
            (self.player_y < y + h):
            return True
        else:
            return False

    def reset(self):
        self.score = 0
        self.player_x = 10
        self.player_y = 10
        self.player_w = 16
        self.player_h = 16
        self.things = []
        self.is_gameover = False

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.blt(self.player_x,self.player_y,0,0,0,self.player_w,self.player_h,pyxel.COLOR_BLACK)
        self.draw_things()
        pyxel.text(0,0,"Score: "+str(self.score),pyxel.COLOR_GREEN)
        if self.is_gameover:
            strings = "Game over"
            x = (pyxel.width - len(strings)*pyxel.FONT_WIDTH)//2
            y = (pyxel.height - pyxel.FONT_HEIGHT)//2
            for posy in range(-1,2):
                for posx in range(-1,2):
                    pyxel.text(x + posx,y + posy,strings,pyxel.COLOR_YELLOW)
            pyxel.text(x,y,strings,pyxel.COLOR_RED)
            strings = "Please press space key!"
            pyxel.text((pyxel.width - len(strings)*pyxel.FONT_WIDTH)//2,(pyxel.height - pyxel.FONT_HEIGHT)//2 + pyxel.FONT_HEIGHT,strings,pyxel.COLOR_PINK)

    def draw_things(self):
        for i, value in enumerate(self.things):
            x,y,w,h = value
            pyxel.blt(x,y,0,16,0,w,h,pyxel.COLOR_BLACK)
App()

