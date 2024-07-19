import pyaudio

def list_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(0, num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        print(f"Device ID {i} - {device_info['name']}")

list_devices()
