#particles class for the social web
import numpy as np
import pygame
import pygameTutorial as pgt

#example particle class 
'''
#drawing a circle (location, color, (x,y) coordinate, radius, thickness)
#thickness = 0 fills the circle
pygame.draw.circle(game_display, (0,0,255), 
                   (int(width / 2), int(height / 2)), 
                   15, 1)
'''

class Particle:
    def __init__(self, color, x, y, radius, thickness, velocity, angle):
        self.color = color
        self.x = x #x position of the center
        self.y = y #y position of the center
        self.radius = radius
        self.thickness = thickness
        self.velocity = velocity
        #why the angle is not being determined based on velocity and position
        #I do not know...but such is the code at this point
        self.angle = angle #in radians...normal raidans or reversed?
        self.mass = 1
        self.airtime = 0
        self.width = pgt.App().width
        self.height = pgt.App().height
        self.game_display = pygame.display.set_mode((self.width, self.height))
        self.dt = 0
        self.selectedParticle = False #ability to click on a particle to drag
    
    
    '''
    def dt_and_oldTime(self, oldTime):
        t = pygame.time.get_ticks()
        dt = (t - oldTime) / 1000.0
        return dt, t
    '''
    def updateDeltaTime(self, newDeltaTime):
        self.dt = newDeltaTime
        
    def yvel(self):
        return self.velocity * np.sin(self.angle)
    
    def xvel(self):
        return self.velocity * np.cos(self.angle)
    
    def updateVel(self, xvel, yvel):
        self.velocity = np.sqrt(xvel**2 + yvel**2)
        self.angle = np.arctan2(yvel, xvel)
        
    def damping(self):
        self.velocity *= 0.98
        
    def move(self):
        if self.selectedParticle == False:
            self.x += self.xvel()
            #we are going to have theta rotate clockwise because the y vector is
            #positive when pointing down
            self.y += self.yvel()
    
    def totalVelocitySq(self):
        return self.x**2 + self.y**2
    
    def kineticEnergy(self):
        return 0.5 * self.mass * self.totalVelocitySq()
    
    def potentialEnergy(self):
        return self.mass * 9.8 * self.height - self.y
    
    def gravity(self,):
         if self.selectedParticle == False:
             self.airtime += self.dt
             self.y += 0.5 * 9.8 * self.airtime**2
        
    #for a rebound reset, self.x = 2 * (width - self.radius) - self.x
    #adding in non elastic collisions
    def bounce(self, elasticityConstant):
        if self.x > self.width - self.radius:
            self.x = 2 * (self.width - self.radius) - self.x
            self.angle = np.pi - self.angle
            self.velocity *= elasticityConstant
        
        elif self.x < self.radius:
            self.x = 2 * self.radius - self.x
            self.angle = np.pi - self.angle
            self.velocity *= elasticityConstant
            
        if self.y > self.height - self.radius:
            self.y = 2 * ( self.height - self.radius) - self.y
            self.angle = - self.angle
            self.airtime = 0
            self.velocity *= elasticityConstant
        
        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle = -self.angle
            self.velocity *= elasticityConstant
    
    #display method to draw the particle on the screen
    def display(self):
        pygame.draw.circle(self.game_display, self.color, 
                           (int(self.x), int(self.y)),
                           self.radius, self.thickness)
    
    #dragging the particle with the mouse and releasing with mousebuttonup
    def mouseDrag(self):
        if self.selectedParticle == True:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            #giving the particle velocity based off of mouse speed
            dx = mouseX - self.x
            dy = mouseY - self.y
            #expensive function because we are using angles for some reason
            self.angle = np.arctan2(dy,dx)
            self.velocity = np.sqrt(dx**2 + dy**2)
            self.x = mouseX
            self.y = mouseY
    
    def circleCircleCollision(self, otherParticle):
        radiusSum = self.radius + otherParticle.radius
        #calculating the squared distance between centers
        distX = self.x - otherParticle.x
        distY = self.y - otherParticle.y
        distSq = distX**2 + distY**2
        magDist = np.sqrt(distX**2 + distY**2)
        #normal direction from self to other particle in x and y direction?
        normDirSelfToPartX = distX / magDist
        normDirSelfToPartY = distY / magDist
        #self should move - normDirSelfTo.. and other should move positive?
        angleReflSelf = np.arctan2(normDirSelfToPartY, normDirSelfToPartX)
        #only doing logic if there is a collision
        if distSq <= radiusSum**2:
            #providing a test impulse in the opposite direction
            self.x += normDirSelfToPartX
            self.y += normDirSelfToPartY
            
            otherParticle.x -= normDirSelfToPartX
            otherParticle.y -= normDirSelfToPartY
            
            self.velocity += 0 ; self.angle += np.pi
            otherParticle.velocity += 0
            otherParticle.angle += np.pi
    
    
     
        
        