import pandas as pd
import numpy as np
from scipy.stats import norm

def blackScholes(s,x,t,vol,r):
    d1=(np.log(s/float(x))+(r+0.5*(vol**2))*t)/(np.sqrt(t)*(vol))
    d2=d1-vol*np.sqrt(t)
    ret=s*norm.cdf(d1)-x*(np.exp(-r*t)*norm.cdf(d2))
    return ret


price=blackScholes(2,3,90,3,1)
print(price)

