import networkx as nx
# Заданные значения количества вершин и вероятности появления ребра
num_nodes = 7
prob = 0.7
# Генерация графа
Graph = nx.erdos_renyi_graph(num_nodes, prob)
# Вычисление средней степени вершины
total_degree = 0
for node in Graph.nodes():
    total_degree = total_degree+Graph.degree(node)
    average_degree = float(total_degree) / len(Graph.nodes())
# Ожидаемая средняя степень вершины по формуле модели Эрдёша-Реньи
expected_degree = prob * (num_nodes - 1)
delta=round(expected_degree-average_degree, 3)
# Вывод результатов
print("Средняя степень вершины в сгенерированном графе:", round(average_degree, 3))
print("Ожидаемая средняя степень вершины по формуле модели Эрдёша-Реньи:", round(expected_degree, 3))
print("Разница значенний степени:", abs(delta))