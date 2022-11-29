import arcade
import math
import random


BREDDE = 800
HOEJDE = 600
MOVEMENT_SPEED = 2
class Planet:
    def __init__(self,centrum_x,centrum_y,radius,farve):
        self.centrum_x=centrum_x
        self.centrum_y=centrum_y
        self.radius=radius
        self.farve=farve

    def tegn(self):
        arcade.draw_circle_filled(self.centrum_x,self.centrum_y,self.radius,self.farve)
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

        if self.slut_x>BREDDE:
            self.slut_x=BREDDE
        if self.slut_x<0:
            self.slut_x=0
        if self.slut_y>HOEJDE:
            self.slut_y=HOEJDE


class MitSpil(arcade.Window):
    def __init__(self,bredde,hoejde,titel):
        super().__init__(bredde,hoejde,titel)
        arcade.set_background_color(arcade.color.SKY_BLUE)



        self.planet = Planet(BREDDE/4,HOEJDE/2,50,arcade.color.BEAVER)
        self.planet2=Planet(BREDDE/1.25,HOEJDE/2,50,arcade.color.RUBY)
        self.kanon = Kanon(BREDDE/4,HOEJDE/2,BREDDE/2-100,HOEJDE/2,0,0,arcade.color.GOLD,15)


    def on_draw(self):
        arcade.start_render()
        self.planet.tegn()
        self.planet2.tegn()
        self.kanon.tegn()
    def update(self, delta_time):
        self.kanon.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.kanon.skift_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.kanon.skift_x=MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.kanon.skift_y=-MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.kanon.skift_y=MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.kanon.skift_x = 0
        elif key == arcade.key.DOWN or key == arcade.key.UP:
            self.kanon.skift_y = 0



def main():
    vindue = MitSpil(BREDDE,HOEJDE,"Mit Spil")
    arcade.run()

main()