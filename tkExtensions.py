import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import tkinter.ttk as ttk
import threading
import time
from commonFunctions import *

######EXTENSIONS TO TKINTER GUI

#Button that changes colour on hover
class HoverButton(tk.Button):
    def __init__(self, parent, hoverColour = "#FFFFFF", hoverText = "#000000", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.bind("<Leave>", self.leave)
        self.bind("<Enter>", self.enter)
        self.background = self['bg']
        self.foreground = self['fg']
        self.hoverColour = hoverColour
        self.hoverText = hoverText

    def leave(self, event):
        self.config(background=self.background, fg=self.foreground)
    def enter(self, event):
        self.config(background=self.hoverColour, fg = self.hoverText)


#A popup window with text and an OK button
class PopupWindow(object):
    def __init__(self, parent, text = "", entryBoxNeeded = False, buttonSettings = None, hoverButton = False, fullScreen = False, *args, **kwargs):
        top=self.top=tk.Toplevel(parent, *args, **kwargs)
        if fullScreen:
            top.state("zoomed")
        self.body = tk.Frame(top) 
        self.entryBoxNeeded = entryBoxNeeded
        #Add the icon
        self.text = text
        if text != "":
            self.l=tk.Label(self.body,text=text)
            self.l.bind('<Configure>', lambda e: self.l.config(wraplength=self.l.winfo_width()))

        if self.entryBoxNeeded: #Only creates entry if requested
            self.e=tk.Entry(top)
        if hoverButton:
            self.b=HoverButton(top, text='Ok', command=self.cleanup, **buttonSettings) #Button destroys window
        else:
            if buttonSettings is None:
                self.b=tk.Button(top, text='Ok', command=self.cleanup, width = 30) #Button destroys window
            else:
                self.b=tk.Button(top, text='Ok', command=self.cleanup, **buttonSettings) #Button destroys window


    #Destroys itself when button is pressed
    def cleanup(self):
        if self.entryBoxNeeded:
            self.value=self.e.get()
        self.top.destroy()
    
    #Display
    def pack(self, *args, **kwargs):
        if self.text != "":
            self.l.pack(pady=5, padx=5)
        kwargs["expand"] = True
        kwargs["fill"] = "both"
        kwargs["padx"] = 5
        kwargs["pady"] = 5
        self.body.pack(*args, **kwargs)
        if self.entryBoxNeeded: #Only creates entry if requested
            self.e.pack(expand=True, fill="both" , pady=5, padx=5)
        self.b.pack(pady=5, padx=5)




#A matplotlib graph
class Graph(tk.Frame):
    def __init__(self, parent, width = 480, height= 480, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.fig = Figure(figsize=(width//96,height//96), dpi=100, tight_layout = True)
        
        
    #Plot a line of int(x) vs int(y)
    def plot(self, x, y, rotation = 0, title = "", xaxis = "", yaxis = ""):
        plt = self.fig.add_subplot(111)
        plt.scatter(x, y)
        plt.plot(x, y)
        plt.draw(FigureCanvasTkAgg(self.fig, self).get_renderer())
        plt.set_xticklabels(plt.get_xticklabels(), rotation=rotation) 
        plt.set_xlabel(xaxis)
        plt.set_ylabel(yaxis)
        plt.set_title(title)
        return plt

    #Plot a line of date(x) vs date(y)
    def datePlot(self, x, y, *args, **kwargs):
        nx = []
        try:
            for d in x:
                nx.append(datetime.datetime.strptime(d,"%d/%m/%Y").date())
        except:
            raise ValueError("Incorrect date format")
        return self.plot(nx, y, rotation=70, *args, **kwargs)
        
    #Show the window
    def show(self):
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    #Display the graph using pack
    def pack(self, *args, **kwargs):
        try:
            super().pack(*args, **kwargs)    
            self.show()
            return True
        except Exception as e:
            raise ValueError("Incorrect pack parameters.\n" + "Error " + str(e))
    
    #Display the graph using grid
    def grid(self, *args, **kwargs):
        try:
            super().grid(*args, **kwargs)    
            self.show()
            return True
        except Exception as e:
            raise ValueError("Incorrect pack parameters.\n" + "Error " + str(e))    
        return False

#A canvas that auto resizes
class ResizingCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(* args, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
    
    def on_resize(self, event):
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        self.config(width = self.width, height =self.height)
        self.scale("all", 0,0,wscale, hscale)
        return self.height, self.width

        

#A scrollable window
class ScrollableFrame(tk.Frame):
    def __init__(self, container, verticalSB = True, horizontalSB = False, height= -1, width=-1, vside="right", hside="bottom", *args, **kwargs):
        """Pass in height, width and background colour"""
        self.verticalSB = verticalSB
        self.horizontalSB = horizontalSB
        self.vside = vside
        self.hside = hside
        self.container = container
        super().__init__(container, *args, **kwargs)

        if height == -1 and width == -1:
            self.canvas = ResizingCanvas(self,highlightthickness=0, *args, **kwargs)
        else:
            self.canvas = ResizingCanvas(self, height = height, width = width, highlightthickness=0, *args, **kwargs)

        if verticalSB:
            self.vscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        if horizontalSB:
            self.hscrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollableFrame = tk.Frame(self.canvas, *args, **kwargs)
        self.scrollableFrame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        

    def FrameWidth(self, event):
        pass
    

    #Display
    def pack(self, *args, **kwargs):
        root = self.container.master
        while True:
            prevRoot = root
            root = root.master
            if root is None:
                break
        prevRoot.update()
        if self.container.winfo_height() == 1 and self.container.winfo_width() == 1:
            self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")
        else:
            self.canvas_frame = self.canvas.create_window((0, 0), height = self.container.winfo_height(), width = self.container.winfo_width(),window=self.scrollableFrame, anchor="nw")
            
        if self.verticalSB:
            self.canvas.configure(yscrollcommand=self.vscrollbar.set)
        if self.horizontalSB:
            self.canvas.configure(xscrollcommand=self.hscrollbar.set)
        
        if self.verticalSB:
            self.vscrollbar.pack(side=self.vside, fill="y")
            self.canvas.pack(side=self.hside, fill="both", expand=True, anchor = 'nw', padx = 10, pady = 10)
        if self.horizontalSB:
            self.hscrollbar.pack(side="bottom", fill="x")
            self.canvas.pack(side="top", fill="both", expand=True, anchor = 'nw', padx = 10, pady =10)

        self.canvas.bind('<Configure>', self.FrameWidth)

        return super().pack(*args, **kwargs)


#A countdown timer that runs on a separate thread
class Timer:
    def __init__(self, parent, root, time, actionOnFinish):
        self.root = root
        self.parent = parent
        self.hours = time//60
        self.minutes = time % 60
        self.seconds = 0
        self.startTime = self.formTime()
        self.timerFrame = tk.Frame(parent)
        self.timerDisplay = tk.Label(self.timerFrame, text = self.formTime())
        self.actionOnFinish = actionOnFinish
        self.timeWhenStopped = "00:00:00"
        self.finished = False
        self.timeThread = None
        self.stopFlag = False
    
    #Get the time as a readable value
    def formTime(self):
        return az(str(self.hours)) + ":" + az(str(self.minutes)) + ":" + az(str(self.seconds))
    
    #Start the timer
    def start(self):

        #Separate thread
        def doTimer():
            while True:
                try:
                    for i in range(10):
                        time.sleep(0.1)
                        self.root.update()
                    if not self.countDown():
                        break
                except:
                    return 0

        #Start the thread
        self.timerThread = threading.Thread(target=doTimer)
        self.timerThread.start()

    #Display
    def pack(self, **kwargs):
        self.timerFrame.pack(**kwargs)
        self.timerDisplay.pack(padx=5, pady=5)

    #Pause the timer
    def pause(self):
        self.pause = True

    #Start the timer again 
    def play(self):
        self.pause = False

    #Stop the timer
    def stop(self):
        self.destroy()
        self.timeWhenStopped = self.formTime()
        return self.timeWhenStopped

    #Destroy the timer
    def destroy(self):
        self.timerFrame.destroy()

    #Count down 1 second
    def countDown(self):
        self.seconds -= 1
        if self.seconds == -1:
            self.seconds = 59
            self.minutes -=1
            if self.minutes == -1:
                self.minutes = 59
                self.hours -= 1
                if self.hours == -1:
                    self.timerDisplay["text"] = "00:00:00"
                    return False
        self.timerDisplay["text"] = self.formTime()
        return True


#A line
class Line(tk.Frame):
    def __init__(self, parent, colour = "#000000", thickness = 1, *args, **kwargs):
        super().__init__(parent, highlightbackground=colour, borderwidth=thickness, background=colour, width=thickness, *args, **kwargs)
        self.width = thickness
        self.parent = parent

    #Display using pack
    def pack(self, direction, *args, **kwargs):
        return super().pack(fill=direction, *args **kwargs)

    #Display using grid
    def grid(self, direction, row, column, rowspan = 1, colspan = 1, *args, **kwargs):
        if direction == 'y':
            for r in range(row, row + rowspan):
                self.parent.grid_rowconfigure(r, minsize=self.width)
            colspan = 1
            sticky = "ns"
        elif direction == 'x':
            for c in range(column, column + colspan):
                self.parent.grid_columnconfigure(c, minsize = self.width)
            rowspan = 1
            sticky="ew"
        else:
            raise(ValueError("Direction must be 'x' or 'y'"))
        super().grid(row=row, column=column, rowspan=rowspan, columnspan=colspan, sticky=sticky, *args, **kwargs)


