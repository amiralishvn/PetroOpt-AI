from dataclasses import dataclass, field


# --------------------------------------------------
# Production Unit
# --------------------------------------------------

@dataclass
class ProductionUnit:

    name: str

    capacity: float

    profit: float

    feed_consumption: float

    energy_consumption: float


# --------------------------------------------------
# Refinery Data
# --------------------------------------------------

@dataclass
class RefineryData:

    total_feed: float = 0.0

    total_energy: float = 0.0

    units: list = field(default_factory=list)

    # ---------------------------------------------

    def add_unit(

        self,

        name,

        capacity,

        profit,

        feed_consumption,

        energy_consumption

    ):

        unit = ProductionUnit(

            name=name,

            capacity=capacity,

            profit=profit,

            feed_consumption=feed_consumption,

            energy_consumption=energy_consumption

        )

        self.units.append(unit)

    # ---------------------------------------------

    def clear_units(self):

        self.units.clear()

    # ---------------------------------------------

    def number_of_units(self):

        return len(self.units)