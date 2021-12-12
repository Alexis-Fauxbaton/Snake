import random
import pygame
import sys

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
NONE = 0


class Snake:
    def __init__(self):
        self.body = [[WINDOW_HEIGHT//2, WINDOW_WIDTH//2]]
        self.head = self.body[0]
        self.length = len(self.body)
        self.dead = False
        self.dir = RIGHT

    def move(self,direction):

        x = self.body[-1][0]
        #print(self.body[0])
        y = self.body[-1][1]

        

        if direction == NONE:
            direction = self.dir
        if direction == UP:
            self.dir = UP
            y = self.body[-1][1] - 10
        elif direction == DOWN:
            self.dir = DOWN
            y = self.body[-1][1] + 10
        elif direction == RIGHT:
            self.dir = RIGHT
            x = self.body[-1][0] + 10
        else:
            self.dir = LEFT
            x = self.body[-1][0] - 10
        
        self.body.append([x,y])

        self.head = self.body[-1]

        if len(self.body) > self.length:
            del self.body[0]
        

    def collision(self):
        #RAJOUTER OBSTACLES
        if self.head[0] < 0 or self.head[0] > WINDOW_HEIGHT or self.head[1] > WINDOW_WIDTH or self.head[1] < 0:
            print("Collision avec le décor, pos = ",self.body)
            self.dead = True
        else:
            if self.length > 2:
                for i in range(1,self.length-1):
                    if self.head == self.body[i]:
                        self.dead = True
                        print("Collision avec soi meme, pos = ",self.body)
        
    def grow(self,respawn):
        if respawn:
            print("Here")
            self.length += 1

    def draw(self,surface):
        for i in range(self.length):
            pygame.draw.rect(surface,'black',pygame.Rect(self.body[i][0],self.body[i][1],10,10))


class Target():
    def __init__(self):
        #self.x = random.randint(0,WINDOW_WIDTH)
        self.x = random.randrange(0, WINDOW_WIDTH, 10)
        self.y = random.randrange(0, WINDOW_HEIGHT, 10)

    def respawn(self,snake):
        if snake.head == [self.x,self.y]:
            self.x = random.randrange(0, WINDOW_WIDTH, 10)
            self.y = random.randrange(0, WINDOW_HEIGHT, 10)
            return True

        return False

    def draw(self,surface):
        pygame.draw.rect(surface,'red',pygame.Rect(self.x,self.y,10,10))

class Obstacle:
    def __init__(self):
        pass

class Obstacles:
    def __init__(self):
        pass

class Jeu():
    def __init__(self):
        self.target = Target()
        self.snake = Snake()

    def play(self):
        surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        clock = pygame.time.Clock()
        snake_move = 0
        while self.snake.dead == False:
            
            for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()

            
            surface.fill('white')

            self.target.draw(surface)
            self.snake.draw(surface)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake_move = 1
                elif event.key == pygame.K_DOWN:
                    snake_move = 3
                elif event.key == pygame.K_RIGHT:
                    snake_move = 2
                elif event.key == pygame.K_LEFT:
                    snake_move = 4
                elif event.key == pygame.K_TAB:
                    self.snake.grow(True)

            clock.tick(30)
            pygame.display.flip()

            self.snake.grow(self.target.respawn(self.snake))

            #self.target.draw(surface)

            self.snake.move(snake_move)

            self.snake.collision()

            



if __name__ == "__main__":
    jeu = Jeu()

    jeu.play()
            



