import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def calcular_distancia(percurso, grafo):
    distancia_total = 0

    for i in range(len(percurso) - 1):
        origem = percurso[i]
        destino = percurso[i + 1]
        distancia_total += grafo[origem][destino]['weight']

    distancia_total += grafo[percurso[-1]][percurso[0]]['weight']

    return distancia_total

def colonia_de_formigas(grafo, num_formigas, max_iteracoes, alpha, beta, rho):
    num_cidades = len(grafo)
    feromonio = np.ones((num_cidades, num_cidades))
    melhor_percurso = []
    melhor_distancia = float('inf')

    for iteracao in range(max_iteracoes):
        feromonio_iteracao = np.zeros((num_cidades, num_cidades))

        for formiga in range(num_formigas):
            cidade_atual = random.randint(0, num_cidades - 1)
            percurso = [cidade_atual]
            cidades_nao_visitadas = list(range(num_cidades))
            cidades_nao_visitadas.remove(cidade_atual)

            while cidades_nao_visitadas:
                probabilidades = [
                    ((feromonio[cidade_atual][j] ** alpha) * ((1.0 / grafo[cidade_atual][j]['weight']) ** beta))
                    if grafo.has_edge(cidade_atual, j) else 0.0001
                    for j in cidades_nao_visitadas
                ]

                soma_probabilidades = sum(probabilidades)
                probabilidades = [prob / soma_probabilidades if soma_probabilidades != 0 else 1.0 / len(probabilidades)
                                  for prob in probabilidades]

                cidade_escolhida = np.random.choice(cidades_nao_visitadas, p=probabilidades)
                percurso.append(cidade_escolhida)
                cidades_nao_visitadas.remove(cidade_escolhida)
                cidade_atual = cidade_escolhida

            distancia_percurso = calcular_distancia(percurso, grafo)

            if distancia_percurso < melhor_distancia:
                melhor_distancia = distancia_percurso
                melhor_percurso = percurso

            for i in range(num_cidades - 1):
                feromonio_iteracao[percurso[i]][percurso[i + 1]] += 1.0
            feromonio_iteracao[percurso[-1]][percurso[0]] += 1.0

        feromonio *= (1 - rho)
        feromonio += feromonio_iteracao / melhor_distancia

    return melhor_percurso, melhor_distancia

def ler_distancias(nome_arquivo):
    G = nx.Graph()  
    num_cidades = 0

    with open(nome_arquivo, 'r') as file:
        linhas = file.readlines()
        arestas = [[int(valor) for valor in linha.split()] for linha in linhas]
        
        for origem, destino, peso in arestas:
            G.add_edge(origem, destino, weight=peso)  
            num_cidades = max(num_cidades, origem, destino) + 1

    return G, num_cidades

nome_arquivo = 'distancias.txt'  
grafo, num_cidades = ler_distancias(nome_arquivo)

num_formigas = num_cidades
max_iteracoes = 100
alpha = 1.0
beta = 5.0
rho = 0.5

melhor_percurso, melhor_distancia = colonia_de_formigas(grafo, num_formigas, max_iteracoes, alpha, beta, rho)
primeiro_elemento = melhor_percurso[0]
melhor_percurso.append(primeiro_elemento)

arestas_melhor_percurso = [(melhor_percurso[i], melhor_percurso[i + 1]) for i in range(len(melhor_percurso) - 1)]
arestas_melhor_percurso.append((melhor_percurso[-1], melhor_percurso[0]))

print("Melhor percurso encontrado:", melhor_percurso)
print("Melhor distância encontrada:", melhor_distancia)

pos = nx.spring_layout(grafo)
nx.draw(grafo, pos, with_labels=True, node_size=500, node_color='skyblue')
nx.draw_networkx_edges(grafo, pos, edgelist=arestas_melhor_percurso, edge_color='red', width=3)
plt.show()
