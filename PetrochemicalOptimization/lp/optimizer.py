from pulp import (
    LpProblem,
    LpMaximize,
    LpVariable,
    lpSum,
    value,
    LpStatus,
    PULP_CBC_CMD
)

from models.refinery import RefineryData
from models.result import OptimizationResult


class LinearProgrammingOptimizer:

    def optimize(self, refinery: RefineryData) -> OptimizationResult:

        model = LpProblem(
            "Petrochemical_Optimization",
            LpMaximize
        )

        production = {}

        # -----------------------------
        # Decision Variables
        # -----------------------------

        for unit in refinery.units:

            production[unit.name] = LpVariable(
                name=unit.name,
                lowBound=0,
                upBound=unit.capacity
            )

        # -----------------------------
        # Objective Function
        # -----------------------------

        model += lpSum(
            production[unit.name] * unit.profit
            for unit in refinery.units
        )

        # -----------------------------
        # Feed Constraint
        # -----------------------------

        model += (
            lpSum(
                production[unit.name] * unit.feed_consumption
                for unit in refinery.units
            )
            <= refinery.total_feed
        )

        # -----------------------------
        # Energy Constraint
        # -----------------------------

        model += (
            lpSum(
                production[unit.name] * unit.energy_consumption
                for unit in refinery.units
            )
            <= refinery.total_energy
        )

        # -----------------------------
        # Solve Model
        # -----------------------------

        model.solve(PULP_CBC_CMD(msg=False))

        # -----------------------------
        # Extract Results
        # -----------------------------

        production_plan = {}

        used_feed = 0.0
        used_energy = 0.0

        for unit in refinery.units:

            amount = production[unit.name].varValue or 0.0

            production_plan[unit.name] = amount

            used_feed += amount * unit.feed_consumption
            used_energy += amount * unit.energy_consumption

        optimal_profit = value(model.objective) or 0.0

        return OptimizationResult(
            status=LpStatus[model.status],
            optimal_profit=optimal_profit,
            production_plan=production_plan,
            used_feed=used_feed,
            used_energy=used_energy,
            remaining_feed=refinery.total_feed - used_feed,
            remaining_energy=refinery.total_energy - used_energy
        )