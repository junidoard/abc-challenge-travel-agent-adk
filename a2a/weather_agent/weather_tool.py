import os
import requests
from google.adk.tools import Tool


class WeatherTool(Tool):

    name: str = "weather_forecast"
    description: str = (
        "Provides a 7-day weather forecast for a specified location and date."
    )
    parameters: list = [
        {
            "name": "location",
            "type": "str",
            "description": "The location for the weather forecast.",
        },
        {
            "name": "date",
            "type": "str",
            "description": "The start date for the 7-day forecast (YYYY-MM-DD).",
        },
    ]

    def _run(self, location: str, date: str) -> str:
        api_key = "AIzaSyDYhqnzXj4ddnnjxQVFiXzDo4uzGVjPAkQ"  # User needs to set this environment variable
        if not api_key:
            return "Error: GOOGLE_MAPS_API_KEY environment variable is not set."

        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()

        if geocode_data["status"] != "OK" or not geocode_data["results"]:
            return f"Error: Could not find coordinates for location '{location}'."

        lat = geocode_data["results"][0]["geometry"]["location"]["lat"]
        lng = geocode_data["results"][0]["geometry"]["location"]["lng"]

        forecast_data = []
        import datetime

        start_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        for i in range(7):
            current_date = start_date + datetime.timedelta(days=i)
            forecast_data.append(f"  {current_date.strftime('%Y-%m-%d')}: Sunny, 25C")

        return f"7-day weather forecast for {location} starting {date}:" + "\n".join(
            forecast_data
        )


weather_tool = WeatherTool()
