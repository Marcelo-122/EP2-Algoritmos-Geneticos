class AlgoritmoGeneticoIndividuo:
    def __init__(self, individuo):
        self.individuo = individuo
        self.erro = float("inf")
        self.geracoes = 1

    def erro_final(self):
        return self.erro

    def qtd_geracoes(self):
        return self.geracoes

    def rodar(self, max_geracoes=100_000, imprimir_em_geracaoes=5000, erro_min=0.01):
        print(
            f"Geração: {self.geracoes}, Erro: {self.erro}, {self.individuo.imprime()}"
        )

        while True:
            if self.geracoes >= max_geracoes or self.erro <= erro_min:
                print(
                    f"Geração: {self.geracoes}, Erro: {self.erro}, {self.individuo.imprime()}"
                )
                break
            novo_individuo = self.individuo.mutacao()
            fitness = novo_individuo.fitness()

            if (1 - fitness) < self.erro:
                self.erro = 1 - fitness
                self.individuo = novo_individuo

            self.geracoes += 1
            if self.geracoes % imprimir_em_geracaoes == 0:
                print(
                    f"Geração: {self.geracoes}, Erro: {self.erro}, {self.individuo.imprime()}"
                )
        return self.individuo
