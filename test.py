import pyaudio

# PyAudio örneği oluşturun
audio = pyaudio.PyAudio()

# USB ses aygıtını bulun
info = audio.get_host_api_info_by_index(1)
numdevices = info.get('deviceCount')
usb_device_index = None

print("Sistemdeki ses aygıtları:")

for i in range(0, numdevices):
    device_info = audio.get_device_info_by_host_api_device_index(0, i)
    device_name = device_info.get('name')
    print(f"İndeks: {i}, Aygıt Adı: {device_name}")
    if "USB" in device_name:
        usb_device_index = i

if usb_device_index is None:
    print("USB ses aygıtı bulunamadı.")
else:
    print(f"USB ses aygıtı indeksi: {usb_device_index}")

audio.terminate()
