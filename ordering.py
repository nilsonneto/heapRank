__author__ = 'nilso'
from operator import itemgetter

def getFile(num=0):
    return open({
        0: "MPEG7ImagesList.txt",
        1: "AIRPreOpt.txt",
        2: "ASCPreOpt.txt",
        3: "BASPreOpt.txt",
        4: "CFDPreOpt.txt",
        5: "IDSCPreOpt.txt",
        6: "SSPreOpt.txt",
    }.get(num), 'r')


def toMatrix(f):
    matrix = []
    for line in iter(f.readline, ''):
        lineList = []
        for idx, val in enumerate(line.split()):
            lineList.append([float(val), idx])
        matrix.append(lineList)
    return matrix


def heapD(t1, t2, k):
    for each in t1[:k]:
        for each2 in t2[:k]:
            True
    return 0


def d(ranked, k):
    newRank = []
    for l in range(maxS):
        newRankLine = []
        for m in range(maxS):
            if l == m:
                result = 0
            else:
                result = heapD(ranked[l], ranked[m], k)
            newRankLine.append([result, m])
        newRank.append(newRankLine)
    return newRank


def efficiency(rList):
    recall = 0

    # pegar k primeiras imagens de rList[i],
    # e verificar quantos idx estão no range do i (for de 20 em vinte, e dentro um que varie de um em um, i*j)
    # com base no index, preciso de uma funcao para verificar a classe. mod??
    p = 20  # precision = intersect k images com as relevantes / k
    r = 40  # recall = intersect k images com as relevantes / 20

    #calcular precisão
    sumPrec = 0
    for index, line in enumerate(rList):
        classe = int(index / 20)
        intersect = 0
        for val in line[:p][1]:
            if int(val / 20) == classe:
                intersect += 1
        sumPrec += intersect / p
    precision = sumPrec / maxS

    #calcular recall
    sumRec = 0
    for index, line in enumerate(rList):
        classe = int(index / 20)
        intersect = 0
        for val in line[:r][1]:
            if int(val / 20) == classe:
                intersect += 1
        sumRec += intersect / p
    recall = sumRec / maxS

    return precision, recall


def maybeSort(line):
    # adapt to get not value, but key[0]
    return True


if __name__ == "__main__":
    maxS = 1400
    numReRanks = 1
    k = 20

    f = getFile(1)
    A = toMatrix(f)
    rankedList = []
    for i in range(maxS):
        lineOrdered = sorted(A[i],key=itemgetter(0))
        rankedList.append(lineOrdered)
    eff = efficiency(rankedList)
    A.clear()

    for t in range(numReRanks):
        newA = d(rankedList, k)
        newRankedList = []
        for i in range(maxS):
            newLineOrdered = sorted(newA[i],key=itemgetter(0))
            newRankedList.append(newLineOrdered)
        newEff = efficiency(newRankedList)
        newA.clear()

        if newEff[0] > eff[0] and newEff[1] > eff[1]:
            rankedList = list(newRankedList)
            eff = tuple(newEff)
        else:
            print("Ultimo ReRank diminuiu a eficiencia.\nT otimo encontrado: " + str(t))
            break
    print("\n\nThe End.")
