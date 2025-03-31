from problemas.tiro import Tiro
from geneticos.algoritmo_genetico_individuo import AlgoritmoGeneticoIndividuo

individuo = Tiro()
genetico = AlgoritmoGeneticoIndividuo(individuo)

individuo_adaptado = genetico.rodar(max_geracoes=1000, imprimir_em_geracaoes=100)

print("\nPrimeiro mais adaptado:")
print(f"Quantidade de gerações: {genetico.qtd_geracoes()}")
print(f"Erro: {genetico.erro_final()}")
print(individuo_adaptado.imprime())

# populacao = PopulacaoCanhoes(Tiro, tamanho_populacao=10)
# genetico = AlgoritmoGeneticoPopulacao(populacao)

# individuo_adaptado = genetico.rodar(max_geracoes = 1000, imprimir_em_geracaoes=100)

# print("\nPrimeiro mais adaptado:")
# print(f"Quantidade de gerações: {genetico.qtd_geracoes()}")
# print(f"Erro: {genetico.erro_final()}")
# print(individuo_adaptado.imprime())

