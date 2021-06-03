import numpy
import numpy as np
from scipy.special import jn
from numpy import heaviside as PHI


class MainCalc:
    L = 0.556167
    L_t0 = 0.5
    L_4 = 0.003
    m = 9.1094e-28
    c = 2.9979e10
    ee = -4.8032e-10
    lambda_1 = 2.4048
    b = 0.025

    def __init__(self, zb=0, rb=0, eps=0, eps_b=0, q=0, ksi_min=0, ksi_max=0.556167, ksi_step=0.003):
        if zb * rb * eps * eps_b == 0:
            raise ValueError('Некоректні значення для розрахунків')
        self.zb = zb
        self.rb = rb
        self.eps = eps
        self.eps_b = eps_b
        self.q = q
        self.ksi_min = ksi_min
        self.ksi_max = ksi_max
        self.ksi_step = ksi_step

        self.v0 = self.c * np.sqrt(1 - 1 / (1 + self.eps_b / (self.m * self.c ** 2)) ** 2)
        self.beta = self.v0 / self.c
        self.E_0 = 8 * self.q * self.c / (self.eps ** 2 * self.b * self.beta * self.L * self.rb)

        self.omega_1 = lambda i: self.c / np.sqrt(self.eps) * np.sqrt((np.pi * i / self.L) ** 2 +
                                                                 (self.lambda_1 / self.b) ** 2)

        self.nb = self.q / (self.ee * (np.pi * self.rb ** 2 * self.zb))  # не используется
        self.gamma = 1 / np.sqrt(1 - self.beta ** 2)  # не используется

        beta = self.beta

        self.Z1 = lambda t, t0, i: (-PHI((t - t0) - self.L / (beta * self.c), 1)) / \
                             ((self.c * beta * i * np.pi) ** 2 - (self.omega_1(i)) ** 2) * \
                             (self.c * beta * i * np.pi / self.L *
                             np.sin(self.c * beta * i * np.pi / self.L * (t - t0)) - \
                             np.power(-1, i) * self.omega_1(i) * \
                             np.sin(self.omega_1(i) * (t - t0 - self.L / (beta * self.c))))

        self.Z2 = lambda t, t0, i: PHI(t - t0, 1) / ((self.c * beta * i * np.pi) ** 2 - (self.omega_1(i)) ** 2) * \
                             (self.c * beta * i * np.pi / self.L *
                             np.sin(self.c * beta * i * np.pi / self.L * (t - t0)) - self.omega_1(i) *
                             np.sin(self.omega_1(i) * (t - t0)))

    def Z(self, t, t0, i):
        return self.Z1(t, t0, i) + self.Z2(t, t0, i)

    def E0_r(self, r):
        return jn(0, self.lambda_1 * r/self.b) * np.exp(-1 * self.lambda_1**2 * self.rb**2 / (2 * self.b**2)) /\
               (jn(1, self.lambda_1) * jn(1, self.lambda_1))

    def E0_ksi(self, ksi):
        res = 0
        for k in range(10):
            for i in range(1, 81):
                res += self.Z(self.L_t0 / self.v0, k * self.L_4 / self.v0, i) * np.cos(np.pi * ksi * i / self.L)
        return res
