import pygame
import math
pygame.init()

Width, Height = 1500, 750
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Phys Sim")
Red = (175,0,0)
Yellow = (255,255,0)
Blue = (100,150,255)
Grey = (80,78,81)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    Scale = 300/AU
    TIMESTEP = 3600*24
    
    def __init__(self, x, y, r, colour, m):
        self.x = x
        self.y = y
        self.r = r
        self.colour = colour
        self.m = m
        self.sun = False
        self.orbit = []
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win):
        x = self.x * self.Scale + Width /2
        y = self.y * self.Scale + Height /2
        pygame.draw.circle(win, self.colour, (x,y), self.r)

    def attraction(self, other):
        other_x, other_y, = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
            
        force = self.G * self.m * other.m / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_y = force * math.sin(theta)
        force_x = force * math.cos(theta)
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
                if self == planet:
                        continue
                fx, fy = self.attraction(planet)
                total_fx += fx
                total_fy += fy

        self.x_vel += total_fx / self.m * self.TIMESTEP
        self.y_vel += total_fy / self.m * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x,self.y))
        
def main():
    run = True
    clock = pygame.time.Clock()
    #Win.fill(Red)

    sun = Planet(0, 0, 30, Yellow, 1.98891e30)
    sun.sun=True
    mercury = Planet(-0.387*Planet.AU, 0, 8, Grey, 3.3e23)
    mercury.y_vel =47400
    venus = Planet(-0.723*Planet.AU, 0, 12, (255,255,255), 6.39e24)
    venus.y_vel = -35020
    earth = Planet(-1*Planet.AU, 0, 16, Blue, 5.9742e24)
    earth.y_vel = 29783
    mars = Planet(-1.524*Planet.AU, 0, 14, Red, 4.8685e24)
    mars.y_vel = 24077
    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60)
        Win.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(Win)
        
        pygame.display.update()
        
    pygame.quit()

main()
