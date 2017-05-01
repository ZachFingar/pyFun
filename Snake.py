from tkinter import *
import random

class PythonSnake:

        def __init__(self):
            #Set TK variables and create frame/title
            self.root = Tk()
            self.root.title("Snake")
            self.frame = Frame(self.root)
            self.frame.pack()

            #Set up the initial canvas
            self.canvas = Canvas(self.frame, bg = "black", width = 200, height = 260)
            self.canvas.pack()

            #Canvas Variables
            self.width = 20 #grid width
            self.height = 20 #grid height
            self.gridColor = "green"
            self.borderColor = "grey"

            #Populate Canvas and track the grid
            self.border = list() #Holds borderIDs and objects 
            self.grid = list() #Holds grid objects / assigns them ids
            self.xy = list() #for easy converting of ID to x-y

            self.packGrid()

            #Create Score Tracker
            self.score = IntVar()
            self.score = 0 #initial score
            self.hiScore = 0
            self.ScoreKeeper = self.canvas.create_text(50, 250, fill = "white", text = "Score: " + str(self.score))
            self.HiScoreKeeper = self.canvas.create_text(150, 250, fill = "white", text = "Hi Score: " + str(self.hiScore))

            #Create start button 
            self.startButton = Button(self.frame, text = "Start", command = self.start)
            self.startButton.pack()


            #Find closest to mid of grid to place snake, use grid so it always places in playable area
            self.initial = max(self.grid)  #max grid ID
            self.x1 = self.xy[self.initial]  #xy was appended x then y - making it twice as large as the actual grid list, so to find the ID at the midway point - insert the max of the grid list
            self.y1 = self.xy[self.initial + 1]   #because the previous appending, the corresponding y variable is the next one in the list
            self.x2 = self.xy[self.initial] + self.width #Add the height / width because the second xy isnt saved in the ID
            self.y2 = self.xy[self.initial  + 1]  + self.height

            #Set up snake tracking
            self.Pos = int(self.initial / 2) + 2 #Tracks the ID of tile the head is on for the rest of the game
            self.snake = list() #Create a list to track the body objects of the snake
            self.chain = list() #This list is to manage the snake positions, they are seperate lists so that the objects can be deleted with ease, while still managing the position IDs
            #Could be bypassed with the xy coordinates, but this is more coherent for late issues
            self.snake.append(self.canvas.create_oval(self.x1,self.y1,self.x2,self.y2, fill = "blue", tags = "head")) #Create the starting Head
            self.chain.append(self.Pos)

            #setup input
            self.canvas.bind("<w>", self.up)
            self.canvas.bind("<s>", self.down)
            self.canvas.bind("<d>", self.right)
            self.canvas.bind("<a>", self.left)
            self.canvas.focus_set()

            #Initial Game Variables
            self.dx = 0  #moves the head to its new position, tkinter move function moves the object by x, y  - so it will be set in the key bindings: Default is north, not changing x and -y is up in the syntax
            self.dy = -self.height      
            self.x1 = 0 #these will be used to find the xy coordinates when creating body / food objects - as seen above
            self.y1 = 0
            self.x2 = 0
            self.y2 = 0
            self.timer = 300 #Creates the timer to update the game loop = 300 miliseconds to start with
            self.game = "off" #The flag that shows the games state
            self.direction = -10 #Current directions is north, so -10 because the grid list was created from top to bottom - so the ID above the current positions is -10 in the list
            self.fobject = list() #holds and manages the food objects that will be deleted and created
            self.fID = 0 #Manages food object grid position
            self.getFood = "ok" #The flag to create more food
            
            self.root.mainloop()

        def packGrid(self):
                for y in range(0,12):
                        for x in range(0, 10):
                            if x == 0 or x == 9 or y == 0 or y == 11: #If on the outside edge create a grey border
                                self.border.append(self.canvas.create_rectangle(self.width * x, self.height * y , (self.width * x) + self.width, (self.height * y) + self.height, \
                                                                                fill = self.borderColor))

                            else: #Otherwise populate with green moveable tiles
                                self.grid.append(self.canvas.create_rectangle(self.width * x, self.height * y , (self.width * x) + self.width, (self.height * y) + self.height, \
                                                                              fill = self.gridColor))
                            self.xy.append(self.width * x) #Track x position for each x thats being created
                            self.xy.append(self.height * y) #Track y position for each y thats being created
                            
        def up(self, event):
                if (self.Pos - 10) in self.chain: #make sure the command is ignored if backward position is given.
                                return
                self.dy = -self.height
                self.dx = 0
                self.direction = -10  #next square up is -10 in the grid list

        def down(self, event):
                if (self.Pos + 10) in self.chain:#make sure the command is ignored if backward position is given.
                                return
                self.dy = self.height
                self.dx = 0
                self.direction = 10  #next square up is +10 in the grid list


        def right(self, event):
                if (self.Pos + 1) in self.chain:#make sure the command is ignored if backward position is given.
                                return
                self.dx = self.width
                self.dy = 0
                self.direction = 1 #right square is +1 in the grid list

        def left(self, event):
                if (self.Pos - 1) in self.chain:#make sure the command is ignored if backward position is given.
                                return
                self.dx = -self.width
                self.dy = 0
                self.direction = -1  #next square left is -1 in the grid list

        def start(self):
                self.startButton["state"] = DISABLED
                self.game = "on"
                while self.game == "on":

                        self.moveHead() #Move  the snake head and track its position
                        self.canvas.update() #update the game
                        
                        self.borderCheck() #Check if the new position touches a border

                        self.hungry() #Creates food objects if there aren't any already on the grid
                        
                        self.foodCheck() #Check if the new position touches food
                        self.canvas.update() #update the game
                           
                        self.updateChain(self.Pos,(len(self.snake)-1)) #Update the new positions of the chian
                        self.moveChain() #use the new positions to create / delete objects
                        self.canvas.update() #update the game

                        self.canvas.after(self.timer) #after the amount set by the timer passes


                                


        def moveHead(self):
                self.Pos = self.Pos + self.direction #Tracker: new position is the most current pressed direction
                self.canvas.move("head", self.dx, self.dy) #Object: move the head to the new position

        def borderCheck(self):
                for x in range(0,len(self.border)): #check if the new position touches the border
                    if self.Pos == self.border[x]:
                        self.game =  "off"
                        self.end()
                        
        def hungry(self):
            if self.getFood == "ok":
                self.fID = (random.randrange(min(self.grid),max(self.grid))) #find a random grid ID
                while (self.fID == self.Pos) or (self.fID in self.border) or (self.fID in self.chain):
                    self.fID = (random.randrange(min(self.grid),max(self.grid))) #if that grid id is on the border, occupies the snakes body or head, find a new number until it finds one that doesnt
                self.x1 = self.xy[self.fID*2]  #same conversion system as described before
                self.y1 = self.xy[self.fID*2 + 1] 
                self.x2 = self.xy[self.fID*2] - self.width
                self.y2 = self.xy[self.fID*2  + 1]  + self.height
                self.fobject.append(self.canvas.create_oval(self.x1,self.y1,self.x2,self.y2, fill = "yellow", tags = "food")) #create the object
                self.getFood = "nope" #flag that food has been created

        def foodCheck(self):
                if self.Pos == self.fID: #if the new position is on top of a food ID, delete the food and append the snakes body
                        self.canvas.delete(self.fobject[len(self.fobject)-1]) #delete food object
                        self.x1 = self.xy[self.Pos*2] #finds the positions of the new body part to be made
                        self.y1 = self.xy[self.Pos*2 + 1] 
                        self.x2 = self.xy[self.Pos*2] - self.width 
                        self.y2 = self.xy[self.Pos*2 + 1]  +  self.height
                        self.snake.append(self.canvas.create_oval(self.x1,self.y1,self.x2,self.y2, fill = "red")) #create the object
                        self.chain.append(self.Pos) #Track the objects position on the grid
                        self.getFood = "ok" #Food has been ate, flag for more
                        self.timer -= 3 #Make snake faster every time food is eaten
                        self.score += 1
                        self.canvas.delete(self.ScoreKeeper)
                        self.ScoreKeeper = self.canvas.create_text(50, 250, fill = "white", text = "Score: " + str(self.score))
                
        def updateChain(self, pos, n=0): #n = the length of the body, pos is the tracker
            if n == 0:
                self.chain[n] = pos #Update the head position in the tracking list
            else:
                self.chain[n] = self.chain[n-1] #update the body position to be the one before it in the list
                self.updateChain(pos, n-1) #recursive loop to go through entire body in this manner

        def moveChain(self):
            for x in range(0, len(self.snake)): #move everything beside the head, because this is managed elsewhere for fluid key control
                if x != 0: #if the body part isnt the head
                    self.canvas.delete(self.snake[x]) #delete the body parts old position
                    self.x1 = self.xy[self.chain[x]*2]  #find where to place the new part (xy grid is 2x more, needs to be compensated for)
                    self.y1 = self.xy[self.chain[x]*2 + 1] 
                    self.x2 = self.xy[self.chain[x]*2] - self.width 
                    self.y2 = self.xy[self.chain[x]*2 + 1]  +  self.height
                    self.snake[x] = self.canvas.create_oval(self.x1,self.y1,self.x2,self.y2, fill = "red") #create its new position

                for x in range(1,len(self.chain)): #Check to see if the new position colides with the new position of the body
                    if self.Pos == self.chain[x]:
                        self.game = "loss" #if it does, end the game
                        self.canvas.delete(self.snake[x])
                        self.end()

        def end(self): #allow user input to reset the game if they wish to play again
                if self.score > self.hiScore:
                        self.canvas.delete(self.HiScoreKeeper)
                        self.hiScore = self.score
                        self.HiScoreKeeper = self.canvas.create_text(150, 250, fill = "white", text = "Hi Score: " + str(self.hiScore))
                self.startButton["state"] = NORMAL
                self.startButton["text"] = "Reset"
                self.startButton["command"] = self.reset

        def reset(self): #Wipe all existing data and reset game variables - leaving only the grid
                self.canvas.delete(self.fobject[len(self.fobject)-1])
                
                for x in range(0, len(self.snake)):
                        self.canvas.delete(self.snake[x])
                        
                self.fobject = list()
                self.score = 0
                self.dx = 0
                self.dy = -self.height
                self.direction = -10
                
                self.x1 = self.xy[self.initial]
                self.y1 = self.xy[self.initial + 1]
                self.x2 = self.xy[self.initial] + self.width
                self.y2 = self.xy[self.initial  + 1]  + self.height
                self.Pos = int(self.initial / 2) + 2
                self.snake = list()
                self.chain = list()
                
                self.snake.append(self.canvas.create_oval(self.x1,self.y1,self.x2,self.y2, fill = "blue", tags = "head")) 
                self.chain.append(self.Pos)
                self.timer = 300
                self.fID = 0 #Manages food object grid position
                self.getFood = "ok" #The flag to create more food

                self.canvas.delete(self.ScoreKeeper)
                self.ScoreKeeper = self.canvas.create_text(50, 250, fill = "white", text = "Score: " + str(self.score))

                self.startButton["text"] = "Start"
                self.startButton["command"] = self.start

                 

   
PythonSnake()

