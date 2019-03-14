# pyAISm

A small and incomplete python decoder for AIS messaging.

A bunch of naive pythons functions to decode somes ais_data/AIVDM messages:

Based on the doc here: (http://catb.org/gpsd/AIVDM.html).

## How to use it
In python 2 console:
```python
> msg = '!AIVDO,1,1,,,B00000000868rA6<H7KNswPUoP06,0*6A'  # standard AIVDO sentence as a string
> ais_data = decod_ais(msg)         # Return a dictionnary
> ais_format = format_ais(ais_data) # A more human readable dictionnary
> print ais_data, ais_data['lon'], ais_format['lon'] # Accessing the value of the key
```

Decode a file:
```python
def decode_file_example():
    """
    Example for decoding a file
    :return:
    """
    with open("ais.exploratorium.edu", "r") as file:
        for aline in file:
            try:
                msg = aline.rstrip("\n")
                ais_data = pyAISm.decod_ais(msg)  # Return a dictionnary
                ais_format = pyAISm.format_ais(ais_data)  # A more human readable dictionnary
                print(ais_format)  # Accessing the value of the key
            except pyAISm.UnrecognizedNMEAMessageError as e:
                print e
            except pyAISm.BadChecksumError as e:
                print e
            except Exception as e:
                print e
        print('End of file')
```

Decode a stream:
```python
def decode_stream_example():
    """
    Example for decoding an online data stream
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("ais.exploratorium.edu", 80))
    s.sendall("GET / HTTP/1.1\r\nHost: www.cnn.com\r\n\r\n".encode())
    while (True):
        msg = (s.recv(4096).decode('utf-8')).splitlines()
        for m in msg:
            try:
                msg = m.rstrip("\n")
                ais_data = pyAISm.decod_ais(msg)  # Return a dictionnary
                ais_format = pyAISm.format_ais(ais_data)  # A more human readable dictionnary
                print(ais_format)  # Accessing the value of the key
            except pyAISm.UnrecognizedNMEAMessageError as e:
                print e
            except pyAISm.BadChecksumError as e:
                print e
            except Exception as e:
                print e
```