class InputValidator:

    @staticmethod
    def validate_refinery(refinery):

        errors = []

        if refinery.total_feed <= 0:
            errors.append("Total Feed must be greater than zero.")

        if refinery.total_energy <= 0:
            errors.append("Total Energy must be greater than zero.")

        if len(refinery.units) == 0:
            errors.append("At least one production unit is required.")

        for i, unit in enumerate(refinery.units):

            if unit.name.strip() == "":
                errors.append(f"Production Unit {i+1}: Name is required.")

            if unit.capacity <= 0:
                errors.append(f"{unit.name or f'Unit {i+1}'}: Capacity must be greater than zero.")

            if unit.profit < 0:
                errors.append(f"{unit.name or f'Unit {i+1}'}: Profit cannot be negative.")

            if unit.feed_consumption <= 0:
                errors.append(f"{unit.name or f'Unit {i+1}'}: Feed Consumption must be greater than zero.")

            if unit.energy_consumption <= 0:
                errors.append(f"{unit.name or f'Unit {i+1}'}: Energy Consumption must be greater than zero.")

        return errors


    @staticmethod
    def validate_maintenance_tasks(tasks):

        errors = []

        if len(tasks) == 0:
            errors.append("At least one maintenance task is required.")
            return errors

        for i, task in enumerate(tasks):

            if task["unit_name"].strip() == "":
                errors.append(
                    f"Maintenance Task {i+1}: Unit Name is required."
                )

            if task["duration"] <= 0:
                errors.append(
                    f"{task['unit_name'] or f'Task {i+1}'}: Duration must be greater than zero."
                )

            if task["latest_finish"] < task["earliest_start"]:
                errors.append(
                    f"{task['unit_name'] or f'Task {i+1}'}: Latest Finish must be greater than or equal to Earliest Start."
                )

        return errors