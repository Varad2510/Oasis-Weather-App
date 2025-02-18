from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
import requests  

app = Flask(__name__)
CORS(app)  # Fix CORS issue

API_KEY = "50c6ad47e13373c6c4e18a57527be896"  

@app.route('/')
def home():
    return "Welcome to the Weather API! Use /get-weather?city=CityName to get weather data."  

@app.route('/get-weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400  

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return jsonify({"error": data.get("message", "Unable to fetch weather data")})  

        weather = {
            "name": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
        return jsonify(weather)
    except Exception as e:
        return jsonify({"error": str(e)})  

if __name__ == "__main__":  
    app.run(debug=True)
