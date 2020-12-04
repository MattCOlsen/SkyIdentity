import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
import random
import Communication_Module
import module1

class Application(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)
        matplotlib.rcParams["figure.figsize"] = [2,6]
        self.data_set = [1,2,3,4,5,6]
        self.initUI()

        # to assign widgets
        self.widget = None
        self.toolbar = None

    def initUI(self):
        self.pack(fill=BOTH, expand=1)

        inteveral_label = Label(self, text="Steps")
        inteveral_label.place(x=200, y=500)

        self.enter_interval = Entry(self, bd=2, width=10)
        self.enter_interval.place(x=200, y=520)


        sizeLabel = Label(self, text="Size")
        sizeLabel.place(x=300, y=500)

        self.enter_size = Entry(self, bd=2, width=10)
        self.enter_size.place(x=300, y=520)


        transmission_label = Label(self, text="Transmission Delay (nanoseconds)")
        transmission_label.place(x=400, y=500)

        self.enter_transmission = Entry(self, bd=2, width=10)
        self.enter_transmission.place(x=400, y=520)
        self.enter_transmission.insert(0, "500")


        processing_label = Label(self, text="Processing Delay (nanoseconds)")
        processing_label.place(x=600, y=500)

        self.enter_processing = Entry(self, bd=2, width=10)
        self.enter_processing.place(x=600, y=520)
        self.enter_processing.insert(0, "500")

        plotbutton = Button(self, text="Plot Data", command=lambda: self.create_plot(self.data_set))
        plotbutton.place(x=300, y=600)

        quitbutton = Button(self, text="Quit", command=self.quit)
        quitbutton.place(x=400, y=600)


    def create_plot(self, dataset):

        # remove old widgets
        if self.widget:
            self.widget.destroy()

        if self.toolbar:
            self.toolbar.destroy()

        size = self.enter_size.get()
        size = int(size)

        step = self.enter_interval.get()
        step = int(step) 

        transmission = self.enter_transmission.get()
        transmission = int(transmission)

        processing = self.enter_processing.get()
        processing = int(processing) 

        # create new elements

        plt = Figure(figsize=(4, 4), dpi=100)

        a = plt.add_subplot(111)

        #print(test)

        test = module1.test_ChaCha20(size, step, transmission, processing)
        xi = [i[0] for i in test]
        yi = [i[1] for i in test]
        a.plot(xi, yi, color="blue", marker='o', label="ChaCha20")

        test = module1.test_RSA(size, step, transmission, processing)
        xi = [i[0] for i in test]
        yi = [i[1] for i in test]
        a.plot(xi, yi, color="red", marker='o', label="RSA")

        a.set_ylabel("seconds per decrytion")
        a.set_xlabel("key ring size")
        a.set_title("Time to Decrypt Each Packages for a Given Key Ring Size")

        canvas = FigureCanvasTkAgg(plt, self)

        self.toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar.update()

        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=BOTH)

        #self.toolbars = canvas._tkcanvas
        #self.toolbars.pack(fill=BOTH)
               


def main():


    root = Tk()
    root.wm_title("RSA vs ChaCha20")
    root.geometry("800x700+100+100")

    app = Application(master=root)
    app.mainloop()

main()