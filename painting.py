import pygame, random

class MyPaint():
    def __init__(self):

        self.screen = pygame.display.set_mode((800,600))

        self.draw_on = False
        self.last_pos = (0, 0)
        self.color = (255, 128, 0)
        self.radius = 10

    def roundline(self, srf, color, start, end, radius=1):
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        distance = max(abs(dx), abs(dy))
        for i in range(distance):
            x = int( start[0]+float(i)/distance*dx)
            y = int( start[1]+float(i)/distance*dy)
            pygame.draw.circle(srf, color, (x, y), radius)

    def Run(self):
        try:
            while True:
                e = pygame.event.wait()
                if e.type == pygame.QUIT:
                    raise StopIteration
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.color = (random.randrange(256), random.randrange(256), random.randrange(256))
                    pygame.draw.circle(self.screen, self.color, e.pos, self.radius)
                    self.draw_on = True
                if e.type == pygame.MOUSEBUTTONUP:
                    self.draw_on = False
                if e.type == pygame.MOUSEMOTION:
                    if self.draw_on:
                        pygame.draw.circle(self.screen, self.color, e.pos, self.radius)
                        self.roundline(self.screen, self.color, e.pos, self.last_pos,  self.radius)
                    self.last_pos = e.pos
                pygame.display.flip()

        except StopIteration:
            pass

        pygame.quit()


if __name__ == "__main__":
    MyPaint().Run()