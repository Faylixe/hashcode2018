#!/usr/bin/env python
# coding: utf8

""" """
import numpy as np
from sys import stdout

from utils.dataset import load_dataset

def updateTuple(value, tuple):
    if value == 'T':
        tuple[0] += 1
    elif value == 'M':
        tuple[1] += 1

    return tuple




def check_rect(rect, pizza, l, h):


def main():
    r, c, l, h, piz = load_dataset()
    pizza = np.matrix(piz)

    xOff=0
    yOff=0
    rect = [0, 0, 1, 1]
    mat = np.ones((r, c))
    for i in range(r):
        for j in range(c):
            if mat[i, j] == 0:
                break

            check_rect(rect, pizza)









    #         mat[i, j] = (tuple[0], tuple[1], 1)

    # print(mat)



if __name__ == '__main__':
    main()
