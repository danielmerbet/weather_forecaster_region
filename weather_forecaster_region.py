import requests
import folium
import plotly.graph_objects as go
import plotly.io as pio
import os

# Function to fetch weather forecast data for a city
def fetch_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation&timezone=auto"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data. HTTP Status: {response.status_code}")
        return None

# Function to generate a plot for the weather forecast of a city
def generate_forecast_plot(data, city, output_dir):
    times = data["hourly"]["time"]
    temperatures = data["hourly"]["temperature_2m"]
    precipitation = data["hourly"]["precipitation"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=temperatures, mode='lines', name='Temperature (°C)'))
    fig.add_trace(go.Scatter(x=times, y=precipitation, mode='lines', name='Precipitation (mm)'))

    fig.update_layout(
        title=f"Weather Forecast for {city}",
        xaxis_title="Time",
        yaxis_title="Values",
        legend_title="Variables",
    )

    # Save plot as an HTML file
    plot_path = os.path.join(output_dir, f"{city.replace(' ', '_')}_forecast.html")
    pio.write_html(fig, file=plot_path, auto_open=False)

    return plot_path

# Function to generate the HTML map with clickable city markers
def generate_map(cities, output_dir):
    m = folium.Map(location=[40.0, -3.0], zoom_start=6)  # Centered roughly on Spain

    for city, coords in cities.items():
        lat, lon = coords
        weather_data = fetch_weather(lat, lon)
        if weather_data:
            # Generate plot and get its file path
            plot_path = generate_forecast_plot(weather_data, city, output_dir)

            # Add marker with a clickable link to the plot
            popup_html = f"<a href='{plot_path}' target='_blank'>View Forecast for {city}</a>"
            popup = folium.Popup(popup_html, max_width=300)
            folium.Marker(location=[lat, lon], popup=popup, tooltip=city).add_to(m)

    return m

# Main function to generate the HTML file
def main():
    # Define cities with their coordinates
    cities = {
        "Madrid": (40.4168, -3.7038),
        "Barcelona": (41.3879, 2.16992),
        "Valencia": (39.4699, -0.3763),
        "Seville": (37.3891, -5.9845),
        "Bilbao": (43.263, -2.935),
    }

    # Output directory for forecast HTML files
    output_dir = "forecast_plots"
    os.makedirs(output_dir, exist_ok=True)

    # Generate map with weather forecast popups
    weather_map = generate_map(cities, output_dir)

    # Save map as HTML
    weather_map.save("index.html")

if __name__ == "__main__":
    main()
