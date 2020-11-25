# Social Web Visualized

Using Pygame is an interactive way to visualize the social web. Although the images may not be as sharp as some other 
data visualization software, the code is largely transferable in that the physics engine I developed does not require
pygame to function, but only uses pygame to draw the positions of the nodes and links.

The most notable portion of this code is the spring solver, which uses an rk4 method to solve for the position of linked particles. 

Also a big thanks to Peter Collingridge for his pygamerr physics simulation tutorial which can be found here:
https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/
This helped me get started with the code. 

## Dependencies

If the social web is being visualized, the files must be in the same folder as the [FB Scraper files](https://github.com/jrbaker4/FacebookScraper)

pygame and numpy are also required, and can be downloaded by:

**pip3 install pygame numpy**

## Physics Engine Demonstration

To run the program, run pygameTutorial.py. This will open a window with several different nodes moving around.
The nodes can be clicked on, dragged around, and thrown as long as your mouse is moving when you release the mouse button.

## Social Web Visualization

Run pygameSocialWebViz visualize the social web with nodes that are linked by springs, able to be dragged, and can collide.
These files must be in the same location as the FB scraper python files, specifically the conMat.csv, which shows who is 
connected with who.

However, this method of visualizing the social web is a work in progress. Because the spring forces are calculated with RK4, and each particle is checking for a collision with every other particle, the simulation is extremely slow. It may even not function on smaller 
computers.

## Future Work and Possible Ideas

Should be described in each uploads comments. The end goal is to visualize the social web in a clutter free manner. 
This can be accomplished by fixing the position of the most influencial person at the center, creating a ring around 
that person using their ~6 most influencial friends, then creating smaller social webs that extend from those 6 people. 
If links occurring across these smaller social webs create clutter, then these links could potentially be shown through
making the nodes the same color. 


