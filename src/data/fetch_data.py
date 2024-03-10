from data_fetcher import DataFetcher

if __name__ == "__main__":
    fetcher = DataFetcher(52.52, 13.41)
    print(fetcher.fetch_weather()[:5])
