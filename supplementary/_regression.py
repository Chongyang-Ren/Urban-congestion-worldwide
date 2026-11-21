"""Log–log fits and table rows."""
import numpy as np
import pandas as pd
import statsmodels.api as sm
def row(label,fit,term):
 ci=fit.conf_int().loc[term]
 return dict(model=label,term=term,estimate=fit.params[term],se=fit.bse[term],ci_low=ci.iloc[0],ci_high=ci.iloc[1],p=fit.pvalues[term],r2=fit.rsquared,n=int(fit.nobs))

def logfit(d,y,x,cov=None):
 d=d[[y]+x].replace([np.inf,-np.inf],np.nan).dropna()
 d=d[(d>0).all(axis=1)]
 model=sm.OLS(np.log10(d[y]),sm.add_constant(np.log10(d[x])))
 return model.fit(cov_type=cov) if cov else model.fit()
