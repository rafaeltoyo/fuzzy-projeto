# ======================================================================================================================
#   Menu
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   26/09/2018
# ======================================================================================================================


class Menu(object):

    def __init__(self, title):
        """

        :param title:
        :type title: str
        """
        self._title = title
        self._options = []

    def add(self, txt):
        self._options.append(txt)

    def show(self):
        print(self._title)
        count = 0
        for opt in self._options:
            count += 1
            print("[" + str(count) + "] " + opt)
        while True:
            output = int(raw_input("R: "))
            if 1 <= output <= count:
                break
            print("Opcao invalida!")
        return output

# ======================================================================================================================
