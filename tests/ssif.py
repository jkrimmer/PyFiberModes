'''
Created on 2014-05-06

@author: cbrunet
'''
import unittest
from math import sqrt

from fibermodes import fixedFiber, Mode, Wavelength


class TestSSIF(unittest.TestCase):

    def testFundamental(self):
        wl = Wavelength(1550e-9)
        fiber = fixedFiber(wl, [4.5e-6], [1.448918, 1.444418])
        he11 = fiber.solve(Mode('HE', 1, 1))
        self.assertAlmostEqual(he11.neff, 1.4464045, places=5)

        lp01 = fiber.solve(Mode('LP', 0, 1))
        self.assertAlmostEqual(he11.neff, lp01.neff, places=5)

    def testvModes(self):
        wl = Wavelength(800e-9)
        fiber = fixedFiber(wl, [4.5e-6], [1.448918, 1.444418])
        modes = fiber.vModes(delta=1e-4)

        self.assertEqual(len(modes), 7)

        sols = [('HE(1,1)', 1.4479082),
                ('TE(0,1)', 1.44643),
                ('HE(2,1)', 1.446427),
                ('TM(0,1)', 1.4464268),
                ('EH(1,1)', 1.444673),
                ('HE(3,1)', 1.444669),
                ('HE(1,2)', 1.4444531)]
        for i, (name, neff) in enumerate(sols):
            self.assertEqual(name, str(modes[i]))
            self.assertAlmostEqual(neff, modes[i].neff)

    def testlpModes(self):
        wl = Wavelength(800e-9)
        fiber = fixedFiber(wl, [4.5e-6], [1.448918, 1.444418])
        modes = fiber.lpModes(delta=1e-4)

        self.assertEqual(len(modes), 4)

    def testvModesFromlpModes(self):
        wl = Wavelength(800e-9)
        fiber = fixedFiber(wl, [4.5e-6], [1.448918, 1.444418])
        lpModes = fiber.lpModes(delta=1e-4)
        modes = fiber.vModes(lpModes, delta=1e-5)

        sols = [('HE(1,1)', 1.4479082),
                ('TE(0,1)', 1.44643),
                ('HE(2,1)', 1.446427),
                ('TM(0,1)', 1.4464268),
                ('EH(1,1)', 1.444673),
                ('HE(3,1)', 1.444669),
                ('HE(1,2)', 1.4444531)]

        self.assertEqual(len(modes), len(sols))
        for i, (name, neff) in enumerate(sols):
            self.assertEqual(name, str(modes[i]))
            self.assertAlmostEqual(neff, modes[i].neff)

    def testBures3_6(self):
        delta = 0.3
        V = 5

        wl = Wavelength(1.55e-6)
        n2 = 1.444

        n1 = sqrt(n2**2 / (1 - 2 * delta))
        rho = V / (sqrt(n1**2 - n2**2) * wl.k0)

        fiber = fixedFiber(wl, [rho], [n1, n2])
        modes = fiber.vModes(delta=1e-3)

        sols = {'HE(1,1)': 2.119,
                'TE(0,1)': 3.153,
                'TM(0,1)': 3.446,
                'HE(2,1)': 3.377,
                'EH(1,1)': 4.235,
                'HE(3,1)': 4.507,
                'HE(1,2)': 4.638}

        self.assertEqual(len(modes), len(sols))
        for m in modes:
            name = str(m)
            if name in sols:
                u = wl.k0 * rho * sqrt(n1**2 - m.neff**2)
                self.assertAlmostEqual(u, sols[name], 3)

    def testBures_4_2_8(self):
        n2 = 1.457420
        n1 = 1.462420
        rho = 8.335e-6
        wl = Wavelength(0.6328e-6)

        fiber = fixedFiber(wl, [rho], [n1, n2])
        modes = fiber.lpModes(delta=1e-4)

        sols = {'LP(0,1)': 2.1845,
                'LP(0,2)': 4.9966,
                'LP(0,3)': 7.7642,
                'LP(1,1)': 3.4770,
                'LP(1,2)': 6.3310,
                'LP(1,3)': 9.0463,
                'LP(2,1)': 4.6544,
                'LP(2,2)': 7.5667,
                'LP(3,1)': 5.7740,
                'LP(3,2)': 8.7290,
                'LP(4,1)': 6.8560,
                'LP(4,2)': 9.8153,
                'LP(5,1)': 7.9096,
                'LP(6,1)': 8.9390,
                'LP(7,1)': 9.9451}

        self.assertEqual(len(modes), len(sols))
        for m in modes:
            name = str(m)
            if name in sols:
                u = wl.k0 * rho * sqrt(n1**2 - m.neff**2)
                self.assertAlmostEqual(u, sols[name], 3)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSSIF']
    unittest.main()
