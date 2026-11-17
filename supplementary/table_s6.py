"""Table S6: monthly interactions with standard errors clustered by city."""
import pandas as pd
from _data import panel_inputs, save
from _models_city import peak_model, size_model

def main():
    panel = panel_inputs()
    rows = []
    for label, model in [('Peak', peak_model), ('City size', size_model)]:
        fit, summary = model(panel)
        for term, value in summary.items():
            if isinstance(value, dict):
                rows.append(dict(model=label, term=term, **value, r2=fit['r2'], n=fit['n'], cities=fit['clusters']))
    save(pd.DataFrame(rows), 'table_S6_city_clustered.csv')

if __name__ == '__main__':
    main()
