# ======================================================================================================================
#   Classes de Funcoes de Pertinencia
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   10/08/2018
# ======================================================================================================================

import abc


# ----------------------------------------------------------------------------------------------------------------------

class Function(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, color=None):
        self.color = color

    @abc.abstractmethod
    def calc(self, x):
        pass

    def gen(self, interval):
        return list(self._generate(interval))

    def _generate(self, interval):
        for x in interval:
            yield self.calc(x)


# ----------------------------------------------------------------------------------------------------------------------

class MembershipFunction(Function):
    def __init__(self):
        Function.__init__(self)
        self.height = 1

    @abc.abstractmethod
    def print_support(self):
        pass

    @abc.abstractmethod
    def print_core(self):
        pass

    @abc.abstractmethod
    def inv_calc(self, y):
        pass

    @abc.abstractmethod
    def card(self):
        pass

    def inclusion(self, target, interval):
        card, sum = 0, 0
        for x in interval:
            card += self.calc(x)
            sum += max(0, (self.calc(x) - target.calc(x)))
        if card == 0:
            return 0
        return (card - sum) / card

    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height
        return self


# ----------------------------------------------------------------------------------------------------------------------

class TrapezoidalMFunction(MembershipFunction):
    def __init__(self, a, m, n, b):
        MembershipFunction.__init__(self)
        self.a = a
        self.m = m
        self.n = n
        self.b = b

    def print_support(self):
        return str("(%.4f, %.4f)" % (self.a, self.b))

    def print_core(self):
        return str("[%.4f, %.4f]" % (self.m, self.n))

    def calc(self, x):
        if self.a < x < self.m:
            return self.height * (x - self.a) / (self.m - self.a)
        elif self.m <= x <= self.n:
            return self.height
        elif self.n < x < self.b:
            return self.height * (self.b - x) / (self.b - self.n)
        return 0

    def inv_calc(self, y):
        if 0 > y > 1:
            return None, None
        elif y == 1:
            return self.m, self.n
        return float(y * float(self.m - self.a) / self.height + self.a), float(
            self.b - y * float(self.b - self.n) / self.height)

    def card(self):
        return self.height * ((self.m - self.a) / 2 + (self.n - self.m) + (self.b - self.n) / 2)


# ----------------------------------------------------------------------------------------------------------------------

class TriagularMFunction(TrapezoidalMFunction):
    def __init__(self, a, m, b):
        TrapezoidalMFunction.__init__(self, a, m, m, b)


# ----------------------------------------------------------------------------------------------------------------------

class RectangularMFunction(TrapezoidalMFunction):
    def __init__(self, a, b):
        TrapezoidalMFunction.__init__(self, a, a, b, b)

# ======================================================================================================================
