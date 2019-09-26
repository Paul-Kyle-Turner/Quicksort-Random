import numpy as np
import timeit
import pandas as pd
import matplotlib.pyplot as plt
import random
import statistics
import math


def quick_sort(partition_func, ar, p, r):
    if p < r:
        q = partition_func(ar, p, r)
        quick_sort(partition_func, ar, p, q-1)
        quick_sort(partition_func, ar, q+1, r)


def random_partition(ar, p, r):
    i = random.randint(p, r)
    print(i)
    ar[r], ar[i] = ar[i], ar[r]
    return partition(ar, p, r)


def partition(ar, p, r):
    i = (p - 1)
    pivot = ar[r]
    for j in range(p, r):
        if ar[j] <= pivot:
            i = i + 1
            ar[i], ar[j] = ar[j], ar[i]
    ar[(i + 1)], ar[r] = ar[r], ar[(i + 1)]
    return i + 1


def create_random_array(number_of_elements):
    return np.random.randint(-10000, 10000, number_of_elements)


def quick_sort_time(start, stop, by, partition_function='partition', file='non_random_times.txt', two_to_the=False):
    SETUP_CODE = '''
from __main__ import create_random_array
from __main__ import partition
from __main__ import random_partition
from __main__ import quick_sort
import random
import numpy as np'''
    TEST_CODE = '''
a = create_random_array(a_size)
quick_sort(partition, a, 0, len(a) - 1)'''
    times = list()
    if two_to_the:
        for i in range(start, stop):
            q = int(math.pow(2, i))
            print(i)
            print(q)
            time = timeit.repeat(setup=SETUP_CODE,
                                 stmt=TEST_CODE.replace('a_size', str(q)).replace('partition', partition_function),
                                 number=10000)
            print(time)
            a_time = statistics.mean(time)
            print(a_time)
            times.append(a_time)
    else:
        for i in range(start, stop, by):
            print(i)
            time = timeit.repeat(setup=SETUP_CODE,
                                 stmt=TEST_CODE.replace('a_size', str(i)).replace('partition', partition_function),
                                 number=10000)
            print(time)
            a_time = statistics.mean(time)
            print(a_time)
            times.append(a_time)
    with open(file, "w+") as file:
        for t in times:
            file.write('%s\n' % t)
    return times


if __name__ == '__main__':
    starts = 1
    stops = 11
    bys = 1
    quick = quick_sort_time(starts, stops, bys, two_to_the=True)
    quick_random = quick_sort_time(starts, stops, bys,
                                   partition_function='random_partition', file='random_quick.txt', two_to_the=True)
    data = pd.DataFrame({'x': range(starts, stops, bys), 'non_random': quick, 'random': quick_random})
    plt.plot('x', 'non_random', data=data)
    plt.plot('x', 'random', data=data)
    plt.legend()
    plt.show()

