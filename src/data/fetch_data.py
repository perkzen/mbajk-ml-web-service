from data_fetcher import DataFetcher

if __name__ == "__main__":
    fetcher = DataFetcher(lat=52.52, lon=13.41)
    print(fetcher.fetch_weather()[:5])
