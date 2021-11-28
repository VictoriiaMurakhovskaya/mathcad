import numpy as np
from scipy.special import jn
from numpy import heaviside as PHI


class MainCalc:
    m = 9.1094e-28
    c = 2.9979e10
    ee = -4.8032e-10
    lambda_1 = 2.4048
    b = 0.025

    def __init__(self,
                 eps: float = 0,
                 eps_b: float = 0,
                 L: float = 0.556167,
                 L_t0: float = 0.5,
                 L_4: float = 0.003,
                 q: float = -6,
                 rb: float = 0,
                 zb: float = 0,
                 ksi_min=0,
                 ksi_max=0.556167,
                 r=0.0001):
        if zb * rb * eps * eps_b == 0:
            raise ValueError('Некоректні значення для розрахунків')
        self.eps = eps
        self.eps_b = eps_b
        self.L = L
        self.L_t0 = L_t0
        self.L_4 = L_4
        self.q = q
        self.rb = rb
        self.zb = zb
        self.ksi_min = ksi_min
        self.ksi_max = ksi_max
        self.r = r
        self.jn2 = jn(1, self.lambda_1) * jn(1, self.lambda_1)
        self.k = np.array([1, 2, 3])
        self.i = np.array([1, 2, 3, 4, 5])
        self.v0, self.beta, self.E_0, self.omega_1, self.nb, self.gamma = 0, 0, 0, 0, 0, 0

    def calculate(self):
        Z1 = self.Z1_calc()
        Z2 = self.Z2_calc()
        Z = lambda k, i: Z1(self.L_t0 / self.v0, k * self.L_4 / self.v0, i) + \
                         Z2(self.L_t0 / self.v0, k * self.L_4 / self.v0, i)

        E0_R = -1 * self.E_0 * self.E0_r(self.r)
        return E0_R

    def pre_calc(self):
        self.v0 = self.c * np.sqrt(1 - 1 / (1 + self.eps_b / (self.m * self.c ** 2)) ** 2)
        self.beta = self.v0 / self.c
        self.E_0 = 8 * self.q * self.c / (self.eps ** 2 * self.b * self.beta * self.L * self.rb)

    def omega_1_func(self):
        return lambda i: self.c / np.sqrt(self.eps) * np.sqrt((np.pi * i / self.L)
                                                                           ** 2 + (self.lambda_1 / self.b) ** 2)

    def omega_1_vector_func(self):
        return np.vectorize(self.omega_1_func())

    def Z2_calc(self, t, t0, i):
        omega_1 = self.omega_1_func()
        first_factor = PHI(t - t0, 1) / ((self.c * self.beta * i * np.pi / self.L)**2 - omega_1(i)**2)
        second_factor_1 = (self.c * self.beta * i * np.pi / self.L) * \
                          np.sin(self.c * self.beta * i * np.pi / self.L * (t - t0))
        second_factor_2 = omega_1(i) * np.sin(omega_1(i) * (t - t0))
        return first_factor * (second_factor_1 - second_factor_2)

    def Z2_ki_calc(self, k, i):
        t = self.L_t0 / self.v0
        t_0 = self.L_4 * k / self.v0
        return self.Z2_calc(t, t_0, i)

    def Z1_calc(self, t, t0, i):
        omega_1 = self.omega_1_func()
        return (-PHI((t - t0) - self.L / (self.beta * self.c), 1)) / \
               ((self.c * self.beta * i * np.pi) ** 2 - (omega_1(i)) ** 2) * \
               (self.c * self.beta * i * np.pi / self.L *
                np.sin(self.c * self.beta * i * np.pi / self.L * (t - t0)) -
                np.power(-1, i) * omega_1(i) *
                np.sin(omega_1(i) * (t - t0 - self.L / (self.beta * self.c))))

    def E0_r(self, r):
        return jn(0, self.lambda_1 * r / self.b) * np.exp(
            -1 * self.lambda_1 ** 2 * self.rb ** 2 / (2 * self.b ** 2)) / self.jn2

    def E0_ksi(self, ksi):
        res = 0
        for k in range(0, 10):
            for i in range(1, 81):
                res += self.Z2_ki_calc(k, i) * np.cos(np.pi * ksi * i / self.L)
        return res

    def E0_r_ksi(self, r, ksi):
        return -self.E_0 * self.E0_r(r) * self.E0_ksi(ksi)

    def E0_vector(self):
        return np.vectorize(self.E0_r_ksi)

    def get_data_for_plot(self):
        self.pre_calc()
        x = np.linspace(self.ksi_min, self.ksi_max, 100)
        y = self.E0_vector()(r=self.r, ksi=x)
        return x, y
