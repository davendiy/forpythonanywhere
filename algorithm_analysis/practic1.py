import numpy as np


cn_list = {}
cn_list[1] = cn_list[0] = 1

cn_list2 = {}
cn_list2[1] = cn_list2[0] = 1


def CN(n):
    if n not in cn_list:
        res = n + 1
        tmp_res = sum(CN(i-1) + CN(n-i) for i in range(1, n+1))
        cn_list[n] = res + tmp_res/n
    return cn_list[n]


def CN2(n):
    return 2*n*np.log(n) - (3 - 2*0.577)*n


def CN3(n):
    if n not in cn_list2:
        cn_list2[n] = ((n + 1)/n) * CN3(n-1) + 2
    return cn_list2[n]


def CN4(n):
    return 2*(n+1)*(np.)


print(CN2(1000), CN3(1000))
