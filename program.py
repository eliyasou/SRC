import arcade
import math
import random


BREDDE = 1000
HOEJDE = 800
MOVEMENT_SPEED = 3
SKUD_HASTIGEDHED = 0
SPORLAENGDE = 200
TYNGDEKRAFT = 0
SPILKØRER = True
SLUT = False
XD = False


class Planet:
    def __init__(self , centrum_x, centrum_y, radius, farve):
        self.centrum_x = centrum_x
        self.centrum_y = centrum_y
        self.radius = radius
        self.farve = farve

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

class Landingsbane:
    def __init__(self,cen_x,cen_y,bredde,hoejde,farve):
        self.cen_x = cen_x
        self.cen_y =cen_y
        self.bredde = bredde
        self.hoejde = hoejde
        self.farve = farve

    def tegn(self):
        arcade.draw_rectangle_filled(self.cen_x,self.cen_y,self.bredde,self.hoejde,self.farve)
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

        #if kanonlaengde>=90:
            #print((f"{kanonlaengde}"))
            #self.slut_x=self.slut_x-MOVEMENT_SPEED



        if self.slut_x>BREDDE/4+90:
            self.slut_x=BREDDE/4+90
        if self.slut_x<BREDDE/4-90:
            self.slut_x=BREDDE/4-90
        if self.slut_y>HOEJDE/2+90:
            self.slut_y=HOEJDE/2+90
        if self.slut_y<HOEJDE/2-90:
            self.slut_y=HOEJDE/2-90


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
        global TYNGDEKRAFT
        global XD
        x, y = self.punkt
        vx, vy = self.retningsvektor
        x += vx * delta_tid
        y += vy * delta_tid
        y -= TYNGDEKRAFT* x**2 * delta_tid
        if x > BREDDE/4+90:
            XD = True
        if XD == True:
            TYNGDEKRAFT += 0.0000012
        #elif x < BREDDE/4-90:
          #  XD = True
        #elif y > HOEJDE/2+90:
        #    XD = True
        #elif y < HOEJDE/2-90:
        #    XD = True
       # else:
         #   XD = True


       # x -= TYNGDEKRAFT * delta_tid
        #x += TYNGDEKRAFT * delta_tid
        #if x>BREDDE/4 +90:
           # vx -= TYNGDEKRAFT *delta_tid
       # elif x<BREDDE/4 -90:
            #vx += TYNGDEKRAFT *delta_tid
      #  if y>HOEJDE/2 +90:
      #      vy -= TYNGDEKRAFT * delta_tid
      #  elif y < HOEJDE/2 - 90:
         #   vy -= TYNGDEKRAFT * delta_tid

        self.punkt = (x, y)

        if x > BREDDE:
            self.punkt= BREDDE,y
        elif x < 0:
            self.punkt = 0,y
        if y > HOEJDE:
            self.punkt = x,HOEJDE
        elif y<0:
            self.punkt = x,0



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
        self.planet3 = Planet(BREDDE/2,0,150,arcade.color.SAGE)
        self.kanon = Kanon(self.planet.centrum_x,self.planet.centrum_y,self.planet.centrum_x+90,HOEJDE/2,0,0,arcade.color.GOLD,15)
        self.skud = Skud((self.kanon.start_x,self.kanon.start_y), (0, 0), arcade.csscolor.YELLOW, 100)
        self.tyngdefelt = Tyngdefelt(self.planet.centrum_x,self.planet.centrum_y,self.planet.radius*4,arcade.color.PLUM)
        self.tyngdefelt2 = Tyngdefelt(self.planet2.centrum_x,self.planet.centrum_y,self.planet2.radius*4,arcade.color.PLUM)
        self.tyngdefelt3 = Tyngdefelt(self.planet3.centrum_x,self.planet3.centrum_y,self.planet3.radius*4,arcade.color.PLUM)
        self.landingsbane = Landingsbane(self.planet2.centrum_x,+self.planet2.centrum_y+self.planet2.radius,25,25,arcade.csscolor.WHITE)


    def on_draw(self):
        self.skud.tegn()
        self.planet.tegn()
        self.kanon.tegn()
        self.landingsbane.tegn()
        self.planet2.tegn()
        self.tyngdefelt3.tegn()
        self.planet3.tegn()

    def on_key_press(self, key, modifiers,):
        global SPILKØRER
        if SPILKØRER:
            if key == arcade.key.LEFT:
                self.kanon.skift_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.kanon.skift_x=MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.kanon.skift_y=-MOVEMENT_SPEED
            elif key == arcade.key.UP:
                self.kanon.skift_y=MOVEMENT_SPEED
            elif key == arcade.key.SPACE:
                    self.skud.retningsvektor
                    self.skud.retningsvektor = self.kanon.slut_x-self.kanon.start_x,self.kanon.slut_y-self.kanon.start_y
                    print(f"vektor = {self.kanon.slut_x-self.kanon.start_x},{self.kanon.slut_y-self.kanon.start_y}")
                    global TYNGDEKRAFT

                    SPILKØRER = False


        else:
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

