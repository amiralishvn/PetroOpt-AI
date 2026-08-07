import random


class Chromosome:

    def __init__(self, maintenance_tasks):

        self.tasks = maintenance_tasks

        self.genes = []

        self.fitness = 0

        self.initialize()

    def initialize(self):

        self.genes = list(range(len(self.tasks)))

        random.shuffle(self.genes)