import json
import urllib.request
import urllib.error
import sys

from load_env import load_weather_env
from datetime import date

weather_api_key = load_weather_env()


def call_visualcrossing_api():
    """
    TODO:
    """
    api_weather_forecast_request = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?locations=Salina,KS,67401&aggregateHours=1&unitGroup=us&forecastDays=1&shortColumnNames=false&contentType=json&key={weather_api_key}"

    print("\nrunning query...\n")

    try:
        response = urllib.request.urlopen(api_weather_forecast_request)
    except urllib.error.HTTPError as e:
        error_info = e.read().decode()
        print(f"Error code: {e.code}, {error_info}")
        sys.exit()
    except urllib.error.URLError as e:
        error_info = e.read().decode()
        print(f"Error code: {e.code}, {error_info}")
        sys.exit()

    # parse results as JSON
    data = response.read()
    json_result = json.loads(data.decode("utf-8"))
    raw_weather_data = json_result.get("locations").get("Salina,KS,67401").get("values")
    return raw_weather_data


def process_weather_data(raw_weather_data):
    """
    TODO:
    """

    today = date.today()
    # today_formatted = today.strftime("%Y-%m-%d")
    today_formatted = "2022-09-01"

    def filter_to_today(element):
        date_string = element.get("datetimeStr")[0:10]
        return date_string == today_formatted

    def filter_to_time_window(element):
        """
        TODO:
        """
        hourInt = int(element.get("datetimeStr")[11:13])
        return hourInt > 4 and hourInt <= 8

    filtered_today_weather = list(filter(filter_to_today, raw_weather_data))
    filtered_hourly_weather = list(
        filter(filter_to_time_window, filtered_today_weather)
    )

    notable_variables = save_notable_variables(filtered_hourly_weather)

    return notable_variables


def save_notable_variables(filtered_hourly_weather):
    """
    TODO:
    """
    saved = {}

    for h in filtered_hourly_weather:

        if saved.get("temp_high") is None or h["temp"] > saved["temp_high"]:
            saved["temp_high"] = h["temp"]

        if saved.get("dewpoint_high") is None or h["dew"] > saved["dewpoint_high"]:
            saved["dewpoint_high"] = h["dew"]

        if saved.get("temp_low") is None or h["temp"] < saved["temp_low"]:
            saved["temp_low"] = h["temp"]

        if saved.get("windchill") is None or (
            h["windchill"] is not None and h["windchill"] < saved["windchill"]
        ):
            saved["windchill"] = h["windchill"]

        if saved.get("windspeed_high") is None or h["wspd"] > saved["windspeed_high"]:
            saved["windspeed_high"] = h["wspd"]

        if saved.get("windgust_high") is None or h["wgust"] > saved["windgust_high"]:
            saved["windgust_high"] = h["wgust"]

        if saved.get("uv_index_high") is None or h["uvindex"] > saved["uv_index_high"]:
            saved["uv_index_high"] = h["uvindex"]

        if saved.get("wind_dir") is None:
            saved["wind_dir"] = [h["wdir"]]
        else:
            saved["wind_dir"].append(h["wdir"])

    saved["av_wind_dir"] = sum(saved["wind_dir"]) / len(saved["wind_dir"])

    return saved


def construct_tweet_with_data(processed_weather_data):
    """
    TODO:
    """
    d = processed_weather_data

    tweet_string = "\n\nFrom 5am to 8am:"
    tweet_string += (
        f"\nHigh of {round(d['temp_high'])} °F, low of {round(d['temp_low'])} °F"
    )
    tweet_string += f"\nUV Index reaches {round(d['uv_index_high'])}"
    tweet_string += f"\nWind mostly from the {degrees_to_direction(d['av_wind_dir'])}, with av. speed of {d['windspeed_high']} mph and gusts of {d['windgust_high']} mph"

    tweet_string = f"\nOur advice: {determine_advisory(d)}" + tweet_string
    tweet_string = f"Good morning TLI commuting Salinans!" + tweet_string

    return tweet_string


def degrees_to_direction(decimal_degree):
    """
    A helper TODO:
    """
    val = int((decimal_degree / 45))

    arr = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    cardinal_direction = arr[(val % 8)]
    return cardinal_direction


def determine_advisory(processed_weather_data):
    """
    TODO:
    """
    advisory = "bike! 🚴🏼‍♀️☀️ - it looks like a nice day for a ride."

    low_temp = processed_weather_data["temp_low"]
    low_temp_boolean = low_temp <= 40 and low_temp > 20
    twenty_low_temp_boolean = low_temp <= 20
    # twenty_low_temp_boolean = low_temp <= 20 and low_temp > 10
    # arctic_low_temp_boolean = low_temp <= 10

    windy_boolean = processed_weather_data["windspeed_high"] >= 20
    # wind_dir = processed_weather_data["av_wind_dir"]
    fave_direction_boolean = "N" in degrees_to_direction(
        processed_weather_data["av_wind_dir"]
    )

    high_temp_boolean = processed_weather_data["temp_high"] >= 95
    high_dewpoint_boolean = processed_weather_data["dewpoint_high"] >= 65

    if windy_boolean and not fave_direction_boolean and twenty_low_temp_boolean:
        advisory = "don't bike! 🌬🚴🏼‍♀️🥶 It's a cold, windy day out there."
    elif twenty_low_temp_boolean:
        advisory = "don't bike! 🥶 - it's below 20 °F"
    elif windy_boolean and not fave_direction_boolean:
        advisory = "don't bike! 🌬🚴🏼‍♀️ - winds are high and unfavorable."
    elif fave_direction_boolean:
        advisory = "bike! 🚴🏼‍♀️💨 use that sweet, sweet tailwind."

    return advisory


def create_advisory():
    """
    TODO:
    """
    raw_weather_data = call_visualcrossing_api()
    processed_weather_data = process_weather_data(raw_weather_data)
    tweet_string = construct_tweet_with_data(processed_weather_data)
    weather_advisory = tweet_string

    return weather_advisory


# for testing of script in isolation
if __name__ == "__main__":
    result = create_advisory()
    assert isinstance(result, str)
    print(f" =====\n{result}\n =====")
