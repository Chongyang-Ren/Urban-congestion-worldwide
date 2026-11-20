"""Tables S2–S3: scaling decomposition and density models."""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from _data import decomposition_inputs, save
from _regression import logfit, row

def main():
    data = decomposition_inputs()
    rows = []
    for outcome in ['mean_daily_congestion_accumulation', 'major_road_length', 'congested_network_ratio']:
        fit = logfit(data, outcome, ['population'], 'HC3')
        rows.append(row(outcome, fit, 'population'))
    save(pd.DataFrame(rows), 'table_S2_decomposition.csv')
    length = 'mean_daily_congestion_accumulation'
    comparison = [row(label, logfit(sample, length, ['population'], 'HC3'), 'population')
                  for label, sample in [('All cities', data), ('Excluding Africa', data.loc[data.continent.ne('Africa')])]]
    save(pd.DataFrame(comparison), 'table_S2_sample_comparison.csv')

    data['logP'] = np.log10(data.population)
    data['logB'] = np.log10(data.major_road_length)
    data['logL'] = np.log10(data.mean_daily_congestion_accumulation)
    rows = []
    models = [('M1', 'logL', ['logP', 'logB']),
              ('M2', 'logBD', ['logPD']),
              ('M3', 'logLD', ['logPD']),
              ('M4', 'logLD', ['logPD', 'logBD'])]
    for name, outcome, predictors in models:
        fit = sm.OLS(data[outcome], sm.add_constant(data[predictors])).fit(cov_type='HC3')
        rows.extend(row(name, fit, term) for term in predictors)
    save(pd.DataFrame(rows), 'table_S3_density_models.csv')

if __name__ == '__main__':
    main()
