import wifi
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
