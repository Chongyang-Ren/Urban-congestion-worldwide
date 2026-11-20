# Urban congestion worldwide

These instructions cover the city-level analyses for “Urban congestion worldwide: cross-city scaling and within-city concentration.” The study also includes a street-segment analysis of 108 cities.

## Figures

```bash
python -m pip install -r requirements.txt
jupyter lab
```

Open the notebooks from the repository root and run the setup cell first. Panels 1b–d and Fig. 2 read the annual and monthly city data in `data/`. Fig. 1a also needs a boundary shapefile under `PROJECT_ROOT`. The notebook specifies its location.

## Supplementary analyses

From the repository root, run:

```bash
python supplementary/tables_s2_s3.py
python supplementary/tables_s4_s5.py
python supplementary/table_s6.py
python supplementary/table_s10.py
python supplementary/fig_s3.py
```

Tables S2, S3, and S10 need `data/city_model_inputs.csv` with matching boundary-based population and area for every city in `data/city_annual.csv`. The scripts use the existing regression helpers. Outputs are written to `supplementary/results/` and `figures/fig_s3/`.
