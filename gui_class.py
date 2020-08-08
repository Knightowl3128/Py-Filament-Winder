import tkinter as tk
from tkinter.ttk import Progressbar

from PIL import ImageTk, Image
from multiprocessing import Process
from winding2 import Winding

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)



        self.title('Py Filament Winder')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        self.values_frm = tk.Frame(container)

        frame_1 = Mandrel_Values_Screen(self.values_frm, self)
        frame_1.pack(side='top', fill="both")
        frame_2 = Winding_Values_Screen(self.values_frm, self)
        frame_2.pack(side='top', fill="both")

        self.run_button = tk.Button(self.values_frm, text="Run", bg="#9bc4c5",command = self.submit_callback)
        self.run_button.pack(side='bottom', fill='both')
        self.values_frm.pack(side='left')
        self.frame_3 = Cylinder_Diagram(container, self)
        self.frame_3.pack(side='right', fill="both")

        self.mandrel_values_dict = {'Total Length': "0", 'Diameter': "0", 'Left Turnaround Length': "0",
                                    'Right Turnaround Length': "0"}


    def submit_callback(self):
        self.run_button.destroy()

        a = Winding()

        def bar():
            import time
            progress['value'] = 20
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 40
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 50
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 60
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 80
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 100
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 80
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 60
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 50
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 40
            tk.update_idletasks()
            time.sleep(0.5)

            progress['value'] = 20
            tk.update_idletasks()
            time.sleep(0.5)
            progress['value'] = 0

        progress = Progressbar(self.values_frm, orient=tk.HORIZONTAL,
                               length=320, mode='indeterminate')
        progress.pack(side='bottom')
        progress.start()
        x = Process(target=a.integrate, args=())
        x.start()



    def filter_callback(self, new_value, mandrel_value):
        self.mandrel_values_dict[mandrel_value] = new_value
        # print(mandrel_value,new_value)
        self.frame_3.update_labels(self.mandrel_values_dict)
        # must return true since we want the validation events to keep coming
        return (True)


class Cylinder_Diagram(tk.Frame):
    CANVAS_HEIGHT = 370
    CANVAS_WIDTH = 700
    CANVAS_COLOR = '#ece8c5'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg=self.CANVAS_COLOR, relief=tk.RIDGE, borderwidth=5)
        self.parent = parent
        img = ImageTk.PhotoImage(Image.open("Cylinder Pics/bitmap.png"))

        #work around for putting pictures in tkinter....something to do with garbage collector
        label = tk.Label(image=img)
        label.image = img

        C = tk.Canvas(self, bg=self.CANVAS_COLOR, height=self.CANVAS_HEIGHT, width=self.CANVAS_WIDTH)
        C.create_image(self.CANVAS_WIDTH / 2, self.CANVAS_HEIGHT / 2, image=img)

        C.pack()

        # lab = tk.Label(image=img).place(x=150, y=50)

        self.lbl_total_l = tk.Label(self,text = '0 mm', width=8)
        self.lbl_total_l.place(x=330, y=40)

        # vcmd = (ent_total_l.register(lambda x : controller.filter_callback(x, 15)), "%P")
        # ent_total_l.config(validate="key", validatecommand=vcmd)

        self.lbl_turnaround_l = tk.Label(self, text = '0 mm', width=6)
        self.lbl_turnaround_l.place(x=97, y=106)

        self.lbl_turnaround_r = tk.Label(self, text = '0 mm', width=6)
        self.lbl_turnaround_r.place(x=471, y=106)

        self.lbl_dia = tk.Label(self, text = '0 mm', width=6)
        self.lbl_dia.place(x=652, y=215)

    def update_labels(self, mandrel_values):
        self.lbl_total_l['text'] = mandrel_values['Total Length'] + " mm"
        self.lbl_turnaround_l['text'] = mandrel_values['Left Turnaround Length'] + " mm"
        self.lbl_turnaround_r['text'] = mandrel_values['Right Turnaround Length'] + " mm"
        self.lbl_dia['text'] = mandrel_values['Diameter'] + " mm"


class LabelEntry(tk.Frame):
    def __init__(self, parent, controller, text, mirror=False):
        super().__init__(parent)
        self.pack(fill=tk.X)

        lbl = tk.Label(self, text=text, width=20, anchor='w')
        lbl.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, padx=5)
        if mirror:
            vcmd = (self.entry.register(lambda x: controller.filter_callback(x, text)), "%P")
            self.entry.config(validate="key", validatecommand=vcmd)


class Mandrel_Values_Screen(tk.Frame):
    mandrel_values = ['Total Length', 'Diameter', 'Left Turnaround Length', 'Right Turnaround Length']
    COLOR = '#59a1a7'
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, relief=tk.RIDGE, borderwidth=5)
        lbl = tk.Label(self, text='Mandrel Values', width=20, anchor='w', font=('Helvetica', 12, 'bold'))
        lbl.pack(fill='x', padx=5)
        self.labels = []
        for value_name in self.mandrel_values:
            self.labels.append(LabelEntry(self, controller, value_name, mirror=True))


class Winding_Values_Screen(tk.Frame):
    winding_values = ['Angular Velocity', 'Tow Thickness', 'Tow Angle (\U000003B1)', 'Skip Index', 'Pattern Number']

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, relief=tk.RIDGE, borderwidth=5)
        lbl = tk.Label(self, text='Winding Parameters', width=20, anchor='w', font=('Helvetica', 12, 'bold'))
        lbl.pack(fill='x', padx=5)
        for value_name in self.winding_values:
            LabelEntry(self, controller, value_name)


if __name__ == '__main__':
    app = MainApplication()

    app.mainloop()
