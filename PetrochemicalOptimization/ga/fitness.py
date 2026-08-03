class FitnessCalculator:

    @staticmethod
    def calculate(chromosome):

        fitness = 0

        current_day = 1

        for gene in chromosome.genes:

            task = chromosome.tasks[gene]

            # ----------------------------
            # Priority Score
            # ----------------------------

            priority_score = task.priority * 100

            # ----------------------------
            # Early Scheduling Bonus
            # ----------------------------

            early_bonus = max(
                0,
                30 - current_day
            )

            # ----------------------------
            # Short Duration Bonus
            # ----------------------------

            duration_bonus = max(
                0,
                20 - task.duration
            )

            # ----------------------------
            # Deadline Penalty
            # ----------------------------

            finish_day = current_day + task.duration

            penalty = 0

            if finish_day > task.latest_finish:

                penalty = (
                    finish_day -
                    task.latest_finish
                ) * 50

            fitness += (
                priority_score +
                early_bonus +
                duration_bonus -
                penalty
            )

            current_day += task.duration

        chromosome.fitness = fitness

        return fitness