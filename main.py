## Boids 
## Run module
import sys, pygame, random, math

pygame.init()

# setup
pygame.display.set_caption("Boids")
WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)

max_speed = 5
pred_max_speed = 7
num_boids = 50
boids_list = []
num_predator = 1
predator_list = []

BORDER = 100
BORDERSPEEDCHANGE = 0.2

#predatorradius = 50
#predator = [200,200]
PREYSPEEDCHANGE = 0.2

barrier = [400,400]
BARRIERRADIUS = 80


class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = random.randint(1, 5) / 5.0
        self.speed_y = random.randint(1, 5) / 5.0
    
    # return the distance of another boid
    def distance(self, boid):
        dist_x = self.x - boid.x 
        dist_y = self.y - boid.y 

        return math.sqrt(dist_x * dist_x + dist_y * dist_y)

    # move closer to set of boids
    def move_closer(self, boids_list):
        global distance
        if len(boids_list) < 1: 
            return
            
        # calculate the average distances from the other boids
        avg_x = 0
        avg_y = 0
        for boid in boids_list:
            if boid.x == self.x and boid.y == self.y:
                continue
                
            avg_x += (self.x - boid.x)
            avg_y += (self.y - boid.y)

        avg_x /= len(boids_list)
        avg_y /= len(boids_list)

        # set our speed towards the others
        distance = math.sqrt((avg_x * avg_x) + (avg_y * avg_y)) * -0.5
       
        self.speed_x -= (avg_x / 100) 
        self.speed_y -= (avg_y / 100) 
        
    # moving with the set of boids
    def move_with(self, boids_list):
        if len(boids_list) < 1: return
        # calculate the average speed of other boids
        avg_x = 0
        avg_y = 0
                
        for boid in boids_list:
            avg_x += boid.speed_x
            avg_y += boid.speed_y
            
        avg_x /= len(boids_list)
        avg_y /= len(boids_list)

        # set our speed towards the others
        self.speed_x += (avg_x / 80)
        self.speed_y += (avg_y / 80)
    
    # moves away from boids, avoids crowding
    def move_away(self, boids_list, min_distance):
        if len(boids_list) < 1: return
        
        distance_x = 0
        distance_y = 0
        num_close = 0

        for boid in boids_list:
            distance = self.distance(boid)
            if  distance < min_distance:
                num_close += 1
                xdiff = (self.x - boid.x) 
                ydiff = (self.y - boid.y) 
                
                if xdiff >= 0: 
                    xdiff = math.sqrt(min_distance) - xdiff
                elif xdiff < 0: 
                    xdiff = - math.sqrt(min_distance) - xdiff
                
                if ydiff >= 0: 
                    ydiff = math.sqrt(min_distance) - ydiff
                elif ydiff < 0: 
                    ydiff = - math.sqrt(min_distance) - ydiff

                distance_x += xdiff 
                distance_y += ydiff 
        
        if num_close == 0:
            return
            
        self.speed_x -= distance_x / 5
        self.speed_y -= distance_y / 5
        
    # preform movement based on the velocity
    def move(self):
        if abs(self.speed_x) > max_speed or abs(self.speed_y) > max_speed:
            sF = max_speed / max(abs(self.speed_x), abs(self.speed_y))
            self.speed_x *= sF
            self.speed_y *= sF
        
        self.x += self.speed_x
        self.y += self.speed_y




class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = random.randint(1, 8) / 5.0
        self.speed_y = random.randint(1, 8) / 5.0
    
    def distance(self, predator):
        dist_x = self.x - predator.x 
        dist_y = self.y - predator.y 

        return math.sqrt(dist_x * dist_x + dist_y * dist_y)

    def move_closer(self, predator_list):
        global distance
        if len(predator_list) < 1: 
            return
            
        avg_x = 0
        avg_y = 0
        for predator in predator_list:
            if predator.x == self.x and predator.y == self.y:
                continue
                
            avg_x += (self.x - predator.x)
            avg_y += (self.y - predator.y)

        avg_x /= len(predator_list)
        avg_y /= len(predator_list)

        distance = math.sqrt((avg_x * avg_x) + (avg_y * avg_y)) * -0.5
       

    def move_away(self, predator_list, min_distance):
        if len(predator_list) < 1: return
        
        distance_x = 0
        distance_y = 0
        num_close = 0

        for predator in predator_list:
            distance = self.distance(predator)
            if  distance < min_distance:
                num_close += 1
                xdiff = (self.x - predator.x) 
                ydiff = (self.y - predator.y) 
                
                if xdiff >= 0: 
                    xdiff = math.sqrt(min_distance) - xdiff
                elif xdiff < 0: 
                    xdiff = - math.sqrt(min_distance) - xdiff
                
                if ydiff >= 0: 
                    ydiff = math.sqrt(min_distance) - ydiff
                elif ydiff < 0: 
                    ydiff = - math.sqrt(min_distance) - ydiff

                distance_x += xdiff 
                distance_y += ydiff 
        
        if num_close == 0:
            return
            
        self.speed_x -= distance_x / 5
        self.speed_y -= distance_y / 5
        
    # preform movement based on the velocity
    def move(self):
        if abs(self.speed_x) > pred_max_speed or abs(self.speed_y) > pred_max_speed:
            sF = pred_max_speed / max(abs(self.speed_x), abs(self.speed_y))
            self.speed_x *= sF
            self.speed_y *= sF
        
        self.x += self.speed_x
        self.y += self.speed_y

window = pygame.display.set_mode((WIDTH, HEIGHT))

ball = pygame.image.load("ball.png")
ball = pygame.transform.scale(ball, (20,20))
ball_rect = ball.get_rect()

red_ball = pygame.image.load("predator.png")
red_ball = pygame.transform.scale(red_ball, (20,20))
red_ball_rect = ball.get_rect()

# create boids at random positions
for i in range(num_boids):
    boids_list.append(Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)))  

for i in range(num_predator):
    predator_list.append(Predator(random.randint(0, WIDTH), random.randint(0, HEIGHT)))  

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for boid in boids_list:
        close_boids = []
        for other_boid in boids_list:
            if other_boid == boid: 
                continue
            distance = boid.distance(other_boid)
            if distance < 90:
                close_boids.append(other_boid)
        
        # bounce off border and slow down
        distance_x = barrier[0] - boid.x
        distance_y = barrier[1] - boid.y
        dist = math.sqrt(distance_x*distance_x + distance_y*distance_y)
        if (dist < BARRIERRADIUS + 15):
            boid.speed_x -= distance_x * 1
            boid.speed_x *= 0.6
            boid.speed_y -= distance_y * 1
            boid.speed_y *= 0.6

        boid.move_closer(close_boids)
        boid.move_with(close_boids)  
        boid.move_away(close_boids, 20)  
        
        # boids move away from border
        if (boid.x < BORDER):
            boid.speed_x += BORDERSPEEDCHANGE
        if (boid.y < BORDER):
            boid.speed_y += BORDERSPEEDCHANGE
        if (boid.x > WIDTH - BORDER):
            boid.speed_x -= BORDERSPEEDCHANGE
        if (boid.y > HEIGHT - BORDER):
            boid.speed_y -= BORDERSPEEDCHANGE

        # boids to stay within the screen space
        border = 25
        if boid.x < border and boid.speed_x < 0:
            boid.speed_x = - boid.speed_x * random.randint(1,5)
        if boid.x > WIDTH - border and boid.speed_x > 0:
            boid.speed_x = - boid.speed_x * random.randint(1,5)
        if boid.y < border and boid.speed_y < 0:
            boid.speed_y = - boid.speed_y * random.randint(1,5)
        if boid.y > HEIGHT - border and boid.speed_y > 0:
            boid.speed_y = - boid.speed_y * random.randint(1,5)
            
        boid.move()
    
    for predator in predator_list:
        for other_predator in predator_list:
            if other_predator == predator: 
                continue
            distance = predator.distance(other_predator)
            if distance < 90:
                close_boids.append(other_predator)
        
        # bounce off border and slow down
        distance_x = barrier[0] - predator.x
        distance_y = barrier[1] - predator.y
        dist = math.sqrt(distance_x*distance_x + distance_y*distance_y)
        if (dist < BARRIERRADIUS + 15):
            predator.speed_x -= distance_x * 1
            predator.speed_x *= 0.6
            predator.speed_y -= distance_y * 1
            predator.speed_y *= 0.6
        
        
        predator.move_away(close_boids, 20)  
        
        # boids move away from border
        if (predator.x < BORDER):
            predator.speed_x += BORDERSPEEDCHANGE
        if (predator.y < BORDER):
            predator.speed_y += BORDERSPEEDCHANGE
        if (predator.x > WIDTH - BORDER):
            predator.speed_x -= BORDERSPEEDCHANGE
        if (predator.y > HEIGHT - BORDER):
            predator.speed_y -= BORDERSPEEDCHANGE

        # boids to stay within the screen space
        border = 25
        if predator.x < border and predator.speed_x < 0:
            predator.speed_x = - predator.speed_x * random.randint(1,5)
        if predator.x > WIDTH - border and predator.speed_x > 0:
            predator.speed_x = - predator.speed_x * random.randint(1,5)
        if predator.y < border and predator.speed_y < 0:
            predator.speed_y = - predator.speed_y * random.randint(1,5)
        if predator.y > HEIGHT - border and predator.speed_y > 0:
            predator.speed_y = - predator.speed_y * random.randint(1,5)
            
        predator.move()

    window.fill(BLACK)
    for boid in boids_list:
        boid_rect = pygame.Rect(ball_rect)
        boid_rect.x = boid.x
        boid_rect.y = boid.y
        window.blit(ball, boid_rect)
    
    for predator in predator_list:
        predator_rect = pygame.Rect(red_ball_rect)
        predator_rect.x = predator.x
        predator_rect.y = predator.y
        window.blit(red_ball, predator_rect)
    
    pygame.draw.circle(window, (0,100,100), (int(barrier[0]), int(barrier[1])), BARRIERRADIUS, 0)
    #pygame.draw.circle(window, (255,0,0), (int(predator[0]), int(predator[1])), predatorradius, 0)

    pygame.display.flip()
    pygame.time.delay(30)
