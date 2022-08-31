import unittest
from weather_call import construct_tweet_with_data


def create_generic_data():
    nice_day = {
        "temp_high": 66.8,
        "dewpoint_high": 55.5,
        "temp_low": 64.8,
        "windchill": None,
        "windspeed_high": 3.4,
        "windgust_high": 7.8,
        "uv_index_high": 1.0,
        "wind_dir": [257.7, 225.2, 51.3, 104.5],
        "av_wind_dir": 159.67499999999998,
    }

    return nice_day


class TestApp(unittest.TestCase):
    def test_nice_day(self):
        weather_day = create_generic_data()
        exp = "Good morning TLI commuting Salinans!\nOur advice: bike! 🚴🏼‍♀️☀️ - it looks like a nice day for a ride.\n\nFrom 5am to 8am:\nHigh of 67 °F, low of 65 °F\nUV Index reaches 1\nWind mostly from the SE, with av. speed of 3.4 mph and gusts of 7.8 mph"
        self.assertEqual(
            construct_tweet_with_data(weather_day), exp, "Should match expected string"
        )

    def test_cold_and_windy_day(self):
        weather_day = create_generic_data()
        weather_day.update(
            {"temp_low": 15.8, "windspeed_high": 22.5, "windgust_high": 31.2}
        )
        exp = "Good morning TLI commuting Salinans!\nOur advice: don't bike! 🌬🚴🏼‍♀️🥶 It's a cold, windy day out there.\n\nFrom 5am to 8am:\nHigh of 67 °F, low of 16 °F\nUV Index reaches 1\nWind mostly from the SE, with av. speed of 22.5 mph and gusts of 31.2 mph"
        self.assertEqual(
            construct_tweet_with_data(weather_day), exp, "Should match expected string"
        )

    def test_cold_day(self):
        weather_day = create_generic_data()
        weather_day.update({"temp_low": 15.8})
        exp = "Good morning TLI commuting Salinans!\nOur advice: don't bike! 🥶 - it's below 20 °F\n\nFrom 5am to 8am:\nHigh of 67 °F, low of 16 °F\nUV Index reaches 1\nWind mostly from the SE, with av. speed of 3.4 mph and gusts of 7.8 mph"
        self.assertEqual(
            construct_tweet_with_data(weather_day), exp, "Should match expected string"
        )

    def test_windy_day(self):
        weather_day = create_generic_data()
        weather_day.update({"windspeed_high": 22.5, "windgust_high": 31.2})
        exp = "Good morning TLI commuting Salinans!\nOur advice: don't bike! 🌬🚴🏼‍♀️ - winds are high and unfavorable.\n\nFrom 5am to 8am:\nHigh of 67 °F, low of 65 °F\nUV Index reaches 1\nWind mostly from the SE, with av. speed of 22.5 mph and gusts of 31.2 mph"
        self.assertEqual(
            construct_tweet_with_data(weather_day), exp, "Should match expected string"
        )

    def test_tailwind_day(self):
        weather_day = create_generic_data()
        weather_day.update(
            {"windspeed_high": 22.5, "windgust_high": 31.2, "av_wind_dir": 0}
        )
        exp = "Good morning TLI commuting Salinans!\nOur advice: bike! 🚴🏼‍♀️💨 use that sweet, sweet tailwind.\n\nFrom 5am to 8am:\nHigh of 67 °F, low of 65 °F\nUV Index reaches 1\nWind mostly from the N, with av. speed of 22.5 mph and gusts of 31.2 mph"
        self.assertEqual(
            construct_tweet_with_data(weather_day), exp, "Should match expected string"
        )


if __name__ == "__main__":
    unittest.main()
