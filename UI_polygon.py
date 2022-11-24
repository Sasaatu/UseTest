
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from Polygons import poly_scale, poly_rotate



class Application(ttk.Frame):

    ##################################################
    # Design GUI
    def __init__(self, master=None):
        super().__init__(master)
        ### window
        self.master = master
        self.master.title('Polygon app')

        # widget
        ### canvas
        '''canvas1 = Canvas(root, width = 200, height = 240, bg="red")
        canvas2 = Canvas(root, width = 200, height = 160, bg="green")
        canvas3 = Canvas(root, width = 400, height = 400, bg="blue")'''

        ### Frame1 ###
        self.frame1 = ttk.Frame(self.master, width=200, height=210,
        borderwidth=10, relief='sunken')
        # label
        self.label1 = ttk.Label(self.frame1, text='--Input Polygon--',
        font=('Arial',14,'bold'))
        # TextBox
        self.text_poly = Text(self.frame1, width=15, height=10)
        # Button
        self.but_disp = ttk.Button(self.frame1, text='Display', command=self.Show_Diagram)

        ### Frame2 ### 
        self.frame2 = ttk.Frame(self.master, width=200, height=180,
        borderwidth=10, relief='sunken')
        self.fr21 = ttk.Frame(self.frame2, width=200, height=160)
        self.fr22 = ttk.Frame(self.frame2, width=200, height=160)
        self.fr23 = ttk.Frame(self.frame2, width=200, height=160)
        self.fr24 = ttk.Frame(self.frame2, width=200, height=160)
        self.fr25 = ttk.Frame(self.frame2, width=200, height=160)
        # Label
        self.label2 = ttk.Label(self.fr21, text='--Transform--',
        font=('Arial',14,'bold'))
        self.label_scnt = ttk.Label(self.fr22, text='Center Point')
        self.label3 = ttk.Label(self.fr23, text='Scaling Rate')
        self.label4 = ttk.Label(self.fr24, text='Rotation Angle')
        # EditBox
        self.edit_scnt = ttk.Entry(self.fr22, width=5)
        self.edit_sc = ttk.Entry(self.fr23, width=5)
        self.edit_rot = ttk.Entry(self.fr24, width=5)
        # Button
        self.but_trans = ttk.Button(self.fr25, text='Transform', command=self.Polygon_Transform)

        ### Frame3 ###
        self.frame3 = ttk.Frame(self.master, width=500, height=400,
        borderwidth=10, relief='sunken')
        ##############
        # Graph 
        # figure
        self.h = plt.figure()
        self.h.set_figheight(4)
        self.h.set_figwidth(3)
        # add axis
        self.axes = self.h.add_subplot()
        # axis
        self.axes.axis('equal')
        #self.axes.axis('tight')
        # label
        label_dict =  {'family':'sans-serif', 'weight':'bold', 'color':'k', 'size':8}
        self.axes.set_xlabel('X [mm]', fontdict = label_dict)
        self.axes.set_ylabel('Y [mm]', fontdict = label_dict)
        # title
        title_dict = {'fontsize':12, 'fontweight':'bold', 'color':'k'}
        plt.title('Polygon Scaling', fontdict = title_dict)
        # bottom and left margin
        self.h.subplots_adjust(left=0.2, bottom=0.2)

        ##############
        # intergrate graph window in GUI
        self.canvas = FigureCanvasTkAgg(self.h, self.frame3)

        # Layout
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=1, column=0)
        self.frame3.grid(row=0, column=1, rowspan=2)

        self.label1.pack(side=TOP)
        self.text_poly.pack(side=TOP, padx=25, pady=10)
        self.but_disp.pack(side=TOP)

        self.fr21.pack(side=TOP, fill=X, pady=10)
        self.fr22.pack(side=TOP, fill=X)
        self.fr23.pack(side=TOP, fill=X)
        self.fr24.pack(side=TOP, fill=X)
        self.fr25.pack(side=TOP, fill=X, pady=5)

        self.label2.pack()
        self.label_scnt.pack(side=LEFT, anchor=W)
        self.edit_scnt.pack(side=LEFT, anchor=E)
        self.label3.pack(side=LEFT, anchor=W)
        self.edit_sc.pack(side=LEFT, anchor=E)
        self.label4.pack(side=LEFT, anchor=W)
        self.edit_rot.pack(side=LEFT, anchor=E)
        self.but_trans.pack(anchor=W)

        self.canvas.get_tk_widget().pack(side=TOP, anchor=CENTER)


    ##################################################
    # CallBack function

    def Show_Diagram(self):
        # Show Original Polygon 
        # Delete axis in the figure and recreate axis and plot
        self.h.clear(())
        self.axes = self.h.add_subplot()

        P1 = self.extract_polygon()
        # append first row
        P1_plt = np.vstack((P1, P1[0,:]))

        # Make plot
        self.axes.plot(P1_plt[:,0], P1_plt[:,1], 'r', marker = 'o', markersize = 6)   # before
        # Show Diagram
        self.canvas.draw_idle()

    def Polygon_Transform(self):
        # Show Original and Scaled Polygons
        # Delete axis in the figure and recreate axis and plot
        self.h.clear(())
        self.axes = self.h.add_subplot()

        P1 = self.extract_polygon()
        # append first row
        P1_plt = np.vstack((P1, P1[0,:]))

        # Get Transform parameter
        cnt_str = self.edit_scnt.get()
        rate_str = self.edit_sc.get()
        rot_str = self.edit_rot.get()
        # Default value setting
        trans_cnt = np.fromstring(cnt_str, dtype=int, sep=' ')
        if np.size(trans_cnt) == 0:
            messagebox.showerror('Please set center point')
            exit()

        if len(rate_str) == 0:
            k = 1
        elif float(rate_str) == 0:
            messagebox.showerror('Please enter nonzero value')
            exit()
        else:
            k = float(rate_str)

        if len(rot_str) == 0:
            theta = 0
        else:
            theta = float(rot_str)

        # Transform
        P2 = poly_scale(P1, trans_cnt, k)
        P2  = poly_rotate(P2, trans_cnt, theta)
        P2_plt = np.vstack((P2, P2[0,:]))
        # Make plot
        self.axes.plot(P1_plt[:,0], P1_plt[:,1], 'r', marker = 'o', markersize = 6)    # origial
        self.axes.plot(P2_plt[:,0], P2_plt[:,1], 'b', marker = 'o', markersize = 6)    # renew
        
        # Show Diagram
        self.canvas.draw_idle()

    ##################################################
    # Polygon function

    def extract_polygon(self):
        # Read all in TextBox
        poly_str = self.text_poly.get("1.0","end-1c")
        # Replace \n by space
        poly_str = poly_str.replace('\n', ' ')
        # string to ndarray
        poly_array = np.fromstring(poly_str, dtype=int, sep=' ')
        # reshape in array of N*2
        #size = np.shape(poly_array)
        col = poly_array.shape[0]
        P1 = np.reshape(poly_array, [col//2, 2])
        return P1



def main():
    # Generate figure
    root = Tk()
    # Instance named "app"
    app = Application(root)
    # keep app stand by
    app.mainloop()


if __name__ == '__main__':
    main()