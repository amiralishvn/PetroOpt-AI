class FitnessCalculator:

    @staticmethod
    def calculate(chromosome):

        fitness = 0

        current_day = 1

        for gene in chromosome.genes:

            task = chromosome.tasks[gene]

            # ---------------------------------
            # Respect Earliest Start
            # ---------------------------------

            start_day = max(
                current_day,
                task.earliest_start
            )

            # ---------------------------------
            # Finish Day
            # ---------------------------------

            finish_day = (
                start_day +
                task.duration -
                1
            )

            # ---------------------------------
            # Priority Score
            # ---------------------------------

            priority_score = (
                task.priority * 100
            )

            # ---------------------------------
            # Early Scheduling Bonus
            # ---------------------------------

            early_bonus = max(
                0,
                30 - start_day
            )

            # ---------------------------------
            # Short Duration Bonus
            # ---------------------------------

            duration_bonus = max(
                0,
                20 - task.duration
            )

            # ---------------------------------
            # Latest Finish Penalty
            # ---------------------------------

            penalty = 0

            if finish_day > task.latest_finish:

                penalty = (
                    finish_day -
                    task.latest_finish
                ) * 100

            # ---------------------------------
            # Earliest Start Penalty
            # ---------------------------------

            early_penalty = 0

            if start_day < task.earliest_start:

                early_penalty = (
                    task.earliest_start -
                    start_day
                ) * 100

            # ---------------------------------
            # Fitness
            # ---------------------------------

            fitness += (
                priority_score +
                early_bonus +
                duration_bonus -
                penalty -
                early_penalty
            )

            # ---------------------------------
            # Move Current Day Forward
            # ---------------------------------

            current_day = finish_day + 1

        chromosome.fitness = fitness

        return fitness