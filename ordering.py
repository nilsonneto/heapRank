from math import log2, ceil
from operator import itemgetter


__author__ = 'nilso'


def printf(toprint):
    f = open("results.txt", "a+")
    f.write(str(toprint))
    f.write("\n\n")
    f.close()


def getfile(num=0):
    return open({
        0: "MPEG7ImagesList.txt",
        1: "AIRPreOpt.txt",
        2: "ASCPreOpt.txt",
        3: "BASPreOpt.txt",
        4: "CFDPreOpt.txt",
        5: "IDSCPreOpt.txt",
        6: "SSPreOpt.txt",
        7: "test.txt",
    }.get(num), 'r')


def tomatrix(file):
    matrix = []
    for line in iter(file.readline, ''):
        linelist = []
        for idx, val in enumerate(line.split()):
            linelist.append([float(val), idx])
        matrix.append(linelist)
    return matrix


def heapd(t1, t2, maxnum):
    heap1 = t1[1:maxnum]
    heap2 = t2[1:maxnum]

    maxh = ceil(log2(len(heap1)))
    heights = list(range(1, maxh+1, 2))
    peso = list(reversed(range(1, maxh+1)))
    sumtotal = 0
    sumweight = 0
    lastindex = 0

    for h in heights:
        numelem = pow(2, h)
        if h + 1 <= maxh:
            numelem += pow(2, h+1)
        numelem += lastindex
        intersect = 0

        # print(h, lastindex, numelem, intersect, sumtotal)

        if (numelem + lastindex) > len(heap1):
            numelem = len(heap1) - lastindex

        # calcular # of intersection
        for ele1 in heap1[lastindex:numelem]:
            for ele2 in heap2[lastindex:numelem]:
                if ele1[1] == ele2[1]:
                    intersect += 1
                    break

        lastindex = int(numelem)
        sumtotal += (intersect * peso[h-1])
        sumweight += peso[h-1]

        # print(h, lastindex, numelem, intersect, sumtotal)

    return sumtotal / sumweight


def d(ranked, maxnum):
    newrank = []
    for l in range(maxS):
        newrankline = []
        for m in range(maxS):
            if l == m:
                result = 0
            else:
                result = 1 / (1 + heapd(ranked[l], ranked[m], maxnum))
            newrankline.append([result, ranked[m][0][1]])
        newrank.append(newrankline)
    return newrank


def efficiency(rlist):
    # pegar k primeiras imagens de rList[i],
    # e verificar quantos idx estao no range do i (for de 20 em vinte, e dentro um que varie de um em um, i*j)
    # com base no index, preciso de uma funcao para verificar a classe. mod??
    p = 20  # precision = intersect k images com as relevantes / k
    r = 40  # recall = intersect k images com as relevantes / 20

    # calcular precisao
    sumprec = 0
    for index, line in enumerate(rlist):
        classe = int(index / 20)
        intersect = 0
        for val in line[:p][1]:
            if int(val / 20) == classe:
                intersect += 1
        sumprec += intersect / p
    precision = sumprec / maxS

    # calcular recall
    sumrec = 0
    for index, line in enumerate(rlist):
        classe = int(index / 20)
        intersect = 0
        for val in line[:r][1]:
            if int(val / 20) == classe:
                intersect += 1
        sumrec += intersect / p
    recall = sumrec / maxS

    return precision, recall


if __name__ == "__main__":
    maxS = 1400
    numReRanks = 6
    k = 20

    for fileNum in range(1, 7, 1):
        fil = getfile(fileNum)
        printf("Arquivo" + str(fil.name))
        A = tomatrix(fil)

        rankedList = []
        for i in range(maxS):
            lineOrdered = sorted(A[i], key=itemgetter(0))
            rankedList.append(lineOrdered)
        eff = efficiency(rankedList)
        printf("First efficiency:")
        printf(eff)
        A.clear()

        for t in range(numReRanks):
            newA = d(rankedList, k)
            newRankedList = []
            for i in range(maxS):
                newLineOrdered = sorted(newA[i], key=itemgetter(0))
                newRankedList.append(newLineOrdered)
            newEff = efficiency(newRankedList)
            printf("Tentativa " + str(fileNum))
            printf(newEff)
            newA.clear()

            if newEff[0] > eff[0] and newEff[1] > eff[1]:
                rankedList = list(newRankedList)
                eff = tuple(newEff)
            else:
                printf("Ultimo ReRank diminuiu a eficiencia.\nT otimo encontrado: " + str(t))
                break

        printf("Last efficiency:")
        printf(eff)

    print("\n\nThe End.")
