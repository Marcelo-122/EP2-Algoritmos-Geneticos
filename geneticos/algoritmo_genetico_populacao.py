class AlgoritmoGeneticoPopulacao:
    def __init__(self, populacao):
        self.populacao = populacao
        self.erro = float("inf")
        self.geracoes = 1

    def erro_final(self):
        return self.erro

    def qtd_geracoes(self):
        return self.geracoes

    def rodar(self, max_geracoes=1000, imprimir_em_geracaoes=100, erro_min=0.01):
        print(
            f"Geração: {self.geracoes}, Erro: {round(self.erro, 3)}, {self.populacao.top_individuo().imprime()}"
        )

        while True:
            if self.geracoes >= max_geracoes or self.erro <= erro_min:
                print(
                    f"Geração: {self.geracoes}, Erro: {self.erro}, {self.populacao.top_individuo().imprime()}"
                )
                break

            populacao_mutada = self.populacao.mutacao()
            populacao_crossover = self.populacao.crossover()

            self.populacao.selecionar(populacao_mutada, populacao_crossover)
            fitness = self.populacao.top_fitness()

            if (1 - fitness) < self.erro:
                self.erro = 1 - fitness

            self.geracoes += 1
            if self.geracoes % imprimir_em_geracaoes == 0:
                print(
                    f"Geração: {self.geracoes}, Erro: {self.erro}, {self.populacao.top_individuo().imprime()}"
                )
        return self.populacao.top_individuo()
