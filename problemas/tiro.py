import math
import random
from geneticos.individuo import Individuo
from geneticos.populacao import Populacao


class Tiro(Individuo):
    GRAVIDADE = 9.80665  # m/sˆ2
    THETA_MAX = math.pi / 2  # 90em radianos
    THETA_MIN = 0
    VELOCIDADE_MAX = 200  # em m/s
    VELOCIDADE_MIN = 1  # em m/s
    VARIACAO_THETA = 0.0174533  # 1 grau
    VARIACAO_VELOCIDADE = 1  # 10 m/s
    X_ALVO = 10000  # distância do alvo em metros

    def __init__(
        self,
        theta=random.uniform(THETA_MIN, THETA_MAX),
        velocidade=random.uniform(VELOCIDADE_MIN, VELOCIDADE_MAX),
    ):
        self.theta = theta  # em radianos
        self.velocidade = velocidade  #

    # quão mais próximo está do alvo
    def fitness(self):
        x_tiro = self._alcance()
        return abs(self.X_ALVO - x_tiro) / self.X_ALVO

    # atualiza os dados do individuo atual
    # dica a variacao pode ser em quantidades
    # positivas ou negativas de Theta ou velocidade
    # usando VARIACAO_THETA e VARIACAO_VELOCIDADE
    # algo com random.uniform(min, max)
    def mutacao(self):
        theta = -1
        velocidade = -1
        while theta < self.THETA_MIN or theta > self.THETA_MAX:
            theta = self.theta + random.uniform(
                -self.VARIACAO_THETA, self.VARIACAO_THETA
            )
        while velocidade < self.VELOCIDADE_MIN or velocidade > self.VELOCIDADE_MAX:
            velocidade = self.velocidade + random.uniform(
                -self.VARIACAO_VELOCIDADE, self.VARIACAO_VELOCIDADE
            )

        return Tiro(theta, velocidade)

    def crossover(self, outro):
        elementos = [self, outro]
        elemento_index = random.choice([0, 1])

        theta = elementos[elemento_index].theta
        velocidade = elementos[1 - elemento_index].velocidade
        return Tiro(theta, velocidade)

    def imprime(self):
        return f"Theta: {round(self.theta, 3)}, Velocidade: {round(self.velocidade, 3)}, Fitness: {round(self.fitness(), 3)}"

    def _alcance(self):
        return (
            self.velocidade * self.velocidade * math.sin(2 * self.theta)
        ) / self.GRAVIDADE


class PopulacaoCanhoes(Populacao):
    pass
