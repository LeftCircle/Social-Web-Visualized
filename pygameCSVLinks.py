'''
creates the links between nodes from the csv to be used in the pygame 
visualization
'''
import numpy as np
import csv

class NodeAndLinkGenerator:
    def __init__(self, rl):
        self.rl = rl #smallest rest length of the spring
        self.linksPerNodeArray = [] #number of links each node has
        #linked nodes format should be [(node i, node j, restLength), ...]
        self.pygameLinkedNodes = []
        self.pygameNodeColors = [] #should be length nodes
        self.pygameNodePositions = []
        
    
    #link array must be updated before anything else occurs
    def updateLinksPerNodeArray(self):
        #check to make sure we are not updating the links array twice
        if self.linksPerNodeArray == []:
            #reading the csv file that has all of the names and connections
            with open("conMat.csv") as f:
                reader = csv.reader(f, delimiter = ',')
                    #first need to determine number of links for each node
                for row in reader:
                    if(len(row)!=0):
                        #getting the total number of links in this row
                        #should be based off of the targets, not the source
                        calculating_links = 0
                        for k in range(len(row)):
                            if row[k] == '1':
                                calculating_links += 1
                        self.linksPerNodeArray.append(calculating_links)
        print('LinksPerNodeArray updated')
                        
    def updateLinksAndDistance(self):
        #check to make sure links array ahs been initialized
        print('update Links and Distance called')
        if self.linksPerNodeArray != []:
            with open("conMat.csv") as f:
                reader = csv.reader(f, delimiter = ',')
                #counter to avoid double links
                iterations = 0
                for row in reader:
                    if(len(row)!=0):
                        for i in range(iterations): 
                            if row[i] == '1': #check to confirm link
                                links = self.linksPerNodeArray[i]
                                #source == iterations ; target == i
                                if links < 10:
                                    self.pygameLinkedNodes.append(
                                        np.array([iterations, i, self.rl]))
                                    
                                if links >= 10 and links < 20:                                   
                                    self.pygameLinkedNodes.append(
                                        np.array([iterations, i, self.rl * 2]))
                                    
                                if links >= 20 and links < 30:
                                    self.pygameLinkedNodes.append(
                                        np.array([iterations, i, self.rl * 3]))
                                    
                                if links >= 30 and links < 40:
                                    self.pygameLinkedNodes.append(
                                        np.array([iterations, i, self.rl * 4]))
                                    
                                if links >= 40 and links < 50:
                                    self.pygameLinkedNodes.append(
                                        np.array([iterations, i, self.rl * 5]))
                                    
                                if links >= 50 and links < 60:
                                    self.pygameLinkedNodes.append(
                                        np.array([iterations, i, self.rl * 6]))
                                    
                                if links >= 60:
                                    self.pygameLinkedNodes.append(
                                        np.array([iterations, i, self.rl * 7]))
                                    
                        iterations += 1
            return self.pygameLinkedNodes

        else:
            print('linksPerNodeArray not initialized')
            
    def updateNodePositions(self):
        print('update node positions called')
        if self.linksPerNodeArray != []:
            nNodes = len(self.linksPerNodeArray)
            for i in range(nNodes):
                x = 1000 *  np.random.random() 
                y = 1000 *  np.random.random()
                self.pygameNodePositions.append(np.array([x, y]))
            return self.pygameNodePositions
            
        else:
            print(' linksPerNodeArray not initialized')


#nodesAndLinks = NodeAndLinkGenerator(25)
#nodesAndLinks.updateLinksPerNodeArray()
#print(nodesAndLinks.nodePositions())                        
'''                        
#goal: Add longer link distances based off of number of connections
#NOTE! row starts at 1, not 0. Everything else starts at 0
links = True
nodes = False
starting = 140
ending = 177
#number of links for each node
linksPerNodeArray = []
with open("conMat.csv") as f:
    reader = csv.reader(f, delimiter = ',')
    if links == True:
        #first need to determine number of links for each node
        for row in reader:
            if(len(row)!=0):
                #getting the total number of links in this row
                #should be based off of the targets, not the source
                calculating_links = 0
                for k in range(len(row)):
                    if row[k] == '1':
                        calculating_links += 1
                linksPerNodeArray.append(calculating_links)
        
        #now determining the javascript for specific node/link
with open("conMat.csv") as f:
    reader = csv.reader(f, delimiter = ',')
    if links == True:
        iterations = 0
        for row in reader:
            if(len(row)!=0):
                #printing the javascript to be copy and pasted
                for i in range(iterations): #range iterations to avoid double counting
                    if row[i] == '1': #check to confirm link
                        #if more than 5 links, greater link distance
                        # if statement to only print a certain amount
                        if iterations >= starting and iterations < ending:
                            links = linksPerNodeArray[i]
                            if links < 10:
                                print('{ source: ', iterations, ', target: ', i ,
                                        ' },')
                            if links >= 10 and links < 20:
                                print('{ source: ', iterations, ', target: ', i ,
                                        ", className: 'tenPlus'},")
                            if links >= 20 and links < 30:
                                print('{ source: ', iterations, ', target: ', i ,
                                        ", className: 'twentyPlus'},")
                            if links >= 30 and links < 40:
                                print('{ source: ', iterations, ', target: ', i ,
                                        ", className: 'thirtyPlus'},")
                            if links >= 40 and links < 50:
                                print('{ source: ', iterations, ', target: ', i ,
                                        ", className: 'fourtyPlus'},")
                            if links >= 50 and links < 60:
                                print('{ source: ', iterations, ', target: ', i ,
                                        ", className: 'fiftyPlus'},")
                            if links >= 60:
                                print('{ source: ', iterations, ', target: ', i ,
                                        ", className: 'sixtyPlus'},")
                iterations += 1
    if nodes == True:
        iterations = 0
        for row in reader:
            print('{ x: ', 1920 * np.random.random(), ', y: ', 1080 * np.random.random(), ' },')
            iterations += 1
        print(iterations)
    f.close()
'''