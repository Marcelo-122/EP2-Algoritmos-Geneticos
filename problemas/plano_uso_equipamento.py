import random
from collections import defaultdict

# Constantes
DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
HORARIOS = [f"{h:02d}:00" for h in range(8, 19)]  # Das 08:00 às 18:00
LIMITES_DIARIOS = {
    "Balança Analítica": 6,
    "Agitador Magnético": 4,
    "Cromatógrafo Líquido": 8,
    "Cromatógrafo Gasoso": 6,
    "Espectrofotômetro UV-VIS": 4,
    "Espectrômetro Infravermelho": 6,
    "Espectrômetro de Massa": 4,
    "Microscópio": 6,
}

# Restrições
EQUIPAMENTOS_POR_ANALISE = {
    "Análise 1": ["Espectrofotômetro UV-VIS", "Cromatógrafo Gasoso"],
    "Análise 2": ["Cromatógrafo Líquido", "Espectrômetro Infravermelho"],
    "Análise 3": ["Microscópio", "Balança Analítica"],
    "Análise 4": ["Espectrômetro de Massa"],
    "Análise 5": ["Agitador Magnético", "Espectrômetro Infravermelho"],
    "Análise 6": ["Cromatógrafo Líquido", "Espectrofotômetro UV-VIS"],
    "Análise 7": ["Espectrofotômetro UV-VIS", "Microscópio"],
    "Análise 8": ["Cromatógrafo Gasoso"],
    "Análise 9": ["Espectrômetro Infravermelho", "Balança Analítica"],
    "Análise 10": ["Espectrômetro de Massa", "Cromatógrafo Gasoso"],
}

# Classe do problema
class PlanoUsoEquipamento:
    def __init__(self, analises_alocadas=None):
        self.analises = list(EQUIPAMENTOS_POR_ANALISE.keys())

        if analises_alocadas:
            self.analises_alocadas = analises_alocadas
        else:
            self.analises_alocadas = self.gerar_alocacao_aleatoria()

    def gerar_alocacao_aleatoria(self):
        alocacoes = {}
        for analise in self.analises:
            dia = random.choice(DIAS)
            horario = random.choice(HORARIOS)
            alocacoes[analise] = {
                "dia": dia,
                "horario": horario,
                "equipamentos": EQUIPAMENTOS_POR_ANALISE[analise],
            }
        return alocacoes

    def fitness(self):
        penalidade = 0
        uso_equipamentos_dia = defaultdict(lambda: defaultdict(int))  # equipamento -> dia -> horas usadas
        uso_equipamentos_hora = defaultdict(set)  # (dia, horario) -> equipamentos em uso

        for analise, info in self.analises_alocadas.items():
            dia = info["dia"]
            horario = info["horario"]
            equipamentos = info["equipamentos"]

            for equipamento in equipamentos:
                # Verificar uso simultâneo do equipamento no mesmo horário
                if equipamento in uso_equipamentos_hora[(dia, horario)]:
                    penalidade += 200  # Equipamento já em uso no mesmo horário
                else:
                    uso_equipamentos_hora[(dia, horario)].add(equipamento)

                # Verificar limite diário
                uso_equipamentos_dia[equipamento][dia] += 1
                if uso_equipamentos_dia[equipamento][dia] > LIMITES_DIARIOS[equipamento]:
                    penalidade += 100  # Excedeu o limite diário

        return 1 / (1 + penalidade)

    def mutacao(self):
        novo_aloc = self.analises_alocadas.copy()
        analise_mutada = random.choice(self.analises)

        # Mudar dia e horário mantendo equipamentos sincronizados
        novo_aloc[analise_mutada] = {
            "dia": random.choice(DIAS),
            "horario": random.choice(HORARIOS),
            "equipamentos": EQUIPAMENTOS_POR_ANALISE[analise_mutada],
        }

        return PlanoUsoEquipamento(novo_aloc)

    def crossover(self, outro):
        novo_aloc = {}
        for analise in self.analises:
            if random.random() < 0.5:
                novo_aloc[analise] = self.analises_alocadas[analise]
            else:
                novo_aloc[analise] = outro.analises_alocadas[analise]
        return PlanoUsoEquipamento(novo_aloc)

    def imprime(self):
        for analise, info in self.analises_alocadas.items():
            print(f"{analise}:")
            print(f"  Dia: {info['dia']}")
            print(f"  Horário: {info['horario']}")
            print(f"  Equipamentos: {', '.join(info['equipamentos'])}")
            print("-" * 30)
