'''Python translation of R function wgt.himedian(x, weights)
x: double array containing the observations
weights: array of (int/double) weights of the observations.
taken from: https://github.com/cran/robustbase/blob/master/src/wgt_himed_templ.h
R function wgt.himedian(x, weights) uses C based function placed here : wgt_himed_templ.h'''

import numpy as np
def himedian(x, weights):
    n = len(x)
    trial = 0
    w_tot = np.sum(weights)
    wrest = 0
    x_cand = [None] * n
    w_cand = [None] * n
    while(True):
        x_srt = x.copy()
        n2 = int(n/2)
        x_srt_low = np.array_split(x_srt, 2)[0]
        x_srt_high = np.array_split(x_srt, 2)[1]
        x_srt = np.concatenate((x_srt_low,np.sort(x_srt_high)))
        trial = x_srt[n2]
        wleft = np.sum(x[np.where(x > trial)])
        wmid = np.sum(x[np.where(x == trial)])
        wright = np.sum(x[np.where(x < trial)])
        kcand = 0
        if(2 * (wrest + wleft) > w_tot):
            for i in range(n):
                if(x[i] < trial):
                    x_cand[kcand] = x[i]
                    w_cand[kcand] = weights[i]
                    kcand += 1
        elif (2 * (wleft + wmid + wright) <= w_tot):
            for i in range(n):
                if(x[i] > trial):
                    x_cand[kcand] = x[i]
                    w_cand[kcand] = weights[i]
                    kcand += 1
            wrest = wrest + wleft + wmid
        else:
            return trial
        n = kcand
        for i in range(n):
            x[i] = x_cand[i]
            weights[i] = w_cand[i]

if __name__ == "__main__":
    x = np.array([1,4,5,46,7,58,9])
    weights = np.array([1, 4, 5, 46, 7, 58, 9])
    himed = himedian(x, weights)
    print("Himed is",himed)
