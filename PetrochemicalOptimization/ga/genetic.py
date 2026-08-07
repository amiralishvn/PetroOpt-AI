from ga.population import Population
from ga.selection import Selection
from ga.crossover import Crossover
from ga.fitness import FitnessCalculator
from ga.mutation import Mutation


class GeneticAlgorithm:

    def __init__(
        self,
        maintenance_tasks,
        population_size=20,
        generations=50
    ):

        self.maintenance_tasks = maintenance_tasks
        self.population_size = population_size
        self.generations = generations

    def run(self):

        population = Population(
            self.maintenance_tasks,
            self.population_size
        )

        best = population.get_best()

        for generation in range(self.generations):

            new_population = []

            while len(new_population) < self.population_size:

                # --------------------------
                # Parent Selection
                # --------------------------

                parent1 = Selection.tournament(population)
                parent2 = Selection.tournament(population)

                # --------------------------
                # Crossover
                # --------------------------

                child = Crossover.order_crossover(
                    parent1,
                    parent2
                )

                # --------------------------
                # Mutation
                # --------------------------

                Mutation.swap(child)

                # --------------------------
                # Fitness Evaluation
                # --------------------------

                FitnessCalculator.calculate(child)

                new_population.append(child)

            # Replace old population
            population.chromosomes = new_population

            # Find best chromosome
            current_best = population.get_best()

            if current_best.fitness > best.fitness:

                best = current_best

        # ---------------------------------
        # Create Maintenance Schedule
        # ---------------------------------

        maintenance_schedule = {}

        current_day = 1

        for gene in best.genes:

            task = self.maintenance_tasks[gene]

            # Respect earliest start
            start_day = max(
                current_day,
                task.earliest_start
            )

            # Calculate finish day
            finish_day = (
                start_day +
                task.duration -
                1
            )

            # Save schedule information
            task.assigned_day = start_day
            task.finish_day = finish_day

            maintenance_schedule[
                task.unit_name
            ] = {
                "start_day": start_day,
                "finish_day": finish_day,
                "duration": task.duration,
                "priority": task.priority
            }

            # Move timeline forward
            current_day = finish_day + 1

        return best, maintenance_schedule