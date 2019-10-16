from localfit import localfit
from velcal2 import velcalc2

def master_vel(XYT, MINt, MAXt, MINV, MAXV, winsize, wint):
    """
    Velocity computation script

    You will probably want to view only a subset of data at a time
    Suggestion: try only a beat at a time first

    Parameters
    ----------
    XYT : numpy matrix
        A matrix with rows consisting of the x,y,t locations of activations (mm,mm,ms)
    MINt :
        Start time of subset of data to analyze
    MAXt :
        End time of subset of data

    Returns
    -------
    X, Y, T :
        Locations of sites with good vel estimates
    vx, vy, v :
        Velocity components and magnitude
    fitxyt :
        Fitting parameters (for debug)
    """

    # Extract locations and times
    x = XYT[:, 1]
    y = XYT[:, 2]
    t = XYT[:, 3]

    # Parameters for local polynomial fitting (change these according to data)
    winx = winsize     # size of x-window (mm)
    winy = winsize     # size of y-window  (mm)
    # Size of time window  (s)?????????????????

    # Minimum number of points included in each fit
    how_many = 8

    # Polynomial fitting
    fitxyt = localfitt(x, y, t, winx, winy, wint, how_many, MINt, MAXt)

    # Parameters for velocity estimation (change these if necessary)
    resthresh = 0.5  # Maximum RMS error   % Drop outlier estimates +- 2 std deviations
    mspersamp = 1    # Scale velocity by time resolution - Drop estimates greater than this (mm/ms)
    xwin = winx      # x-window size for averaging velocity estimates
    ywin = winy      # y-window
    twin = wint      # time window
    how_many2 = 8    # minimum number of velocity estimates to include in avg.

    # Velocity estimation
    vx, vy, v, X, Y, _, good, _, _, _ = velcalc2(fitxyt,
                                                 resthresh,
                                                 mspersamp,
                                                 MINV,
                                                 MAXV,
                                                 xwin,
                                                 ywin,
                                                 twin,
                                                 how_many2)

    vx = vx[good]  # GOod estimates of x-velocity
    vy = vy[good]  # Good estimates of y-vel
    v = v[good]    # good estimates of vel. magnitude
    X = X[good]    # X-locations of good estimates
    Y = Y[good]    # Y-locations ...
    T = t[good]    # T-locations ...

    return X, Y, T, vx, vy, v, fitxyt
