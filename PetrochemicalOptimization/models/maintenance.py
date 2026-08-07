from dataclasses import dataclass


@dataclass
class MaintenanceTask:

    unit_name: str

    duration: int

    priority: int

    earliest_start: int

    latest_finish: int

    assigned_day: int = -1

    finish_day: int = -1