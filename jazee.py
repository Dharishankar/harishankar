import warnings
warnings.filterwarnings('ignore')

import requests,json,re,pytz
from datetime import datetime



def clean(match,repl,strg):
        return re.sub(match,repl,str(strg))
#          
def regMatch(patn, blk, cln=False,repl=["'","''"]):
    if cln:
        return clean(repl[0],repl[1],re.search(patn, blk).group(1) if re.search(patn, blk) else '')
    else:
        return re.search(patn, blk).group(1) if re.search(patn, blk) else ''
 
def jsonMatch(key, subj, cln=False,repl=["'","''"]):
    if key in subj:
        c = subj[key] if subj[key] else ''
        return clean(repl[0], repl[1], c) if c and cln else c
    else:
        return ''
#    
def gettingtimezone(airportcode):
    url = "https://airports-api.s3-us-west-2.amazonaws.com/iata/{airportcode.lower()}.json"
    try:loczone = requests.get(url).json()['timezone']
    except:loczone = "UTC"
    blocks[airportcode] = loczone
    return loczone
 
# def timeformat(timevalue):
#     fulltime = datetime.timedelta(days = timevalue.days).total_seconds() + timevalue.total_seconds()
#     hours, minutes = divmod(int(fulltime//60), 60)
#     toreturn = "{hours:02d}:{minutes:02d}"
#     return toreturn

   
def load(flyfrom, Departdate,flyto, returndare, routetype,travelers,priceclass,proxy):
   
    adult=str(travelers['adults'])
    infant=str(travelers['infants'])
    ses=requests.session()
    proxies = {'https':'http://{proxy}'} if proxy else None
    ses.proxies=proxies
    ses.timeout=10
    headers = {'authority': 'j9api.jazeeraairways.com', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"', 'accept': 'application/json, text/plain, */*', 'sec-ch-ua-mobile': '?0', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36', 'content-type': 'application/json', 'origin': 'https://booking.jazeeraairways.com', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://booking.jazeeraairways.com/', 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8', }
   
    data = '{}'
    response = ses.post('https://j9api.jazeeraairways.com/api/Postman/api/nsk/v1/token', headers=headers, data=data)
    data = response.text
#     print(data)
#     exit()
    data = json.loads(data)
   
    token = jsonMatch('token', data['data'])
    # print(token)
   
    '------------------Main Load----------------------'
   
    headers = {'authority': 'j9api.jazeeraairways.com','sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"','accept': 'application/json, text/plain, */*','authorization': token,# 'sec-ch-ua-mobile': '?0','user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','content-type': 'application/json',# 'origin': 'https://booking.jazeeraairways.com',# 'sec-fetch-site': 'same-site',# 'sec-fetch-mode': 'cors',# 'sec-fetch-dest': 'empty', 'referer': 'https://booking.jazeeraairways.com/', 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
               }
    if routetype == 2:
        data = '{"passengers":{"types":[{"type":"ADT","count":"'+adult+'"}],"residentCountry":""},"criteria":[{"stations":{"destinationStationCodes":["'+str(flyto)+'"],"originStationCodes":["'+str(flyfrom)+'"],"searchDestinationMacs":true,"searchOriginMacs":true},"dates":{"beginDate":"'+str(departdate)+'"},"filters":{"maxConnections":10,"compressionType":"CompressByProductClass","exclusionType":"Default"}},{"stations":{"destinationStationCodes":["'+str(flyfrom)+'"],"originStationCodes":["'+str(flyto)+'"],"searchDestinationMacs":true,"searchOriginMacs":true},"dates":{"beginDate":"'+str(returndate)+'"},"filters":{"maxConnections":10,"compressionType":"CompressByProductClass"}}],"codes":{"promotionCode":"","currencyCode":"USD"},"numberOfFaresPerJourney":10}'
    else:
        data = '{"passengers":{"types":[{"type":"ADT","count":"'+adult+'"}],"residentCountry":""},"criteria":[{"stations":{"destinationStationCodes":["'+str(flyto)+'"],"originStationCodes":["'+str(flyfrom)+'"],"searchDestinationMacs":true,"searchOriginMacs":true},"dates":{"beginDate":"'+str(departdate)+'"},"filters":{"maxConnections":10,"compressionType":"CompressByProductClass","exclusionType":"Default"}}],"codes":{"promotionCode":"","currencyCode":"USD"},"numberOfFaresPerJourney":10}'
    response = ses.post('https://j9api.jazeeraairways.com/api/jz/v1/Availability', headers=headers, data=data)
    # open('/home/ai/Documents/jazeer_source.html', 'w').write(str(response.text))
   
    return response

flyfrom    = 'TAS'
flyto      = 'SAW'
departdate = '2021-11-20'
returndate = '2021-11-07'
routetype  = 1
priceclass = 1
travelers  = {'adults':1,'infants':0}
proxy      = ''
los        = None
pos        = None
source     = ''
refid      = ''

response = load(flyfrom, departdate,flyto,returndate,routetype,travelers,priceclass,proxy)
html = response.text
open(r'C:\Users\haris\Desktop\jazeer_html.html','w').write(html)
# exit()
j=json.loads(html)

outbound=[]
inbound=[]
totalbound=[]


for count, bounds in enumerate(j['data']['availabilityv4']['results']):
    print('count:',count)
    for flight in bounds['trips']:
       
        stopls=[]
        Airlinels=[]
        Aircraftls=[]
        waitls=[]
                 
        for segments in flight['journeysAvailableByMarket'][0]['value'][0]['segments']:
            blocks = segments['legs'][0]['legInfo']

            Aircraft = blocks['prbcCode']
            print('Airlinecode:',Aircraft)
            origin = segments['designator']['origin']
            print('origin:',origin)
            Desti = segments['designator']['destination']
            print('Destination:',Desti)
            av = segments['designator']['arrival']
            Arrivaldate=re.match("(.*?)T(.*)",(av)).group(1)
            Arritime=re.match("(.*?)T(.*)",(av)).group(2)
            dd = segments['designator']['departure']
            Departdate=re.match("(.*?)T(.*)",(dd)).group(1)
            print('Departdate:',Departdate)
            Departime=re.match("(.*?)T(.*)",(dd)).group(2)
            print('Departure time:',Departime)
            print('Arrivaldate',Arrivaldate)
            print('Arritime',Arritime)
#             print(type(Departime))
#             pytz.timezone('Asia/samarkand').localize(datetime.datetime(2021-11-20)).strftime('%z')

            d = datetime.strptime(Departdate+' '+Departime,'%Y-%m-%d %H:%M:%S')
            url = "https://airports-api.s3-us-west-2.amazonaws.com/iata/"+str(origin.lower())+".json"
            try:
                loczone = requests.get(url).json()['timezone']
                print("loczone:",loczone)
                   
            except:
                loczone  = "UTC"
               
            local_time = pytz.timezone(loczone)
            Dlocal_datetime = local_time.localize(d)
            print('D.localtime:',Dlocal_datetime)
                       
            a = datetime.strptime(Arrivaldate+' '+Arritime,'%Y-%m-%d %H:%M:%S')
            url = "https://airports-api.s3-us-west-2.amazonaws.com/iata/"+str(Desti.lower())+".json"
            try:
                loczone = requests.get(url).json()['timezone']
                print("loczone:",loczone)
                     
            except:
                loczone  = "UTC"
                 
            local_time = pytz.timezone(loczone)
            Alocal_datetime = local_time.localize(a)
            print('A.localtime:',Alocal_datetime)  
            Ftime =Alocal_datetime - Dlocal_datetime
            print('Flighttime',Ftime)
#             rawwaittime = datetime.strptime(flight("layoverTime", blocks), "%Hh%Mm")
#             waittime    = rawwaittime.strftime("%H:%M")
           
#             waittime = datetime.strptime(Arrivallocal_time,'%H:%M:%S')-datetime.strptime(Departurelocal_time,'%H:%M:%S')
#             print('Waitime:',waittime)
       
#             Dutc = local_datetime.astimezone(pytz.utc).strftime('%H:%M:%S')
#             print('Depart LocalTime:',Dutc)
#                            
#             a = datetime.strptime(Arrivaldate+' '+Arritime,'%Y-%m-%d %H:%M:%S')
#             local_time = pytz.timezone(loczone)
#             naive_datetime = datetime.strptime(datetime_str,format)
#              local_datetime = local_time.localize(a)
#             Autc= local_datetime.astimezone(pytz.utc).strftime('%H:%M:%S')
#             print('Arrival LocalTime:',Autc)
#            
#             Ftime =datetime.strptime(Autc,'%H:%M:%S')-datetime.strptime(Dutc,'%H:%M:%S')
#             print('Flighttime',Ftime)
#            
#             Duration = datetime.strptime(str(Ftime),'%H:%M:%S').strftime('%M:%H:%S')
           


#             print('Flighttime:',flighttime)
#             duration = datetime.datetime.strptime(str(flighttime),'%H:%M:%S').strftime('%H:%M:%S')
#             print("Duration:",duration)
#             local_time = pytz.timezone(datetime_str)
#             naive_datetime = datetime.datetime.strptime ( datetime_str,format)
#             local_datetime = local_time.localize(naive_datetime)
#             utc_datetime = local_datetime.astimezone(pytz.utc).strftime('%H:%M:%S')
#             print('LocalTime:',utc_datetime)
                               
#             rawwaittime = datetime.datetime.strptime(datetime_str("layoverTime", blocks), "%H%M")
#             waittime    = rawwaittime.strftime("%H:%M")
#             print('Waittime:',waittime)
                   
#             ddtraw  = datetime.datetime.strptime("{Departdate} {Departime}", "%Y-%m-%d %H:%M")
#             adtraw  = datetime.datetime.strptime("{Arrivaldate} {Arritime}", "%Y-%m-%d %H:%M")
#             depzone = segments[origin] if origin in segments else gettingtimezone(origin)
#             arrzone = segments[Arritime] if Arritime in segments else gettingtimezone(Arritime)
#             chkdep  = pytz.timezone(depzone).localize(ddtraw)#ddtraw.replace(tzinfo=pytz.timezone(depzone))
#             chkarr  = pytz.timezone(arrzone).localize(adtraw)#adtraw.replace(tzinfo=pytz.timezone(arrzone))
#             flttime = timeformat(chkarr-chkdep)
#             layovertime =+ int(((rawwaittime.hour * 60) + rawwaittime.minute))
 
            Airlineno = segments['identifier']['carrierCode']
            print('Airlinenumber:',Airlineno)
            flino = segments['identifier']['identifier']
            print('Flightnumber:',flino)
#             rawwaittime = datetime.datetime.strptime(flight("layoverTime", blocks),"%H:%M:%S")
#             waittime    = rawwaittime.strftime("%H:%M:%S")
#             print('Waittime',waittime)
                   
            print('*'*100)
 
            facilities = {"faretype":None,"carryonbaggage":{"General":None,"1xfree_bag":None,"2xfree_bag":None,"3xfree_bag":None},"checkedbaggage":{"General":None,"1st_checkedbag":None,"2nd_checkedbag":None,"prioritybaggage":None},"miles":{"50%_miles":None,"100%_miles":None,"150%_miles":None,"200%_miles":None,"miles_earned":None},"snacks":None,"meals":None,"alcoholicdrinks":None,"wifi":None,"loungeaccess":None,"cancellation":None,"changes":None,"seatchoice":None,"prioritycheckin":None,"prioritysecurity":None,"premiumseating":None,"priorityboarding":None}
            stop =({"origin":origin,"Destination":Desti,"description":None,"Departuredate":Departdate,"Departuretime": Departime,"Arrivaldate":Arrivaldate,"Arrivaltime":av, "Flightno":flino,"flighttime":'',"Waitime":"", "facilities":facilities,"airlinename":"", "aircraft":"","distance":None})
            stopls.append(stop)
           
#         layover     = timeformat(datetime.timedelta(minutes=int(layovertime)))
#         stop_count  = jsonMatch('numberOfLayovers', segments)
     
        if len(list(set(Aircraftls))) > 1:                
            aircraftchange = 1
        else:
            aircraftchange = 0
                   
        if len(list(set(Airlinels))) > 1:
            multipleairline = 1
        else:
            multipleairline = 0
                         
        for price in j['data']['availabilityv4']['faresAvailable']:
            price=price['value']['totals']
#             print(price)
            Amount = price['fareTotal']
            print("price:",Amount)
           
            if 'availabilityv4' in (j['data']):
                ava=j['data']['availabilityv4']
                a1=ava['currencyCode']
                print("currency:",a1)
           

                if ava:
                    flight_statuscode=200
                    taxstatus=1
                else:
                    flight_statuscode=201
                    taxstatus=None
                    print("="*10)  
                stopcount=len(stopls)-1 if stopls else 0
                print(stopcount)
           
                if count==0:
                    outbound.append({'multipleairline':multipleairline, 'layover':'0:00',  'basefare':0, 'aircraftchange':aircraftchange, "price":Amount,"priceclass":"","currency":a1,"feesandothers":0,"description":'',"numofstops":stopcount,"stop":stopls,"flight_statuscode":flight_statuscode,"taxstatus":taxstatus})
                else:
                    inbound.append({'multipleairline':multipleairline, 'laytover':'0:00',  'basefare':0, 'aircraftchange':aircraftchange, "price":Amount,"priceclass":"","currency":a1,"feesandothers":0,"description":'',"numofstops":stopcount,"stop":stopls,"flight_statuscode":flight_statuscode,"taxstatus":taxstatus})

open(r'C:\Users\haris\Desktop\outbound.text','w').write(json.dumps(outbound))
open(r'C:\Users\haris\Desktop\inbound.text','w').write(json.dumps(inbound))
if routetype==2:
   
    for outbound_ in outbound:
        for inbound_ in inbound:
            totalbound.append({'outbound':outbound_,'inbound':inbound_})
else:
    for outbound_ in outbound:
        totalbound.append({'outbound':outbound_})
       
open(r'C:\Users\haris\Desktop\totalbound.text','w').write((json.dumps(totalbound)))

jdata={"cabinclass":priceclass,"refid":refid,"flyfrom":flyfrom,"flyto":flyto,"routetype":routetype,"departdate":"Departdate","returndate":returndate,"los":los,"travellers":"","source":source,"pos":pos,"details":totalbound,"totaldistance":"","dtcollected":"","status_code":0}
# print(jdata)
open(r'C:\Users\haris\Desktop\jdata.text','w').write((json.dumps(jdata)))
 
