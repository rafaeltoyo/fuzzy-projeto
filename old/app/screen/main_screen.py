# ======================================================================================================================
#   Tela Inicial
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   11/08/2018
# ======================================================================================================================

import Tkinter as tk


# ----------------------------------------------------------------------------------------------------------------------

class MainScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        author = tk.Label(self, text="Aluno: Rafael Hideo Toyomoto", font=("Arial", 12))
        author.pack(pady=10, padx=10)

        authorra = tk.Label(self, text="RA: 1722085", font=("Arial", 12))
        authorra.pack(pady=10, padx=10)

# ======================================================================================================================