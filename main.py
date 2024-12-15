class Graph:
    def __init__(self, matrix):
        """
        Инициализация графа с матрицей смежности.
        matrix: Двумерный список (матрица смежности), где matrix[u][v] — пропускная способность ребра u -> v.
        """
        self.vertices = len(matrix)  # Количество вершин (размер матрицы)
        self.graph = matrix  # Матрица смежности

    def get_graph(self):
        """
        Возвращает матрицу смежности графа.
        """
        return self.graph

    def print_graph(self):
        """
        Красивый вывод матрицы смежности графа.
        """
        # Заголовки столбцов (вершины)
        print("   ", end="")
        for i in range(self.vertices):
            print(f"{chr(65 + i):>4}", end="")  # Преобразуем индексы в A, B, C, ...
        print("\n" + "   " + "-" * (self.vertices * 4))

        # Строки матрицы с подписями вершин
        for i in range(self.vertices):
            print(f"{chr(65 + i):<2} |", end="")  # Преобразуем индексы в A, B, C, ...
            for j in range(self.vertices):
                print(f"{self.graph[i][j]:>4}", end="")
            print()
        print()


def bfs(graph, source, sink, parent):
    """
    Поиск в ширину (BFS) для нахождения увеличивающего пути.
    """
    visited = [False] * len(graph)  # Массив посещённых вершин
    queue = [source]  # Очередь для BFS
    visited[source] = True  # Исток отмечаем как посещённый

    while queue:
        u = queue.pop(0)

        for idx, val in enumerate(graph[u]):
            # Если вершина ещё не посещена и остаточная пропускная способность > 0
            if not visited[idx] and val > 0:
                queue.append(idx)
                visited[idx] = True
                parent[idx] = u

                if idx == sink:  # Если дошли до стока, возвращаем True
                    return True
    return False  # Увеличивающий путь не найден


def ford_fulkerson(graph_obj, source, sink):
    """
    Реализация алгоритма Форда-Фалкерсона для нахождения максимального потока.
    """
    graph = graph_obj.get_graph()  # Получаем матрицу смежности
    parent = [-1] * len(graph)  # Массив для хранения пути
    max_flow = 0  # Инициируем максимальный поток

    # Пока есть увеличивающий путь из истока в сток
    while bfs(graph, source, sink, parent):
        # Находим минимальную пропускную способность вдоль пути
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        # Обновляем остаточные пропускные способности рёбер и обратных рёбер
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow  # Уменьшаем пропускную способность
            graph[v][u] += path_flow  # Увеличиваем обратный поток
            v = parent[v]

        # Увеличиваем общий поток
        max_flow += path_flow

    # По завершении работы алгоритма возвращаем максимальный поток и остаточную сеть
    return max_flow, graph_obj


# Задаём матрицу смежности для графа
matrix = [
    [0, 7, 4, 0, 0, 0],  # A -> (B: 7, C: 4)
    [0, 0, 4, 0, 2, 0],  # B -> (C: 4, E: 2)
    [0, 0, 0, 4, 8, 0],  # C -> (D: 4, E: 8)
    [0, 0, 0, 0, 0, 12], # D -> (F: 12)
    [0, 0, 0, 4, 0, 5],  # E -> (D: 4, F: 5)
    [0, 0, 0, 0, 0, 0]   # F (нет исходящих рёбер)
]

# Создаём граф на основе матрицы
g = Graph(matrix)

# Печать исходной матрицы
print("Исходная матрица смежности графа:")
g.print_graph()

# Запуск алгоритма Форда-Фалкерсона
source = 0  # Исток (A)
sink = 5    # Сток (F)
max_flow, final_graph = ford_fulkerson(g, source, sink)

# Вывод результатов
print(f"Максимальный поток: {max_flow}")
print("Остаточная сеть после выполнения алгоритма:")
final_graph.print_graph()