import pygame as pg
import numpy as np
import threading

class App():
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1600, 900
        self.FPS = 120
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("A* Pathfinding Algorithm")
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.clicks = (False, False, False)
        self.blocks = []
        self.phase = "block placing"
        self.departure = None
        self.arrival = None
        self.path = []
        self.pos = None

        self.running = True

    def reset(self):
        self.blocks = []
        self.phase = "block placing"
        self.departure = None
        self.arrival = None
        self.path = []
        self.pos = None
        self.clicks = (False, False, False)
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
    
    def pathfinding(self):
        self.pos = self.departure
        grid = [(x, y, 0, 0) for x in range(0, self.WIDTH, 50) for y in range(0, self.HEIGHT, 50)]
        self.path = []
        while self.pos != self.arrival:
            self.path.append(self.check_surroundings())
            self.pos = self.path[-1]
            if self.pos is None:
                print("No path found")
                self.path.pop()
                self.pos = self.path[-1]

        
    def check_surroundings(self):
        best_f_cost = 100000
        best_pos = None
        for x in [-50, 0, 50]:
            for y in [-50, 0, 50]:
                if x == 0 and y == 0:
                    continue
                new_pos = (self.pos[0] + x, self.pos[1] + y)
                if new_pos in self.blocks or new_pos in self.path:
                    continue
                if new_pos[0] < 0 or new_pos[0] > self.WIDTH or new_pos[1] < 0 or new_pos[1] > self.HEIGHT:
                    continue
                g_cost = np.sqrt((new_pos[0] - self.departure[0])**2 + (new_pos[1] - self.departure[1])**2)
                h_cost = np.sqrt((new_pos[0] - self.arrival[0])**2 + (new_pos[1] - self.arrival[1])**2)
                f_cost = g_cost + h_cost
                if f_cost < best_f_cost:
                    best_f_cost = f_cost
                    best_pos = new_pos

        if best_pos is not None:
            return best_pos
        else:
            return None



    def draw(self):
        self.screen.fill((30, 30, 30))
        for y in np.arange(0, self.HEIGHT, 50):
            pg.draw.line(self.screen, (50, 50, 50), (0, y), (self.WIDTH, y))
        for x in np.arange(0, self.WIDTH, 50):
            pg.draw.line(self.screen, (50, 50, 50), (x, 0), (x, self.HEIGHT))

        for block in self.blocks:
            pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(block[0], block[1], 50, 50))
        if self.departure is not None:
            pg.draw.rect(self.screen, (0, 255, 0), pg.Rect(self.departure[0], self.departure[1], 50, 50))
        if self.arrival is not None:
            pg.draw.rect(self.screen, (255, 0, 0), pg.Rect(self.arrival[0], self.arrival[1], 50, 50))
        if self.phase == "pathfinding":
            for pos in self.path:
                pg.draw.rect(self.screen, (147, 112, 219), pg.Rect(pos[0], pos[1], 50, 50))

        if self.phase == "block placing":
            pg.draw.rect(self.screen, (20, 20, 20), pg.Rect(self.mouse_x + 20, self.mouse_y + 20, 10, 10))
        elif self.phase == "green placing":
            pg.draw.rect(self.screen, (0, 255, 0), pg.Rect(self.mouse_x + 20, self.mouse_y + 20, 10, 10))
        elif self.phase == "red placing":
            pg.draw.rect(self.screen, (255, 0, 0), pg.Rect(self.mouse_x + 20, self.mouse_y + 20, 10, 10))

        pg.draw.rect(self.screen, (60, 60, 60), pg.Rect(0, 0, self.WIDTH, 50))

        offset_x = 100

        green_text = pg.font.SysFont("Arial", 20).render("Place Departure", True, (0, 255, 0))
        pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(offset_x - 10, 0, green_text.get_width() + 20, 50))
        self.screen.blit(green_text, (100, green_text.get_height() // 2))
        if self.clicks[0] and pg.Rect(100, 0, green_text.get_width() + 20, 50).collidepoint(self.mouse_x, self.mouse_y):
            self.phase = "green placing"
        offset_x += green_text.get_width() + 20 + 50

        red_text = pg.font.SysFont("Arial", 20).render("Place Arrival", True, (255, 0, 0))
        pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(offset_x - 10, 0, red_text.get_width() + 20, 50))
        self.screen.blit(red_text, (offset_x, red_text.get_height() // 2))
        if self.clicks[0] and pg.Rect(offset_x - 10, 0, red_text.get_width() + 20, 50).collidepoint(self.mouse_x, self.mouse_y):
            self.phase = "red placing"
        offset_x += red_text.get_width() + 20 + 50

        black_text = pg.font.SysFont("Arial", 20).render("Place Blocks", True, (200, 200, 200))
        pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(offset_x - 10, 0, black_text.get_width() + 20, 50))
        self.screen.blit(black_text, (offset_x, black_text.get_height() // 2))
        if self.clicks[0] and pg.Rect(offset_x - 10, 0, black_text.get_width() + 20, 50).collidepoint(self.mouse_x, self.mouse_y):
            self.phase = "block placing"
        offset_x += black_text.get_width() + 20 + 50

        start_text = pg.font.SysFont("Arial", 20).render("Start Pathfinding", True, (147,112,219))
        pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(offset_x - 10, 0, start_text.get_width() + 20, 50))
        self.screen.blit(start_text, (offset_x, start_text.get_height() // 2))
        if self.clicks[0] and pg.Rect(offset_x - 10, 0, start_text.get_width() + 20, 50).collidepoint(self.mouse_x, self.mouse_y):
            if self.departure is not None and self.arrival is not None:
                if self.departure != self.arrival:
                    self.phase = "pathfinding"
                    threading.Thread(target=self.pathfinding).start()
        offset_x += start_text.get_width() + 20 + 50
    
        reset_text = pg.font.SysFont("Arial", 20).render("Reset", True, (255, 165, 0))
        pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(offset_x - 10, 0, reset_text.get_width() + 20, 50))
        self.screen.blit(reset_text, (offset_x, reset_text.get_height() // 2))
        if self.clicks[0] and pg.Rect(offset_x - 10, 0, reset_text.get_width() + 20, 50).collidepoint(self.mouse_x, self.mouse_y):
            self.reset()
        offset_x += reset_text.get_width() + 20 + 50


    def handle_events(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

        self.clicks = pg.mouse.get_pressed()[0:3]

        if self.clicks[0]:
            if self.phase == "block placing" and self.mouse_y > 100:
                if (self.mouse_x // 50 * 50, self.mouse_y // 50 * 50) not in self.blocks:
                    self.blocks.append((self.mouse_x // 50 * 50, self.mouse_y // 50 * 50))
            elif self.phase == "green placing" and self.mouse_y > 100:
                self.departure = (self.mouse_x // 50 * 50, self.mouse_y // 50 * 50)
            elif self.phase == "red placing" and self.mouse_y > 100:
                self.arrival = (self.mouse_x // 50 * 50, self.mouse_y // 50 * 50)
        elif self.clicks[1]:
            pass
        elif self.clicks[2]:
            if self.phase == "block placing":
                if (self.mouse_x // 50 * 50, self.mouse_y // 50 * 50) in self.blocks:
                    self.blocks.remove((self.mouse_x // 50 * 50, self.mouse_y // 50 * 50))
            elif self.phase == "green placing":
                self.departure = None
            elif self.phase == "red placing":
                self.arrival = None

    def run(self):
        while self.running:

            self.handle_events()
            self.draw()

            pg.display.update()
            self.clock.tick(self.FPS)
        pg.quit()


if __name__ == "__main__":
    pg.init()
    pg.display.init()
    app = App()
    app.run()
