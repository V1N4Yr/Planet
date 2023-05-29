import pygame
import math
pygame.init()

Width, Height = 1500, 750
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Two Body Sim")
Scale = 2

class Body:
    def __init__(self, x, y, colour, m):
        self.x = x
        self.y = y
        self.colour = colour
        self.m = m
        self.r = math.log(self.m) * 3
        self.orbit = []
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x + Width /2
        y = self.y + Height /2
        pygame.draw.circle(win, self.colour, (x,y), self.r)

    def attraction(self, other):
        other_x, other_y, = other.x, other.y
        distance_x = (other_x - self.x)
        distance_y = (other_y - self.y)
        distance = math.sqrt(distance_x**2 + distance_y**2) * Scale
            
        force = 3 * self.m * other.m / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_y = force * math.sin(theta)
        force_x = force * math.cos(theta)
        return force_x, force_y

    def update_position(self, bodies):
        total_fx = total_fy = 0
        for i in bodies:
                if self == i:
                        continue
                fx, fy = self.attraction(i)
                total_fx += fx
                total_fy += fy

        self.x_vel += total_fx / self.m
        self.y_vel += total_fy / self.m
        self.x += (self.x_vel * 0.75)
        self.y += (self.y_vel * 0.75)
        self.orbit.append((self.x,self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    b1 = Body(-300, 0, (255,0,0), 15000)
    b2 = Body(-300, 300, (0,0,255), 300)
    b1.x_vel = 2
    b2.x_vel = 10
    body = [b1,b2]

    while run:
        clock.tick(60)
        Win.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for i in body:
            i.update_position(body)
            i.draw(Win)
        
        pygame.display.update()
        
    pygame.quit()

main()
