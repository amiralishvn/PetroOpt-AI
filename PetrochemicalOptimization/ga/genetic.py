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

        for day, gene in enumerate(best.genes):

            task = self.maintenance_tasks[gene]

            task.assigned_day = day + 1

            maintenance_schedule[
                task.unit_name
            ] = task.assigned_day

        return best, maintenance_schedule