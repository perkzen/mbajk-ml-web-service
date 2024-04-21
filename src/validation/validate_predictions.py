from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data.data_manager import DataManager
from src.serve.database import create_database_engine
from src.serve.models.prediction import Prediction


def main():
    engine = create_database_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    all_predictions = session.query(Prediction).all()

    dm = DataManager(data_path="data/processed")
    station = dm.get_dataframe(folder="1", file_name="mbajk_station_1")
    print(station.head())


if __name__ == '__main__':
    main()
