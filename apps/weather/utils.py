import io
import base64
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


def generate_temperature_chart(weather_data):
    """Generate a temperature chart using matplotlib"""
    plt.switch_backend('Agg')
    plt.figure(figsize=(10, 4))
    
    dates = [record.recorded_at for record in weather_data]
    temperatures = [record.temperature for record in weather_data]
    
    plt.plot(dates, temperatures, color='#4bc0c0', linewidth=2)
    plt.title('Temperature Over Time')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(DateFormatter('%m/%d %H:%M'))
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save plot to a temporary buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    # Encode the image to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{image_base64}"