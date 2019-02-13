import socket

import pyAISm

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("ais.exploratorium.edu", 80))
s.sendall("GET / HTTP/1.1\r\nHost: www.cnn.com\r\n\r\n".encode())
while (1):
    msg = (s.recv(4096).decode('utf-8')).splitlines()
    for m in msg:
        try:
            msg = m.rstrip("\n")
            ais_data = pyAISm.decod_ais(msg)  # Return a dictionnary
            ais_format = pyAISm.format_ais(ais_data)  # A more human readable dictionnary
            print(ais_format)  # Accessing the value of the key
        except pyAISm.UnrecognizedNMEAMessageError as e:
            print(e)
        except pyAISm.BacChecksumError as e:
            print(e)
        except Exception as e:
            print(e)
s.close
