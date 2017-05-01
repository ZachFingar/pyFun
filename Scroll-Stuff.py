from tkinter import *
from tkinter.colorchooser import *
import tkinter.messagebox
import tkinter.simpledialog
import random


class ScrollStuff:
    def __init__(self):
        self.root = Tk()
        self.root.title("Assignment 4")

        self.frame = Frame(self.root, relief=GROOVE)
        self.frame.pack()

        self.roomSelector = Scrollbar(self.frame, orient=HORIZONTAL)
        self.roomSelector.pack(side=BOTTOM)
        self.canvas = Canvas(self.frame, bd=5, height=600, width=1000, bg="black",
                             xscrollcommand=self.roomSelector.set, scrollregion=(0, 0, 3000, 600),
                             xscrollincrement=1000)
        self.canvas.pack()
        self.roomSelector.config(command=self.canvas.xview)

        #Doug's Optimization
        self.interactions = {"other" : None}

        self.running = False
        self.RACERS = 4
        self.money = 1000
        self.bet = 0
        self.currentRacer = "None"
        self.winner = "None"
        self.wColor = "black"
        self.squareX = 0
        self.squareY = 0
        self.timeToMove = False

        self.pane1()
        self.pane2()
        self.pane3()

        self.canvas.bind("<Button-1>", self.interact)
        
        #Doug's Bindings
        self.canvas.bind("<B1-Motion>", self.squareUpdate)
        self.canvas.bind("<ButtonRelease-1>", self.squarePos)

        self.root.mainloop()

    #Doug's Widget
    def pane1(self):
        self.canvas.create_rectangle(375, 175, 625, 425, fill='#baa887', tags="square")
        self.interactions["square"] = ("Information:", "You clicked on the tan square!")

    def pane2(self):
        self.canvas.create_polygon(1300, 500, 1700, 500, 1500, 100, fill='#466ffb', tags="triangle")
        self.interactions["triangle"] = ("Information:", "You clicked on the triangle, want to change its color?")

    def pane3(self):
        self.raceButton()
        self.fillScoreBoards()
        self.createWinBanner()
        self.createFinishLine()
        self.packRacers()


    def createFinishLine(self):
        for y in range(190, 561, 20):
            self.canvas.create_rectangle(2900, y, 2920, y + 10, fill='white')

    def createWinBanner(self):
        self.canvas.create_rectangle(2700, 0, 2999, 150, fill='grey')
        self.canvas.create_text(2850, 75, fill=self.wColor, font=("Times", "24"),
                                text=("WINNER! : " + str(self.winner)), tags="WinText", state=HIDDEN)

    def raceButton(self):
        self.canvas.create_text(2500, 50, activefill='red', fill='blue', font=("Times", "64", "bold"), text="RACE",
                                tags="RaceText")
        self.interactions["RaceText"] = "race"

    def packRacers(self):
        self.canvas.create_oval(2100, 200, 2150, 250, fill='green', tags="racer0")
        self.canvas.create_oval(2100, 300, 2150, 350, fill='blue', tags="racer1")
        self.canvas.create_oval(2100, 400, 2150, 450, fill='red', tags="racer2")
        self.canvas.create_oval(2100, 500, 2150, 550, fill='white', tags="racer3")

    def fillScoreBoards(self):
        self.canvas.create_rectangle(2000, 0, 2300, 150, fill='grey') 
        self.canvas.create_text(2070, 50, fill='black', font=("Times", "12"), text=("Current Bet: " + str(self.bet)),
                                justify=LEFT, anchor=W, tags="BetText")
        self.canvas.create_text(2070, 100, fill='black', font=("Times", "12"),
                                text=("Current Money: " + str(self.money)), justify=LEFT, anchor=W, tags="MoneyText")
        self.canvas.create_text(2070, 75, fill='black', font=("Times", "12"),
                                text=("Current Racer: " + str(self.currentRacer)), justify=LEFT, anchor=W,
                                tags="RacerText")



    def interact(self, event):
        #Doug's Optimization
        widget = self.canvas.gettags(event.widget.find_withtag("current"))
        
        if widget != ():
            widget = widget[0]

        #Doug's Widget
        if widget == "square":
            self.timeToMove = True
            
        else:
            self.process(widget)

    def process(self, widget):
        #Doug's Optimization
        try:
            info = self.interactions[widget]
        except KeyError:
            info = self.interactions["other"]

        #Doug's Widget
        if widget == ():
            self.timeToMove = False
            self.canvas.delete("square")
            self.pane1()
            
        elif widget == "triangle":
            self.timeToMove = False
            title = info[0]
            message = info[1]
            self.processAsk(title, message)
            
        elif widget == "RaceText":
            self.timeToMove = False
            self.race()


    def processAsk(self, title, message):
        if tkinter.messagebox.askyesno(title, message):
                color = askcolor()
                color = color[1]
                self.canvas.itemconfig("triangle", fill = color)

    def race(self):
        pos = self.canvas.coords("racer0")
        x = pos[0]
        if (self.running == False) and (x == 2100):
            self.gamble()
            self.betting()
            self.racePrepare()
            self.running = True
        else:
            self.running = False
            self.canvas.itemconfig("RaceText", text="RACE", activefill="red", fill="blue")
            for i in range(0, self.RACERS):
                self.canvas.delete("racer" + str(i))
            self.packRacers()
            self.canvas.update()

        while self.running:
            self.doRace()

    def gamble(self):
        self.currentRacer = (
            tkinter.simpledialog.askstring("Gamble", "Choose your racer! (Green, Red, Blue, or White):"))
        if self.currentRacer is None:
            self.currentRacer = "none"
        self.currentRacer = self.currentRacer.lower()
        if self.currentRacer not in ("green", "red", "blue", "white", "none"):
            tkinter.messagebox.showerror("Error!",
                                         "Invalid racer name! Please Try again using green, red, blue, or white.")
            self.gamble()

    def betting(self):
        if self.currentRacer != "none":
                self.bet = tkinter.simpledialog.askinteger("Bet!", "Enter your wager!:")
                if self.bet is None:
                    self.bet = 0
                    return
                if  (self.bet < 0) or (self.bet > self.money):
                    tkinter.messagebox.showerror("Error!",
                                                 "You entered an invalid bet. Please hit cancel or enter a new number that is <= your money.")
                    return self.betting()
        else:
            self.bet = 0
            
    def racePrepare(self):
        if self.currentRacer == "none":
            color = "black"
        else:
            color = self.currentRacer

        self.canvas.itemconfig("RacerText", text="Current Racer: " + self.currentRacer.capitalize(),
                               fill=color)
        self.canvas.itemconfig("BetText", text="Current Bet: " + str(self.bet))
        self.canvas.itemconfig("RaceText", text="RESTART", activefill="blue", fill="red")
        self.canvas.itemconfig("WinText", state=HIDDEN)

    def doRace(self):
        for i in range(0, self.RACERS):
            if self.running == True:
                pos = self.canvas.coords("racer" + str(i))
                x = pos[0]
                dx = random.randrange(1, 5)
                self.canvas.move("racer" + str(i), dx, 0)
                if x >= 2850:
                    self.running = False
                    if i == 0:
                        self.wColor = "green"
                        self.winner = "Green!"
                    elif i == 1:
                        self.wColor = "blue"
                        self.winner = "Blue!"
                    elif i == 2:
                        self.wColor = "red"
                        self.winner = "Red!"
                    else:
                        self.wColor = "white"
                        self.winner = "White!"

                    if self.wColor == self.currentRacer.lower():
                        self.money += self.bet
                    else:
                        self.money -= self.bet
                    self.canvas.itemconfig("MoneyText", text="Current Money: " + str(self.money))
                    self.canvas.itemconfig("WinText", fill=self.wColor, text=("Winner! : " + self.winner),
                                           state=NORMAL)
                self.canvas.update()
                self.canvas.after(4)

    #Doug's Widget
    def squareUpdate(self, event):
        self.canvas.delete("square")
        if self.timeToMove:
            self.squareX = event.x
            self.squareY = event.y
            self.canvas.create_rectangle(self.squareX-125, self.squareY+125, self.squareX+125, self.squareY-125,
                                         fill='#baa887', tags="square")
            self.canvas.update()
            
    #Doug's Widget
    def squarePos(self, event):
        if self.timeToMove:
            tkinter.messagebox.showinfo("Position:", "Square is at " + str(self.squareX) + ", " + str(self.squareY) + \
                               ". Try dragging it around!")

            
                

ScrollStuff()
