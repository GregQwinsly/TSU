class Node:
    def __init__(self, data, indexloc=None):
        self.data = data
        self.index = indexloc
class Graph:
    @classmethod
    def create_from_nodes(self, nodes):
        return Graph(len(nodes), len(nodes), nodes)
    # установка матрицы смежности
    def __init__(self, row, col, nodes=None):
        self.adj_mat = [[0] * col for _ in range(row)]
        self.nodes = nodes 
        for i in range(len(self.nodes)):
            self.nodes[i].index = i
    # связывание node1 с node2 (ряд - источник, а столбец - назначение)
    def connect_dir(self, node1, node2, weight=1):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = weight
    # весовой аргумент для поддержки алгоритма Дейкстры
    def connect(self, node1, node2, weight=1):
        self.connect_dir(node1, node2, weight)
        self.connect_dir(node2, node1, weight)
    # возвращает матрицу кортежей (узел, вес)
    def connections_from(self, node):
        node = self.get_index_from_node(node)
        return [(self.nodes[col_num], self.adj_mat[node][col_num]) for col_num in range(len(self.adj_mat[node])) if
                self.adj_mat[node][col_num] != 0]
    # приводит матрицу к столбцу узлов только для ненулевых элементов
    def connections_to(self, node):
        node = self.get_index_from_node(node)
        column = [row[node] for row in self.adj_mat]
        return [(self.nodes[row_num], column[row_num]) for row_num in range(len(column)) if column[row_num] != 0]
    # вспомогательные функциии
    def print_adj_mat(self):
        for row in self.adj_mat:
            print(row)
    def node(self, index):
        return self.nodes[index]
    def remove_conn(self, node1, node2):
        self.remove_conn_dir(node1, node2)
        self.remove_conn_dir(node2, node1)
    # Убирает связь
    def remove_conn_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = 0
    def can_traverse_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        return self.adj_mat[node1][node2] != 0
    def has_conn(self, node1, node2):
        return self.can_traverse_dir(node1, node2) or self.can_traverse_dir(node2, node1)
    def add_node(self, node):
        self.nodes.append(node)
        node.index = len(self.nodes) - 1
        for row in self.adj_mat:
            row.append(0)
        self.adj_mat.append([0] * (len(self.adj_mat) + 1))
    # получаем вес, как путь от n1 к n2.
    def get_weight(self, n1, n2):
        node1, node2 = self.get_index_from_node(n1), self.get_index_from_node(n2)
        return self.adj_mat[node1][node2]
    def get_index_from_node(self, node):
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(node, int):
            return node
        else:
            return node.index

    # Реализация алгоритма Дейкстры
    def dijkstra(self, node):
        nodenum = self.get_index_from_node(node) # Получаем индекс узла
        dist = [None] * len(self.nodes) # отслеживание расстояние от одного до любого узла в массиве
        for i in range(len(dist)):
            dist[i] = [float("inf")]
            dist[i].append([self.nodes[nodenum]])
        dist[nodenum][0] = 0
        queue = [i for i in range(len(self.nodes))] # добавляем в очередь все узлы графа
        seen = set()
        while len(queue) > 0:
            # поиск узла, который не был рассмотрен и находится на кратчайшем расстоянии от начального узла
            min_dist = float("inf")
            min_node = None
            for n in queue:
                if dist[n][0] < min_dist and n not in seen:
                    min_dist = dist[n][0]
                    min_node = n
            queue.remove(min_node)
            seen.add(min_node) # добавляем мин. расстояние от узла
            connections = self.connections_from(min_node)
            # если полное расст. < текущее расст., то для каждой связи обновляем путь и расст. от начального узла в массиве
            for (node, weight) in connections:
                tot_dist = weight + min_dist
                if tot_dist < dist[node.index][0]:
                    dist[node.index][0] = tot_dist
                    dist[node.index][1] = list(dist[min_node][1])
                    dist[node.index][1].append(node)
        return dist

# задаем вершины графа
a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
e = Node("E")
f = Node("F")
g = Node("G")
h = Node("H")
w_graph = Graph.create_from_nodes([a, b, c, d, e, f, g, h]) # строим граф
# задаем ребра и расстояния
w_graph.connect(a, b, 5)
w_graph.connect(a, e, 10)
w_graph.connect(b, a, 5)
w_graph.connect(b, c, 11)
w_graph.connect(b, d, 12)
w_graph.connect(b, h, 15)
w_graph.connect(c, b, 11)
w_graph.connect(c, e, 8)
w_graph.connect(c, f, 9)
w_graph.connect(d, b, 12)
w_graph.connect(d, e, 9)
w_graph.connect(d, g, 13)
w_graph.connect(e, a, 10)
w_graph.connect(e, c, 8)
w_graph.connect(e, d, 9)
w_graph.connect(e, g, 7)
w_graph.connect(f, c, 9)
w_graph.connect(f, e, 13)
w_graph.connect(f, h, 10)
w_graph.connect(g, e, 7)
w_graph.connect(g, h, 11)
w_graph.connect(g, d, 13)
w_graph.connect(h, b, 15)
w_graph.connect(h, f, 10)
w_graph.connect(h, g, 11)
# вывод кратчайших путей (растояние - путь)
print("Кратчайшие пути от вершины А (расстояние,путь): ",[(weight, [n.data for n in node]) for (weight, node) in w_graph.dijkstra(a)])
