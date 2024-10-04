# M5Stack Cardputer Script Selector

This project provides a script selection menu for the M5Stack cardputer, allowing users to easily choose and run Python scripts stored on the device. The menu displays a paginated list of available scripts, enabling navigation through the options. Users can run selected scripts directly from the menu, enhancing the functionality of their cardputer setup.

## Features
- Lists Python scripts from the internal storage and optionally from an external SD card.
- Paginated display for easy navigation through multiple scripts.
- Simple user interface for selecting and running scripts.
- Example scripts included: Gemini chat, sd mount, print mac address

## Installation
- Python scripts should be placed in a folder named `scripts` both on the SD card and in the root directory.
- Copy code.py to your device and run the code to start selecting scripts.
- To use the Gemini chat, you need the sdmount script in `lib` folder and you gemini api key in the settings.toml file. An sd card is also needed to read and write wifi details. 
