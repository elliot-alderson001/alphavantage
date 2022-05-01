from dotenv import dotenv_values
import requests
import json
import datetime

class AlphaVantage:

    def __init__(self):
        self.APIKEY = dotenv_values(".env")['API_KEY']
        self.URL = "https://www.alphavantage.co/query?"
        
        #temp data
        self.data = None
        self.params = None

    def get_data(self, params):
        URL = self.URL
        r = requests.get(URL, params)
        return r.json()

    def current_time(self):
        now = datetime.datetime.now()
        time_text = now.strftime("%Y%b%d")
        return time_text

    def time_series_daily(self, symbol, outputsize="compact", datatype="json"):
        params = {
                "function":"TIME_SERIES_DAILY",
                "symbol":symbol,
                "apikey": self.APIKEY,
                "outputsize" : outputsize, #full, #compact
                "datatype" : datatype, #json, #csv
                }
        
        # attach param to class for creating export filename
        self.params = params

        data = self.get_data(params)
        self.data = data
        return data

    def export_json(self, filename=None):
        data = self.data
        if filename==None:
            p = self.params
            filename = f"{p['symbol']}_{p['function']}_{self.current_time()}.json"
        else:
            filename = filename

        with open(filename, "w") as file:
            json.dump(data, file, indent=8)

        print(f"file: {filename} is exported")


def main():
    API = AlphaVantage()
    API.time_series_daily(symbol = "AMD")
    # API.export_json()
    API.export_json()
    

if __name__ == "__main__":
    main()
