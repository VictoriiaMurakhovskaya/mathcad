from unittest import TestCase, main
from calc import MainCalc
import matplotlib.pyplot as plt


class TestApp(TestCase):
    mc = MainCalc(zb=0.015, rb=0.015, eps=1.725, eps_b=1e6 * 1.6e-12, q=-2e-9 * 3e9, r=0.0001)

    def test_v0(self):
        self.assertAlmostEqual(self.mc.v0, 2.821e10, delta=0.01 * 2.821e10)

    def test_beta(self):
        self.assertAlmostEqual(self.mc.beta, 0.941, delta=0.01 * 0.941)

    def test_nb(self):
        self.assertAlmostEqual(self.mc.nb, 1.178e15, delta=0.01 * 1.178e15)

    def test_gamma(self):
        self.assertAlmostEqual(self.mc.gamma, 2.954, delta=0.02)

    def test_eps_b(self):
        self.assertAlmostEqual(self.mc.eps_b, 1.6e-6, delta=1.6e-8)

    def test_q(self):
        self.assertAlmostEqual(self.mc.q, -6, delta=0.06)

    def test_E0(self):
        self.assertAlmostEqual(self.mc.E_0, -2.464e15, delta=1e13)

    def test_omega(self):
        self.assertAlmostEqual(self.mc.omega_1(50), 6.81e12, delta=2e10)

    def test_Z1(self):
        t = self.mc.L_t0 / self.mc.v0
        t0 = self.mc.L_4 / self.mc.v0
        self.assertAlmostEqual(self.mc.Z1(t, t0, 1), 0, delta=1e-12)

    def test_Z2(self):
        t = self.mc.L_t0 / self.mc.v0
        t0 = self.mc.L_4 / self.mc.v0
        self.assertAlmostEqual(self.mc.Z2(t, t0, 1), 3.859e-13, delta=4e-15)

    def test_Z(self):
        t = self.mc.L_t0 / self.mc.v0
        t0 = self.mc.L_4 / self.mc.v0
        self.assertAlmostEqual(self.mc.Z(t, t0, 1), 0, delta=1e-12)

    def test_E0_r(self):
        self.assertAlmostEqual(self.mc.E0_r(0.001), 1.307, delta=0.02)

    def test_E0_ksi(self):
        self.assertAlmostEqual(self.mc.E0_ksi(0.4), 5.869e-11, delta=1e-11)

    def test_E0_vector(self):
        print(self.mc.E0_vector())

    def test_plot(self):
        x, y = self.mc.E0_vector()
        plt.plot(x, y)
        plt.show()


if __name__ == '__main__':
    main()