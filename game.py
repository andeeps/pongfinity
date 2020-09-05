import pygame
#import pandas as pd
import random as rd

#Initializing variables
width = 1200
height = 600
border = 20
framerate = 800
score = 0

# Define classes       
class Paddle:
    
    width = 20
    height = 100
    
    def __init__(self,Y):
        self.Y = Y
        
    def show(self,color):
        global screen
        pygame.draw.rect(screen, color, pygame.Rect(width-self.width,self.Y-self.height//2, width,self.height))
        
    def update(self):
        
        global fgcolor, bgcolor

        self.show(bgcolor)
        Y = pygame.mouse.get_pos()[1]
        
        if height-border-self.height//2 > Y > border+self.height//2 :
            self.Y = Y
        
        self.show(fgcolor)
        
class Ball:
    
    radius = 10
    
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
    def show(self,color):
        global screen
        pygame.draw.circle(screen,color, (int(self.x),int(self.y)), self.radius)
        
    def update(self,Y):
        global fgcolor, bgcolor, width, height, score
        
        newx = self.x + self.vx
        newy = self.y + self.vy
        
        if newx < border+self.radius or newx > width-self.radius:
            self.vx = -self.vx
        elif newy>Y-50 and newy<Y+50 and newx==width-border-self.radius:
            self.vx = -self.vx
            score = score+1
            #self.vy = -self.vy
        elif newx > width-border:
            score = 0
            self.vx = -self.vx
        elif newy < border+self.radius or newy > height-border-self.radius:
            self.vy = -self.vy
        else:
            self.show(bgcolor)
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            self.show(fgcolor)


# setting up dynamic variables:            
x,y = rd.randint(border+15,width-border-5),rd.randint(border+15,height-border-5)        # location of the ball is radomized within the field and changes from game to game
velocity_x, velocity_y = round(rd.uniform(0.5,1.5),1),round(rd.uniform(0.5,1.5),1)      # velocity of the ball is changes from game to game

# Create objects:
ball = Ball(x, y, -velocity_x, -velocity_y)                                             # defining 
paddle = Paddle(height/2)

# Draw the scenario
pygame.init()

screen = pygame.display.set_mode((width,height))

bgcolor = pygame.Color("black")
fgcolor = pygame.Color("white")

pygame.draw.rect(screen, fgcolor,pygame.Rect((0,0),(width,border)))
pygame.draw.rect(screen, fgcolor,pygame.Rect(0,0,border,height))
pygame.draw.rect(screen, fgcolor,pygame.Rect((0,0),(width,border)))
pygame.draw.rect(screen, fgcolor,pygame.Rect(0,height-border,width,border))

font = pygame.font.SysFont('Calibri', 20, False, False)

######################################################
#label = myfont.render(text, 1, (0,0,250))
#previous_rect = label.get_rect(topleft=(100,100))
#screen.blit(label, (100, 100))
######################################################

ball.show(fgcolor)
paddle.show(fgcolor)

clock = pygame.time.Clock()

# Create a file to store the generated data:
sample = open ("game.csv", "w")
sample.truncate(0)
print( "x,y,vx,vy,Paddle.y", file = sample)

######################################################
#from sklearn.neighbors import KNeighborsRegressor
#from sklearn.linear_model import LinearRegression
#clf = KNeighborsRegressor(n_neighbors = 3)
#clf = LinearRegression().fit(X, Y)
######################################################

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
    clock.tick(framerate)
    pygame.display.flip()
    
    ##################################################
    #pong = pd.read_csv("C:/Users/sandeep.p/Desktop/pygame/game.csv")
    #pong = pong.drop_duplicates()
    #X = pong.drop(columns="Paddle.y")
    #Y = pong['Paddle.y']
    #clf = clf.fit(X,Y)
    #df = pd.DataFrame(columns = ['x','y','vx','vy'])
    #toPredict = df.append ({'x': ball.x, 'y': ball.y, 'vx': ball.vx, 'vy': ball.vy}, ignore_index = True)
    #padpos = clf.predict(toPredict)
    ##################################################
    
    paddle.update()         #padpos
    ball.update(paddle.Y)
    
    # Score update code needs to be optimised
    text = font.render('Score : ' + str(score), True, fgcolor)
    textpos = text.get_rect()
    textpos.center = (width//2,border*2)
    screen.fill(bgcolor, rect=textpos)
    screen.blit(text,textpos)
    
    print("{},{},{},{},{}".format(ball.x,ball.y,ball.vx,ball.vy,paddle.Y), file = sample)
    
pygame.quit()
    