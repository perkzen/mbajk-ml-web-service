from sqlalchemy import create_engine
from src.config import settings


def create_database_engine(echo: bool = False):
    engine = create_engine(settings.database_url, echo=echo)
    return engine
