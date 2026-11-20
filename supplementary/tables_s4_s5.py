"""Tables S4–S5: monthly estimates for the two city-size groups."""
import pandas as pd
from _data import monthly, save
from _regression import logfit, row

def main():
    data = monthly()
    for peak, table in [('morning', 'S4'), ('evening', 'S5')]:
        outcome = peak + '_peak_congested_network_length'
        rows = []
        for month, cities in data.groupby('month'):
            for large, label in [(False, '<1 million'), (True, '>=1 million')]:
                group = cities.loc[(cities.population >= 1e6) == large]
                fit = logfit(group, outcome, ['population'])
                rows.append(dict(month=month, group=label, **row(peak, fit, 'population')))
        save(pd.DataFrame(rows), f'table_{table}_monthly_{peak}.csv')

if __name__ == '__main__':
    main()
