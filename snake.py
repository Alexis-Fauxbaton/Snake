import random
import pygame
import sys
import Q_learning
import bitmap
import numpy as np

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
NONE = 0

ACTION_UP = 0
ACTION_RIGHT = 1
ACTION_DOWN = 2
ACTION_LEFT = 3


# States

#Configurations
# Snake is above/under the apple
# Snake is at the left/right of the apple
# Danger at the left/right/above/under within len(snake) blocks 

# position : 4 configurations
# Danger : 4 configurations

"""
State Configuration table:

Above/under apple : 1,0
Right/Left of apple : 1,0
Danger left : 1,0
Danger right : 1,0
Danger above : 1,0
Danger underneath : 1,0

"""
STATES = 2**6
ACTIONS = 4
# Actions


class Snake:
    def __init__(self, train=False):
        self.body = [[WINDOW_HEIGHT//2, WINDOW_WIDTH//2]]
        self.head = self.body[0]
        self.x = self.head[0]
        self.y = self.head[1]
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
            y = self.body[-1][1] - 25
        elif direction == DOWN:
            self.dir = DOWN
            y = self.body[-1][1] + 25
        elif direction == RIGHT:
            self.dir = RIGHT
            x = self.body[-1][0] + 25
        else:
            self.dir = LEFT
            x = self.body[-1][0] - 25
        
        self.body.append([x,y])

        self.head = self.body[-1]
        self.x = self.head[0]
        self.y = self.head[1]

        if len(self.body) > self.length:
            del self.body[0]
        

    def collision(self):
        #RAJOUTER OBSTACLES
        if self.x < 0 or self.x >= WINDOW_WIDTH or self.y >= WINDOW_HEIGHT or self.y < 0:
            #print("Collision avec le décor, pos = ",self.body)
            self.dead = True
        else:
            if self.length > 2:
                for i in range(1,self.length-1):
                    if self.head == self.body[i]:
                        self.dead = True
                        #print("Collision avec soi meme, pos = ",self.body)
        
    def grow(self,respawn):
        if respawn:
            #print("Here")
            self.length += 1

    def draw(self,surface):
        for i in range(self.length):
            pygame.draw.rect(surface,'black',pygame.Rect(self.body[i][0],self.body[i][1],25,25))

    def encode_state(self,target):
        encoded_map = bitmap.BitMap(6)
        bit_position = 0
        collision_left = False
        collision_right = False
        collision_up = False
        collision_down = False

        #Encode relative position to apple
        if self.y < target.y:
            encoded_map.set(bit_position)
        bit_position+=1
        if self.x > target.x:
            encoded_map.set(bit_position)
        bit_position+=1
        #Encode Danger
        for i in range(1,self.length):
                    if [self.x-25,self.y] == self.body[i]:
                        collision_left = True
        for i in range(1,self.length):
                    if [self.x+25,self.y] == self.body[i]:
                        collision_right = True
        for i in range(1,self.length):
                    if [self.x,self.y+25] == self.body[i]:
                        collision_down = True
        for i in range(1,self.length):
                    if [self.x,self.y-25] == self.body[i]:
                        collision_up = True
        if self.x-10 < 0 or collision_left:
            encoded_map.set(bit_position)
        bit_position+=1
        if self.x+10 > WINDOW_WIDTH or collision_right:
            encoded_map.set(bit_position)
        bit_position+=1
        if self.y-10 < 0 or collision_up:
            encoded_map.set(bit_position)
        bit_position+=1
        if self.y+10 > WINDOW_HEIGHT or collision_down:
            encoded_map.set(bit_position)

        return encoded_map.tostring()[2:]
        
    def reward(self,target):
        if self.head == [target.x,target.y]:
            return 500

        elif self.dead == True:
            return -100

        else:
            return -3



class Target():
    def __init__(self):
        #self.x = random.randint(0,WINDOW_WIDTH)
        self.x = random.randrange(0, WINDOW_WIDTH, 25)
        self.y = random.randrange(0, WINDOW_HEIGHT, 25)

    def respawn(self,snake):
        if snake.head == [self.x,self.y]:
            self.x = random.randrange(0, WINDOW_WIDTH, 25)
            self.y = random.randrange(0, WINDOW_HEIGHT, 25)
            return True

        return False

    def draw(self,surface):
        pygame.draw.rect(surface,'red',pygame.Rect(self.x,self.y,25,25))

class Obstacle:
    def __init__(self):
        pass

class Obstacles:
    def __init__(self):
        pass

class Jeu():
    def __init__(self, train=False):
        self.target = Target()
        self.snake = Snake()
        self.pause = False
        if train:
            self.Q_learning = Q_learning.Q_learning(STATES, ACTIONS)

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
                    self.pause = True

            clock.tick(30)
            pygame.display.flip()

            while self.pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            self.pause = False


            self.snake.grow(self.target.respawn(self.snake))

            #self.target.draw(surface)

            self.snake.move(snake_move)

            #print(self.snake.encode_state(self.target))

            self.snake.collision()

            print(self.snake.reward(self.target))

    def train_q_learning(self):
        surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        clock = pygame.time.Clock()
        episode = 0
        display = False
        for episode in range(self.Q_learning.max_episodes):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        if display==False:
                            display = True
            
            if episode % 1000 == 0:
                print("Episode : ",episode)
                self.Q_learning.max_steps = self.Q_learning.max_steps*1.01
            
            curr_reward = 0
            self.target = Target()
            self.snake = Snake()
            step = 0
            if display:
                print("\n\n\n\n",self.Q_learning.q_table)
            while self.snake.dead == False and step<self.Q_learning.max_steps: 
                if display:
                    surface.fill('white')

                    self.target.draw(surface)
                    self.snake.draw(surface)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: sys.exit()
                        
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_d:
                                if display==False:
                                    display = True
                                elif display==True:
                                    display = False
                            elif event.key == pygame.K_p:
                                    self.pause = True
                            elif event.key == pygame.K_s:
                                    np.savetxt("Q_table.txt",self.Q_learning.q_table)
                        
                
                while self.pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: sys.exit()
                        
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                self.pause = False

                            elif event.key == pygame.K_i:
                                print(self.snake.head)
                
                state = int(self.snake.encode_state(self.target),2)

                action = self.Q_learning.choose_action(state)
                if display:
                    clock.tick(30)
                    pygame.display.flip()

                self.snake.grow(self.target.respawn(self.snake))

                self.snake.move(action+1)

                self.snake.collision()

                next_state = int(self.snake.encode_state(self.target),2)

                reward = self.snake.reward(self.target)

                curr_reward += reward

                self.Q_learning.update_q_table(state, action, reward, next_state)
                
                step+=1

                

            self.Q_learning.rew_list.append(curr_reward)

            self.Q_learning.update_epsilon(episode)

            display = False
            surface.fill('black')
            pygame.display.flip()

        rew_per_thousand_episodes = np.array_split(np.array(self.Q_learning.rew_list),episode/1000)

        count = 1000

        print("*********Average reward per 1000 episode**********")

        for r in rew_per_thousand_episodes:
            print(count, " :", str(sum(r/1000)))
            count+=1000

        print("**********Optimal Q table*********")

        print(self.Q_learning.q_table)
            


    def evaluate_training(self,n_games):
        surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        clock = pygame.time.Clock()
        Q_table = np.loadtxt("Q_table.txt")
        score_list = []
        for game in range(n_games):
            score = 0
            self.target = Target()
            self.snake = Snake()
            step = 0
            while self.snake.dead == False:

                state = int(self.snake.encode_state(self.target),2)


                for event in pygame.event.get():
                        if event.type == pygame.QUIT: sys.exit()
                        
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                self.pause = True

                surface.fill('white')

                self.target.draw(surface)
                self.snake.draw(surface)

                clock.tick(30)
                pygame.display.flip()

                while self.pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: sys.exit()
                        
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                self.pause = False

                            elif event.key == pygame.K_i:
                                print(self.snake.head)

                

                action = np.argmax(Q_table[state])

                self.snake.grow(self.target.respawn(self.snake))

                self.snake.move(action+1)

                self.snake.collision()

                score += self.snake.reward(self.target)
            score_list.append(score)

            print("Game : ",game,"\n")
            print("Score : ",score)
            print(np.array(score_list).mean())
            print("\n\n")







            



if __name__ == "__main__":
    jeu = Jeu(True)

    #jeu.play()

    #jeu.train_q_learning()

    jeu.evaluate_training(n_games=100)
            



