# Urban congestion worldwide

Plotting code and city-level data for “Urban congestion worldwide: cross-city scaling and within-city concentration”.

The code is organized into four notebooks, with one cell per figure panel. Run the setup cell first, then the panel you want. Each panel saves its files and displays the output.

| Notebook | Panels |
| --- | --- |
| `fig1.ipynb` | a–d; a includes the city-count inset |
| `fig2.ipynb` | a–c |
| `fig3.ipynb` | a–d |
| `fig4.ipynb` | a–i; each of d–i contains one city's map and bars |

## Run

```bash
python -m pip install -r requirements.txt
jupyter lab
```

Open a notebook from the repository folder. `BASE` should point to this folder; change it in the setup cell if needed. Outputs are saved under `figures/fig1/a/`, etc.

The included data support Fig. 1's count inset and panels b–d, and all of Fig. 2. The remaining panels require additional map and segment-level inputs. Set `PROJECT_ROOT` in the setup cell to the directory containing these inputs, or set the `TOMTOM_PROJECT_ROOT` environment variable before opening Jupyter.

Required inputs, relative to `PROJECT_ROOT`:

| Panels | Inputs |
| --- | --- |
| Fig. 1a | `GIS/world-administrative-boundaries/world-administrative-boundaries.shp` and companion files |
| Fig. 3 | `GIS/segment_congestion_all_cities/by_city/`, `GIS/segment_congestion_all_cities/all_cities_aggregate/all_city_metrics.csv`, and `data/final_data/API_2025_full_year_city_summary_filtered_merged_with_time_shift_v2.csv` |
| Fig. 4a | `GIS/GHSL_city_rings/london, United Kingdom/all_rings.geojson` and the CartoDB basemap accessed through contextily |
| Fig. 4b–i | `GIS/segment_congestion_all_cities/fig5_stage0_outputs/` and `GIS/segment_congestion_all_cities/fig5_highway_ring_outputs/csv/` |

Segment-level tables and map inputs are not included. The notebooks retain saved outputs for viewing. The displayed maps in Fig. 1a and Fig. 4a are previously exported images, as noted in their cells. To regenerate Fig. 4a, supply the required inputs and set `USE_SAVED_MAPS = False`.

## Data

- `data/city_annual.csv`: 411 cities for 2025.
- `data/city_monthly.csv`: the same cities over 12 months, totaling 4,932 records.

The files contain identifiers, map coordinates and variables used in the city-level analyses.

| Field | Meaning |
| --- | --- |
| `city`, `country`, `continent` | City, country code and continent. Use city and country together to identify a city. |
| `year`, `month` | Year and calendar month. Month appears only in the monthly file. |
| `population` | Population used in the city-level analysis. |
| `longitude`, `latitude` | Population-weighted city coordinates in degrees. Annual file only. |
| `congested_network_length` | All-day congestion-length accumulation for the year or month. |
| `morning_peak_congested_network_length`, `evening_peak_congested_network_length` | Corresponding peak-hour accumulations. |
| `congestion_intensity` | Delay divided by congested network length, in min/km. Annual file only. |
| `congested_network_ratio` | Mean daily congestion accumulation divided by major-road length. Stored as a ratio and plotted as a percentage. Annual file only. |
| `mean_daily_congestion_accumulation` | Mean daily congestion-length accumulation used in the decomposition. Annual file only. |
| `major_road_length` | Major-road length within the urban boundary, in km. Annual file only. |

## Correspondence with the manuscript

Final figure layouts and labels were edited separately. Fig. 3a–b retain population cutoffs of 5, 10 and 20 million, while Fig. 3c–d use 1, 5 and 10 million. Some saved Fig. 4 bar values and ring assignments also differ from the manuscript figures. These differences remain to be checked.

## Sources

[TomTom Traffic API](https://docs.tomtom.com/#traffic), [WorldPop](https://www.worldpop.org/), [Global Human Settlement Layer (GHSL)](https://human-settlement.emergency.copernicus.eu/) and [OpenStreetMap](https://www.openstreetmap.org/copyright), as described in the manuscript.
