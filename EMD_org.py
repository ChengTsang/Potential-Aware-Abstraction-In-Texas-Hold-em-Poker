'''
This code computes the Earth Mover's Distance
'''

import numpy as np
import scipy.optimize


# Constraints
def positivity(f):
    '''
    Constraint 1:
    Ensures flow moves from source to target
    '''
    return f


def fromSrc(f, wp, i, shape):
    """
    Constraint 2:
    Limits supply for source according to weight
    """
    fr = np.reshape(f, shape)
    f_sumColi = np.sum(fr[i, :])
    return wp[i] - f_sumColi


def toTgt(f, wq, j, shape):
    """
    Constraint 3:
    Limits demand for target according to weight
    """
    fr = np.reshape(f, shape)
    f_sumRowj = np.sum(fr[:, j])
    return wq[j] - f_sumRowj


def maximiseTotalFlow(f, wp, wq):
    """
    Constraint 4:
    Forces maximum supply to move from source to target
    """
    return f.sum() - np.minimum(wp.sum(), wq.sum())


# Objective function
def flow(f, D):
    """
    The objective function
    The flow represents the amount of goods to be moved
    from source to target
    """
    f = np.reshape(f, D.shape)
    return (f * D).sum()


# Distance
def groundDistance(x1, x2, norm=2):
    """
    L-norm distance
    Default norm = 2
    """
    return np.linalg.norm(x1 - x2, norm)


# Distance matrix
def getDistMatrix(s1, s2, norm=2):
    """
    Computes the distance matrix between the source
    and target distributions.
    The ground distance is using the L-norm (default L2 norm)
    """
    # rows = s1 feature length
    # cols = s2 feature length
    numFeats1 = s1.shape[0]
    numFeats2 = s2.shape[0]
    distMatrix = np.zeros((numFeats1, numFeats2))

    for i in range(0, numFeats1):
        for j in range(0, numFeats2):
            distMatrix[i, j] = groundDistance(s1[i], s2[j], norm)

    return distMatrix


# Flow matrix
def getFlowMatrix(P, Q, D):
    """
    Computes the flow matrix between P and Q
    """
    numFeats1 = P[0].shape[0]
    numFeats2 = Q[0].shape[0]
    shape = (numFeats1, numFeats2)

    # Constraints
    cons1 = [{'type': 'ineq', 'fun': positivity},
             {'type': 'eq', 'fun': maximiseTotalFlow, 'args': (P[1], Q[1],)}]

    cons2 = [{'type': 'ineq', 'fun': fromSrc, 'args': (P[1], i, shape,)} for i in range(numFeats1)]
    cons3 = [{'type': 'ineq', 'fun': toTgt, 'args': (Q[1], j, shape,)} for j in range(numFeats2)]

    cons = cons1 + cons2 + cons3

    # Solve for F (solve transportation problem)
    F_guess = np.zeros(D.shape)
    F = scipy.optimize.minimize(flow, F_guess, args=(D,), constraints=cons)
    F = np.reshape(F.x, (numFeats1, numFeats2))

    return F


# Normalised EMD
def EMD(F, D):
    """
    EMD formula, normalised by the flow
    """
    return (F * D).sum() / F.sum()


# Runs EMD program
def getEMD(P, Q, norm=2):
    """
    EMD computes the Earth Mover's Distance between
    the distributions P and Q

    P and Q are of shape (2,N)

    Where the first row are the set of N features
    The second row are the corresponding set of N weights

    The norm defines the L-norm for the ground distance
    Default is the Euclidean norm (norm = 2)
    """

    D = getDistMatrix(P[0], Q[0], norm)
    F = getFlowMatrix(P, Q, D)

    return EMD(F, D)


# Example 1
def getExampleSignatures():
    """
    returns signature1[features][weights], signature2[features][weights]
    """
    # features1 = np.array([[100, 40, 22],
    #                       [211, 20, 2],
    #                       [32, 190, 150],
    #                       [2, 100, 100]])
    features1 = np.array([[1],[2],[3],[4]])
    weights1 = np.array([0.25, 0.25, 0.25, 0.25])

    # features2 = np.array([[0, 0, 0],
    #                       [50, 100, 80],
    #                       [255, 255, 255]])
    features2 = np.array([[1],[2],[3]])
    weights2 = np.array([1/3.0, 1/3.0, 1/3.0])

    signature1 = (features1, weights1)
    signature2 = (features2, weights2)

    return signature1, signature2

def getEMD_1(p,q):
    #print(11111)
    l = len(p)
    m = len(q)
    features1 = []
    for i in range(l):
        features1.append([i])
    weights1 = np.array(p)
    #print(features1)
    #print(weights1)
    features1 = np.array(features1)
    features2 = []
    for i in range(m):
        features2.append([i])
    weights2 = np.array(q)
    features2 = np.array(features2)
    signature1 = (features1, weights1)
    signature2 = (features2, weights2)
    emd = getEMD(signature1, signature2)
    return emd



if __name__ == '__main__':
    print('EMD')

    # Setup
    P, Q = getExampleSignatures()

    # Get EMD
    emd = getEMD(P, Q)

    # Output result
    print('We got:', emd)
    print('C example got 160.54277')

    print('Success')