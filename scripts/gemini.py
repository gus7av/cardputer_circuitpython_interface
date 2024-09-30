import time
import wifi
import socketpool
import ssl
import adafruit_requests
import json

# Define your Wi-Fi network credentials
ssid = "your_ssid"
password = "your_ssid_password"

# Define the Google API key and URL
api_key = "your_api_key"
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}'

# Define the request headers
headers = {
    'Content-Type': 'application/json'
}

# Function to connect to the Wi-Fi network
def connect_to_wifi(ssid, password):
    try:
        wifi.radio.connect(ssid, password)
        # print(f'Connected to Wi-Fi: {wifi.radio.ipv4_address}')
        return True
    except Exception as e:
        print(f'Failed to connect to Wi-Fi: {e}')
        return False

# Function to split long text into lines
def split_text(text, max_chars_per_line=80):
    return [text[i:i + max_chars_per_line] for i in range(0, len(text), max_chars_per_line)]

# Main function to handle the conversation and input/output
def main():
    # Connect to Wi-Fi
    if connect_to_wifi(ssid, password):
        pool = socketpool.SocketPool(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl.create_default_context())

        while True:
            # Get user input
            user_input = input(">>> ")

            # Create request payload
            data = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": user_input}]
                    }
                ]
            }

            # Convert to JSON format
            json_data = json.dumps(data)

            # Make the HTTP POST request
            retry_count = 0
            while retry_count < 3:
                try:
                    # print("Sending Input...")
                    response = requests.post(url, headers=headers, data=json_data)
                    # print(f'Received HTTP response: {response.status_code}')

                    if response.status_code == 200:
                        # Handle successful response
                        response_data = response.json()

                        # Parse response
                        candidates = response_data.get('candidates', [])
                        if candidates:
                            first_candidate = candidates[0]
                            content_parts = first_candidate.get('content', {}).get('parts', [])
                            if content_parts:
                                model_response_text = content_parts[0].get('text', '')
                                # print("Model Response:\n")

                                # Split response into lines
                                response_lines = split_text(model_response_text)

                                # Display the response
                                for line in response_lines:
                                    print(line)

                    elif response.status_code == 500:
                        # Handle server error 500
                        print("Server Error 500. Retrying in 5 seconds...")
                        time.sleep(5)
                        retry_count += 1
                        continue

                    else:
                        print(f'HTTP Error: {response.status_code}')
                    break  # Exit retry loop if successful

                except Exception as e:
                    print(f'Error: {e}')
                    retry_count += 1
                    print("Retrying in 5 seconds...")
                    time.sleep(5)

    else:
        print("Unable to establish Wi-Fi connection.")

# Run the main function
main()
