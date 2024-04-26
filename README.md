# Bike Station Availability Prediction Service

## Description

Web application for predicting the number of available bike stands at one of the MBajk bike stations. The prediction service is based on a recurrent neural network model (GRU). Its components are a FastAPI REST API and Next.js frontend.

This project implements machine learning pipelines for continuous data fetching and model training to ensure that the prediction models are constantly improving over time. 
It utilizes ONNX (Open Neural Network Exchange) Runtime for fast prediction performance and model quantization techniques to reduce model size without significantly impacting accuracy.



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
  ├── validation <- Scripts for data validation
  |── tests <- Tests for the project
  |── utils <- Utility functions
  └── visualization <- Scripts for visualization

```

## ML Service  environment variables example

```env
WINDOW_SIZE=48
TOP_FEATURES=4
LAT=46.5547
LON=15.6466
MBAJK_API_KEY=<mbajk_api_key>
MLFLOW_TRACKING_URI=<mlflow_tracking_uri>
MLFLOW_TRACKING_USERNAME=<mlflow_tracking_username>
MLFLOW_TRACKING_PASSWORD=<mlflow_tracking_password>
DAGSHUB_USER_TOKEN=<dagshub_user_token>
TF_USE_LEGACY_KERAS=1
```
## ML Client environment variables example

```env
NEXT_PUBLIC_API_URL=<mbajk_api_key>
NEXT_PUBLIC_GOOGLE_MAPS_KEY=<google_maps_api_key>
```

## Scripts

Python scripts that can be run are defined in the `pyproject.toml` file.

### Script usage

To run a script, use the following command:

```bash
poetry run poe <script_name>
```


## Makefile

The `Makefile` contains the most commonly used commands for the project. To run a command, use the following command:

Make commands:

- `build` - Builds the Docker images for the project and runs them in docker-compose.
- `up` - Starts the Docker containers.
- `down` - Stops the Docker containers.
- `dev-server` - Starts the development server for backend.
- `dev-client` - Starts the development server for frontend.
- `dev` - Starts the development server for backend and frontend.
- `test` - Runs the tests for the project.

```bash
make <command_name>
```

### Setup

- Python `3.12`
- Poetry `1.8.2`
- Docker `25.0.0`
- Node.js `20.0.0`
- npm `10.0.0`



