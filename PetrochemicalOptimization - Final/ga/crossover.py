import random

from ga.chromosome import Chromosome


class Crossover:

    @staticmethod
    def order_crossover(parent1, parent2):

        size = len(parent1.genes)

        # -------------------------------
        # Safety Checks
        # -------------------------------

        if size == 0:
            return Chromosome(parent1.tasks)

        if size == 1:
            child = Chromosome(parent1.tasks)
            child.genes = parent1.genes.copy()
            return child

        if len(parent1.genes) != len(parent2.genes):
            raise ValueError(
                "Parents must have the same chromosome length."
            )

        # -------------------------------
        # Create Child
        # -------------------------------

        child = Chromosome(parent1.tasks)

        child.genes = [-1] * size

        # -------------------------------
        # Random Segment
        # -------------------------------

        start = random.randint(0, size - 2)

        end = random.randint(start + 1, size - 1)

        # -------------------------------
        # Copy Segment
        # -------------------------------

        child.genes[start:end + 1] = parent1.genes[start:end + 1]

        # -------------------------------
        # Fill Remaining Genes
        # -------------------------------

        parent2_index = 0

        for i in range(size):

            if child.genes[i] != -1:
                continue

            while parent2.genes[parent2_index] in child.genes:
                parent2_index += 1

            child.genes[i] = parent2.genes[parent2_index]

        return child