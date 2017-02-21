#!/usr/bin/env python
# coding: latin-1
# A bunch of naive pythons functions to decode somes ais_data/AIVDM messages:
# try with !AIVDO,1,1,,,B00000000868rA6<H7KNswPUoP06,0*6A
# doc : http://catb.org/gpsd/AIVDM.html
#################################################################################
# HOW TO USE IT :
# msg = '!AIVDO,1,1,,,B00000000868rA6<H7KNswPUoP06,0*6A' 
# ais_data = decod_ais(msg)
# ais_format = format_ais(ais_data)
# print ais_data, ais_data['lon'], ais_format['lon']
#################################################################################

def sign_int(s_bytes):
    # converts signed pack of bytes (as a string) to signed int
    # @param s_bytes (string) : '1001001010010010...'
    # @return (int) : signed integer 
    temp = s_bytes
    if s_bytes[0]=='1':
        l = temp.rfind('1') #find last one
        temp2=temp[:l].replace('1', '2')
        temp2=temp2.replace('0', '1')
        temp2=temp2.replace('2', '0')
        temp=temp2+temp[l:]
        return -int(temp,2)
    else:
        return int(temp,2)

def compute_checksum(msg):
    # compute the checksum of an AIS sentense by XOR every char
    # then confront it to the checksum validator
    # @param (string) msg : one AIS sentense '!AIVDO,1,1,,,B00000000868rA6<H7KNswPUoP06,0*6A'
    # @return (string) : string representation of hexadecimal sum of XORing every char bitwise
    end = msg.rfind('*') # we're gonna read from after '?'' to before '*
    start = 0
    if msg[0] in ('$','!'): start=1 # reading after '!' if it exists
    chcksum = 0
    for c in msg[start:end]: # for every char in the ais sentenses (comma included)
        chcksum = chcksum ^ ord(c) # compare them with the x-or operator '^'
    sumHex = "%x" % chcksum # makes it hexadecimal
    return sumHex.zfill(2).upper()

##############################################################################

def get_payload(msg):
    # read the ais sentense and return the payload
    # @param (string) msg : one AIS sentense '!AIVDM,2,1,3,B,55P5TL01VIaAL@7WKO@mBplU@<PDhh000000001S;AJ::4A80?4i@E53,0*3E'
    # @return (string) : the payload '55P5TL01VIaAL@7WKO@mBplU@<PDhh000000001S;AJ::4A80?4i@E53'
    return msg.split(',')[5]

def get_sentense_number(msg):
    # read the ais sentense and return the number of sentenses the payload is splitted in
    # @param (string) msg : one AIS sentense '!AIVDM,2,1,3,B,55P5TL01VIaAL@7WKO@mBplU@<PDhh000000001S;AJ::4A80?4i@E53,0*3E'
    # @return (string) number of sentenses: '2'
    return msg.split(',')[1]

def get_sentense_count(msg):
    # read the ais sentense and return the number of the sentense
    # @param (string) msg : one AIS sentense '!AIVDM,2,1,3,B,55P5TL01VIaAL@7WKO@mBplU@<PDhh000000001S;AJ::4A80?4i@E53,0*3E'
    # @return (string) the number of the current: '1'
    return msg.split(',')[2]

def get_checksum(msg):
    # read the ais sentense and return the number of the sentense
    # @param (string) msg : one AIS sentense '!AIVDM,2,1,3,B,55P5TL01VIaAL@7WKO@mBplU@<PDhh000000001S;AJ::4A80?4i@E53,0*3E'
    # @return (string) checksum validator: '3E'
    return msg.split('*')[-1]

##############################################################################

def decod_payload(payload):
    # convert the payload from ASCII char to their 6-bits representation for every char
    # doc : http://catb.org/gpsd/AIVDM.html#_aivdm_aivdo_payload_armoring
    # @param (string) payload : '177KQ' up to 82 chars
    # @return (string) data :  '000001000111000111011011100001'
    data = ''
    for i in range(len(payload)):
        char = ord(payload[i])-48
        if char>40:
            char = char -8
        bit = '{0:b}'.format(char)
        bit = bit.zfill(6) # makes it a full 6 bits
        data = data + bit
    return data

def decod_6bits_ascii(bits):
    # decode 6bits into an ascii char, with respect to the 6bits ascii table
    # doc : http://catb.org/gpsd/AIVDM.html#_ais_payload_data_types
    # @param (string) bits : '101010'
    # @return (char) a ascii charater : '*'
    letter = int(bits,2)
    if letter < 32:
        letter+=64
    return chr(letter)

def decod_str(data):
    # decode a string of bits to an ascii one with respect to the 6bits ascii table
    # doc : http://catb.org/gpsd/AIVDM.html#_ais_payload_data_types
    # @param (string) data : a string of bits  '000001000001000001'
    # @return (string) a string of bits : 'AAA'
    name = ''
    for k in range(len(data)/6):
        letter = decod_6bits_ascii(data[6*k:6*(k+1)])
        if letter != '@':
            name += letter
    return name

def decod_data(data):
    # decode AIS payload and return a dictionnary with key:value
    # doc : http://catb.org/gpsd/AIVDM.html
    # @param (string) data : '11110011000101....' by pack of 6 bits
    # @return (dict) ais_data : {'type':18, etc...}
    type_nb = int(data[0:6],2)

    def decod_5(data):
        ais_data                 = {'type':int(data[0:6],2)}
        ais_data['repeat']       = int(data[6:8],2)
        ais_data['mmsi']         = int(data[8:38],2)
        ais_data['ais_version']  = int(data[38:40],2)
        ais_data['imo']          = int(data[40:70],2)
        ais_data['callsign']     = decod_str(data[70:112])
        ais_data['shipname']     = decod_str(data[112:232])
        ais_data['shiptype']     = int(data[232:240],2)
        ais_data['to_bow']       = int(data[240:249],2)
        ais_data['to_stern']     = int(data[249:258],2)
        ais_data['to_port']      = int(data[258:264],2)
        ais_data['to_starboard'] = int(data[264:270],2)
        ais_data['epfd']         = int(data[270:274],2)
        ais_data['month']        = int(data[274:278],2)
        ais_data['day']          = int(data[278:283],2)
        ais_data['hour']         = int(data[283:288],2)
        ais_data['minute']       = int(data[288:294],2)
        ais_data['draught']      = int(data[294:302],2)*10
        ais_data['dte']          = data[302]
        return ais_data

    def decod_18(data):
        ais_data             = {'type':int(data[0:6],2)}
        ais_data['repeat']   = int(data[6:8],2)
        ais_data['mmsi']     = int(data[8:38],2)
        ais_data['speed']    = int(data[46:56],2)
        ais_data['accuracy'] = data[56]
        ais_data['lon']      = sign_int(data[57:85])/600000.0
        ais_data['lat']      = sign_int(data[85:112])/600000.0
        ais_data['course']   = int(data[112:124],2)*0.1
        ais_data['heading']  = int(data[124:133],2)
        ais_data['second']   = int(data[133:139],2)
        ais_data['regional'] = int(data[139:141],2)
        ais_data['cs']       = data[141]
        ais_data['display']  = data[142]
        ais_data['dsc']      = data[143]
        ais_data['band']     = data[144]
        ais_data['msg22']    = data[145]
        ais_data['assigned'] = data[146]
        ais_data['raim']     = data[147]
        ais_data['radio']    = int(data[148:168],2)
        return ais_data
    
    def decod_19(data):
        ais_data                 = {'type':int(data[0:6],2)}
        ais_data['speed']        = int(data[46:56],2)
        ais_data['accuracy']     = data[56]
        ais_data['lon']          = sign_int(data[57:85])/600000.0
        ais_data['lat']          = sign_int(data[85:112])/600000.0
        ais_data['course']       = int(data[112:124],2)*0.1
        ais_data['heading']      = int(data[124:133],2)
        ais_data['second']       = int(data[133:139],2)
        ais_data['regional']     = int(data[139:143],2)
        ais_data['shipname']     = decod_str(data[143:263])
        ais_data['to_bow']       = int(data[271:280],2)
        ais_data['to_stern']     = int(data[280:288],2)
        ais_data['to_port']      = int(data[289:295],2)
        ais_data['to_starboard'] = int(data[295:301],2)
        ais_data['epfd']         = int(data[301:305],2)
        ais_data['raim']         = data[305]
        ais_data['dte']          = data[306]
        ais_data['assigned']     = data[307]
        return ais_data

    decod_type = {                              # list of the ais message type we can decode
                    5  : decod_5,
                    18 : decod_18,
                    19 : decod_19,
                 }
    try:
        ais_data = decod_type[type_nb](data)    # try to decode the sentense without assumption of its type
    except:                                     # if it fails, like a type 16 message, execute following code
        print "ERROR : Cannot decode message type "+str(type_nb)
        ais_data = {'type':type_nb}
        #raise                                  # raise will raise the last error (WrongKey) and crash the script
    return ais_data

globPayload = '' # in case of multi-lines sentenses, declare global var to store previous payload
def decod_ais(msg):
    # decode AIS messages, especially AIVDM/AIVDO sentenses:
    # if the message is splitted on several lines, return a dict with 'none' key as 'empty' value
    # if the checksum doesn't correspond, raise and error
    # @param (string) msg : one AIS sentense  '!AIVDO,1,1,,,B00000000868rA6<H7KNswPUoP06,0*6A'
    # @return (dict) ais_data : {'type':18, etc...}
    payload = get_payload(msg)
    s_size  = get_sentense_number(msg)
    s_count = get_sentense_count(msg)

    try:
        assert compute_checksum(msg) == get_checksum(msg)
    except:
        print 'ERROR : Checksum not valid ('+str(checkAis(msg))+'!='+str(get_checksum(msg))+'), message is broken/corrupted'
        raise

    if s_size != '1' :                          # usefull only if multi-line sentenses.
        global globPayload 
        if s_size != s_count:                   # if this isn't the last messages
            globPayload = payload + globPayload # append the current payload to the main payload
            return {'none':'empty'}
        else:
            payload = globPayload + payload     # append the last payload
            globPayload = ''                    # reset the global var for future messages

    data = decod_payload(payload)
    ais_data = decod_data(data)
    return ais_data

##############################################################################

def format_coord(coord_dec,Dir=''):
    # get position in decimal base and return a string with position in arc-base
    # @param (int) coord_dec : degree decimal coordinate 43.29492333333334
    # @param (char) Dir : char to specify the direction like 'N' for North. By default, nothing.
    # @return (string) : a degree,minute,second coordinate + direction  43°17'41.7"N
    tmp = str(coord_dec).split('.')
    deg = float(tmp[0])
    mnt = float('0.'+tmp[1])*60
    tmp = str(mnt).split('.')
    sec = float('0.'+tmp[1])*60
    return str(int(deg))+'°'+str(int(mnt))+"'"+str(sec)[:4]+'"'+Dir

def format_ais(ais_base):
    # format the ais_data database to a more user-friendly display
    # @param (dict) ais_base : the ais_data base to format 
    # @return (dict) ais_format : a dictionnary with the same kay as ais_data but other value
    ais_format = ais_base.copy()

    def format_lat(lat):
        return (format_coord(lat,'N') if lat > 0 else format_coord(lat,'S'))

    def format_lon(lon):          
        return (format_coord(lon,'E') if lon > 0 else format_coord(lon,'W'))

    def format_course(course):
        return 'N/A' if course == 3600 else str(course)+'° relative to North'

    def format_speed(speed):
        if speed == 1023:
            return 'N/A'
        elif speed == 1022:
            return ' > 102 knots'
        else:
            return str(speed*0.1) + ' knots'

    def format_heading(heading):
        return 'N/A' if heading == 511 else str(heading)+'°'

    def format_month(month):
        return 'N/A' if month == 0 else month

    def format_day(day):
        return 'N/A' if day == 0 else day

    def format_hour(hour):
        return 'N/A' if hour == 24 else hour

    def format_minute(minute):
        return 'N/A' if minute == 60 else minute

    def format_second(second):
        if second == 60:
            return 'N/A'
        elif second == 61:
            return 'manual mode'
        elif second == 62:
            return 'EPFS in estimated mode'
        elif second == 63:
            return 'PS inoperative'
        else:
            return second

    def format_cs(cs):
        return 'Class B SOTDMA' if cs == '0' else 'Class B CS'

    def format_display(display):
        return 'N/A' if display == '0' else 'Display available'

    def format_dsc(dsc):
        if dsc == '1':
          return 'VHF voice radio with DSC capability'
  
    def format_band(band):
        if band == '1':
            return 'Can use any frequency of the marine channel'

    def format_msg22(msg22):
        if msg22 == '1':
            return 'Accepts channel assignment via Type 22 Message'

    def format_assigned(assigned):
        if assigned == '0':
            return 'Autonomous mode'

    def format_dte(dte):
        return 'Data terminal ready' if dte == '0' else 'Data terminal N/A'

    def format_epfd(epfd):
        epfd_types = [  'Undefined',
                        'GPS',
                        'GLONASS',
                        'GPS/GLONASS',
                        'Loran-C',
                        'Cayka',
                        'Integrated',
                        'Surveyed',
                        'Galileo' ]
        return epfd_types[epfd]
    

    def format_shiptype(shiptype):
        shiptype_list = [
        "Not available",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Reserved for future use",
        "Wing in ground (WIG) - all ships of this type",
        "Wing in ground (WIG) - Hazardous category A",
        "Wing in ground (WIG) - Hazardous category B",
        "Wing in ground (WIG) - Hazardous category C",
        "Wing in ground (WIG) - Hazardous category D",
        "Wing in ground (WIG) - Reserved for future use",
        "Wing in ground (WIG) - Reserved for future use",
        "Wing in ground (WIG) - Reserved for future use",
        "Wing in ground (WIG) - Reserved for future use",
        "Wing in ground (WIG) - Reserved for future use",
        "Fishing",
        "Towing",
        "Towing: length exceeds 200m or breadth exceeds 25m",
        "Dredging or underwater ops",
        "Diving ops",
        "Military ops",
        "Sailing",
        "Pleasure Craft",
        "Reserved",
        "Reserved",
        "High speed craft (HSC) - all ships of this type",
        "High speed craft (HSC) - Hazardous category A",
        "High speed craft (HSC) - Hazardous category B",
        "High speed craft (HSC) - Hazardous category C",
        "High speed craft (HSC) - Hazardous category D",
        "High speed craft (HSC) - Reserved for future use",
        "High speed craft (HSC) - Reserved for future use",
        "High speed craft (HSC) - Reserved for future use",
        "High speed craft (HSC) - Reserved for future use",
        "High speed craft (HSC) - No additional information",
        "Pilot Vessel1",
        "Search and Rescue vessel",
        "Tug",
        "Port Tender",
        "Anti-pollution equipment",
        "Law Enforcement",
        "Spare - Local Vessel",
        "Spare - Local Vessel",
        "Medical Transport",
        "Ship according to RR Resolution No. 18",
        "Passenger - all ships of this type",
        "Passenger - Hazardous category A",
        "Passenger - Hazardous category B",
        "Passenger - Hazardous category C",
        "Passenger - Hazardous category D",
        "Passenger - Reserved for future use",
        "Passenger - Reserved for future use",
        "Passenger - Reserved for future use",
        "Passenger - Reserved for future use",
        "Passenger - No additional information",
        "Cargo - all ships of this type",
        "Cargo - Hazardous category A",
        "Cargo - Hazardous category B",
        "Cargo - Hazardous category C",
        "Cargo - Hazardous category D",
        "Cargo - Reserved for future use",
        "Cargo - Reserved for future use",
        "Cargo - Reserved for future use",
        "Cargo - Reserved for future use",
        "Cargo - No additional information",
        "Tanker - all ships of this type",
        "Tanker - Hazardous category A",
        "Tanker - Hazardous category B1",
        "Tanker - Hazardous category C1",
        "Tanker - Hazardous category D1",
        "Tanker - Reserved for future use",
        "Tanker - Reserved for future use",
        "Tanker - Reserved for future use",
        "Tanker - Reserved for future use",
        "Tanker - No additional information",
        "Other Type - all ships of this type",
        "Other Type - Hazardous category A",
        "Other Type - Hazardous category B",
        "Other Type - Hazardous category C",
        "Other Type - Hazardous category D",
        "Other Type - Reserved for future use",
        "Other Type - Reserved for future use",
        "Other Type - Reserved for future use",
        "Other Type - Reserved for future use",
        "Other Type - no additional information"
        ]
        return shiptype_list[shiptype]

    format_list = {                                                #list of all the key that can be formatted 
                  'lat'      : format_lat,
                  'lon'      : format_lon,
                  'course'   : format_course,
                  'speed'    : format_speed,
                  'heading'  : format_heading,
                  'second'   : format_second,
                  'cs'       : format_cs,
                  'display'  : format_display,
                  'dsc'      : format_dsc,
                  'band'     : format_band,
                  'msg22'    : format_msg22,
                  'assigned' : format_assigned,
                  'dte'      : format_dte,
                  'epfd'     : format_epfd,
                  'shiptype' : format_shiptype,
                  'month'    : format_month,
                  'day'      : format_day,
                  'hour'     : format_hour,
                  'minute'   : format_minute
                  }

    for key in ais_base.keys():                                 #for every key we have
        if format_list.has_key(key):                            #if we can format it
            ais_format[key] = format_list[key](ais_format[key]) #format it

    return ais_format

##############################################################################
