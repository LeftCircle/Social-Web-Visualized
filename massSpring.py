# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:38:59 2019
basic mass spring solver using rk4

In order to update SWParticles, the velocity and the positions of the particles
must be extracted. New values are then calculated through the SpringLink class
and must then be put back into the SWParticles class. 
"""
import numpy as np
'''
#initial conditions (will have to be trashed. Cannot be used in general code)
ks = 5    #spring constant
kd = 5    #damping coefficient
r = 10    #rest length | will be a function to determine this for social web
h = 0.05 #timestep NOTE: this will have to be dt from wherever we built that
endTime = 10 #seconds the simulation will run
'''
#note, as endT -> inf, |I - r| -> 0

class SpringLink:
    def __init__(self, position1, velocity1, 
                 position2, velocity2, ks, kd, restLength, dt):
        #all positions and velocites are given in vectors, so we need the x 
        #and y direction of the pos/vel.
        self.position1 = position1
        self.velocity1 = velocity1
        self.position2 = position2
        self.velocity2 = velocity2
        self.ks = ks
        self.kd = kd
        self.restLength = restLength
        self.dt = dt
        
    #damped spring equation from pixar lecture (inlcudes direction)
    # fa = -[ks(|I| - r) + kd*Idot dot I / |I|] * I / |I| 
    # I = a - b    Idot = va - vb (relative velocity)    
    #fb = -fa
    #------------------------------        
    # m*xdd + c*xd + kx = 0
    def relPos(self, position1, position2):
        return position1 - position2
    
    #negative velocity is moving towards the rest lenght?
    def relVel(self, velocity1, velocity2):
        return velocity1 - velocity2
    
    def mag(self, I):
        return np.sqrt(I[0]**2 + I[1]**2)
    
    
    #NOTE: currently not accounting for mass in force, but this could
    # be done by using a weighted average mass?
    #dx = dv
    #dv = -[ks(|I| - r) + kd*Idot dot I / |I|] * I / |I|
    #NOTE - consider dimensionless ks(|I|/r - 1) instead
    def dv(self, rk4PosAdd, rk4VelAdd):
        I    = self.relPos(self.position1 + rk4PosAdd,
                           self.position2 + rk4PosAdd) #vector
        Idot = self.relVel(self.velocity1 + rk4VelAdd,
                           self.velocity2 + rk4VelAdd) #vector
        magI = self.mag(I)
        return -(self.ks * (magI/self.restLength - 1) + self.kd * 
                 np.dot(Idot,I) / magI) * I / magI 
    
    def dx(self, rk4Addition):
        return self.relVel(self.velocity1 + rk4Addition,
                           self.velocity2 + rk4Addition) 
    
    def springForceRK4(self):
        #goal is to just take one timestep and update results    
                    
        k1 = self.dx(np.array([0,0]))    #position estimate
        l1 = self.dv(np.array([0,0]), np.array([0,0])) #velocity estimate
        
        k2 = self.dx(l1 * self.dt / 2) 
        l2 = self.dv(k1 * self.dt / 2, l1 * self.dt / 2)
        
        k3 = self.dx(l2 * self.dt / 2) 
        l3 = self.dv(k2 * self.dt / 2, l2 * self.dt / 2)
        
        k4 = self.dx(l3 * self.dt) 
        l4 = self.dv(k3 * self.dt, l3 * self.dt)
        
        posAdd = self.dt / 6.0 * ( k1 + 2.0 * k2 + 2.0 * k3 + k4)
        velAdd = self.dt / 6.0 * ( l1 + 2.0 * l2 + 2.0 * l3 + l4)
        
        self.position1 += posAdd ; self.position2 -= posAdd
        self.velocity1 += velAdd ; self.velocity2 -= velAdd
        
        #new values to update nodes with
        newvals = [self.position1, self.velocity1,
                   self.position2, self.velocity2]
        '''
        to access info:  springForceRK4[i][j]
        i = position1/2 or velocity1/2 (0 = pos1, 1 = vel1, ...)
        j = x/y (0 = x, 1 = y)
        '''
        return newvals