from pulp import *


class LPModelBuilder:

    def create_model(self):

        return LpProblem(
            "Petrochemical_Optimization",
            LpMaximize
        )