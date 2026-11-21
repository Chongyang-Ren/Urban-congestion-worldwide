# Urban congestion worldwide

Code for *Urban congestion worldwide: cross-city scaling and within-city concentration*. The street-segment analysis covers 108 cities.

## Getting started

Use Python 3.10 or later. From the repository root, install the dependencies and open JupyterLab.

```bash
python -m pip install -r requirements.txt
jupyter lab
```

Run the setup cell before running any figure panel. Set `TOMTOM_PROJECT_ROOT` to the folder containing the original project inputs, or set `PROJECT_ROOT` in the setup cell. The notebooks save their outputs under `figures/`.

## Main figures

| Figure | Notebook | Inputs |
| --- | --- | --- |
| Fig. 1 | `fig1.ipynb` | `data/city_annual.csv`. The map in panel a also needs the administrative boundary shapefile or the saved map specified in the notebook. |
| Fig. 2 | `fig2.ipynb` | `data/city_annual.csv` for the annual models and `data/city_monthly.csv` for the monthly estimates. |
| Fig. 3 | `fig3.ipynb` | Road-segment summaries and city metadata under `PROJECT_ROOT`. |
| Fig. 4 | `fig4.ipynb` | A ring map for panel a, city and ring summaries for panels b–c, and `data/city_road_recurrence.csv` or the project’s matching CSV for the stacked bars in panels d–i. Set `RUN_CITY_MAPS = True` to regenerate the city maps from the project geometries. |

The annual and monthly tables support the city-level figures. Recreating the street-segment figures requires the corresponding project inputs. The figure notebooks specify the file paths.

## Supplementary analyses

Run the scripts from the repository root. Outputs are saved under `supplementary/results/`.

| Tables | Command |
| --- | --- |
| S1, country-level scaling | `python supplementary/table_s1.py` |
| S2–S3, scaling decomposition and density models | `python supplementary/tables_s2_s3.py` |
| S4–S5, monthly scaling by city size | `python supplementary/tables_s4_s5.py` |
| S6, monthly interaction models | `python supplementary/table_s6.py` |
| S10, models with standard errors clustered by country | `python supplementary/table_s10.py` |

Tables S2, S3 and S10 require `data/city_model_inputs.csv` with boundary-based population and urban area (`area_km2`) for every city in `data/city_annual.csv`. Both files use `city` and `country` as identifiers.

## Data sources

[TomTom Traffic API](https://docs.tomtom.com/#traffic) · [WorldPop](https://www.worldpop.org/) · [Global Human Settlement Layer](https://human-settlement.emergency.copernicus.eu/) · [OpenStreetMap](https://www.openstreetmap.org/copyright)
