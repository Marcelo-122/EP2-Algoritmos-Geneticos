import random

class Populacao:
    def __init__(self, Individuo_classe, tamanho_populacao=10):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = [Individuo_classe() for _ in range(tamanho_populacao)]
        self.fitness = 0

    def mutacao(self):
        nova_lista = []
        for individuo in self.populacao:
            nova_lista.append(individuo.mutacao())
        return nova_lista

    def crossover(self):
        filhos = []
        for _ in range(self.tamanho_populacao):
            pai1, pai2 = random.sample(self.populacao, 2)
            filho = pai1.crossover(pai2)
            filhos.append(filho)
        return filhos

    def selecionar(self, populacao1=None, populacao2=None):
        if populacao1 is None:
            populacao1 = self.populacao
        if populacao2 is None:
            populacao2 = []

        nova_lista = sorted(
            populacao1 + populacao2, key=self._fitness_populacao, reverse=True
        )
        self.populacao = nova_lista[: self.tamanho_populacao]

    def top_fitness(self):
        return self.top_individuo().fitness()

    def top_individuo(self):
        return self.populacao[0]

    def _fitness_populacao(self, individuo):
        return individuo.fitness()
