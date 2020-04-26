"""Created on Sat Nov 24 11:43:57 2018 @author: Dasharath Adhikari"""

from __future__ import division
import numpy as np
import math

def kaiser_FIR(ripple, f_s, fp, fs):
    """
    ripple : float
     (The desired attenuation in the stopband and maximum ripple in
    the passband.For example delta_factor = 0.001. This should be a *positive* number.)
    For given ripple and the normalized transition width (fs-fp)/fN,
    fp = pass band frequency
    fs = stop band frequency
    f_s = sampling frequency
    fn = Nyquist frequency  = 0.5 * f_s
    returns the length for the Kaiser window's impulse response function.
    
    """    
    ripple = float(ripple)
    
    a = -20*math.log10(ripple)       # Attenuation in dB
    
    if a > 50:
        beta = 0.1102 * (a - 8.7)
    elif a > 21:
        beta = 0.5842 * (a-21) ** 0.4 + 0.07886 * (a-21)
    else:
        beta = 0.0

    TB = (fs - fp)/ (f_s)         # Normalized transition band      
    
    fc = (fp + fs) / (2* f_s)     # cut-off frequency and is always defined as the fraction of sampling frequency
    
    M = int(( a - 8 )/ ( 2.285* 2 *  np.pi * TB ))        # Order of the Kaiser window
    N = M + 1                                         # Length of the Kaiser window
    alpha = M/2
    
    n = np.arange(N)                                # create 1-D array of lenght N
    
    h = np.sinc(2 * fc * (n - ( alpha / 2 ) ) )                        # Sinc filter
    
    w = np.i0( beta * np.sqrt ( 1 - ( ( n/alpha ) - 1  ) ** 2 ) ) / np.i0 ( beta )      # Kaiser window function
    
       
    h = h*w                                   # Windowed sinc-filter 
    
    h = h/np.sum(h)
    
    return h                              # Returns an windnow-sinc filter of length N. 


def kaiser_beta(ripple):
    
    """
    delta_factor : float
        The desired attenuation in the stopband and maximum ripple in
        the passband.For example delta_factor = 0.001. This should be a *positive* number.
    """ 
    ripple = float(ripple)
    a = -20*math.log10(ripple)       # Attenuation in dB
    
    if a > 50:
        beta = 0.1102 * (a - 8.7)
    elif a > 21:
        beta = 0.5842 * (a-21) ** 0.4 + 0.07886 * (a-21)
    else:
        beta = 0.0
        
    return a, beta


def transition_band(fp, fs, f_S):
    
    """
    fp = pass band frequency
    fs = stop band frequency
    f_S = sampling frequency
    fn = Nyquist frequency  = 0.5 * f_S
    
    """
    TB = (fs - fp)/ (0.5 * f_S)
    
    return TB


def kaiser_window_length(ripple, fp, fs, f_s):
    
    """
    For given ripple and the normalized transition width (fs-fp)/fN,
    fp = pass band frequency
    fs = stop band frequency
    f_S = sampling frequency
    fn = Nyquist frequency  = 0.5 * f_s
    returns the length for the Kaiser window's impulse response function.
    
    """
    a = -20*math.log10(ripple)
    TB = (fs - fp)/ (0.5 * f_s)         # Normalized transition band
    
    
    
    M = int(np.ceil((a - 8)/(2.285*np.pi*TB)))        # Order of the Kaiser window
    N = M + 1                                         # Length of the Kaiser window
    
    return N 

# Three stages decimation factors
D1 = 4   # first stage
D2 = 2    # second stage
D3 = 2     # third stage

def three_stage_decimation(x):
    
    """
    The initial sampling rate is 256 Hz, where the oversampling factor is 16. That means I have to 
    downsample the signal to 16 Hz rate considering the bandwidth is 8 Hz (Nyquist theorem). I will
    be doing three stages of signal decimation (antialiasing filtering + decimation) with  
    downsampling factors of 4, 2, and 2 respectively. 
    """  
    # ----------------------------First Stage of Signal Decimation----------------------------------
    # ripple = 0.01
    f_s = 256   # sampling frequency (in Hz)
    # fp = 8     pass band (in Hz)
    # fs = 128   stop band (in Hz)
    window = kaiser_FIR(0.01, 256, 8, 128)
    x = np.convolve(x, window)
    x = x[::D1]
    f_s = f_s / D1     # new sampling frequency = 256 Hz/ 4 = 64 Hz
    
    # ---------------------------Second Stage of Signal Decimation ---------------------------------
    # ripple = 0.01
    # f_s = 64 Hz
    # fp =  8 Hz 
    # fs =  32 Hz 
    window = kaiser_FIR(0.01, 64, 8, 32)
    x = np.convolve(x, window)
    x = x[::D2]
    f_s = f_s/ D2  # new sampling frequency f_s = 64 Hz/ 2 = 32 Hz    
    
    #--------------------------Third Stage of Signal Decimation-------------------------------------
    # ripple = 0.01
    # f_s = 32 Hz
    # fp = 8 Hz
    # fs = 16 Hz
    window = kaiser_FIR(0.01, 32, 8, 16)
    x = np.convolve(x, window)
    # Now the sampling frequency reduces to 16 Hz meaning 8 Hz bandwidth
    x = x[::D3]
    return x