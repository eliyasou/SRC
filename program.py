import arcade
import math
import random


BREDDE = 1000
HOEJDE = 800
MOVEMENT_SPEED = 3
SKUD_HASTIGEDHED = 0
SPORLAENGDE = 200
TYNGDEKRAFT = 1
SPILKØRER = True




class Planet:
    def __init__(self,centrum_x,centrum_y,radius,farve):
        self.centrum_x=centrum_x
        self.centrum_y=centrum_y
        self.radius=radius
        self.farve=farve

    def tegn(self):
        arcade.draw_circle_filled(self.centrum_x,self.centrum_y,self.radius,self.farve)
class Tyngdefelt:
    def __init__(self,centrum_x,centrum_y, radius,farve):
        self.centrum_x=centrum_x
        self.centrum_y=centrum_y
        self.radius=radius
        self.farve=farve

    def tegn(self):
        arcade.draw_circle_outline(self.centrum_x,self.centrum_y,self.radius,self.farve)
class Kanon:

    def __init__(self,start_x,start_y,slut_x,slut_y,skift_x,skift_y,farve,linje_bredde):
        self.start_x=start_x
        self.start_y=start_y
        self.slut_x=slut_x
        self.slut_y=slut_y
        self.skift_x=skift_x
        self.skift_y=skift_y
        self.farve=farve
        self.linje_bredde=linje_bredde

    def tegn(self):
        arcade.draw_line(self.start_x,self.start_y,self.slut_x,self.slut_y,self.farve,self.linje_bredde)

    def update(self):
        self.slut_x+=self.skift_x
        self.slut_y+=self.skift_y

        kanonlaengde = math.sqrt((self.slut_x-self.start_x)**2+(self.slut_y-self.start_y)**2)

        if kanonlaengde>=90:
            print((f"{kanonlaengde}"))
            pass


#        if self.slut_x>BREDDE/4+90:
 #           self.slut_x=BREDDE/4+90
  #      if self.slut_x<BREDDE/4-90:
   #         self.slut_x=BREDDE/4-90
    #    if self.slut_y>HOEJDE/2+90:
     #       self.slut_y=HOEJDE/2+90
      #  if self.slut_y<HOEJDE/2-90:
       #     self.slut_y=HOEJDE/2-90

class Skud:

    def __init__(self, fast_punkt, retningsvektor, farve, sporlaengde=None):
        self.fast_punkt = fast_punkt
        self.retningsvektor = retningsvektor
        self.punkt = self.fast_punkt
        self.farve = farve
        self.sporlaengde = sporlaengde
        if self.sporlaengde:
            self.spor = list()


    def opdater(self, delta_tid):
            if self.sporlaengde:
                self.spor.append(self.punkt)
            if self.sporlaengde and len(self.spor) >= self.sporlaengde:
                self.spor.pop(0)

            x, y = self.punkt
            vx, vy = self.retningsvektor
            x += vx * delta_tid
            y += vy * delta_tid
            self.punkt = (x, y)

    def tegn(self):
        x, y = self.punkt
        arcade.draw_circle_filled(x, y, 5, self.farve)
        for punkt in self.spor:
            x, y = punkt
            arcade.draw_circle_filled(x, y, 2, self.farve)


    def tegn(self):
        x, y = self.punkt
        arcade.draw_circle_filled(x, y, 5, self.farve)
        for punkt in self.spor:
            x, y = punkt
            arcade.draw_circle_filled(x, y, 2, self.farve)
class MitSpil(arcade.Window):
    def __init__(self,bredde,hoejde,titel):
        super().__init__(bredde,hoejde,titel)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.planet = Planet(BREDDE/4,HOEJDE/2,50,arcade.color.BEAVER)
        self.planet2=Planet(BREDDE/1.25,HOEJDE/2,50,arcade.color.RUBY)
        self.kanon = Kanon(self.planet.centrum_x,self.planet.centrum_y,self.planet.centrum_x+90,HOEJDE/2,0,0,arcade.color.GOLD,15)
        self.skud = Skud((self.kanon.start_x,self.kanon.start_y), (0, 0), arcade.csscolor.YELLOW, 100)
        self.tyngdefelt = Tyngdefelt(self.planet.centrum_x,self.planet.centrum_y,self.planet.radius*4,arcade.color.PLUM)

    def on_draw(self):
        self.skud.tegn()
        self.kanon.tegn()
        self.planet.tegn()
        self.planet2.tegn()
        self.tyngdefelt.tegn()


    def on_key_press(self, key, modifiers,):
        global SPILKØRER
        if SPILKØRER == True:
            if key == arcade.key.LEFT:
                self.kanon.skift_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.kanon.skift_x=MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.kanon.skift_y=-MOVEMENT_SPEED
            elif key == arcade.key.UP:
                self.kanon.skift_y=MOVEMENT_SPEED
            elif key == arcade.key.SPACE:
                    global SKUD_HASTIGEDHED
                    self.skud.retningsvektor
                    self.skud.retningsvektor = self.kanon.slut_x-self.kanon.start_x,self.kanon.slut_y-self.kanon.start_y
                    SPILKØRER = False
        elif not SPILKØRER:
            pass



    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.kanon.skift_x = 0
        elif key == arcade.key.DOWN or key == arcade.key.UP:
            self.kanon.skift_y = 0
    def update(self, delta_tid):
        self.clear()
        self.kanon.update()
        self.skud.opdater(delta_tid)

def main():
    vindue = MitSpil(BREDDE,HOEJDE,"Mit Spil")
    vindue.setup()
    arcade.run()

main()

