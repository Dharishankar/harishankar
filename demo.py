import warnings
warnings.filterwarnings('ignore')

import requests, re, json,datetime

travelers   = {"adults": 1,  "infant": 0}
flyfrom     = 'LAX'
flyto       = 'GYE'
routetype   = 1
departdate  = '2023-07-25'
returndate  = '2023-12-30'
source      = 0
proxy       = ''
refid       = ""
priceclass  = 1
pos         = None
proxy_state = False 
los = 1

def clean(self,match,repl,strg):
    return re.sub(match,repl,str(strg))
 
def jsonMatch(key, subj, cln=False,repl=["'","''"]):
    if key in subj:
        c = subj[key] if subj[key] else ''
        return clean(repl[0], repl[1], c) if c and cln else c
    else:
        return ''
     
def regMatch(patn, blk, cln=False,repl=["'","''"]):
    if cln:
        return clean(repl[0],repl[1],re.search(patn, blk).group(1) if re.search(patn, blk) else '')
    else:
        return re.search(patn, blk).group(1) if re.search(patn, blk) else ''   

# lam1=[]
# lam2=[]
    
def load(flyfrom,flyto,proxy,routetype,departdate,returndate,travelers,priceclass):
    proxies = {"https": "http://%s"%proxy} if proxy else None
    ses     = requests.Session();ses.proxies=proxies
    ses.verify=False;ses.timeout=15
    headers = {'authority': 'www.latamairlines.com','pragma': 'no-cache','cache-control': 'no-cache','sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"','x-latam-client-name': 'web-air-offers','sec-ch-ua-mobile': '?0','x-latam-app-session-id': 'e62bf546-be72-428e-8220-e77b12534ca7','x-latam-application-lang': 'en','x-latam-track-id': '6afd367d-b61b-48cc-9f07-4a1f4f539d8c','content-type': 'application/json','user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36','x-latam-application-oc': 'us','x-latam-application-name': 'web-air-offers','x-latam-request-id': 'fa087689-08f2-4687-9215-1e9bfd2d1615','x-latam-application-country': 'US','sec-ch-ua-platform': '"Linux"','accept': '*/*','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','referer': 'https://www.latamairlines.com/us/en/flight-offers?dataFlight=%7B%22tripTypeSelected%22%3A%7B%22label%22%3A%22Ida%20y%20Vuelta%22%2C%22value%22%3A%22RT%22%7D%2C%22cabinSelected%22%3A%7B%22label%22%3A%22Economy%22%2C%22value%22%3A%22Economy%22%7D%2C%22passengerSelected%22%3A%7B%22adultQuantity%22%3A1%2C%22childrenQuantity%22%3A0%2C%22infantQuantity%22%3A0%7D%2C%22originSelected%22%3A%7B%22id%22%3A%22LAX_US_AIRPORT%22%2C%22name%22%3A%22Los%20Angeles%20Intl.%22%2C%22city%22%3A%22Los%20Angeles%22%2C%22cityIsoCode%22%3A%22LAX%22%2C%22country%22%3A%22United%20States%22%2C%22iata%22%3A%22LAX%22%2C%22latitude%22%3A33.94250107%2C%22longitude%22%3A-118.4079971%2C%22timezone%22%3A-8%2C%22tz%22%3A%22America%2FLos_Angeles%22%2C%22type%22%3A%22AIRPORT%22%2C%22countryAlpha2%22%3A%22US%22%2C%22allAirportsText%22%3Anull%2C%22airportIataCode%22%3A%22LAX%22%7D%2C%22destinationSelected%22%3A%7B%22id%22%3A%22GYE_EC_AIRPORT%22%2C%22name%22%3A%22Jj%20De%20Olmedo%20Intl.%22%2C%22city%22%3A%22Guayaquil%22%2C%22cityIsoCode%22%3A%22GYE%22%2C%22country%22%3A%22Ecuador%22%2C%22iata%22%3A%22GYE%22%2C%22latitude%22%3A-2.1574199199699997%2C%22longitude%22%3A-79.88359832760001%2C%22timezone%22%3A-5%2C%22tz%22%3A%22America%2FGuayaquil%22%2C%22type%22%3A%22AIRPORT%22%2C%22countryAlpha2%22%3A%22EC%22%2C%22allAirportsText%22%3Anull%2C%22airportIataCode%22%3A%22GYE%22%7D%2C%22dateGoSelected%22%3A%222021-12-20T06%3A30%3A00.000Z%22%2C%22dateReturnSelected%22%3A%222021-12-30T06%3A30%3A00.000Z%22%2C%22redemption%22%3Afalse%7D&sort=RECOMMENDED','accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',}
    if priceclass ==1:
        __class = 'Economy'
#         print(__class)
    if routetype==2:
        params = (('sort', 'RECOMMENDED'),('cabinType', __class),('origin', flyfrom),('destination', flyto),('inFlightDate', 'null'),('inFrom', returndate),('inOfferId', 'null'),('outFlightDate', 'null'),('outFrom', departdate),('outOfferId', 'null'),('adult', str(travelers['adults'])),('child', '0'),('infant', str(travelers['infant'])),('redemption', 'false'),)
        response1 = ses.get('https://www.latamairlines.com/bff/air-offers/offers/search', headers=headers, params=params)
        FareId    = regMatch('"offerId":"(.*?)"',response1.text)
        params = (('sort', 'RECOMMENDED'),('cabinType', __class),('origin', flyfrom),('destination', flyto),('inFlightDate', 'null'),('inFrom', returndate),('inOfferId', 'null'),('outFlightDate', 'null'),('outFrom', departdate),('outOfferId', FareId),('adult', str(travelers['adults'])),('child', '0'),('infant', str(travelers['infant'])),('redemption', 'false'),)
        response2 = ses.get('https://www.latamairlines.com/bff/air-offers/offers/search', headers=headers, params=params)
        return response1,response2
        
    elif routetype==1:    
        params = (('sort', 'RECOMMENDED'),('cabinType', __class),('origin', flyfrom),('destination', flyto),('inFlightDate', 'null'),('inFrom', returndate),('inOfferId', 'null'),('outFlightDate', 'null'),('outFrom', departdate),('outOfferId', 'null'),('adult', str(travelers['adults'])),('child', '0'),('infant', str(travelers['infant'])),('redemption', 'false'),)
        response1 = ses.get('https://www.latamairlines.com/bff/air-offers/offers/search', headers=headers, params=params)
        return response1

if routetype==2:
    response1,response2=load(flyfrom,flyto,proxy,routetype,departdate,returndate,travelers,priceclass)
#     print(res)
else:
    response1=load(flyfrom,flyto,proxy,routetype,departdate,returndate,travelers,priceclass)

res1=response1.text
res2=response2.text
# print(res2)
open(r'C:\Users\haris\Desktop\lam1.html',"w").write(str(res1))
open(r'C:\Users\haris\Desktop\latam.html',"w").write(str(res2))
latam=json.loads(res1)
latam1=json.loads(res2)
responselist=[latam,latam1]
 
totalbound=[]
outbound=[]
inbound=[]

for count,reslistdata in enumerate(responselist):
    for data in reslistdata['content']:
        stop=[]
        airlinelist=[]
        aircraftlist=[]
        i=0
        for iti in data['itinerary']:
            origin=iti['origin']
            destination=iti['destination']
            departure=iti['departure']
            DD=re.match("(.*?)T(.*?)",str(departure))
            departuredate=DD.group(1)
            DT=iti['departure']
            DT=re.match("(.*?)T(.*)",str(DT))
            departuretime=DT.group(2)
            arrival=iti['arrival']
            AD=re.match("(.*?)T(.*?)",str(arrival))
            arrivaldate=AD.group(1)
            arrival=iti['arrival']
            AT=re.match("(.*?)T(.*)",str(arrival))
            arrivaltime=AT.group(2)
            ft=iti['duration']
            flighttime='{:02d}:{:02d}'.format(*divmod(ft, 60))
            airline=iti['flight']['airlineCode']
            flightNumber=iti['flight']['flightNumber']   
            aircraftName=iti['equipment']
            airlineName=iti['aircraftLeaseText']
            print('origin--',origin)
            print('destination--',destination)
            print('departuredate--',departuredate)
            print('departuretime--',departuretime)
            print('arrivaldate--',arrivaldate)
            print('arrivaltime--',arrivaltime)
            print('duration--',flighttime)
            print('airline--',airline)
            print('flightnumber--',flightNumber)
            print('aircraftname--',aircraftName)
            print('airlineName--',airlineName)
            i+=1
            if i<len(data['itinerary']):
                dt=data['itinerary'][i]['departure']
                Dt=re.match('(.*?)T(.*)',(dt)).group()
#                 print(Dt)
#                 Dt=re.Match('(.*?)T(.*)',(AT)).group(2)
#                 print(Dt)
                Waittime=str(datetime.datetime.strptime(Dt,"%Y-%m-%dT%H:%M:%S")-datetime.datetime.strptime(arrival,"%Y-%m-%dT%H:%M:%S"))
                waittime=datetime.datetime.strptime(Waittime,"%H:%M:%S").strftime("%H:%M")
                print('waittime--',waittime)
                print("="*10)
                facilities = {"faretype":None,"carryonbaggage":{"General":None,"1xfree_bag":None,"2xfree_bag":None,"3xfree_bag":None},"checkedbaggage":{"General":None,"1st_checkedbag":None,"2nd_checkedbag":None,"prioritybaggage":None},"miles":{"50%_miles":None,"100%_miles":None,"150%_miles":None,"200%_miles":None,"miles_earned":None},"snacks":None,"meals":None,"alcoholicdrinks":None,"wifi":None,"loungeaccess":None,"cancellation":None,"changes":None,"seatchoice":None,"prioritycheckin":None,"prioritysecurity":None,"premiumseating":None,"priorityboarding":None}
                STOP = {"origin":origin,"destination":destination,"description":None,"departuredate":departdate,"departuretime": departuretime,"arrivaldate":arrivaldate,"arrivaltime":arrivaltime,"airline":airline, "flightnumber":flightNumber,"flighttime":flighttime,"waittime":waittime, "facilities":facilities,"airlinename":airlineName,"aircraft":aircraftName,"distance":None}
                stop.append(STOP)
                     
        open(r'C:\Users\haris\Desktop\latamstop.html',"w").write(json.dumps(stop)) 
        if len(list(set(airlinelist)))>1:
            multipleairline=1
        else:
            multipleairline=0
                  
        if len(list(set(aircraftlist)))>1:
            aircraftchange=1
        else:
            aircraftchange=0
        lay=data['summary']['duration']
        layover='{:02d}:{:02d}'.format(*divmod(lay, 60))
        print('layover--',layover)
        stopcount=data['summary']['stopOvers']
        print('stopcount--',stopcount)
        for brand in data['summary']['brands']:
            price_class=brand['brandText']
            basefare=brand['farebasis'] 
            currency=brand['price']['currency']
            price=brand['price']['amount']

            print('price_class--',price_class)
            print('basefare--',basefare)
            print('currency--',currency)
            print('price--',price)
            if price:
                flight_statuscode=200
                taxstatus=1  
            else:
                flight_statuscode=201
                taxstatus=0      
     
# #         if count==0:
# #         json_data={'multipleairline':multipleairline, 'layover':layover,  'basefare':basefare, 'aircraftchange':aircraftchange, "price":price,"priceclass":price_class,"currency":currency,"feesandothers":'feesandothers',"description":'',"numofstops":stopcount,"stop":stop,"flight_statuscode":flight_statuscode,"taxstatus":taxstatus}
# #         else:
# #             json_data=({'multipleairline':multipleairline, 'layover':layover,  'basefare':basefare, 'aircraftchange':aircraftchange, "price":price,"priceclass":price_class,"currency":currency,"feesandothers":'feesandothers',"description":'',"numofstops":stopcount,"stop":stop,"flight_statuscode":flight_statuscode,"taxstatus":taxstatus})
# #         js.append(json_data)
#
# # print(json.dumps(js))

        
            if count==0:
                outbound.append({'multipleairline':multipleairline, 'layover':layover,  'basefare':basefare, 'aircraftchange':aircraftchange, "price":price,"priceclass":price_class,"currency":currency,"feesandothers":'feesandothers',"description":'',"numofstops":stopcount,"stop":stop,"flight_statuscode":flight_statuscode,"taxstatus":taxstatus})
            else:
                inbound.append({'multipleairline':multipleairline, 'layover':layover,  'basefare':basefare, 'aircraftchange':aircraftchange, "price":price,"priceclass":price_class,"currency":currency,"feesandothers":'feesandothers',"description":'',"numofstops":stopcount,"stop":stop,"flight_statuscode":flight_statuscode,"taxstatus":taxstatus})
# # 
# print(json.dumps(outbound))
# print(json.dumps(inbound))
# 
open(r'C:\Users\haris\Desktop\latamoutbound.html',"w").write(json.dumps(outbound))
open(r'C:\Users\haris\Desktop\lataminbount.html',"w").write(json.dumps(inbound))
# # 
if routetype==2:
    for OUTBOUND in outbound:
        for INBOUND in inbound:
            totalbound.append({'outbound':OUTBOUND,'inbound':INBOUND})
else:
    for outbound_ in outbound:
        totalbound.append({'outbound':outbound_}) 
# # 
open(r'C:\Users\haris\Desktop\latamtotalbound.html',"w").write(json.dumps(totalbound))
  
print(json.dumps(totalbound))





