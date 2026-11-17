"""Table S1: country estimates and Benjamini–Hochberg adjustment."""
import pandas as pd
from statsmodels.stats.multitest import multipletests
from _data import annual, save
from _regression import logfit, row

def main():
    rows = []
    for country, cities in annual().groupby('country'):
        if len(cities) < 8:
            continue
        for outcome in ['congested_network_length', 'congestion_intensity', 'congested_network_ratio']:
            fit = logfit(cities, outcome, ['population'])
            rows.append(dict(country=country, **row(outcome, fit, 'population')))
    result = pd.DataFrame(rows)
    result['p_BH'] = multipletests(result.p, method='fdr_bh')[1]
    save(result, 'table_S1_country_scaling.csv')

if __name__ == '__main__':
    main()
