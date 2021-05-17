from datetime import datetime
from scipy.io import loadmat


def convert_to_time(hmm):
    return datetime(year=int(hmm[0]), month=int(hmm[1]), day=int(hmm[2]), hour=int(hmm[3]), minute=int(hmm[4]),
                    second=int(hmm[5]))


def loadMat(matfile):
    data = loadmat(matfile)
    from ntpath import basename, split
    basename("a/b/c")
    head, tail = split(matfile)
    m1 = tail
    filename = m1.split(".")[0]
    col = data[filename]
    col = col[0][0][0][0]
    size = col.shape[0]

    da = []

    for i in range(size):
        k = list(col[i][3][0].dtype.fields.keys())
        d1 = {}
        d2 = {}
        if str(col[i][0][0]) != 'impedance':
            for j in range(len(k)):
                t = col[i][3][0][0][j][0];
                l = []
                for m in range(len(t)):
                    l.append(t[m])
                d2[k[j]] = l
            d1['cycle'] = str(col[i][0][0])
            d1['temp'] = int(col[i][1][0])
            d1['time'] = str(convert_to_time(col[i][2][0]))
            d1['data'] = d2
            da.append(d1)

    return da
