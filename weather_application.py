import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
import requests
import re


LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


def find_webpage():
    url = ("http://www.bom.gov.au/places/")
    locs = ["nsw","vic","qld","wa","sa","tas","act","nt"]
    places = {}
    placesd = []
    for i in locs:
        turl = (url+i)
        f = requests.get(turl)
        raw_places = re.findall(r'<a href=".*?" class=".*?">.*?</a>', f.text)
        for j in raw_places:
            current = j.replace("<a href=\"","").replace("\" class=\"", "|").replace("\">", "|").replace("</a>", "").split("|")
            places[current[-1]] = ("http://www.bom.gov.au%s" %current[0])

    print(places)
    return(places)


def get_info(link):
    max_temp = []
    min_temp = []
    corf2 = []
    r = requests.get(link)
    #print(r.text)
    raw_max = re.findall(r'<dd class="max">.*?</dd>', r.text)
    raw_min = re.findall(r'<dd class="min">.*?</dd>', r.text)
    corf = re.findall(r'<dd class="pop">.*? <img ', r.text)
    #ln = re.findall(r'<h1>Canberra Weather <span class="beta">(beta)</span></h1>', r.text)
    #ln = re.findall(r'.*? Weather <span class="beta">(beta)', r.text)
    for i in corf:
        corf2.append(int(i.replace('% <img ', "").replace('<dd class="pop">', "")))

    for i in raw_max:
        max_temp.append(int(i.replace('<dd class="max">', "").replace(' &deg;C</dd>', "")))

    for i in raw_min:
        min_temp.append(int(i.replace('<dd class="min">', "").replace(' &deg;C</dd>', "")))
    return (np.array(corf2),max_temp,min_temp)




class WeatherApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        try:
            tk.Tk.iconbitmap(self, default="icon.ico")
        except:
            pass

        tk.Tk.wm_title(self, "Weather Application")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}


        for f in {StartPage, Page1, Page2}:

            frame = f(container, self)

            self.frames[f] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):
    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Visit Page 1", command=lambda : controller.show_frame(Page1),font=MEDIUM_FONT)
        button1.pack()
        button2 = tk.Button(self, text="Visit Page 2", command=lambda : controller.show_frame(Page2),font=MEDIUM_FONT)
        button2.pack()

class Page1(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Page 1", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back To Home", command=lambda : controller.show_frame(StartPage),font=MEDIUM_FONT)
        button1.pack()


class Page2(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Page 2", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back To Home", command=lambda : controller.show_frame(StartPage),font=MEDIUM_FONT)
        button1.pack()




root = WeatherApp()
root.mainloop()
for i in find_webpage().values():
    print(get_info(i))
