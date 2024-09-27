# M5Stack Cardputer Script Selector

This project provides a script selection menu for the M5Stack cardputer, allowing users to easily choose and run Python scripts stored on the device. The menu displays a paginated list of available scripts, enabling navigation through the options. Users can run selected scripts directly from the menu, enhancing the functionality of their cardputer setup.

## Features
- Lists Python scripts from the internal storage and optionally from an external SD card.
- Automatically adds the `lib` folder from the SD card to the `sys.path` for importing additional libraries.
- Paginated display for easy navigation through multiple scripts.
- Simple user interface for selecting and running scripts.

## Installation
- Python scripts should be placed in a folder named `sketches` both on the SD card and in the root directory.
- Copy code.py to your device and run the code to start selecting scripts.
