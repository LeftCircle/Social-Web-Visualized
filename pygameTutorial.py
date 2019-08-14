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
                                            yPos, 15, 0, 2, np.pi / 3.)
                                            )
        
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
        
        #creating dt
        currentTime = pygame.time.get_ticks()
        self.dt = (currentTime - self.oldTime) / 1000.0
        #sloppy fix to get the first dt correct
        if self.dt > 10:
                self.dt = 0        
        self.oldTime = currentTime
        
        #updating particles | doing this with cuda would be hot
        for i in range(self.numberOfParticles):
            #update dt then move the particle 
            self.particleList[i].updateDeltaTime(self.dt)
            self.particleList[i].move()
            self.particleList[i].mouseDrag()
            if i == self.numberOfParticles - 1:
                self.particleList[i].gravity()
            self.particleList[i].bounce(0.8)
            
        #updating particles 1 and 2 which are linked by a spring
        #NOTE!!!! springs break the ability to click on a linked particle.
        pos1 = np.array([self.particleList[0].x, self.particleList[0].y]) 
        pos2 = np.array([self.particleList[1].x, self.particleList[1].y])
        
        vel1 = np.array([self.particleList[0].xvel(),
                         self.particleList[0].yvel()])
        vel2 = np.array([self.particleList[1].xvel(),
                         self.particleList[1].yvel()])
        #position1, velocity1, position2, velocity2, ks, kd, restLength, dt
        firstLink = spring.SpringLink(pos1, vel1, pos2, vel2,
                                      5, 2, 50, self.dt)
        newPosAndVel = firstLink.springForceRK4()
        self.particleList[0].x = newPosAndVel[0][0]
        self.particleList[0].y = newPosAndVel[0][1]
        self.particleList[0].updateVel(newPosAndVel[1][0], 
                                       newPosAndVel[1][1])
                
        self.particleList[1].x = newPosAndVel[2][0]
        self.particleList[1].y = newPosAndVel[2][1]
        self.particleList[1].updateVel(newPosAndVel[3][0], 
                                       newPosAndVel[3][1])
        
        
        #collision must be checked after all of the movement occurs
        for i in range(self.numberOfParticles):
            for j in range(self.numberOfParticles - 1 - i):
                if self.particleList[i].circleCircleCollision(
                        self.particleList[i+j+1]) == True:
                    print('Collision detected')
                    self.particleList[i].angle += np.pi
                    self.particleList[i+j].angle += np.pi
                
                    
    
    def on_render(self):
        #render the updated positions
        self.game_display.fill(self.background_color)
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
    