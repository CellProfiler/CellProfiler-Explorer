# CellProfiler-Explorer
Web app built with dash for exploring CellProfiler data and combining with metadata


## Set up dev environment
There is a provided .yml file for creating the minimal environment to run the dash app. To load this using (mamba)[https://mamba.readthedocs.io/en/latest/installation.html] or (conda)[https://docs.anaconda.com/anaconda/install/index.html], navigate to this repo in terminal and run the appropriate command below: 

```
mamba env create --file env.yaml
conda env create --file env.yaml
```

## How to run the app locally
Navigate to this repo in terminal and enter `python app.py` and visit http://127.0.0.1:8050/ in your web browser.

The repo includes `Cells.csv`, which can be dragged and dropped into the app to load as an example dataset. 

<img width="1359" alt="image" src="https://user-images.githubusercontent.com/28116530/221624348-3d12a210-52d3-4b00-b851-28004593f8b8.png">
