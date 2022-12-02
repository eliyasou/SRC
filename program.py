#Hej Jacob eller Martin hvem end der læser dette. Jeg havde en ide om hvordan mit program skulle fungere, det endte så med at være svært at gennemføre
#derfor endte det med at blive lidt kludret til sidst håber stadig der er en hvis grad af mening i det.
#Venlig Hilsen Elias Westh Jensen.

import arcade
import math

#Vi bestemmer konstanter for programmet
BREDDE = 1000
HOEJDE = 800
SPORLAENGDE = 200
MOVEMENT_SPEED = 3
TYNGDEKRAFT = 0
SPILKØRER = True
XD = False

#vi bestmmer klassen for Planeter
class Planet:
    def __init__(self , centrum_x, centrum_y, radius, farve):
        self.centrum_x = centrum_x
        self.centrum_y = centrum_y
        self.radius = radius
        self.farve = farve

    def tegn(self):
        arcade.draw_circle_filled(self.centrum_x,self.centrum_y,self.radius,self.farve)
#vi bestmmer klassen for "landingsbanen"
class Landingsbane:
    def __init__(self,cen_x,cen_y,bredde,hoejde,farve):
        self.cen_x = cen_x
        self.cen_y =cen_y
        self.bredde = bredde
        self.hoejde = hoejde
        self.farve = farve

    def tegn(self):
        arcade.draw_rectangle_filled(self.cen_x,self.cen_y,self.bredde,self.hoejde,self.farve)
#vi bestmmer klassen for kanonen
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
#her bliver enden af kanon ændret ved at addere med self.skift.x/y
        self.slut_x+=self.skift_x
        self.slut_y+=self.skift_y
#vi limiter den mulige længde af kanonen
        if self.slut_x>BREDDE/4+90:
            self.slut_x=BREDDE/4+90
        if self.slut_x<BREDDE/4-90:
            self.slut_x=BREDDE/4-90
        if self.slut_y>HOEJDE/2+90:
            self.slut_y=HOEJDE/2+90
        if self.slut_y<HOEJDE/2-90:
            self.slut_y=HOEJDE/2-90

#vi bestemmer klassen for skudfet
class Skud:

    def __init__(self, fast_punkt, retningsvektor, farve, sporlaengde=None):
        self.fast_punkt = fast_punkt
        self.retningsvektor = retningsvektor
        self.punkt = self.fast_punkt
        self.farve = farve
        self.sporlaengde = sporlaengde
#vi gør sporet til en liste
        if self.sporlaengde:
            self.spor = list()

    def opdater(self, delta_tid):
#vi tegner sporet
        if self.sporlaengde:
            self.spor.append(self.punkt)
            # vi fjerner enden af sporet hvis det bliver for langt
        if self.sporlaengde and len(self.spor) >= self.sporlaengde:
            self.spor.pop(0)
#vi henter de globale konstanter for at ændre på dem
        global TYNGDEKRAFT
        global XD
#vi gør brug af ligningen for en retningsvektor til at bestemme vores retningsvektor
        x, y = self.punkt
        vx, vy = self.retningsvektor
        x += vx * delta_tid
        y += vy * delta_tid
        # vi trækker tyngdekraften fra y koordinatet for skudet
        y -= TYNGDEKRAFT* x**2 * delta_tid
        # vi bestemmer at tyngdekraften først får en værdi og effekt når skudet er ude af kanonen
        if x > BREDDE/4+90:
            XD = True
        if XD == True:
            TYNGDEKRAFT += 0.0000012

#vi gør så skudet stopper op hvis det rammer kanterne af vinduet
        self.punkt = (x, y)

        if x > BREDDE:
            self.punkt= BREDDE, y
        elif x < 0:
            self.punkt = 0, y
        if y > HOEJDE:
            self.punkt = x, HOEJDE
        elif y<0:
            self.punkt = x, 0

    def tegn(self):
        x, y = self.punkt
        arcade.draw_circle_filled(x, y, 5, self.farve)
        for punkt in self.spor:
            x, y = punkt
            arcade.draw_circle_filled(x, y, 2, self.farve)

#Vi bestemmer klassen for vinduet
class MitSpil(arcade.Window):
    def __init__(self,bredde,hoejde,titel):
        super().__init__(bredde,hoejde,titel)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        #i setup giver vi værdierne til vores forskellige obejekter vha. de klasser vi har bestemt
        self.planet = Planet(BREDDE/4,HOEJDE/2,50,arcade.color.BEAVER)
        self.planet2=Planet(BREDDE/1.25,HOEJDE/2,50,arcade.color.RUBY)
        self.planet3 = Planet(BREDDE/2,0,150,arcade.color.SAGE)
        self.kanon = Kanon(self.planet.centrum_x,self.planet.centrum_y,self.planet.centrum_x+90,HOEJDE/2,0,0,arcade.color.GOLD,15)
        self.skud = Skud((self.kanon.start_x,self.kanon.start_y), (0, 0), arcade.csscolor.YELLOW, 100)
        self.landingsbane = Landingsbane(self.planet2.centrum_x,+self.planet2.centrum_y+self.planet2.radius,25,25,arcade.csscolor.WHITE)

    # vi tegner hver af vores objekter
    def on_draw(self):
#vi tegner hver af vores objekter
        self.skud.tegn()
        self.landingsbane.tegn()
        self.planet.tegn()
        self.planet2.tegn()
        self.planet3.tegn()
        self.kanon.tegn()

# vi bestemmer hvad de forskellige knapper gør
    def on_key_press(self, key, modifiers,):
        global SPILKØRER
        if SPILKØRER:
#vi bestemmer længden af kanonen som skudets hastighed er afhænig af
            kanonlaengde = math.sqrt((self.kanon.slut_x - self.kanon.start_x) ** 2 + (self.kanon.slut_y - self.kanon.start_y) ** 2)
            if key == arcade.key.LEFT:
                #når vi klikker på den venstre piltast bliver x-værdien for kanonen mindre
                self.kanon.skift_x = -MOVEMENT_SPEED
                #når vi klikker printer vi hastigheden og vektoren for kanon efter det klik
                print(f"hastigheden af skuden bliver {kanonlaengde}")
                print(f"vektor = {self.kanon.slut_x - self.kanon.start_x},{self.kanon.slut_y - self.kanon.start_y}")
            elif key == arcade.key.RIGHT:
                self.kanon.skift_x=MOVEMENT_SPEED
                print(f"hastigheden af skuden bliver {kanonlaengde}")
                print(f"vektor = {self.kanon.slut_x - self.kanon.start_x},{self.kanon.slut_y - self.kanon.start_y}")
            elif key == arcade.key.DOWN:
                self.kanon.skift_y=-MOVEMENT_SPEED
                print(f"hastigheden af skuden bliver {kanonlaengde}")
                print(f"vektor = {self.kanon.slut_x - self.kanon.start_x},{self.kanon.slut_y - self.kanon.start_y}")
            elif key == arcade.key.UP:
                self.kanon.skift_y=MOVEMENT_SPEED
                print(f"hastigheden af skuden bliver {kanonlaengde}")
                print(f"vektor = {self.kanon.slut_x - self.kanon.start_x},{self.kanon.slut_y - self.kanon.start_y}")
            elif key == arcade.key.SPACE:
#når vi trykker på spacebaren skyder skudet med vektoren af kanonen og hastigheden af længden af kanonen
#når vi skydder sætter vi også SPILKØRER = falsk så vi ikke kan ændre klikke på tasterne med en effekt
                    self.skud.retningsvektor
                    self.skud.retningsvektor = self.kanon.slut_x-self.kanon.start_x,self.kanon.slut_y-self.kanon.start_y
                    print(f"vektor = {self.kanon.slut_x-self.kanon.start_x},{self.kanon.slut_y-self.kanon.start_y}")
                    global TYNGDEKRAFT
                    SPILKØRER = False

        else:
            pass

# vi gør så når vi giver slip på knapperne stopper kanonen med at bevæge sig
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
#tak fordi du kikkede i gennem min kode, og have en nat eller dag :)