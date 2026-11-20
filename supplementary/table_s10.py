"""Table S10: country-clustered uncertainty for the existing models."""
import numpy as np
import pandas as pd
from _data import annual, panel_inputs, decomposition_inputs, save
from _models_country import fit_ols_cluster, linear_combo, peak_model, size_model
def main():
    a=annual(); rows=[]
    def record(label,r,weights):
        rows.append(dict(model=label,**linear_combo(r,weights),n=r['n'],countries=r['clusters'],r2=r['r2']))
    d=decomposition_inputs();d['const']=1.;d['logP']=np.log10(d['population'])
    for label,column in [('Decomposition L','mean_daily_congestion_accumulation'),('Decomposition B','major_road_length'),('Decomposition E','congested_network_ratio')]:
        d['y']=np.log10(d[column]);record(label,fit_ols_cluster(d,'y',['const','logP']),{'logP':1})
    assert a.groupby('city').country.nunique().max()==1
    for peak in ['Morning','Evening']:
        col=peak.lower()+'_peak_congested_network_length'
        q=a[(a['population']>0)&(a[col]>0)].groupby('city',as_index=False).agg({'population':'first',col:'sum','country':'first'})
        q['const']=1.;q['logP']=np.log10(q['population']);q['y']=np.log10(q[col])
        record('Fig2a '+peak,fit_ols_cluster(q,'y',['const','logP']),{'logP':1})
    density=decomposition_inputs()
    density['const']=1.;density['logP']=np.log10(density.population)
    density['logB']=np.log10(density.major_road_length)
    density['logL']=np.log10(density.mean_daily_congestion_accumulation)
    for label,y,xcols in [('M1','logL',['logP','logB']),('M2','logBD',['logPD']),('M3','logLD',['logPD']),('M4','logLD',['logPD','logBD'])]:
        r=fit_ols_cluster(density,y,['const']+xcols)
        for x in xcols:record(label+' '+x,r,{x:1})
    panel = panel_inputs()
    r,_=peak_model(panel)
    for name,w in [('Monthly morning',{'z':1}),('Monthly evening',{'z':1,'z_evening':1}),('Monthly evening minus morning',{'z_evening':1})]:record(name,r,w)
    r,_=size_model(panel)
    for name,w in [('Monthly below 1 million',{'z':1}),('Monthly above 1 million',{'z':1,'z_large':1}),('Monthly above minus below',{'z_large':1})]:record(name,r,w)
    result=pd.DataFrame(rows);save(result, 'table_S10_country_clustered.csv')
    print(result.to_string(index=False))
    return result

if __name__=='__main__':main()
