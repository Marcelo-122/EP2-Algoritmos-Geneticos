import random
from collections import defaultdict

# Constantes
DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
HORARIOS = [f"{h:02d}:00" for h in range(8, 18)]  # Das 08:00 às 17:00
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
        uso_equipamentos = defaultdict(lambda: defaultdict(int))
        conflitos_temporais = defaultdict(set)

        # Verificar restrições
        for analise, info in self.analises_alocadas.items():
            dia = info["dia"]
            horario = info["horario"]

            # Verificar equipamentos simultâneos
            for equipamento in info["equipamentos"]:
                # Contagem de uso diário
                uso_equip_dia = uso_equipamentos[equipamento][dia]
                if uso_equip_dia >= LIMITES_DIARIOS[equipamento]:
                    penalidade += 100  # Penalidade por hora excedida
                else:
                    uso_equipamentos[equipamento][dia] += 1

                # Verificar conflitos de horário
                chave = (equipamento, dia, horario)
                if chave in conflitos_temporais:
                    penalidade += 200  # Conflito no mesmo equipamento/horário
                conflitos_temporais[chave].add(analise)

        # Verificar sincronização de equipamentos para a mesma análise
        for analise, info in self.analises_alocadas.items():
            if len(info["equipamentos"]) > 1:
                # Todos equipamentos devem estar no mesmo dia/horário
                equipamentos = info["equipamentos"]
                primeira_chave = (equipamentos[0], info["dia"], info["horario"])
                for equip in equipamentos[1:]:
                    chave = (equip, info["dia"], info["horario"])
                    if chave not in conflitos_temporais:
                        penalidade += 300  # Equipamentos não sincronizados

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

    def mostrar_plano(self):
        for analise, info in self.analises_alocadas.items():
            print(f"{analise}:")
            print(f"  Dia: {info['dia']}")
            print(f"  Horário: {info['horario']}")
            print(f"  Equipamentos: {', '.join(info['equipamentos'])}")
            print("-" * 30)


class Populacao:
    def __init__(self, tamanho):
        self.individuos = [PlanoUsoEquipamento() for _ in range(tamanho)]

    def evolui(self, geracoes, taxa_mutacao=0.1):
        for _ in range(geracoes):
            # Seleção por torneio
            pais = []
            for _ in range(2):
                competidores = random.sample(self.individuos, 3)
                pais.append(max(competidores, key=lambda x: x.fitness()))

            # Crossover
            filho = pais[0].crossover(pais[1])

            # Mutação
            if random.random() < taxa_mutacao:
                filho = filho.mutacao()

            # Substituir o pior indivíduo
            self.individuos.sort(key=lambda x: x.fitness())
            self.individuos[0] = filho

        return max(self.individuos, key=lambda x: x.fitness())


# Exemplo de uso
if __name__ == "__main__":
    pop = Populacao(tamanho=50)
    melhor = pop.evolui(geracoes=100)
    print("\nMelhor plano encontrado:")
    melhor.mostrar_plano()
    print(f"Fitness: {melhor.fitness():.4f}")
