# ======================================================================================================================
#   Exercicio 1 - Parte 1
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   11/08/2018
# ======================================================================================================================

import Tkinter as tk
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from base import TrapezoidalMFunction, TriagularMFunction, RectangularMFunction
from base import PlotOperation

# ----------------------------------------------------------------------------------------------------------------------

class Ex1Part1Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.plot_config = PlotOperation(1,2,1000)

        self.__build_draw_area()
        self.__build_form_area()
        self.update_plot()

    # ------------------------------------------------------------------------------------------------------------------

    def __build_draw_area(self):
        draw = tk.Frame(self, width=400, height=550, bg="#ccc")
        draw.grid(row=0, column=0, sticky="ns")

        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.plot.set_xlabel('Pertinencia')
        self.plot.set_ylabel('Altura')

        self.canvas = FigureCanvasTkAgg(self.figure, draw)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, draw)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def __build_form_area(self):
        main = tk.Frame(self)
        main.grid(row=0, column=1, sticky="nsew")

        self.frames = {}

        for F in (Ex1Part1FunctionsMenu, Ex1Part1ActionsMenu):
            frame = F(main, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_function_menu()

    # ------------------------------------------------------------------------------------------------------------------

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_function_menu(self):
        self.unset_acut_function()
        frame = self.frames[Ex1Part1FunctionsMenu]
        frame.tkraise()

    def show_action_menu(self):
        self.unset_acut_function()
        frame = self.frames[Ex1Part1ActionsMenu]
        frame.update_values()
        frame.tkraise()

    def set_func_selected(self, func):
        self.current_func_label = func

    def get_func_selected(self):
        return self.plot_config.get_func(self.current_func_label)

    # ------------------------------------------------------------------------------------------------------------------

    def update_plot(self):
        self.plot.clear()
        self.plot_config.plot(self.plot)
        self.plot.legend()
        self.canvas.draw()

    def set_functions_1(self):
        self.plot_config.add_func("Baixo", TriagularMFunction(1, 1, 1.5))
        self.plot_config.add_func("Medio", TriagularMFunction(1, 1.5, 2))
        self.plot_config.add_func("Alto", TriagularMFunction(1.65, 2, 2))

    def set_functions_2(self):
        self.plot_config.add_func("Baixo", TrapezoidalMFunction(1, 1, 1.2, 1.5))
        self.plot_config.add_func("Medio", TrapezoidalMFunction(1, 1.4, 1.6, 2))
        self.plot_config.add_func("Alto", TrapezoidalMFunction(1.5, 1.8, 2, 2))

    def set_acut_function(self, a, b):
        self.plot_config.add_func("a-Corte", RectangularMFunction(a, b))

    def unset_acut_function(self):
        try:
            self.plot_config.remove_func("a-Corte")
        except:
            pass


# ----------------------------------------------------------------------------------------------------------------------

class Ex1Part1FunctionsMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Button(self, text="Baixo", command=lambda: self.select_function("Baixo")).pack()
        ttk.Button(self, text="Medio", command=lambda: self.select_function("Medio")).pack()
        ttk.Button(self, text="Alto", command=lambda: self.select_function("Alto")).pack()


    def select_function(self, func):
        self.controller.set_func_selected(func)
        self.controller.show_action_menu()


# ----------------------------------------------------------------------------------------------------------------------

class Ex1Part1ActionsMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.row = 0

        ttk.Button(self, text="Voltar", command=lambda: self.controller.show_function_menu()).grid(row=0, columnspan=2)

        self.sv_a, self.out_a = self.__build_input_question("Pertinencia de um ponto:", "Ponto:", self.__exec_a)
        self.sv_b, self.out_b = self.__build_input_question("Pertinencia de um intervalo:", "Step:", self.__exec_b)
        self.out_c = self.__build_output_question("Suporte:")
        self.out_d = self.__build_output_question("Nucleo:")
        self.out_e = self.__build_output_question("Altura(Height):")
        self.sv_f, self.out_f = self.__build_input_question("Alfa-Corte:", "Alfa:", self.__exec_f)
        self.out_g = self.__build_output_question("Grau de Inclusao:")

    def update_values(self):
        self.__exec_a()
        self.__exec_b()
        self.__exec_c()
        self.__exec_d()
        self.__exec_e()
        self.__exec_f()
        self.__exec_g()

    def __build_input_question(self, title="", label="", func=None):
        row1 = self.row
        self.row += 1
        row2 = self.row
        self.row += 1
        row3 = self.row
        self.row += 1

        # Output Print
        output = tk.Label(self, text="", font=("Arial", 12))
        output.grid(row=row3, columnspan=2)
        # Input Handler
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv = sv: func())
        # Title
        tk.Label(self, text=title, font=("Arial", 12)).grid(row=row1, columnspan=2)
        # Input Label and Entry
        self.row += 1
        tk.Label(self, text=label, font=("Arial", 12)).grid(row=row2, column=0)
        input = tk.Entry(self, textvariable=sv)
        input.grid(row=row2, column=1)

        return sv, output

    def __build_output_question(self, title="", label="", func=None):
        row1 = self.row
        self.row += 1
        row2 = self.row
        self.row += 1

        # Title
        tk.Label(self, text=title, font=("Arial", 12)).grid(row=row1, column=0)
        # Output Print
        output = tk.Label(self, text="", font=("Arial", 12))
        output.grid(row=row2, columnspan=2)

        return output

    @staticmethod
    def __get_value(sv):
        try:
            return float(sv.get())
        except:
            return None

    def __exec_a(self):
        self.out_a['text'] = ""

        func = self.controller.get_func_selected()
        read = self.__get_value(self.sv_a)

        if (func is not None) and (read is not None):
            self.out_a['text'] = str("%.6f" % func.calc(read))

    def __exec_b(self):
        self.out_b['text'] = ""

        func = self.controller.get_func_selected()
        read = self.__get_value(self.sv_b)

        if (func is not None) and (read is not None) and (read > 0):
            iter = 1
            while iter <= 2:
                self.out_b['text'] += str("%.4f -> %.4f \n" % (iter, func.calc(iter)))
                iter += read

    def __exec_c(self):
        func = self.controller.get_func_selected()

        if (func is not None):
            self.out_c["text"] = func.print_support()

    def __exec_d(self):
        func = self.controller.get_func_selected()

        if (func is not None):
            self.out_d["text"] = func.print_core()

    def __exec_e(self):
        func = self.controller.get_func_selected()

        if (func is not None):
            self.out_e["text"] = str("%.6f" % func.get_height())

    def __exec_f(self):
        self.out_f['text'] = ""
        self.controller.unset_acut_function()

        func = self.controller.get_func_selected()
        read = self.__get_value(self.sv_f)

        if (func is not None) and (read is not None) and (read > 0):
            xi, xf = func.inv_calc(read)
            if xi != None and xf != None:
                self.out_f["text"] = str("[%.6f, %.6f]" % (xi, xf))
                self.controller.set_acut_function(xi, xf)
        self.controller.update_plot()

    def __exec_g(self):
        func_b = self.controller.plot_config.get_func("Baixo")
        func_m = self.controller.plot_config.get_func("Medio")
        func_a = self.controller.plot_config.get_func("Alto")

        if (func_b is not None) and (func_m is not None) and (func_a is not None):
            self.out_g["text"] = ("Inclusao de Baixo em Medio: %.6f \n" % float(func_b.inclusion(func_m, self.controller.plot_config.points)))
            self.out_g["text"] += ("Inclusao de Medio em Alto: %.6f \n" % float(func_m.inclusion(func_a, self.controller.plot_config.points)))

# ======================================================================================================================
