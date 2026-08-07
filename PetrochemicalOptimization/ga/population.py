from ga.chromosome import Chromosome
from ga.fitness import FitnessCalculator


class Population:

    def __init__(self, maintenance_tasks, population_size=20):

        self.population_size = population_size

        self.chromosomes = []

        self.initialize_population(maintenance_tasks)

    def initialize_population(self, maintenance_tasks):

        self.chromosomes = []

        for _ in range(self.population_size):

            chromosome = Chromosome(maintenance_tasks)

            # Calculate Fitness
            FitnessCalculator.calculate(chromosome)

            self.chromosomes.append(chromosome)

    def get_best(self):

        return max(
            self.chromosomes,
            key=lambda chromosome: chromosome.fitness
        )

    def get_average_fitness(self):

        if len(self.chromosomes) == 0:
            return 0

        total = sum(
            chromosome.fitness
            for chromosome in self.chromosomes
        )

        return total / len(self.chromosomes)

    def size(self):

        return len(self.chromosomes)