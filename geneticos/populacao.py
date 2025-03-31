class Populacao:
    def __init__(self, Individuo_classe, tamanho_populacao=10):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = [Individuo_classe()] * tamanho_populacao
        self.fitness = 0

    def mutacao(self):
        nova_lista = []
        for individuo in self.populacao:
            nova_lista.append(individuo.mutacao())
        return nova_lista

    def crossover(self):
        return []

    def selecionar(self, populacao1=[], populacao2=[]):
        nova_lista = sorted(self.populacao, key=self._fitness_populacao, reverse=True)
        self.populacao = nova_lista[0 : self.tamanho_populacao]

    def top_fitness(self):
        return self.top_individuo().fitness()

    def top_individuo(self):
        return self.populacao[0]

    def _fitness_populacao(self, individuo):
        return individuo.fitness()
