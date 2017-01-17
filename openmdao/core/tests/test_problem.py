""" Unit tests for the problem interface."""

import unittest

from openmdao.api import Problem, Group, IndepVarComp, ScipyIterativeSolver
from openmdao.devtools.testutil import assert_rel_error
from openmdao.solvers.ln_direct import DirectSolver
from openmdao.test_suite.components.paraboloid import Paraboloid


class TestProblem(unittest.TestCase):

    def test_compute_total_derivs_basic(self):
        # Basic test for the method using default solvers on simple model.

        top = Problem()
        root = top.root = Group()
        root.add_subsystem('p1', IndepVarComp('x', 0.0), promotes=['x'])
        root.add_subsystem('p2', IndepVarComp('y', 0.0), promotes=['y'])
        root.add_subsystem('comp', Paraboloid(), promotes=['x', 'y', 'f_xy'])

        # TODO: We should use our default solver here, when it is working.
        root.ln_solver = DirectSolver()

        top.setup(check=False, mode='fwd')
        #top.root.suppress_solver_output = True
        top.run()

        of = ['f_xy']
        wrt = ['x', 'y']
        derivs = top.compute_total_derivs(of=of, wrt=wrt)

        top.setup(check=False, mode='rev')
        top.run()

        # TODO: Forward don't work yet

        of = ['f_xy']
        wrt = ['x', 'y']
        derivs = top.compute_total_derivs(of=of, wrt=wrt)

        assert_rel_error(self, derivs[('f_xy', 'x')], -6.0, 1e-6)
        assert_rel_error(self, derivs[('f_xy', 'y')], 8.0, 1e-6)

    def test_setup_bad_mode(self):
        # Test error message when passing bad mode to setup.

        top = Problem()
        root = top.root = Group()

        try:
            top.setup(mode='junk')
        except ValueError as err:
            msg = "Unsupported mode: 'junk'"
            self.assertEqual(str(err), msg)
        else:
            self.fail('Expecting ValueError')


if __name__ == "__main__":
    unittest.main()
