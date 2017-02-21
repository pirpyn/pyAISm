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
