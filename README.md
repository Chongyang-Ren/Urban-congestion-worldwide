# Urban congestion worldwide

Original plotting code for “Urban congestion worldwide: cross-city scaling and within-city concentration”, arranged as four notebooks. Run the setup cell, then the cell for the panel you want. Each panel saves its files and displays the output below the cell.

| Notebook | Panel cells | Original source |
| --- | --- | --- |
| `fig1.ipynb` | a–d; a includes the city-count inset | `Fig 1_new.ipynb`, cells 2, 3 and 0 |
| `fig2.ipynb` | a–c | `Fig2_new.ipynb`, cells 0 and 1 |
| `fig3.ipynb` | a–d | `S4.ipynb`, cells 18, 15, 21 and 23 |
| `fig4.ipynb` | a–i; each of d–i contains one city's map and bars | `Fig5.ipynb`, cells 7, 2, 5, 3 and 6 |


## Run

```bash
python -m pip install -r requirements.txt
jupyter lab
```

Open a notebook from this folder. `BASE` should point to this folder; change it in the setup cell if Jupyter starts elsewhere. Figures are saved to `figures/fig1/a/`, etc. Original export filenames are retained.

The included data run Fig. 1's count inset and panels b–d, and all of Fig. 2. Fig. 1a's map and the street-segment panels need additional original inputs. Set `PROJECT_ROOT` in the setup cell to your original TomTom project directory, or set the `TOMTOM_PROJECT_ROOT` environment variable before opening Jupyter.

Required inputs under that directory:

- Fig. 1a: `GIS/world-administrative-boundaries/world-administrative-boundaries.shp` and companion files.
- Fig. 3: `GIS/segment_congestion_all_cities/by_city`, `all_cities_aggregate/all_city_metrics.csv` within the same directory, and `data/final_data/API_2025_full_year_city_summary_filtered_merged_with_time_shift_v2.csv`.
- Fig. 4b–i: `fig5_stage0_outputs` and `fig5_highway_ring_outputs/csv` under `GIS/segment_congestion_all_cities`. Bars read the saved matching results.
- Fig. 4a: `GIS/GHSL_city_rings/london, United Kingdom/all_rings.geojson`, plus the CartoDB basemap accessed by contextily.

These segment tables and map inputs are not included. The notebooks retain the outputs from the local check. Fig. 1a's map is an existing export because the original boundary shapefile could not be located. Fig. 4a also displays its existing export; set `USE_SAVED_MAPS = False` to fetch the basemap and regenerate it. Both cached outputs are identified in their cells.

## Data

`data/city_annual.csv`: 411 cities, 2025. `data/city_monthly.csv`: the same cities over 12 months, 4,932 rows. Only identifiers, map coordinates and variables used in the city-level analyses are included.

| Field | Meaning |
| --- | --- |
| `city`, `country`, `continent` | City, country code and continent. Use city and country together to identify a record. |
| `year`, `month` | Year and calendar month; month is in the monthly file only. |
| `population` | Population used in the city-level analysis. |
| `longitude`, `latitude` | Population-weighted city coordinates in degrees. Annual file only. |
| `congested_network_length` | All-day congestion-length accumulation for the year or month. |
| `morning_peak_congested_network_length`, `evening_peak_congested_network_length` | Corresponding peak-hour accumulations. |
| `congestion_intensity` | Delay divided by congested network length, in min/km. Annual file only. |
| `congested_network_ratio` | Mean daily congestion accumulation divided by major-road length; stored as a ratio and plotted as a percentage. Annual file only. |
| `mean_daily_congestion_accumulation` | Mean daily congestion-length accumulation used in the decomposition. Annual file only. |
| `major_road_length` | Major-road length within the urban boundary, in km. Annual file only. |


## Correspondence with the manuscript

These are original plotting cells, not a pixel-identical export of the submitted artwork. Fonts, labels, legends and layout were edited later. Fig. 3a–b retain the original 5/10/20-million population cutoffs, while Fig. 3c–d use 1/5/10 million. The Fig. 4 saved bar tables also differ from parts of the submitted artwork, including the Paris inner/outer ordering and New York bar values. Those differences have been retained for checking rather than adjusted to match the artwork.

Sources: TomTom Traffic API, WorldPop, Global Human Settlement Layer (GHSL) and OpenStreetMap, as described in the manuscript.
