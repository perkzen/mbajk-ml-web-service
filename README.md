# Bike Station Availability Prediction Service

## Description

REST web service for predicting the number of available bike stands at one of the MBajk bike stations. The prediction
service is based on a recurrent neural network model.

## Project structure

```
├── README.md           <- Description of the project and setup instructions
├── data
│   ├── processed       <- Processed data prepared for training
│   └── raw             <- Original downloaded data
├── models              <- Trained and serialized models
├── notebooks           <- Jupyter notebooks
├── reports             <- Generated analysis files
│   └── figures         <- Generated graphs and images used in analysis
├── pyproject.toml      <- Defines dependencies and library versions
└── src                 <- Source code of the project
    ├── __init__.py     <- Initialize "src" directory as a Python module
    ├── data            <- Scripts for data downloading, processing, etc.
    ├── models          <- Scripts for training predictive models and using them for prediction
    ├── serve           <- Scripts for serving models as web services
    └── visualization   <- Scripts for visualization

```

## Web service

The web service is based on the FastAPI framework. It provides two endpoints:

- `/` - health check endpoint, returns "OK
```json

  "status": "ok",
  "date": "2024-03-11T10:31:54.783620"
}
```

- `/mbajk/predict` - for predicting the number of available bike stands at a given station

```json
{
  "prediction": 12
}
```

## Running the service

To run the service, execute the following command in the terminal:

```bash
poetry run poe serve
```

