from unittest import TestCase, main
from application.calc import MainCalc
from numpy.testing import assert_array_almost_equal
import numpy as np


class TestApp(TestCase):

    def setUp(self) -> None:
        self.mc = MainCalc(zb=0.015, rb=0.015, eps=1.725,
                           eps_b=1e6 * 1.6e-12, q=-2e-9 * 3e9, r=0.0001,
                           L=0.556167, L_4=0.003, L_t0=0.5)

    def test_precalc(self):
        self.mc.pre_calc()
        self.assertAlmostEqual(2.821e10, self.mc.v0, delta=0.01 * 2.821e10)
        self.assertAlmostEqual(self.mc.beta, 0.941, delta=0.01 * 0.941)
        self.assertAlmostEqual(self.mc.E_0, -2.464e15, delta=0.01 * 2.464e15)

    def test_omega(self):
        expected = [2.199e12, 2.211e12, 2.229e12, 2.255e12, 2.288e12]
        omega_1_func = self.mc.omega_1_func()
        actual = list(map(omega_1_func, [1, 2, 3, 4, 5]))
        assert_array_almost_equal(np.array(expected), np.array(actual), decimal=-9)

    def test_Z2_calc(self):
        self.mc.pre_calc()
        expected = [1.865e-12, 5.167e-13, 5.666e-13, -3.52e-13, 1.888e-13]
        actual = [self.mc.Z2_ki_calc(0, 15),
                  self.mc.Z2_ki_calc(2, 30),
                  self.mc.Z2_ki_calc(6, 38),
                  self.mc.Z2_ki_calc(9, 0),
                  self.mc.Z2_ki_calc(7, 77)]
        assert_array_almost_equal(np.array(expected), np.array(actual), decimal=15)

    def test_E0_r(self):
        self.mc.pre_calc()
        expected = [1.307, 1.283]
        actual = [self.mc.E0_r(0.001), self.mc.E0_r(0.003)]
        assert_array_almost_equal(np.array(expected), np.array(actual), decimal=2)

    def test_Z2_sum(self):
        self.mc.pre_calc()
        expected = 9.95e-12
        actual = 0
        for k in range(0, 10):
            for i in range(1, 81):
                actual += self.mc.Z2_ki_calc(k, i)
        self.assertAlmostEqual(expected, actual, delta=1e-14)

    def test_E0_ksi(self):
        self.mc.pre_calc()
        expected = [-3.758e-12, 1.748e-11, 3.107e-11, 5.869e-11, 1.512e-11, -9.374e-13]
        actual = [self.mc.E0_ksi(0.1), self.mc.E0_ksi(0.2), self.mc.E0_ksi(0.3),
                  self.mc.E0_ksi(0.4), self.mc.E0_ksi(0.5), self.mc.E0_ksi(0.55)]
        assert_array_almost_equal(np.array(expected), np.array(actual), decimal=13)

    def test_E0_total(self):
        self.mc.pre_calc()
        expected = [-1.213e4, 4.88e4, -3.026e3]
        actual = [self.mc.E0_r_ksi(0.0001, 0.1), self.mc.E0_r_ksi(0.0001, 0.5), self.mc.E0_r_ksi(0.0001, 0.55)]
        assert_array_almost_equal(np.array(expected), np.array(actual), decimal=-2)

    def test_vectorization(self):
        self.mc.pre_calc()
        func = np.vectorize(self.mc.E0_r_ksi, excluded='r')
        expected = [-1.213e4, 4.88e4, -3.026e3]
        actual = func(r=0.0001, ksi=[0.1, 0.5, 0.55])
        assert_array_almost_equal(np.array(expected), np.array(actual), decimal=-2)

    def test_vectorized(self):
        self.mc.pre_calc()
        expected = [-1.213e4, 4.88e4, -3.026e3]
        actual = self.mc.E0_vector()(r=0.0001, ksi=[0.1, 0.5, 0.55])
        assert_array_almost_equal(np.array(expected), np.array(actual), decimal=-2)