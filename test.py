import pyaudio

p = pyaudio.PyAudio()

print("USB audio input cihazları:")

usb_device_index = None
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if device_info["maxInputChannels"] > 0 and "USB" in device_info["name"]:
        usb_device_index = i
        print(f"Device ID: {i} - Name: {device_info['name']}")

if usb_device_index is None:
    print("USB audio input cihazı bulunamadı.")

p.terminate()
