import sdmount
import time
import wifi
import socketpool
import ssl
import adafruit_requests
import json
import os

# Define the Google API key and URL
api_key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

instructions = "Keep the answer very short and without markdown formatting"

# Define the request headers
headers = {"Content-Type": "application/json"}

# Read known Wi-Fi networks from config.txt
def read_known_networks():
    if "config.txt" not in os.listdir("/sd"):
        # If config.txt does not exist, return an empty list
        return []
    with open("sd/config.txt", "r") as file:
        networks = []
        for line in file:
            ssid, password = line.strip().split(",")
            networks.append((ssid, password))
    return networks


# Add new Wi-Fi network to config.txt
def add_network_to_config(ssid, password):
    with open("sd/config.txt", "a") as file:
        file.write(f"{ssid},{password}\n")
    print(f"Network {ssid} has been added.")


# Function to scan available networks
def scan_available_networks():
    print("Scanning for available networks...")
    available_networks = [net.ssid for net in wifi.radio.start_scanning_networks()]
    wifi.radio.stop_scanning_networks()
    return available_networks


# Function to connect to Wi-Fi with retry limit and delay
def connect_to_wifi(ssid, password, retries=3, delay=5):
    for attempt in range(retries):
        try:
            wifi.radio.connect(ssid, password)
            print(f"Connected to Wi-Fi: {wifi.radio.ipv4_address}")
            return True
        except Exception as e:
            print(f"Failed to connect to {ssid} (Attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)
    return False


# Handle Wi-Fi connection
def wifi_connection_manager():
    known_networks = read_known_networks()
    available_networks = scan_available_networks()
    connected = False

    # Try only the known networks that are available
    for ssid, password in known_networks:
        if ssid in available_networks:
            print(f"Trying to connect to {ssid}...")
            connected = connect_to_wifi(ssid, password)
            if connected:
                break
    # If no known networks work, ask the user whether to retry or add a new network
    while not connected:
        action = input(
            "Failed to connect to a known Wi-Fi network. Do you want to (r)etry or (a)dd a new network?: "
        ).lower()
        if action == "r":
            available_networks = (
                scan_available_networks()
            )  # Re-scan for available networks
            for ssid, password in known_networks:
                if ssid in available_networks:
                    print(f"Retrying connection to {ssid}...")
                    connected = connect_to_wifi(ssid, password)
                    if connected:
                        break
        elif action == "a":
            ssid = input("Enter Wi-Fi SSID: ")
            password = input("Enter Wi-Fi password: ")
            connected = connect_to_wifi(ssid, password)
            if connected:
                add_network_to_config(ssid, password)
    return connected


# Chat with Gemini
def gemini_chat():
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    while True:
        # Get user input
        user_input = input("Your message: ")
        if not user_input:
            print("No message entered. Please try again...")
            continue
        print("Sending message to Gemini...")

        # Create request payload
        data = {
            "system_instruction": {"parts": {"text": "Answer very short and without markdown formatting"}},
            "contents": [{"role": "user", "parts": [{"text": user_input}]}],
            "generationConfig": {"maxOutputTokens": 50}
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
                    candidates = response_data.get("candidates", [])
                    if candidates:
                        first_candidate = candidates[0]
                        content_parts = first_candidate.get("content", {}).get(
                            "parts", []
                        )
                        if content_parts:
                            model_response_text = content_parts[0].get("text", "")
                            model_response_text = "Gemini: " + model_response_text
                            # Replace newlines with a space
                            model_response_text = model_response_text.replace("\n", " ")

                            # print response
                            print(model_response_text)
                elif response.status_code == 500:
                    # Handle server error 500
                    print("Server Error 500. Retrying in 5 seconds...")
                    time.sleep(5)
                    retry_count += 1
                    continue
                else:
                    print(f"HTTP Error: {response.status_code}")
                break  # Exit retry loop if successful
            except Exception as e:
                print(f"Error: {e}")
                retry_count += 1
                print("Retrying in 5 seconds...")
                time.sleep(5)


# Main function
def main():
    if wifi_connection_manager():
        print("Wi-Fi connection established. Starting Gemini chat function...")
        gemini_chat()
    else:
        print("Failed to connect to Wi-Fi. Program exiting.")


# Run the main function
main()
