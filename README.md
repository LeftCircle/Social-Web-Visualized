Using Pygame is an interactive way to visualize the social web. Although the images may not be as sharp as some other 
data visualization software, the code is largely transferable. 

In order to run the code, pygame and numpy are required. These can be installed with

pip3 install pygame numpy

To run the program, run pygameTutorial.py. This will open a window with several different nodes moving around.
The nodes can be clicked on, dragged around, and thrown as long as your mouse is moving when you release the mouse button.

Next goals:
Should be described in each uploads comments. The end goal is to visualize the social web in a clutter free manner. 
This can be accomplished by fixing the position of the most influencial person at the center, creating a ring around 
that person using their ~6 most influencial friends, then creating smaller social webs that extend from those 6 people. 
If links occurring across these smaller social webs create clutter, then these links could potentially be shown through
making the nodes the same color. 
