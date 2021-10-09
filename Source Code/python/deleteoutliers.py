"""
"""

import np

def deleteoutliers(a, alpha, rep=False):
    """
    Parameters
    ----------
    a :
    alpha :
    rep : boolean, optional

    Returns
    -------
    b :
    idx :
    outliers :

    For input vector A, returns a vector B with outliers (at the significance
    level alpha) removed. Also, optional output argument idx returns the
    indices in A of outlier values. Optional output argument outliers returns
    the outlying values in A.

    ALPHA is the significance level for determination of outliers. If not
    provided, alpha defaults to 0.05.

    REP is an optional argument that forces the replacement of removed
    elements with NaNs to presereve the length of a. (Thanks for the
    suggestion, Urs.)

    This is an iterative implementation of the Grubbs Test that tests one
    value at a time. In any given iteration, the tested value is either the
    highest value, or the lowest, and is the value that is furthest
    from the sample mean. Infinite elements are discarded if rep is 0, or
    replaced with NaNs if rep is 1 (thanks again, Urs).

    Appropriate application of the test requires that data can be reasonably
    approximated by a normal distribution. For reference, see:
    1) "Procedures for Detecting Outlying Observations in Samples," by F.E.
       Grubbs; Technometrics, 11-1:1--21; Feb., 1969, and
    2) _Outliers in Statistical Data_, by V. Barnett and
       T. Lewis; Wiley Series in Probability and Mathematical Statistics;
       John Wiley & Sons; Chichester, 1994.
    A good online discussion of the test is also given in NIST's Engineering
    Statistics Handbook:
    http://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm

    ex:
    [B,idx,outliers] = deleteoutliers([1.1 1.3 0.9 1.2 -6.4 1.2 0.94 4.2 1.3 1.0 6.8 1.3 1.2], 0.05)
       returns:
       B = 1.1000    1.3000    0.9000    1.2000    1.2000    0.9400    1.3000    1.0000    1.3000    1.2000
       idx =  5     8    11
       outliers = -6.4000    4.2000    6.8000

    ex:
    B = deleteoutliers([1.1 1.3 0.9 1.2 -6.4 1.2 0.94 4.2 1.3 1.0 6.8 1.3 1.2
    Inf 1.2 -Inf 1.1], 0.05, 1)
    returns:
    B = 1.1000  1.3000  0.9000  1.2000  NaN  1.2000  0.9400  NaN  1.3000  1.0000  NaN  1.3000  1.2000  NaN  1.2000  NaN  1.1000
    Written by Brett Shoelson, Ph.D.
    shoelson@helix.nih.gov
    9/10/03
    Modified 9/23/03 to address suggestions by Urs Schwartz.
    Modified 10/08/03 to avoid errors caused by duplicate "maxvals."
       (Thanks to Valeri Makarov for modification suggestion.)
    """

    if alpha == None:
        alpha = 0.05

    b = a;
    b[np.isinf(a)] = NaN;

    # Delete outliers
    outlier = 1
    while outlier:
        tmp = b[np.logical_not(np.isnan(b))]
        meanval = np.mean(tmp)

        maxval = tmp(find(abs(tmp-mean(tmp))==max(abs(tmp-mean(tmp)))))
        maxval = maxval(1);
        sdval = std(tmp);
        tn = abs((maxval-meanval)/sdval);
        critval = zcritical(alpha,length(tmp));
        outlier = tn > critval;
        if outlier:
            tmp = find(a == maxval);
            b(tmp) = NaN;


    if nargout >= 2:
        idx = find(isnan(b)) #TODO
    if nargout > 2:
        outliers = a[idx]
    if not rep:
        b = b[not isnan(b)] #TODO

    return b, idx, outliers

def zcritical(alpha, n):
    """
    Computes the critical z value for rejecting outliers (GRUBBS TEST).

    Parameters
    ----------
    alpha :
    n :

    Returns
    -------
    zcrit :

    """

    tcrit = tinv(alpha / (2 * n), n-2)
    zcrit = (n - 1) / sqrt(n) * (sqrt(tcrit^2 / (n - 2 + tcrit^2)))
    return zcrit