import pyAISm
file = open("ais.exploratorium.edu", "r")

for aline in file:
    try:
        msg = aline.rstrip("\n")
        ais_data = pyAISm.decod_ais(msg)  # Return a dictionnary
        ais_format = pyAISm.format_ais(ais_data)  # A more human readable dictionnary
        print(ais_format)  # Accessing the value of the key
    except pyAISm.UnrecognizedNMEAMessageError as e:
        print(e)
    except pyAISm.BacChecksumError as e:
        print(e)
    except Exception as e:
        print(e)

file.close()

print('End of file')
