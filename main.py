from problemas.plano_uso_equipamento import PlanoUsoEquipamento
from geneticos.algoritmo_genetico_individuo import AlgoritmoGeneticoIndividuo

# Create an initial individual (random equipment usage plan)
individuo = PlanoUsoEquipamento()

# Run the genetic algorithm
genetico = AlgoritmoGeneticoIndividuo(individuo)
individuo_adaptado = genetico.rodar(max_geracoes=1000, imprimir_em_geracaoes=100)

# Print results
print("\nBest adapted solution found:")
print(f"Total generations: {genetico.qtd_geracoes()}")
print(f"Final error: {genetico.erro_final()}")
print(individuo_adaptado.imprime())

