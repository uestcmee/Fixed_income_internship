import time, threading
from tkinter import *
from tkinter import messagebox

class Interface:
    def __init__(self):
        #threading.Thread.__init__(self)
        self.attrib1 = "Attrib from Interface class"
        #Main Window
        self.mainWindow = Tk()
        self.mainWindow.geometry("200x200")
        self.mainWindow.title("My GUI Title")
        self.mainWindow.protocol("WM_DELETE_WINDOW", self.quit)
        #Label
        lbCommand = Label(self.mainWindow, text="Hello world", font=("Courier New", 16)).place(x=20, y=20)

    #def run(self):

    def start(self): #Start
        self.mainWindow.mainloop()

    #The Interface class contains methods that use attributes from itself and attributes from Process class.
    def method1(self):
        print(self.attrib1)
        print(SecondThread.attrib2)

    def quit(self):
        if messagebox.askyesno('App','Are you sure you want to quit?'):
            #In order to use quit function, mainWindow MUST BE an attribute of Interface.
            self.mainWindow.destroy()
            self.mainWindow.quit()

class Process(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.attrib2 = "Attrib from Process class"

    def run(self):
        global finish
        while not finish:
            print("Proceso infinito")
            #Inside the infinite process a method from Interface class is used.
            GUI.method1()
            time.sleep(3)

finish = False
#Starts the GUI

GUI = Interface()
#Starts the infinity process
SecondThread = Process()
GUI.mainWindow.after(50, SecondThread.start)
#Waits until GUI is closed
GUI.start()
#GUI.join()
print("When GUI is closed this message appears")
#When GUI is closed we set finish to True, so SecondThread will be closed.
finish = True
#After all the program should finish but it raises the error: Tcl_AsyncDelete: async handler deleted by the wrong thread
