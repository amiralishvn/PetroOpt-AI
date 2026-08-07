from pulp import lpSum


class ConstraintBuilder:

    def add_feed_constraint(
        self,
        model,
        refinery,
        production
    ):

        model += lpSum(
            production[unit.name] * unit.feed_consumption
            for unit in refinery.units
        ) <= refinery.total_feed

    def add_energy_constraint(
        self,
        model,
        refinery,
        production
    ):

        model += lpSum(
            production[unit.name] * unit.energy_consumption
            for unit in refinery.units
        ) <= refinery.total_energy