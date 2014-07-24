''' Calculates the inputs for an autocorrelogram and/or normal probability plot
    I.e. tests for autocorrelation and normality of residuals for OLS regression '''

from sklearn import linear_model
from scipy import stats
import numpy as np
import statsmodels.tsa.stattools as ts


### Test for OLS assumptions
class OLSAssumptions():
    
    def __init__(self, Y_train, Y_predicted):
        self.residuals = (Y_predicted - Y_train).flatten()
    
    ### Test for autocorrelation
    def autocorrel(self, lag=1):
        
        top_5 = stats.norm.ppf(0.975) / (len(self.residuals)**0.5)
        top_1 = stats.norm.ppf(0.995) / (len(self.residuals)**0.5)
        bottom_5 = stats.norm.ppf(0.025) / (len(self.residuals)**0.5)
        bottom_1 = stats.norm.ppf(0.005) / (len(self.residuals)**0.5)
        corrs = np.array([np.corrcoef(self.residuals[i:], self.residuals[:-i])[0, 1] for i in range(1, lag+1)])
        
        return (corrs, top_1, top_5, bottom_5, bottom_1) # inputs for an autocorrelogram plot
    
    ### Test for normality 
    def normaltest(self):
        r_percent = np.array([stats.percentileofscore(self.residuals, i) if i != np.max(self.residuals) else 99.9 for i in self.residuals]) # percentile of each obs
        r_znorm = stats.norm.ppf(r_percent/100) # Theoretical z-score in a normdist
        
        clf = linear_model.LinearRegression()
        clf.fit(r_znorm[:, np.newaxis], self.residuals[:, np.newaxis]) # Make inputs correct shape (X , 1)
        r_predicted = clf.predict(r_znorm[:, np.newaxis]) # Predicted residuals given normdist, z-score input
        
        return (self.residuals, r_znorm, r_predicted) # inputs for a normal probability plot

