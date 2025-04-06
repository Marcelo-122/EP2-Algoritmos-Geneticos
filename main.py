# main.py
from problemas.plano_uso_equipamento import PlanoUsoEquipamento
from geneticos.algoritmo_genetico_individuo import AlgoritmoGeneticoIndividuo

# Cria um indivíduo (plano de uso de equipamentos aleatório)
individuo = PlanoUsoEquipamento()

# Executa o algoritmo genético
gen = AlgoritmoGeneticoIndividuo(individuo)
individuo_adaptado = gen.rodar(max_geracoes=1000, imprimir_em_geracaoes=100)

# Imprime os resultados
print("\nMelhor solução adaptada:")
print(f"Total de gerações: {gen.qtd_geracoes()}")
print(f"Erro final: {gen.erro_final()}")
print(individuo_adaptado.imprime())



