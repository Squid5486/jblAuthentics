import socket
import xml.etree.ElementTree as ET
import time

lastRequest = time.time()

host = '192.168.0.192' # JBL Authentics ip address
port = 10025
debug = False
packageSendDelay = 0.4 # sec delay between packages being sent.
sources = ["Bluetooth", "dlna", "phono", "AUX", "OPTICAL1", "Airplay"]

def prepareMessage(payload):
    # send a message
    message = "POST MM HTTP/1.1\r\n"
    message += "Host: :10025\r\n"
    message += "User-Agent: Harman Remote Controller/1.0"
    message += "Content-Length: {}\r\n".format(len(payload))
    message += "\r\n"
    message += payload
    return message

def getVolume():
    # get volume
    payload = '<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>query-status</name> <zone>Main Zone</zone> <para>volume</para> </control> </common> </mm> </harman>'
    waitForResponse = True
    response = sendMessage(payload, waitForResponse)
    # parse the XML string
    root = ET.fromstring(response)
    # find the volume parameter
    volume = root.find(".//status[name='volume']/para").text
    return volume

def setVolume(volume):
    # set volume
    payload = f'<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>set_system_volume</name> <zone>Main Zone</zone> <para>{volume}</para> </control> </common> </mm> </harman>'
    waitForResponse = False
    sendMessage(payload, waitForResponse)

def getEqualizerSettings():
    payload = '<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>query-status</name> <zone>Main Zone</zone> <para>bass_level</para> </control> </common> </mm> </harman>'
    waitForResponse = True
    response = sendMessage(payload, waitForResponse)
    start = "<para>"
    end = "</para>"
    return response[response.find(start) + len(start):response.find(end)]

def getDeviceName():
    payload = '<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>query-status</name> <zone>Main Zone</zone> <para>device_name</para> </control> </common> </mm> </harman>'
    waitForResponse = True
    response = sendMessage(payload, waitForResponse)
    start = "<para>"
    end = "</para>"
    return response[response.find(start) + len(start):response.find(end)]

def getSource():
    payload = '<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>query-status</name> <zone>Main Zone</zone> <para>source</para> </control> </common> </mm> </harman>'
    waitForResponse = True
    response = sendMessage(payload, waitForResponse)
    start = "<para>"
    end = "</para>"
    return response[response.find(start) + len(start):response.find(end)]

def setSource(source):
    # set volume
    payload = f'<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>source-selection</name> <zone>Main Zone</zone> <para>{source}</para> </control> </common> </mm> </harman>'
    waitForResponse = False
    sendMessage(payload, waitForResponse)

def setBassLevel(level):
    # set volume
    payload = f'<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>set_bass_level</name> <zone>Main Zone</zone> <para>{level}</para> </control> </common> </mm> </harman>'
    waitForResponse = False
    sendMessage(payload, waitForResponse)

def setMidLevel(level):
    # set volume
    payload = f'<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>set_mid_level</name> <zone>Main Zone</zone> <para>{level}</para> </control> </common> </mm> </harman>'
    waitForResponse = False
    sendMessage(payload, waitForResponse)

def setHighLevel(level):
    # set volume
    payload = f'<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>set_high_level</name> <zone>Main Zone</zone> <para>{level}</para> </control> </common> </mm> </harman>'
    waitForResponse = False
    sendMessage(payload, waitForResponse)

def heartAlive(): # probably not needed
    payload = '<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>heart-alive</name> <zone></zone> <para></para> </control> </common> </mm> </harman>'
    waitForResponse = True
    response = sendMessage(payload, waitForResponse)
    print(response)

def getClariFiStatus(): # experimental
    # get status
    payload = '<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>query-status</name> <zone>Main Zone</zone> <para>signal_doctor</para> </control> </common> </mm> </harman>'
    waitForResponse = True
    response = sendMessage(payload, waitForResponse)
    print(response)

def setClariFiStatus(level): # experimental, for some reason <para>on||0</para> can be on and 0 at the same time
    if level <= -1:
        parameter = "off||0"
    else:
        parameter = f"on||{level}"
    payload = f'<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>signal_doctor_control</name> <zone>Main Zone</zone> <para>{parameter}</para> </control> </common> </mm> </harman>'
    waitForResponse = False
    sendMessage(payload, waitForResponse)

def getSpectrumData(): # experimental
    # get status
    payload = '<?xml version="1.0" encoding="UTF-8"?> <harman> <mm> <common> <control> <name>query-status</name> <zone>Main Zone</zone> <para>spectrum_data</para> </control> </common> </mm> </harman>'
    waitForResponse = True
    response = sendMessage(payload, waitForResponse)
    print(response)
    

def sendMessage(payload, waitForResponse):
    time.sleep(packageSendDelay) # This isnt the prettiest solution, but it works. I ran into problems with sending packages too fast 

    # create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    message = prepareMessage(payload)
    if debug:
        print("message\n", message)
    s.sendall(message.encode())

    if waitForResponse:
        # receive the response
        data = s.recv(1024)

    # close the socket
    s.close()

    if waitForResponse:
        response = data.decode('utf-8', 'backslashreplace') # i got into problems here without "backslashreplace" as a option
        return response.split("\n")[-1]

def main():  
    print(getDeviceName())
    print(getVolume())
    # setVolume(9)
    print(getSource())
    # setSource(sources[3])
    print(getEqualizerSettings())
    # getStatus()
    # getHeartAlive()
    # getSpectrumData()

if __name__ == '__main__':
    main()