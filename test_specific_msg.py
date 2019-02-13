import pyAISm

file = open("ais.exploratorium.edu", "r")
message_types = dict()
for aline in file:

    try:
        msg = aline.rstrip("\n")
        ais_data = pyAISm.decod_ais(msg)  # Return a dictionnary

        if 'type' in ais_data:
            msg_type = ais_data['type']
            if msg_type in message_types:
                message_types[msg_type] += 1
            else:
                message_types[msg_type] = 1
            ais_format = pyAISm.format_ais(ais_data)  # A more human readable dictionnary
            if msg_type == 24:
                print(ais_format)  # Accessing the value of the key
    except pyAISm.UnrecognizedNMEAMessageError as e:
        print(e)
    except pyAISm.BacChecksumError as e:
        print(e)
    except Exception as e:
        print(e)

file.close()
print(message_types) #{4: 1998, 3: 10303, 18: 2438, 1: 59644, 21: 2880, 24: 2208, 5: 1660, 8: 1126, 20: 509, 15: 106, 42: 13, 19: 1}
print('End of file')
