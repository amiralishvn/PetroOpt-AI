from dataclasses import dataclass
from typing import Dict


@dataclass
class OptimizationResult:

    status: str

    optimal_profit: float

    production_plan: Dict

    used_feed: float

    used_energy: float

    remaining_feed: float

    remaining_energy: float

    maintenance_schedule: Dict = None