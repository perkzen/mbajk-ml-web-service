from sqlalchemy import create_engine


def create_database_engine():
    engine = create_engine("sqlite:///predictions.sqlite", echo=True)
    return engine
