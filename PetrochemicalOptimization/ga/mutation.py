import random


class Mutation:

    @staticmethod
    def swap(chromosome, mutation_rate=0.1):

        if random.random() > mutation_rate:
            return

        i = random.randint(
            0,
            len(chromosome.genes) - 1
        )

        j = random.randint(
            0,
            len(chromosome.genes) - 1
        )

        chromosome.genes[i], chromosome.genes[j] = (
            chromosome.genes[j],
            chromosome.genes[i]
        )