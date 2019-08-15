import pygame
import numpy as np
import SWParticles as swp
import massSpring as spring

class App:
    def __init__(self):
        self.running = True
        self.game_display = None
        self.image_surf = None
        self.background_color = (255,255,255)
        self.width = 650
        self.height = 650
        #initializing getTicksLastGrame to create a dt but this might not work
        self.oldTime = pygame.time.get_ticks()
        self.dt = 0
        self.numberOfParticles = 5
        self.particleList = []
    
    #list of functions that will be used below
    def updateDt(self):
        #creating dt
        currentTime = pygame.time.get_ticks()
        self.dt = (currentTime - self.oldTime) / 1000.0
        #sloppy fix to get the first dt correct
        if self.dt > 10:
                self.dt = 0        
        self.oldTime = currentTime
    
    #linking particle i and particle j
    def linkParticles(self, i, j):
        pos1 = np.array([self.particleList[i].x, self.particleList[i].y]) 
        pos2 = np.array([self.particleList[j].x, self.particleList[j].y])
        
        vel1 = np.array([self.particleList[i].xvel(),
                         self.particleList[i].yvel()])
        vel2 = np.array([self.particleList[j].xvel(),
                         self.particleList[j].yvel()])
        #position1, velocity1, position2, velocity2, ks, kd, restLength, dt
        firstLink = spring.SpringLink(pos1, vel1, pos2, vel2,
                                      5, 2, 50, self.dt)
        newPosAndVel = firstLink.springForceRK4()
        self.particleList[i].x = newPosAndVel[0][0]
        self.particleList[i].y = newPosAndVel[0][1]
        self.particleList[i].updateVel(newPosAndVel[1][0], 
                                       newPosAndVel[1][1])
                
        self.particleList[j].x = newPosAndVel[2][0]
        self.particleList[j].y = newPosAndVel[2][1]
        self.particleList[j].updateVel(newPosAndVel[3][0], 
                                       newPosAndVel[3][1])
        
    def drawLink(self, i, j, color):
        pygame.draw.aaline(self.game_display, color, (self.particleList[i].x,
                           self.particleList[i].y), (self.particleList[j].x,
                                            self.particleList[j].y))
#------------------------------------------------------------------------------    
    #rendering and everything goes on below here
    #starting positions of particles should go here    
    def on_init(self):
        pygame.init()
        self.game_display = pygame.display.set_mode((self.width,self.height))
        self.running = True
                
        #other variables such as mass, charge, spring constant, etc can go here        
        for i in range(self.numberOfParticles):
            #randomizing the positions for the starting particles 
            xPos = (np.random.randint(20, self.width  - 20))
            yPos = (np.random.randint(20, self.height - 20))
            #color, x, y, radius, thickness, velocity, angle 
            self.particleList.append(swp.Particle((0,0,255), xPos, 
                                            yPos, 15, 0, 2, np.pi / 3., i))
        
    def on_event(self, event):
        #closing the window
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and (
                        event.key == pygame.K_ESCAPE)):
            pygame.quit()
            self.running = False
        
        #checking to see if the player has clicked the screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            #adding functionality with clicks | currently happening before move
            for i in range(self.numberOfParticles):
                particle = self.particleList[i]
                if (abs(mouseX - particle.x) < particle.radius and 
                    abs(mouseY - particle.y) < particle.radius):
                        particle.color = (255,0,0)
                        self.particleList[i].selectedParticle = True
        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(self.numberOfParticles):
                self.particleList[i].selectedParticle = False
                self.particleList[i].color = (0,0,255)
                
       
    #logic to occur each loop. Can create a dt here!        
    def on_loop(self):
        #generating dt for this frame
        self.updateDt()
        
        #updating particles | doing this with cuda would be hot
        for i in range(self.numberOfParticles):
            #update dt then move the particle 
            self.particleList[i].updateDeltaTime(self.dt)
            self.particleList[i].move()
            self.particleList[i].mouseDrag()
            if i == self.numberOfParticles - 1:  #just giving the last particle gravity for testing
                self.particleList[i].gravity()
            self.particleList[i].bounce(0.8)
           
        #updating particles 1 and 2 which are linked by a spring
        self.linkParticles(0,1)   

        #collision detection must occur last
        #collision must be checked after all of the movement occurs
        for i in range(self.numberOfParticles):
            for j in range(i+1, self.numberOfParticles):
                self.particleList[i].circleCircleCollision(
                        self.particleList[j])                                
    
    def on_render(self):
        #render the updated positions
        self.game_display.fill(self.background_color)
        
        self.drawLink(0, 1, (0,0,0))
        #drawing links first 
        #(display, color, (x1, y1), (x2, y2))
        #pygame.draw.aaline(self.game_display, (0,0,0), (self.particleList[0].x,
        #                   self.particleList[0].y), (self.particleList[1].x,
        #                                    self.particleList[1].y))
        for i in range(self.numberOfParticles):
            self.particleList[i].display()
        
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self.running = False
 
        while( self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

#main statement! 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
    