import os
import dotenv
import requests


def get_api_key() -> str:
    dotenv.load_dotenv()
    API_KEY: str = os.environ.get("WEATHER_API_KEY")
    return API_KEY


def get_weather_data(city) -> dict:
    result = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={get_api_key()}&q={city}"
    )

    if "error" in result.json():
        return {"error": result.json()["error"]["message"]}

    json = {
        "location": result.json()["location"]["name"],
        "temperature": result.json()["current"]["temp_f"],
        "wind_speed": result.json()["current"]["wind_mph"],
        "weather": result.json()["current"]["condition"]["text"],
        "time": result.json()["location"]["localtime"][11:],
    }
    return json
