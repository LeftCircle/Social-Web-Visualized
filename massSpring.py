# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:38:59 2019

basic mass spring solver using rk4

Need to generalize how the nodes are updated so that the rk4 infomration is 
included in the Node class. 
"""
import numpy as np
#initial conditions
ks = 5    #spring constant
kd = 5    #damping coefficient
r = 10    #rest length | will be a function to determine this for social web
h = 0.05 #timestep
endTime = 10 #seconds the simulation will run

#note, as endT -> inf, |I - r| -> 0

class Node:
    #position, velocity, force function, mass
    def __init__(self, position, velocity, forceFunc, mass):
        self.pos = position
        self.vel = velocity
        self.ff = forceFunc
        self.m = mass

class vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#damped spring equation from pixar lecture (inlcudes direction)
# fa = -[ks(|I| - r) + kd*Idot dot I / |I|] * I / |I| 
# I = a - b    Idot = va - vb (relative velocity)    
#fb = -fa
#------------------------------        
# m*xdd + c*xd + kx = 0
def relPos(position1, position2):
    return position1 - position2

#negative velocity is moving towards the rest lenght?
def relVel(velocity1, velocity2):
    return velocity1 - velocity2

def mag(I):
    return np.sqrt(I[0]**2 + I[1]**2)


#NOTE: currently not accounting for mass in force, but this could
# be done by using a weighted average mass?
#dx = dv
#dv = -[ks(|I| - r) + kd*Idot dot I / |I|] * I / |I|
#NOTE - consider dimensionless ks(|I|/r - 1) instead
def dv(node1, node2, rk4PosAdd, rk4VelAdd):
    I    = relPos(node1.pos + rk4PosAdd, node2.pos + rk4PosAdd) #vector
    Idot = relVel(node1.vel + rk4VelAdd, node2.vel + rk4VelAdd) #vector
    magI = mag(I)
    return -(ks * (magI/r - 1) + kd * np.dot(Idot,I) / magI) * I / magI 

def dx(node1, node2, rk4Addition):
    return relVel(node1.vel + rk4Addition, node2.vel + rk4Addition) 

def springForceRK4(node1, node2):
    t = 0
        
    while t < endTime:
        
        k1 = dx(node1, node2, np.array([0,0]))    #position estimate
        l1 = dv(node1, node2, np.array([0,0]), np.array([0,0])) #velocity estimate
        
        k2 = dx(node1, node2, l1 * h / 2) 
        l2 = dv(node1, node2, k1 * h / 2, l1 * h / 2)
        
        k3 = dx(node1, node2, l2 * h / 2) 
        l3 = dv(node1, node2, k2 * h / 2, l2 * h / 2)
        
        k4 = dx(node1, node2, l3 * h) 
        l4 = dv(node1, node2, k3 * h, l3 * h)
        
        posAdd = h / 6.0 * ( k1 + 2.0 * k2 + 2.0 * k3 + k4)
        velAdd = h / 6.0 * ( l1 + 2.0 * l2 + 2.0 * l3 + l4)
        
        node1.pos += posAdd ; node2.pos -= posAdd
        node1.vel += velAdd ; node2.vel -= velAdd
        
        t += h
    
    #new values to update nodes with
    newvals = [node1.pos, node1.vel, node2.pos, node2.vel]
    return newvals

#force function has not yet been implimented into indiv. nodes
pos1 = np.array([0.0, 0.0]) ; vel1 = np.array([1.0, 0.0])
pos2 = np.array([2.0, 0.0]) ; vel2 = np.array([-1.0, 0.0])

point1 = Node(pos1, vel1, 0, 1.0)
point2 = Node(pos2, vel2, 0, 1.0)

print(springForceRK4(point1, point2))

 