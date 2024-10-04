# M5Stack Cardputer Script Selector

This project provides a script selection menu for the M5Stack cardputer, allowing users to easily choose and run Python scripts stored on the device. 

## Features
- Lists Python scripts from the internal storage and optionally from an external SD card.
- Paginated display for easy navigation through multiple scripts.
- Example scripts included: Gemini chat, sd-card mount, print mac address

## Installation
- Python scripts should be placed in a folder named `scripts` both on the SD card and in the root directory.
- Copy code.py to your device and run the code to start selecting scripts.
- To use the Gemini chat, you need the sdmount script in `lib` folder and you gemini api key in the settings.toml file. An sd card is also needed to read and write wifi details.
- sdmount.py adds "/sd/lib" to path, so you can keep the full circuitpython library selection there
