import numpy as np
import time


def benchmark(func):

    def _benchmark(*args, **kwargs):
        t = time.time()
        print("function {} started".format(func.__name__))
        res = func(*args, **kwargs)
        print("function {} ended, time elapsed: {}".format(func.__name__,
                                                           time.time() - t))
        return res

    return _benchmark


@benchmark
def quick_sort(array, key=lambda a: a):
    """ Реалізує алгоритм швидкого сортування

    :param array: Масив (список однотипових елементів)
    :param key: функція, по якій виконується порівняння
    :return: None
    """
    quick_sort_helper(array, 0, len(array) - 1, key)


def quick_sort_helper(array, first, last, key=lambda a: a):
    """ Допоміжний рекурсивний метод,
        що реалізує сортування фрагменту списку обмеженого заданими позиціями

    :param array: Масив (список однотипових елементів)
    :param first: Ліва межа списку
    :param last: Права межа списку
    :param key: функція, по якій виконується порівняння
    :return: None
    """
    if first < last:
        # Визанчення точки розбиття спику
        splitpoint = partition(array, first, last, key)
        # Рекурсивний виклик функції швидкого сортування
        # для отриманих частин списку
        quick_sort_helper(array, first, splitpoint - 1, key)
        quick_sort_helper(array, splitpoint + 1, last, key)


def partition(array, first, last, key=lambda a: a):
    """ Визначає точку розбиття списку

    :param array: Масив (список однотипових елементів)
    :param first: Ліва межа списку
    :param last: Права межа списку
    :param key: функція, по якій виконується порівняння
    :return: Позицію розбиття списку
    """
    pivot = array[first]
    left = first + 1
    right = last
    done = False
    while not done:
        # Рухаємося зліва на право,
        # поки не знайдемо елемент, що більший за опорний
        while left <= right and key(array[left]) <= key(pivot):
            left += 1

        # Рухаємося справа на ліво,
        # поки не знайдемо елемент, що менший за опорний
        while key(array[right]) >= key(pivot) and right >= left:
            right -= 1

        # Якщо індекс правого елемента менший за індекс лівого
        if right < left:
            # то розбиття списку завершено
            done = True
        else:
            # міняємо знайдений елементи місцями
            array[left], array[right] = array[right], array[left]

    # ставимо опорний елемент на його позицію
    array[first], array[right] = array[right], array[first]
    return right


def generate_random_array(n):
    return [np.random.randint(n) for _ in range(n)]


if __name__ == '__main__':
    for n in [10, 100, 1000, 10000, 100000]:
        print("\nn = {}".format(n))
        quick_sort(generate_random_array(n))
