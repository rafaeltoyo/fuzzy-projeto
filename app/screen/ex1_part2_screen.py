# ======================================================================================================================
#   Exercicio 1 - Parte 2
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   11/08/2018
# ======================================================================================================================

import numpy as np

import Tkinter as tk
import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

from base.function import TrapezoidalMFunction, TriagularMFunction, RectangularMFunction
from base.operation.standard_operation import StdUnion, StdIntersection, StdComplement
from base.operation.tnorm_operation import TNorm1, TNorm9
from base.operation.conorm_operation import CoNorm4, CoNorm9
from base.util import PlotOperation

# ----------------------------------------------------------------------------------------------------------------------


class Ex1Part2Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.plot_config = None

        self.__build_plot_area()
        self.__build_plot_area_3d()
        self.__build_form_area()
        self.show_option_frame()

    # ------------------------------------------------------------------------------------------------------------------

    def __build_plot_area(self):
        self.plot_frame = tk.Frame(self, width=400, height=550, bg="#ccc")
        self.plot_frame.grid(row=0, column=0, sticky="ns")

        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.plot.set_xlabel('Pertinencia')
        self.plot.set_ylim(0, 1)

        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def __build_plot_area_3d(self):
        self.plot_frame_3d = tk.Frame(self, width=400, height=550, bg="#ccc")
        self.plot_frame_3d.grid(row=0, column=0, sticky="ns")

        self.figure_3d = Figure(figsize=(5, 5), dpi=100)
        self.plot_3d = self.figure_3d.add_subplot(111, projection='3d')

        self.canvas_3d = FigureCanvasTkAgg(self.figure_3d, self.plot_frame_3d)
        self.canvas_3d.draw()
        self.canvas_3d.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar_3d = NavigationToolbar2Tk(self.canvas_3d, self.plot_frame_3d)
        self.toolbar_3d.update()
        self.canvas_3d._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def show_plot_frame(self):
        self.plot_frame.tkraise()

    def show_plot_frame_3d(self):
        self.plot_frame_3d.tkraise()

    # ------------------------------------------------------------------------------------------------------------------

    def __build_form_area(self):
        self.option_frame = Ex1Part2OptionsMenu(self, self)
        self.option_frame.grid(row=0, column=0, sticky="nsew")

        self.variable_frame = Ex1Part2VariableMenu(self, self)
        self.variable_frame.grid(row=0, column=0, sticky="nsew")

        self.altura_frame = Ex1Part2AlturaMenu(self, self)
        self.altura_frame.grid(row=0, column=0, sticky="nsew")

        self.peso_frame = Ex1Part2PesoMenu(self, self)
        self.peso_frame.grid(row=0, column=0, sticky="nsew")

    def show_option_frame(self):
        self.option_frame.tkraise()

    def show_variable_frame(self, operation):
        self.variable_frame.set_operation(operation)
        self.variable_frame.tkraise()

    def show_altura_frame(self, operation):
        self.altura_frame.operation = operation
        self.altura_frame.tkraise()

    def show_peso_frame(self, operation):
        self.peso_frame.operation = operation
        self.peso_frame.tkraise()

    # ------------------------------------------------------------------------------------------------------------------

    def update_plot(self):
        self.plot.clear()
        if self.plot_config is not None:
            self.plot_config.plot(self.plot)
        self.plot.legend()
        self.canvas.draw()

    def update_plot_3d(self, norm):
        self.plot_3d.clear()

        x = np.linspace(1, 2, 100)
        y = np.linspace(0, 100, 100)
        X, Y = np.meshgrid(x, y)
        zs = np.array([norm.calc_z(x, y) for x, y in zip(np.ravel(X), np.ravel(Y))])
        Z = zs.reshape(X.shape)

        self.plot_3d.plot_surface(X, Y, Z)

        self.plot_3d.legend()
        self.canvas_3d.draw()

    # ------------------------------------------------------------------------------------------------------------------

    def set_plot_1(self):
        self.plot_config = PlotOperation(1, 2, 1000)

    def set_plot_2(self):
        self.plot_config = PlotOperation(0,100,1000)

    def set_function(self, label, func):
        if self.plot_config is not None:
            self.plot_config.clear()
            self.plot_config.add_func(label, func)

    def get_function_1(self, name):
        if name == "Baixo":
            return TriagularMFunction(1, 1, 1.5)
        elif name == "Medio":
            return TriagularMFunction(1, 1.5, 2)
        elif name == "Alto":
            return TriagularMFunction(1.5, 2, 2)

    def get_function_2(self, name):
        if name == "Leve":
            return TriagularMFunction(0, 0, 50)
        elif name == "Moderado":
            return TriagularMFunction(0, 50, 100)
        elif name == "Pesado":
            return TriagularMFunction(50, 100, 100)


# ----------------------------------------------------------------------------------------------------------------------


class Ex1Part2OptionsMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Button(self, text="(a)", command=lambda: self.select_a()).pack()
        ttk.Button(self, text="(b)", command=lambda: self.select_b()).pack()
        ttk.Button(self, text="(c)", command=lambda: self.select_c()).pack()
        ttk.Button(self, text="(d)", command=lambda: self.select_d()).pack()
        ttk.Button(self, text="(e)", command=lambda: self.select_e()).pack()
        ttk.Button(self, text="(e-bonus)", command=lambda: self.select_e_bonus()).pack()
        ttk.Button(self, text="(f)", command=lambda: self.select_f()).pack()
        ttk.Button(self, text="(f-bonus)", command=lambda: self.select_f_bonus()).pack()

    def select_a(self):
        self.controller.show_variable_frame("union")

    def select_b(self):
        self.controller.show_variable_frame("intersection")

    def select_c(self):
        f = StdIntersection()
        f.add_func("Nem Baixo", StdComplement(self.controller.get_function_1("Baixo")))
        f.add_func("Nem Alto", StdComplement(self.controller.get_function_1("Alto")))
        self.controller.set_plot_1()
        self.controller.set_function("Nem Baixo E Nem Alto", f)
        self.controller.update_plot()
        self.controller.show_plot_frame()

    def select_d(self):
        f = StdUnion()
        f.add_func("Nao Muito Leve", StdComplement(self.controller.get_function_2("Leve")))
        f.add_func("Pesado", self.controller.get_function_2("Pesado"))
        self.controller.set_plot_2()
        self.controller.set_function("Pesado OU Nao Muito Leve", f)
        self.controller.update_plot()
        self.controller.show_plot_frame()

    def select_e(self):
        n = TNorm9(self.controller.get_function_1("Baixo"), self.controller.get_function_2("Leve"))
        self.controller.update_plot_3d(n)
        self.controller.show_plot_frame_3d()

    def select_e_bonus(self):
        n = TNorm1(self.controller.get_function_1("Baixo"), self.controller.get_function_2("Leve"), 2)
        self.controller.update_plot_3d(n)
        self.controller.show_plot_frame_3d()

    def select_f(self):
        n = CoNorm9(self.controller.get_function_1("Alto"), self.controller.get_function_2("Pesado"))
        self.controller.update_plot_3d(n)
        self.controller.show_plot_frame_3d()

    def select_f_bonus(self):
        n = CoNorm4(self.controller.get_function_1("Alto"), self.controller.get_function_2("Pesado"))
        self.controller.update_plot_3d(n)
        self.controller.show_plot_frame_3d()

# ----------------------------------------------------------------------------------------------------------------------


class Ex1Part2VariableMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.operation = None

        ttk.Button(self, text="Altura", command=lambda: self.select_altura()).pack()
        ttk.Button(self, text="Peso", command=lambda: self.select_peso()).pack()

    def set_operation(self, operation):
        self.operation = operation

    def select_altura(self):
        self.controller.show_altura_frame(self.operation)

    def select_peso(self):
        self.controller.show_peso_frame(self.operation)

# ----------------------------------------------------------------------------------------------------------------------


class Ex1Part2AlturaMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.func = None
        self.func_name = None
        self.operation = None

        ttk.Button(self, text="Baixo", command=lambda: self.select_function("Baixo")).pack()
        ttk.Button(self, text="Medio", command=lambda: self.select_function("Medio")).pack()
        ttk.Button(self, text="Alto", command=lambda: self.select_function("Alto")).pack()

    def tkraise(self, aboveThis=None):
        self.func = None
        self.func_name = None

        tk.Frame.tkraise(self, aboveThis=aboveThis)

    def select_function(self, func):
        if self.func is None:
            if self.operation is None or self.operation == "union":
                self.func = StdUnion()
            else:
                self.func = StdIntersection()
            self.func.add_func(func, self.controller.get_function_1(func))
            self.func_name = func
        else:
            self.func.add_func(func, self.controller.get_function_1(func))
            self.controller.set_plot_1()
            self.controller.set_function(self.func_name + " OU " + func, self.func)
            self.controller.update_plot()
            self.controller.show_plot_frame()

# ----------------------------------------------------------------------------------------------------------------------


class Ex1Part2PesoMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.func = None
        self.func_name = None
        self.operation = None

        ttk.Button(self, text="Leve", command=lambda: self.select_function("Leve")).pack()
        ttk.Button(self, text="Moderado", command=lambda: self.select_function("Moderado")).pack()
        ttk.Button(self, text="Pesado", command=lambda: self.select_function("Pesado")).pack()

    def tkraise(self, aboveThis=None):
        self.func = None
        self.func_name = None

        tk.Frame.tkraise(self, aboveThis=aboveThis)

    def select_function(self, func):
        if self.func is None:
            if self.operation is None or self.operation == "union":
                self.func = StdUnion()
            else:
                self.func = StdIntersection()
            self.func.add_func(func, self.controller.get_function_2(func))
            self.func_name = func
        else:
            self.func.add_func(func, self.controller.get_function_2(func))
            self.controller.set_plot_2()
            self.controller.set_function(self.func_name + " OU " + func, self.func)
            self.controller.update_plot()
            self.controller.show_plot_frame()

# ======================================================================================================================
