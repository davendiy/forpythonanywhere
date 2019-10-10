from source.T7_Graphs.P1.VertexForAlgorithms import INF
from source.T6_Trees.P2_BinaryTree.L7_PriorityQueue import PriorityQueue
from source.utils.benchmark import benchmark


@benchmark
def Dijkstra(graph, start, end):
    """ Реалізує алгоритм Дейкстри

    :param graph: Граф
    :param start: Стартова вершина
    :param end: Кінцева вершина
    :return: Кортеж, що містить список вершин - найкоротший шлях, що сполучає вершини start та end та його вагу
    """

    # Ініціалізуємо додаткову інформацію у графі для роботи алгоритму.
    for vertex in graph:
        vertex.set_distance(INF)  # Відстань для кожної вершини від стартової ставиться як нескінченність
        vertex.set_source(None)   # Вершина з якої прийшли по найкорошому шляху невизначена

    # Відстань у старотовій вершині (тобто від стартової вершини до себе) визначається як 0
    graph[start].set_distance(0)

    pq = PriorityQueue()                  # Створюємо пріоритетну чергу
    pq.insert(start, 0)                   # Додаємо у чергу початкову вершину з нульовим пріоритетом

    while not pq.empty():
        vertex_key = pq.extractMinimum()  # Беремо індекс вершини з черги з найнижчим пріоритетом
        vertex = graph[vertex_key]         # Беремо вершину за індексом

        for neighbor_key in vertex.neighbors():             # Для всіх сусідів (за ключами) поточної вершини
            neighbour = graph[neighbor_key]                 # Беремо вершину-сусіда за ключем
            newDist = vertex.distance() + vertex.weight(neighbor_key)  # Обчислюємо потенційну відстань у вершині-сусіді
            if newDist < neighbour.distance():              # Якщо потенційна відстань у вершині-сусіді менша за її поточне значення
                neighbour.set_distance(newDist)             # Змінюємо поточне значення відстані у вершині-сусіді обчисленим
                neighbour.set_source(vertex_key)            # Встановлюємо для сусідньої вершини ідентифікатор звідки ми прийшли у неї

                if neighbor_key in pq:                           # Якщо вершина сусід міститься у черзі
                    pq.decreasePriority(neighbor_key, newDist)   # перераховуємо її пріоритет в черзі
                else:
                    pq.insert(neighbor_key, newDist)             # або додаємо елемент до черги, якщо його там ще немає.

    return graph.construct_way(start, end)    # Повертаємо шлях та його вагу
