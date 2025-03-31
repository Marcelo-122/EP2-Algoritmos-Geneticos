class IndividuoSimples:
  def fitness(self):
    raise NotImplementedError("Implementar")

  def mutacao(self):
    raise NotImplementedError("Implementar")

class Individuo(IndividuoSimples):
  def crossover(self):
    raise NotImplementedError("Implementar")