#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/6/20 17:38
# @Author  : wei
# @Site    : 
# @File    : trca_trial.py
# @Software: PyCharm
# @Description: 

import numpy as np

def trca(X, t1, Nexp):
    '''

    :param X: data matrix (N channels * T time points)
    :param t1: task onsets (vector)
    :param Nexp: task duration (sampling unit)
    :return:
    '''
    nb_channel = X.shape[0]
    nb_trial = t1.shape[0]

    S = np.zeros((nb_channel, nb_channel))

    # computation of correlation matrices:
    for i in range(nb_channel):
        for j in range(nb_channel):
            for k in range(nb_trial):
                for l in range(nb_trial):
                    if k != l:
                        tk =t1[k] # onset of k-th block
                        tl =t1[l] # onset of l-th block
                        xi = X[i,tk:tk+Nexp].reshape(1,Nexp)
                        xj = X[j,tl:tl+Nexp].reshape(1,Nexp)
                        S[i,j] += np.dot((xi-np.mean(xi, axis=1)),(xj-np.mean(xj,axis=1)).T)

    X_aver = X - np.tile(np.mean(X, axis=1).reshape(nb_channel,1),(1, X.shape[1]))
    Q = np.dot(X_aver, X_aver.T)
    D, V = np.linalg.eig(np.dot(np.linalg.inv(Q), S))
    Y = np.dot(V.T, X_aver)

    return Y, V, D, S

data = np.random.randint(1,34,(10,600))
t = np.array([0,200,400])
Nb = 200
Y, V, D, S = trca(data, t, Nb)
print('done')