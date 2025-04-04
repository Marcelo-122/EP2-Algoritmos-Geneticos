import random
from geneticos.individuo import Individuo
from geneticos.populacao import Populacao

class PlanoUsoEquipamento(Individuo):
    def __init__(self, plano=None, max_tempo_por_equip=40):
        # Definição das análises e os equipamentos disponíveis para cada uma
        self.analises = [
            "Analise 1", "Analise 2", "Analise 3", "Analise 4", "Analise 5",
            "Analise 6", "Analise 7", "Analise 8", "Analise 9", "Analise 10"
        ]
        self.equipamentos_por_analise = {
            "Analise 1": ["Espectrofotômetro UV-VIS", "Cromatógrafo Gasoso"],
            "Analise 2": ["Cromatógrafo Líquido", "Espectrômetro Infravermelho"],
            "Analise 3": ["Microscópio", "Balança Analítica"],
            "Analise 4": ["Espectrômetro de Massa"],
            "Analise 5": ["Agitador Magnético", "Espectrômetro Infravermelho"],
            "Analise 6": ["Cromatógrafo Líquido", "Espectrofotômetro UV-VIS"],
            "Analise 7": ["Espectrofotômetro UV-VIS", "Microscópio"],
            "Analise 8": ["Cromatógrafo Gasoso"],
            "Analise 9": ["Espectrômetro Infravermelho", "Balança Analítica"],
            "Analise 10": ["Espectrômetro de Massa", "Cromatógrafo Gasoso"]
        }
        self.max_tempo_por_equip = max_tempo_por_equip  # Tempo máximo disponível por equipamento na semana
        
        # Se um plano for passado, utiliza-o; caso contrário, gera um plano inicial aleatório
        if plano:
            self.plano = plano
        else:
            self.plano = self.gerar_plano_inicial()

    def gerar_plano_inicial(self):
        """
        Gera um plano aleatório, onde para cada análise é selecionado:
          - Um equipamento dentre os disponíveis
          - Um tempo de uso aleatório entre 1 e max_tempo_por_equip
        """
        plano = {}
        for analise in self.analises:
            equipamento = random.choice(self.equipamentos_por_analise[analise])
            tempo = random.randint(1, self.max_tempo_por_equip)
            plano[analise] = (equipamento, tempo)
        return plano

    def fitness(self):
        """
        Calcula a aptidão do plano. Penaliza se o tempo total de uso de um equipamento
        ultrapassar o limite máximo (max_tempo_por_equip).
        """
        penalidade = 0
        uso_equipamentos = {}
        for analise in self.analises:
            equipamento, tempo = self.plano[analise]
            uso_equipamentos[equipamento] = uso_equipamentos.get(equipamento, 0) + tempo

        for equipamento, uso in uso_equipamentos.items():
            if uso > self.max_tempo_por_equip:
                penalidade += (uso - self.max_tempo_por_equip)

        return 1 / (1 + penalidade)  # Quanto menor a penalidade, maior a fitness

    def mutacao(self):
        """
        Realiza mutação alterando aleatoriamente o equipamento e/ou tempo de uma análise.
        """
        novo_plano = self.plano.copy()
        analise_mutada = random.choice(self.analises)
        opcoes_equip = self.equipamentos_por_analise[analise_mutada]
        novo_equipamento = random.choice(opcoes_equip)
        novo_tempo = random.randint(1, self.max_tempo_por_equip)
        novo_plano[analise_mutada] = (novo_equipamento, novo_tempo)
        return PlanoUsoEquipamento(plano=novo_plano, max_tempo_por_equip=self.max_tempo_por_equip)

    def crossover(self, outro):
        """
        Combina os planos de dois indivíduos, escolhendo aleatoriamente o valor de cada análise
        de um dos pais.
        """
        novo_plano = {}
        for analise in self.analises:
            if random.random() < 0.5:
                novo_plano[analise] = self.plano[analise]
            else:
                novo_plano[analise] = outro.plano[analise]
        return PlanoUsoEquipamento(plano=novo_plano, max_tempo_por_equip=self.max_tempo_por_equip)

    def imprime(self):
        """
        Retorna uma string representando o plano de uso e sua aptidão.
        """
        s = "Plano de Uso dos Equipamentos:\n"
        for analise in self.analises:
            equipamento, tempo = self.plano[analise]
            s += f"{analise}: {equipamento} por {tempo} hora(s)\n"
        s += f"Fitness: {round(self.fitness(), 3)}"
        return s
