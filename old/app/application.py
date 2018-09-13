# ======================================================================================================================
#   Aplicacao principal
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   11/08/2018
# ======================================================================================================================

import Tkinter as tk
import ttk

from app import MainScreen
from app import Ex1Part1Screen
from app import Ex1Part2Screen


# ----------------------------------------------------------------------------------------------------------------------

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('PP1 - Fuzzy')
        self.resizable(width=False, height=False)
        #self.geometry('{}x{}'.format(620,600))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.__build_menu_frame()
        self.__build_main_frame()

    def __build_menu_frame(self):
        menu = tk.Frame(self, width=620, height=50, bg="#ccc")
        menu.grid(row=0, column=0, sticky="ns")

        ttk.Button(menu, text="Home", command=lambda: self.show_main()).grid(row=0, column=0)
        ttk.Button(menu, text="Ex 1.1", command=lambda: self.show_ex1(1)).grid(row=0, column=1)
        ttk.Button(menu, text="Ex 1.2", command=lambda: self.show_ex1(2)).grid(row=0, column=2)
        ttk.Button(menu, text="Ex 2", command=lambda: self.show_ex2()).grid(row=0, column=3)

    def __build_main_frame(self):
        main = tk.Frame(self, width=620, height=550)
        main.grid(row=1, column=0, sticky="ns")
        self.frames = {}
        for F in (MainScreen, Ex1Part1Screen, Ex1Part2Screen):
            frame = F(main, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_main()

    def show_main(self):
        frame = self.frames[MainScreen]
        frame.tkraise()

    def show_ex1(self, id):
        frame = self.frames[Ex1Part1Screen]
        if id == 1:
            frame.set_functions_1()
        elif id == 2:
            frame.set_functions_2()
        frame.show_function_menu()
        frame.update_plot()
        frame.tkraise()

    def show_ex2(self):
        frame = self.frames[Ex1Part2Screen]
        frame.show_option_frame()
        frame.tkraise()


# ======================================================================================================================
