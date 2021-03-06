# Covid-19 EDA
Covid-19 EDA, plots tell more than just numbers.

Using the Johns Hopkins CSSE COVID-19 data: https://github.com/CSSEGISandData/COVID-19 <br>
Using list of countries by population from Wikipedia: https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)

## Top 10 - absolute numbers
The top 10 affected countries regarding absolute numbers of confirmed Covid-19 infections and deaths due to Covid-19 infections. 
A second diagram is showing the same 10 countries normalizing the case numbers by the population (per millions of the population in the specified country, 2019)

### Confirmed cases logarithmic scale
![](./plots/Confirmed_top10_Log_10.svg)
![](./plots/Confirmed_top10_Log_10_normalized.svg)
### Confirmed cases linear scale
![](./plots/Confirmed_top10_Linear.svg)
![](./plots/Confirmed_top10_Linear_normalized.svg)

### Deaths logarithmic scale
![](./plots/Deaths_top10_Log_10.svg)
![](./plots/Deaths_top10_Log_10_normalized.svg)
### Deaths linear scale
![](./plots/Deaths_top10_Linear.svg)
![](./plots/Deaths_top10_Linear_normalized.svg)


---
# Docker container
In case you like to run the scripts from a Docker container have alook at [./docker/README.md](./docker/README.md). The scripts for building the docker image and running the container were created on a system running Ubuntu 18.04.

# Installation of the requirements using Miniconda
In case you like to run the scripts from a virual environment (currently only tested on Windows)
1. Install Miniconda with Python 3.7 or later [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
2. OS dependent
    * Linux &rarr; Open a terminal window
    * Windows &rarr; Open the Ananconda Prompt
4. Create a virtual environment and activate the virtual environment
    ```bash
    conda create -n csse_covid19_eda python=3.7
    conda activate csse_covid19_eda
    ```
5. Install the required libraries using the [requirements.txt](requirements.txt) file
    ```bash
    pip install -r ./docker/requirements
    ```
6. Start Jupyter-Lab
    ```bash
    jupyter-lab
    ```
    A browser will open running Jupyter-Lab
7. Open the Jupyter notebook [CSSE_Covid_19_time_series.ipynb](CSSE_Covid_19_time_series.ipynb) and run all cells.

The first plot can be manipulated using interactive controls
* Diagram type
    * Confirmed cases
    * Deaths
* Top X
    * Plotting the reported cases of the X (here: 10) countries with the highest absolute number of reported cases
* Y scale
    * Linear
    * Logatrithmic using base 10
![](screen_shot_ipywidgets.JPG)


