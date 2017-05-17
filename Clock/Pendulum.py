#Pendulum
from tkinter import *
import math

class Pendulum:

    def __init__(self):
        self.speed = 100 #idle timer
        
        self.PR = 5 # Weight radius
        self.CR = 60 # Weight Path Radius
        
        self.px1, self.py1 = 0, 0 #Weight 1st coor
        self.px2, self.py2 = 0, 0 #Weight 2nd coor
        self.px = 0 #XY midpoints
        self.py = 0
        
        self.BASEX = 150 #Center of circle the pendulum follows, top of line.
        self.BASEY = 20
        
        self.TOP = 101 #Top angle that the pendulum ends at, in degrees
        self.BOTTOM = 79
        
        self.index = self.TOP #indexed position
        self.step = 2 #Current angle step
        
        self.root = Tk()
        self.root.title("Pendulum")
        
        self.canvas = Canvas(self.root, bg = "grey", width = 400, height = 800)

    def packPen(self):
        self.packLine()
        self.packWeight()
        
    def packLine(self):
        #Formula finds closest point on circle to the base of the line.
        vx = self.BASEX - self.px #finds vector xy components between base and circle center
        vy = self.BASEY - self.py
        magV = math.sqrt(vx**2 + vy ** 2) #Basic vector magnitude formula, merging x/y vectors
        
        lx = self.px  + vx / magV * self.PR
        # vx / |V| returns cos(φ), * r converts it from unit circle to real paramters,
        # add the circle's x point to line it up on graph correctly
        
        ly = self.py + vy / magV * self.PR
        self.canvas.create_line(self.BASEX, self.BASEY, lx, ly, tags = "line")

    def packWeight(self):
        #swing index finds center point, have to compensate
        self.px1 = self.px - self.PR
        self.px2 = self.px + self.PR
        self.py1 = self.py - self.PR
        self.py2 = self.py + self.PR
        self.canvas.create_oval(self.px1, self.py1, self.px2, self.py2, tags = "w", fill = "yellow")
        

    def animation(self):
            if self.step > 0: #Determines if it should swing left or right.
                self.swing(self.index,self.TOP,self.step)
            else:
                self.swing(self.index,self.BOTTOM,self.step)

    def swing(self, a1, a2, j):
        
        #a1/a2 are the ending angles of the pendulum, in degress - j is step
        for i in range(a1,a2, j):
            self.canvas.after(self.speed)
            rad = math.radians(i) #convert degrees to radians, since for loop only takes integers
            self.index = i #Index this position, so that animation knows where to begin
        
            self.px = self.CR*math.cos(rad) + self.BASEX #Finds path along edge of circle with radius CR
            self.py = self.CR*math.sin(rad) + self.BASEY
            
            self.canvas.delete("w")
            self.canvas.delete("line")
            self.packPen()

            self.canvas.update()

        #Prepare for next loop.
        self.step = -self.step #Flip swing direction
        

