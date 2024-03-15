# Bike Station Availability Prediction Service

## Description

REST web service for predicting the number of available bike stands at one of the MBajk bike stations. The prediction
service is based on a recurrent neural network model.

## Project structure

```
├── README.md <- File containing project description and setup instructions
├── data
    ├── processed <- Processed data, prepared for training
    └── raw <- Raw downloaded data
├── models <- Trained and serialized models, model predictions, or summaries of models
├── notebooks <- Jupyter notebooks
├── reports <- Generated analysis files
    └── figures <- Generated graphs and images used in the analysis
├── pyproject.toml <- File defining dependencies, library versions, etc.
├── src <- Source code of the project
  ├── __init__.py <- Initializes the "src" directory as a Python module
  ├── data <- Scripts for data downloading, processing, etc.
  ├── models <- Scripts for training predictive models and using models for prediction
  ├── serve <- Scripts for serving models as web services
  ├── client <- Source code for the user interface
  └── visualization <- Scripts for visualization

```

## Scripts

Python scripts that can be run are defined in the `pyproject.toml` file.

### Data scripts

- `fetch` - Downloads the data from the MBajk API and OpenMeteo API and saves it to the `data/raw` directory.
- `process` - Processes the raw data and saves it to the `data/processed` directory.

## Model scripts

- `train` - Trains the predictive model and saves it to the `models` directory.
- `predict` - Uses the trained model to make predictions and saves them to the `models` directory.

## Serve scripts

- `serve` - Starts the web service for making predictions using the trained model. The service is available at `http://localhost:8000`.

## Setup

- Python `3.12`
- Poetry `1.8.2`
- Docker `25.0.0`
- Node.js `20.0.0`
- npm `10.0.0`



