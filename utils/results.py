import csv

from evolution.objective import OptimizationObjective


class Results:
    def __init__(self, objectives: [OptimizationObjective]):
        self.times = []
        self.alg = []
        self.population_size = []
        self.generations = []
        self.objectives = objectives
        self.objectives_values = [[] for _ in range(len(objectives))]

    def save_to_file(self, filename, append=False):
        mode = 'a' if append else 'w'
        with open(filename, mode, newline='') as csvfile:
            writer = csv.writer(csvfile)

            if not append:
                writer.writerow(["Algorithm", "Population Size", "Generations", "Time"] + [obj.name for obj in self.objectives])

            num_rows = max(len(self.times), len(self.alg), len(self.population_size),
                           max(len(vals) for vals in self.objectives_values))
            for i in range(num_rows):
                alg = self.alg[i] if i < len(self.alg) else ""
                pop_size = self.population_size[i] if i < len(self.population_size) else ""
                generations = self.generations[i] if i < len(self.generations) else ""
                time = self.times[i] if i < len(self.times) else ""
                obj_values = [vals[i] if i < len(vals) else "" for vals in self.objectives_values]
                writer.writerow([alg, pop_size, generations, time] + obj_values)
