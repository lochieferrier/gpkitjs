from gpkit import Variable, VectorVariable, Model
from gpkit.tools import te_exp_minus1
import numpy as np


class ShoppingCart(Model):
    def __init__(self, goods=None, bads=None, taylor_order=10):
        goods = goods if goods else {}
        bads = bads if bads else {}

        for monomial, options in goods.items():
            if monomial.units and not hasattr(options, "units"):
                options = map(float, options) * monomial.units
            goods[monomial] = options

        for monomial, options in bads.items():
            if monomial.units and not hasattr(options, "units"):
                options =  map(float, options) * monomial.units
            goods[1/monomial] = 1./options
        N = check_values_length(goods)

        c = 0.1
        objective = 1
        exp_S = VectorVariable(N, "e^{S}")
        constraints = [[exp_S >= 1, exp_S.prod() == np.e]]
        for monomial, options in goods.items():
            u = 10*max(options) if (1/monomial) in bads else 0
            options_star = (options + u)**c
            m_st = Variable("%s^*" % monomial.latex(excluded=["models", "units"]))
            m_nd = Variable("|%s^*|" % monomial.latex(excluded=["models", "units"]))
            exp_m = Variable("e^{%s}" % m_nd.latex(excluded=["models"]))
            objective /= monomial
            options_star_scale = options_star.mean()
            options_star /= options_star_scale
            if getattr(options_star, "dimensionless", None):
                options_star = options_star.magnitude
            constraints.append([
                (m_nd*options_star_scale.magnitude)**(1./c) * options.units >= monomial + u,
                (exp_S**options_star).prod() == exp_m,
                exp_m >= 1 + te_exp_minus1(m_nd, taylor_order),
                ])
        Model.__init__(self, objective, constraints)

    def selection_string(self, sol):
        return "  ".join(map(lambda f: "%3i%%"%(100*f), np.log(sol(self["e^{S}"]))))



def check_values_length(dictionary, N=None):
    for option in dictionary.values():
        if N is None:
            N = len(option)
        elif len(option) != N:
            raise ValueError("all values must be of equal length, but one was"
                             "length %i while another was length %i" % (N, len(option)))
    return N
