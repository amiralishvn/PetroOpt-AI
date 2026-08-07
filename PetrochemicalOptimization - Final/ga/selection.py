import random


class Selection:

    @staticmethod
    def tournament(population, tournament_size=3):

        contestants = random.sample(
            population.chromosomes,
            tournament_size
        )

        contestants.sort(
            key=lambda chromosome: chromosome.fitness,
            reverse=True
        )

        return contestants[0]