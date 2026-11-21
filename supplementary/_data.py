"""Inputs and output paths shared by the supplementary analyses."""
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
RESULTS = HERE / 'results'

def source_file(name):
    for path in (HERE / 'data' / name, REPOSITORY / name, REPOSITORY / 'data' / name):
        if path.is_file():
            return path
    raise FileNotFoundError(f'Place {name} in supplementary/data or the repository root.')

def annual():
    return pd.read_csv(source_file('city_annual.csv'))

def monthly():
    return pd.read_csv(source_file('city_monthly.csv'))

def decomposition_inputs():
    annual_data = annual()
    model_data = pd.read_csv(source_file('city_model_inputs.csv'))
    # These models use the population measured within the analysis boundary.
    joined = model_data.merge(annual_data.drop(columns='population'),
                             on=['city', 'country'], how='left',
                             validate='one_to_one', indicator=True)
    if len(joined) != len(annual_data) or not joined['_merge'].eq('both').all():
        raise ValueError('The annual and model-input city lists must match.')
    joined = joined.drop(columns='_merge')
    joined['logPD'] = np.log10(joined.population / joined.area_km2)
    joined['logBD'] = np.log10(joined.major_road_length / joined.area_km2)
    joined['logLD'] = np.log10(joined.mean_daily_congestion_accumulation / joined.area_km2)
    return joined

def panel_inputs():
    panel = monthly().copy()
    panel['city_id'] = panel.country + ' | ' + panel.city
    panel['z'] = np.log10(panel.population) - 6
    panel['large'] = (panel.population >= 1e6).astype(float)
    panel['z_large'] = panel.z * panel.large
    return panel

def save(frame, name):
    RESULTS.mkdir(exist_ok=True)
    path = RESULTS / name
    frame.to_csv(path, index=False)
    print(path)
