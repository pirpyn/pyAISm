import socket

import pyAISm


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


######################################################################################

def count_message_types_example():
    """
    Example for decoding a file and counting the number of message per type
    :return: 
    """
    with open("ais.exploratorium.edu", "r") as file:
        message_types = dict()
        for aline in file:
            try:
                msg = aline.rstrip("\n")
                ais_data = pyAISm.decod_ais(msg)  # Return a dictionnary
                if 'type' in ais_data:
                    if ais_data['type']:
                        msg_type = ais_data['type']
                        if msg_type in message_types:
                            message_types[msg_type] += 1
                        else:
                            message_types[msg_type] = 1
            except pyAISm.UnrecognizedNMEAMessageError as e:
                pass
            except pyAISm.BadChecksumError as e:
                pass
            except Exception as e:
                print e
        print('End of file')
        print(message_types)


######################################################################################

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

