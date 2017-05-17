from Pendulum import *

class Clock:

    def __init__(self):
        self.P = Pendulum()
        self.P.speed = 98
        
        self.root = self.P.root
        self.root.title("Clock")
        
        self.canvas = self.P.canvas
        self.canvas.pack()

        self.frame = Frame(self.root, width = 400, height = 40)
        self.frame.pack()

        
        self.h = IntVar()
        self.m = IntVar()
        self.s = IntVar()

        l = Label(self.frame, text = "Time:  ")
        hour = Entry(self.frame, textvariable = self.h, width = 20)
        f1 = Label(self.frame, text = " : ")
        minute = Entry(self.frame, textvariable = self.m, width = 20)
        f2 = Label(self.frame, text = " : ")
        sec = Entry(self.frame, textvariable = self.s, width = 20)
        button = Button(self.frame, text = "Set Time", command = self.reset)
                   
        l.grid(row = 1, column = 0)
        hour.grid(row = 1, column = 1)
        f1.grid(row = 1, column = 2)
        minute.grid(row = 1, column = 3)
        f2.grid(row = 1, column = 4)
        sec.grid(row = 1, column = 5)
        button.grid(row = 2, column = 3)
        
        self.P.PR = 30
        self.P.CR = 300
        self.P.BASEX = 200
        self.P.BASEY = 340

        self.flag = True
        
        self.indexS = int((((0 / 60) * 12) - 3) * 30)
        self.indexM = int((((0 / 60) * 12) - 3) * 30)
        self.indexH = (12 - 3) * 30
        
        self.packClock()
        self.P.packPen()
        self.animation()
        
        self.root.mainloop()

    def packClock(self):
        self.packBase()
        self.packFace()


    def packBase(self):
        self.canvas.create_rectangle(50,750,  75,780, fill = "#804000")
        self.canvas.create_rectangle(325,750,  350,780, fill = "#804000")
        self.canvas.create_rectangle(50,20,  350,750, fill = "#804000")
        self.canvas.create_rectangle(90, 340, 310, 710, fill = "#3c1e00")

    def packFace(self):
        self.canvas.create_oval(100, 50, 300, 250, fill = "white")
        for h in range(0, 360,30):            
            rad = math.radians(h)
            x = 100*math.cos(rad) + 200
            y = 100*math.sin(rad) + 150
            self.canvas.create_line(x,y, 200,150)
        self.canvas.create_oval(125, 75, 275, 225, fill = "white", outline = "white")

        self.canvas.create_line(200,150, 200, 80, width = 2, fill = "red", tags = "s")
        self.canvas.create_line(200,150, 200, 90, width = 5, fill = "grey", tags = "m")
        self.canvas.create_line(200,150, 200, 110, width = 8, fill = "black", tags = "h")

    def animation(self):
        self.flag = True
        while self.flag == True:
                for s in range(self.indexS, 360,6):
                    if self.flag == False:
                        return
                    self.P.animation()
                    self.second()
                    self.minute()
                    self.hour()

                    self.canvas.update()


    def second(self):
        if self.indexS >= 354:
            self.indexS = 0
        else:
            self.indexS += 6
            
        rad = math.radians(self.indexS)
        x = 80*math.cos(rad) + 200
        y = 80*math.sin(rad) + 150
        self.canvas.delete("s")
        self.canvas.create_line(200,150, x, y, width = 2, fill = "red", tags = "s")

            
    def minute(self):
        if self.indexM  >=  360:
            self.indexM = 0
        else:
            self.indexM += .1
            
        a= math.radians(self.indexM)
        x = 70*math.cos(a) + 200
        y = 70*math.sin(a) + 150
        self.canvas.delete("m")
        self.canvas.create_line(200,150, x, y, width = 5, fill = "grey", tags = "m")
 
    def hour(self):
        if self.indexH  >=  360:
            self.indexH = 0
        else:
            self.indexH += (.0083)

        a = math.radians(self.indexH)    
        x = 50*math.cos(a) + 200
        y = 50*math.sin(a) + 150
        self.canvas.delete("h")
        self.canvas.create_line(200,150, x, y, width = 8, tags = "h")
                        
    def reset(self):
        self.indexS = int((((self.s.get() / 60) * 12) - 3) * 30)
        self.indexM = int((((self.m.get() / 60) * 12) - 3) * 30)
        self.indexH = (self.h.get() - 3) * 30
        self.flag = False
        self.animation()
Clock()
