# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import pprint
from typing import Any, Text, Dict, List
import string
from googletrans import Translator
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset
from geopy.geocoders import Nominatim
from algoliasearch.search_client import SearchClient
import requests
from rasa_sdk import Tracker, FormValidationAction
from math import sin, cos, sqrt, atan2, radians
import json, ast
import datetime 
from datetime import date,timedelta
import time
import re
import result
from rasa_sdk.types import DomainDict

from typing import Any, Text, Dict, List, Union
url = "https://cargoarabia.com/graphql"

global timeslotid
global first_name
global last_name
global email
global convert_date
global mobile
global number_list
global conver_string
global provincecity, road, postcode
class ActionHelloWorld(Action):

    def name(self):
        return 'action_hello_world'

    def run(self, dispatcher, tracker, domain):



        
        #API TO get vendor list
        payload="{\"query\":\"query {\\r\\n  vendorCollection(category_id: 0, search_key: \\\"\\\", name: \\\"\\\", pageSize: 6, currentPage: 1, location: \\\"{\\\\\\\"city\\\\\\\":\\\\\\\"Riyadh\\\\\\\",\\\\\\\"state\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"latitude\\\\\\\":\\\\\\\"24.7135517\\\\\\\",\\\\\\\"longitude\\\\\\\":\\\\\\\"46.6752957\\\\\\\",\\\\\\\"country\\\\\\\":\\\\\\\"Saudi Arabia\\\\\\\"}\\\") {\\r\\n    total_counts\\r\\n    allVendors {\\r\\n      seller_id\\r\\n      shop_url\\r\\n      shop_title\\r\\n      logo_pic\\r\\n      company_locality\\r\\n      contact_number\\r\\n      seller_rating\\r\\n      lng\\r\\n      lat\\r\\n      banner\\r\\n    }\\r\\n  }\\r\\n}   \\r\\n\",\"variables\":{}}"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'PHPSESSID=uhsgdunfva5t1h1536bgibdbv0; private_content_version=d6934f95eb3556f1dd02f8399afafa8e'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        message = tracker.latest_message['text']
        print(message)
        all_shops=response.json()

        print(all_shops,'--------------')


        global shop       
            # global shop            
        shop=(all_shops["data"]["vendorCollection"]['allVendors'])
        print(shop,"-------------shop")
        global shop_url
        global vendor_list
        vendor_list=[]
        sr_no=[]

        shop_url=[]
        for name_details in shop:
            vendor_list.append(name_details['shop_title'])
            shop_url.append(name_details['shop_url'])
            



        global ven
        ven=vendor_list

        count=len(vendor_list)
        print(count)
        for i in range(len(vendor_list)):
            sr_no.append(str(i+1)+ '. ' +vendor_list[i])
        new_dict=[]
        print(sr_no,"sr no")
        new_dict.append({
            "value_list": vendor_list
        })
        string='\n'.join([i for i in sr_no[:]])

        # create buttons dynamically
        buttons = []
        for i, vendor in enumerate(shop):
            button = {
                "title": vendor['shop_title'],
                "payload": f"{i+1}"
            }
            buttons.append(button)

        # send the buttons to the user
        print(buttons)
        message = "*Welcome* *to* *CargoArabia*\n*Please* *select* *the* *Store:-*\n"
        dispatcher.utter_button_message(message, buttons)

        
        return []



class ActionProductlist(Action):

    def name(self) -> Text:
        return "action_product_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_intent = tracker.latest_message['intent'].get('name')
        print(current_intent)
    
        output_vendore_message = "*please* *select* *the* *product*.\n"
        #getting the value form entity
        try:
            message = tracker.latest_message['text']
            print(message)
            print(vendor_list,"vendor list in product list")
            print(ven)
            value=shop_url[int(message)-1]
            lng_list = []
            lat_list = []
            for i in shop:
                lng_list.append(i['lng'])
                lat_list.append(['lat'])

            print(lng_list,lat_list,"--------------")  
            lat_of_vendor=lng_list[int(message)-1]
            long_of_vendor=lat_list[int(message)-1]
            print(lat_of_vendor,long_of_vendor)          
            print(value,"value of vendor to stor to database")

            print(value,"print")
            
        
            


            client = SearchClient.create("6TIB7HRWU5", "8c38e6c91aaf0979432238c722150e2e")

            index = client.init_index("magento2_default_products")

            results = index.search("", {
                "filters": "shop_url:" + value + " AND salable_qty > 0",
                "hitsPerPage": 100,
            })
            print(results,"result")
            product=results["hits"]

            print("----------------------------------------------",product)
            print(len(product))
            if len(product)==0:
                dispatcher.utter_message(text='There are no product available')
                return[FollowupAction('action_hello_world')]
            else:   
                    
                print (len(product))
                print(product,"----printing product")
                global sku   #sku get from API 
                sku=[]
                product_name=[] #list of product name
                global vendor_ID
                vendor_ID=[] # list of vendor id    get from user input
                price=[]
                sr_no=[]# display this list to user
                global product_ID
                product_ID=[]
                global selecttype
                selecttype=[]

                # seperating the data fron json and append to the list
                for product_list in product:
                    product_name.append(product_list['name'])
                    price.append(product_list['real_price'])
                    product_ID.append(product_list['objectID'])# to check product id
                    sku.append(product_list['sku'])
                    selecttype.append(product_list['select_type'])
                length=(len(product_name),"lenth of product")

                print(selecttype,"select type")
                print(product_name,"product name")  
                print(product_ID,"product id")
                print(price,"price list")
                print(sku,"sku")

                if length==0:
                    dispatcher.utter_message(text='There is no product: please choose another vendor')
                    return[FollowupAction('action_hello_world')]
                else:
                    test_list=[]
                    alpha='A'
                    for i in range(0, 26):
                        test_list.append(alpha)
                        alpha = chr(ord(alpha) + 1)
                    print(test_list)

                    for i in range(0, len(product_name)):
                        sr_no.append(product_name[i]+':'+price[i])
                    print(sr_no,"sr no list")

                    for vendor_id in product:
                        vendor_ID.append(vendor_id['vendor_id'])
                    print(vendor_ID,"vendor_id")
                    global vendor
                    vendor=vendor_ID[0]
                    print(vendor,"---------------------------")
                
                    message="*Please* *select* *the* *product*/service\n"
                    



                    buttons = []
                    for i, name in enumerate(product_name):
                        payload = f"{chr(ord('A') + i)}"
                        formatted_title = name[:8] + "..(" + price[i][:8] + ")"
                        formatted_title = formatted_title.ljust(20)  # Pad the title with spaces if necessary
                        button = {
                            "title": formatted_title,
                            "payload": payload
                        }
                        print(formatted_title,len(formatted_title))
                        buttons.append(button)

                    print(buttons)

                    print(formatted_title,len(formatted_title))
                    print(buttons,"=-----------")
                    dispatcher.utter_button_message(message, buttons)
                    output_message='\n'.join([i for i in sr_no[:]])# converting list into string
                    
        except IndexError:
            dispatcher.utter_message(text='Please Enter a correct serial number')
            return[FollowupAction('action_hello_world')]





class Actionget_product_id(Action):

    def name(self) -> Text:
        return "action_get_product_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            try:                
                print(selecttype,"------")

                message = tracker.get_slot('alpha')
                print(message)
                x = re.search("^[A-Z]$", message)   
                if x:
                    print("YES! We have a match!")
                else:
                    dispatcher.utter_message(text="Please select the correct Alphabet")  
                    return[SlotSet("alpha",None)]      
                global product_ID
                value_no=[]
                print(product_ID,"product id")
                input = str(message)
                print(input,"inpute value")
                input = input.lower()
                #creating guest cart
                response=requests.post('https://cargoarabia.com/rest/V1/guest-carts')
                print(response)
                global guest_cart
                guest_cart=response.json()
                print(guest_cart,"guest_cart")
                for character in input:
                    number = ord(character) - 97
                    value_no.append(number)
                print(number,"num")
                print(value_no)
                global value_product
                global sku_product
                number=(value_no[0])   
                print(number,"sku")       
                value_product=(product_ID[number])
                sku_product=(sku[number])
                service=(selecttype[number])

                print(sku_product,"------sku",service,type(service))

                print(value_product,"product id")


                strvalue_product=str(value_product)

                strvendor=str(vendor)
                print("-------------",strvendor,strvalue_product)
                # check product can be added or not
                payload="{\"query\":\"mutation{\\r\\ncheckVendor(\\r\\nadd_other: false,\\r\\nproduct_id: \\\""+strvalue_product+"\\\",\\r\\nquote_id:\\\""+guest_cart+"\\\",\\r\\nsign_in: false,\\r\\nvendor_id:\\\""+strvendor+"\\\" \\r\\n){\\r\\nsuccess\\r\\nmessage \\r\\n}\\r\\n}\",\"variables\":{}}"
                headers = {
                'Content-Type': 'application/json',
                'Cookie': 'PHPSESSID=h4obnfmht1h9g0v2khrgb3fcvc; private_content_version=45b54d2feff74ae99af88a57f0d11b48'
                }


                response1 = requests.get("https://cargoarabia.com/rest/V1/guest-carts/{}".format(guest_cart))
                data1=response1.json()
                print(data1,"print id  data1")
                timeslotid=data1['id']
                global conver_string
                conver_string=(str(timeslotid))
                print(type(timeslotid))
                print(timeslotid,"---------------------------------imp id ")

                print(payload,"-------product add")
                response = requests.request("POST", url, headers=headers, data=payload)

                data1= response.json()
                print(data1)
                string=data1['data']['checkVendor']['message']

                print(string)


                if string!="Product can be added":
                    dispatcher.utter_message(text="This product is out of stock.\nPlease choose another product.")
                    return[FollowupAction('action_hello_world')]
                elif service == 5459:
                    return[FollowupAction('action_order_quantity'),SlotSet("quantity","1")]
                else:
                    dispatcher.utter_message(text="*Please* *select* *the* *quantity*.")

                return [SlotSet("alpha",None)]
            except IndexError:
                dispatcher.utter_message(text='Please Enter a correct alphabet')
                return[SlotSet("alpha",None)]
        except NameError:
            return[SlotSet("alpha",None)]



class Actionorderquantity(Action):

    def name(self) -> Text:
        return "action_order_quantity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        quantity = tracker.get_slot('quantity')
        print(quantity,"---------->>>>>>>>>>quanity of product")
        

        print(type(quantity),"------------>>>>>>>>type of quantity input from user")
    
        str_quantity=(str(quantity))
        print(str_quantity,"----------------->>>>>>-----str_quantity")
        # adding item 
        print(guest_cart,"next api nedded data")

        #Add quntity of items in
        adding_product_url=("https://cargoarabia.com/rest/V1/guest-carts/{}/items".format(guest_cart))#created string from api

        # API OF adding to cart
        payload = json.dumps({
          "cartItem": {
            "qty": str_quantity,
            "quote_id": guest_cart,
            "sku": sku_product
          }
        })
        headers = {
          'Content-Type': 'application/json',
          'Cookie': 'PHPSESSID=j2fpkkaqsm994len0mu0t4lm0g; private_content_version=601fa22aa8a1295e9af68fdf36b8db1f'
        }
        print(payload,"adding sku")
        response = requests.request("POST", adding_product_url, headers=headers, data=payload)
        print(response,"------->>>>>-----adding_product_url_post_api")
        adding=response.json()
        
        print(adding,"---------------->>>>>>------data response from adding")
        
        #Test for item is added
        response2 = requests.get("https://cargoarabia.com/rest/V1/guest-carts/{}".format(guest_cart))
        data2=response2.json()
        print(data2,"------=====>>>>>>------Check if ITEMS added in api")
        quntityCheck1=data2['items_qty']
        print(quntityCheck1,"----------->>>>>>---quentity check 1")
        print(type(quntityCheck1),"------------------type of quntityCheck1")

        if quntityCheck1 < 1:
            return[FollowupAction('action_order_quantity')]


        dispatcher.utter_message(text="*Please* *share* *your* *location*.")
        return [SlotSet("quantity",None)]



class ActionLocationData(Action):
    def name(self):
        return "action_location_data"
    
    def run(self,dispatcher,tracker,domain):

      
        try:
            global number_list
            latitude = tracker.get_slot('lat')
            longitude = tracker.get_slot('long') 
            mobile_num = tracker.get_slot('mob_num') 

            print(mobile_num,"--------------")
            location1=f"{latitude},{longitude},{mobile_num}"  
            print(location1,type(location1),"-") 
            print(type(latitude),type(longitude),type(mobile_num),"---------------")     

            geolocator = Nominatim(user_agent="MyApp",timeout=10)
            # Latitude & Longitude input
            regex = r"\d+\.\d+|\d+"

            # Extract numbers using regex
            numbers = re.findall(regex, location1)

            # Store numbers in a list and exclude None value
            number_list = []
            for number in numbers:
                if number != "None":
                    if "." in number:
                        number_list.append(float(number))
                    else:
                        number_list.append(int(number))

            print(number_list,"--------------------------")
            geofile=[number_list[0],number_list[1]]
            print(geofile,"---------")
            location = geolocator.reverse(geofile, language="en")
            address = location.raw['address']
            print(address)
            global road
            global postcode
            # Traverse the 
            city = address.get('city', '')
            state = address.get('state', '')
            country = address.get('country', '')
            province1 = address.get('province','')
            road=address.get('road','')
            postcode=address.get('postcode',"")            

            if 'city' in (address):
                print('1')
                getcity = address['city']
            elif 'province' in (address):
                print('2')
                getcity = address['province']
            else:
                #dispatcher.utter_message(text='i did not get your location')
                getcity = None 

            global provincecity
            provincecity=''
            if getcity=='Riyadh governorate':
                print('3')
                provincecity='Riyadh'
            elif getcity=='Riyadh':
                print('4')
                provincecity='Riyadh'
            elif getcity=='Jeddah':
                print('3')
                provincecity='Jeddah'
            else:                
                raise ValueError('Invalid location')
            

            print(getcity)
            print(provincecity,"-------------------------------")
            print(type(road))
            return[SlotSet("change_flow",True)]
            
        except ValueError:
            dispatcher.utter_message(text='Sorry, we are not operating in this location.\nFor more assistance please contact to our customer care   +966112200555')
            return[SlotSet("change_flow","false")]
        


class Actioncheckforregistration(Action):
    
    #@check_login
    def name(self) -> Text:
        return "check_for_registration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global mobile_num
        change_flow = tracker.get_slot('change_flow')
        # change_flow1 = tracker.get_slot('change_flow1')
        print(change_flow,"--------change----in the check mobile function--------------")
        global mobile
        print(number_list[2],type(number_list[2]),"-------->>>>>>>>-------mob no in check registration")
        mobile=str(number_list[2])
        print(mobile,type(mobile),"type converstion")
        payload="{\"query\":\"mutation {\\n\\nsendOtp(\\nmobile: \\\"+"+mobile+"\\\",\\n    from: \\\"login\\\",\\nsms: false\\n) {\\nsuccess\\nmessage\\n\\n}\\n}\",\"variables\":{}}"
        headers = {
          'Content-Type': 'application/json',
          'Cookie': 'PHPSESSID=qb2geqekjqhpmo2hsc146ga9t7; private_content_version=59e7a8527d9042ae84079017d591daaa'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        data=response.json()
        print(data['data']['sendOtp']['success'],"----------->>>>>>>>>>>>>----------check login")
        success1=data['data']['sendOtp']['success']
        if success1==False:
            print("-------->>>>>>>----FollowupAction('userDetails_form')")
            return[FollowupAction('userDetails_form'),SlotSet("fName",None),SlotSet("change_flow1",False)]
        elif success1==True:
            print("------>>>>>>>>>------FollowupAction('action_check_auth')")
            return[FollowupAction('action_check_auth')]
        else:
            dispatcher.utter_message(text='Sorry inconvieneve')


class ValidateuserDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_userDetails_form"


    def validate_fName(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate first name value."""
        print(slot_value)
        if slot_value.lower() != None:
            # validation succeeded, set the value of the "first value" slot to value
            return {"fName": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"fName": None}

    def validate_lName(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate last value."""
        print(slot_value)
        if slot_value.lower() != None:
            # validation succeeded, set the value of the "last value" slot to value
            return {"lName": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"lName": None}

    def validate_email_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate email value."""
        print(slot_value)
        # regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if slot_value != None:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"email_id": slot_value}
        else:
            return {"email_id": None}



class ActionCheckAuth(Action):
    
    #@check_login
    def name(self) -> Text:
        return "action_check_auth"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("-------->>>>>>>>>-----action_check_login-----<<<<<<<<<<<<-------")

        print("---------->>>>>>>>-----in check/auth LOGIN------<<<<<<<<<-------")
        

        print(conver_string,"------cover_string---->>>>>>>>-----in check/auth LOGIN------<<<<<<<<<-------")
        
        payload="{\"query\":\"mutation {\\n\\nsignIn(\\n mobile:\\\"+"+mobile+"\\\",\\ncart_id: \\\""+conver_string+"\\\"\\n){\\nsuccess\\nmessage\\ntoken\\n  }\\n}\",\"variables\":{}}"
        headers = {
        'Content-Type': 'application/json',
        'Cookie': 'PHPSESSID=ehl1rucd3biag43hvit40r13i0; private_content_version=68e96511641946db621660ea4ae80236'
        }
        
        print(payload,"payload")
        response1= requests.request("POST", url, headers=headers, data=payload)
        
        
        data=response1.json()
        print(data,response1)
        global token
        
        success=data['data']['signIn']['success']
        token=data['data']['signIn']['token']

        
        print(success,"sucess message ")
        print(token)
        if success==False:
            dispatcher.utter_message(text='Please login')
        else:    
            info_url = "https://cargoarabia.com/rest/V1/customers/me"

            payload="{\"query\":\"\",\"variables\":{}}"
            headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json',
            'Cookie': 'PHPSESSID=2ejoiel7m0f2d8uuiruqi9v2ij; private_content_version=54a7f0f3e683de57fd73894bcd7702fe'
            }

            response = requests.request("GET", info_url, headers=headers, data=payload)
            data=response.json()
            global first_name
            global last_name
            global email
            first_name=data['firstname']
            last_name=data['lastname']
            email=data['email']
            print(first_name,"-----info_url")
            print(last_name,"----lastname")
            print(email,"-----email")

            mine_url = "https://cargoarabia.com/rest/V1/carts/mine"
            
            payload={}
            headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Cookie': 'PHPSESSID=2ejoiel7m0f2d8uuiruqi9v2ij; private_content_version=54a7f0f3e683de57fd73894bcd7702fe'
            }
            
            response = requests.request("POST", mine_url, headers=headers, data=payload)
            #mine_data=response.json()
            global cart_id
            cart_id=response.text
        
            print(cart_id,"----------card mine id")
            shipping_info_url = "https://cargoarabia.com/rest/V1/carts/mine/shipping-information"
            payload = json.dumps({
            "addressInformation": {
                "billing_address": {
                "city": provincecity,
                "country_id": "SA",
                "firstname": first_name,
                "lastname": last_name,
                "postcode": postcode,
                "region": "Riyadh Province",
                "save_in_address_book": 0,
                "street": [
                    road
                ],
                "telephone": "+"+mobile
                },
                "shipping_address": {
                "city": "Riyadh",
                "country_id": "SA",
                "firstname": first_name,
                "lastname": last_name,
                "postcode": postcode,
                "region": "Riyadh Province",
                "save_in_address_book": 0,
                "street": [
                    road
                ],
                "telephone": "+"+mobile
                },
                "shipping_carrier_code": "flatrate",
                "shipping_method_code": "flatrate"
            },
            "cartId": cart_id
            })
            headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json',
            'Cookie': 'PHPSESSID=2ejoiel7m0f2d8uuiruqi9v2ij; private_content_version=54a7f0f3e683de57fd73894bcd7702fe'
            }
            print(payload,'shipping-information')
            response1 = requests.request("POST", shipping_info_url, headers=headers, data=payload)
            print(response,"shipping info")
            data1=response1.text
            print(data1,"------------------------data from info")
            return[FollowupAction('action_date_time')]





            
class Actionformegistrationsubmit(Action):
    
    
    def name(self) -> Text:
        return "form_registration_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global fName
        global lName
        global email
        first_name = tracker.get_slot('fName')
        last_name = tracker.get_slot('lName')
        email= tracker.get_slot('email_id')
        payload="{\"query\":\"mutation {\\n    \\nsignUp(\\n      contact_number: \\\"+"+mobile+"\\\",\\n    email: \\\""+email+"\\\",\\n    firstname: \\\""+first_name+"\\\",\\n    lastname: \\\""+last_name+"\\\",\\n    cart_id: \\\""+conver_string+"\\\"\\n    ) {\\n    success \\nmessage\\n    token\\n  }\\n}\",\"variables\":{}}"
        print(payload,"printing payload of submit form")
        headers = {
          'Content-Type': 'application/json',
          'Cookie': 'PHPSESSID=23teb9vqfg9jjkca393oc4egt0; private_content_version=c44ffdbd72f1ccf92ed1c24f1f6edf34'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        data=response.json()
        print(data,"data submit form")
        global token2
        global success2
        print(data,"-------->>>>>>>>>---------registration data")
        success2=data['data']['signUp']['success']
        token2=data['data']['signUp']['token']
        print(token2,"------------------token----------------------")
        print(success2,"------------registration-success2------")        
        if success2==True:
            print("111111111111111111111111111111111111111111111")
            return[FollowupAction('action_payemnt_info')]                
        else:
            dispatcher.utter_message(text="Your Registration has been not Successfull done with Cargo Services...!!!!!!!!")
            
            





class Actionpayemntinfo(Action):

    def name(self) -> Text:
        return "action_payemnt_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print('inside action payement info')
          
            print(conver_string,"------cover_string---->>>>>>>>-----in check/auth LOGIN------<<<<<<<<<-------")
            global token
            success=success2
            print(token2,"----------------------------token from registration")
            token=token2
            info_url = "https://cargoarabia.com/rest/V1/customers/me"
            payload="{\"query\":\"\",\"variables\":{}}"
            headers = {
              'Authorization': 'Bearer {}'.format(token),
              'Content-Type': 'application/json',
              'Cookie': 'PHPSESSID=2ejoiel7m0f2d8uuiruqi9v2ij; private_content_version=54a7f0f3e683de57fd73894bcd7702fe'
            }
            response = requests.request("GET", info_url, headers=headers, data=payload)
            data=response.json()
            global first_name
            global last_name
            
            first_name=data['firstname']
            last_name=data['lastname']
            
            print(first_name,"-----info_url")
            print(last_name,"----lastname")
           

            mine_url = "https://cargoarabia.com/rest/V1/carts/mine"

            payload={}
            headers = {
              'Authorization': 'Bearer {}'.format(token),
              'Cookie': 'PHPSESSID=2ejoiel7m0f2d8uuiruqi9v2ij; private_content_version=54a7f0f3e683de57fd73894bcd7702fe'
            }

            response = requests.request("POST", mine_url, headers=headers, data=payload)
            # mine_data=response.json()
            global cart_id
            cart_id=response.text

            print(cart_id,"----------card mine id")
            shipping_info_url = "https://cargoarabia.com/rest/V1/carts/mine/shipping-information"
            payload = json.dumps({
              "addressInformation": {
                "billing_address": {
                  "city": provincecity,
                  "country_id": "SA",
                  "firstname": first_name,
                  "lastname": last_name,
                  "postcode": postcode,
                  "region": "Riyadh Province",
                  "save_in_address_book": 0,
                  "street": [
                    road
                  ],
                  "telephone": "+"+mobile
                },
                "shipping_address": {
                  "city": provincecity,
                  "country_id": "SA",
                  "firstname": first_name,
                  "lastname": last_name,
                  "postcode": postcode,
                  "region": "Riyadh Province",
                  "save_in_address_book": 0,
                  "street": [
                    road
                  ],
                  "telephone": "+"+mobile
                },
                "shipping_carrier_code": "flatrate",
                "shipping_method_code": "flatrate"
              },
              "cartId": cart_id
            })
            headers = {
              'Authorization': 'Bearer {}'.format(token),
              'Content-Type': 'application/json',
              'Cookie': 'PHPSESSID=2ejoiel7m0f2d8uuiruqi9v2ij; private_content_version=54a7f0f3e683de57fd73894bcd7702fe'
            }
            print(payload,'shipping-information')
            response1 = requests.request("POST", shipping_info_url, headers=headers, data=payload)
            print(response,"shipping info")
            data1=response1.text
            buttons=[]
            button = {
                "title": "Next",
                "payload": "correct"
            }
            buttons.append(button)

            message='Thanks for registering with us, Click Next to proceed further?'
            # dispatcher.utter_message(message)
            dispatcher.utter_button_message(message,buttons)
            print('sending registration message')
            
            return[]


class Actiondatetime(Action):

    def name(self) -> Text:
        return "action_date_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("////////-------In the action date time------///////////")

        print('printing location',number_list[0],number_list[1])
        
        lat=str(number_list[0])
        longtitude=str(number_list[1])
        print(lat,longtitude)
        try:        
            payload="{\"query\":\"mutation {\\n  dateTimeSlots(\\n    cart_id: \\\""+cart_id+"\\\",\\n city: \\\""+provincecity+"\\\",\\n\\nlatitude: \\\""+lat+"\\\",\\n\\nlongitude: \\\""+longtitude+"\\\"\\n    ) {\\n    success\\n    data\\n     \\n  }\\n}\\n  \",\"variables\":{}}"
            headers = {
            'Content-Type': 'application/json'
            }
            # get datetimeslot API
            response = requests.request("POST", url, headers=headers, data=payload)
            data=response.json()
            print(data,"response from date time slot api")






            data1=(data['data']['dateTimeSlots']['data'])
            data_json=json.loads(data1)
            print(data_json)
            print(type(data_json))

            global todaycost
            global tommarowcost
            global thedayafter    
            now_cost=data_json['costData']['directCost']
            today_cost=data_json['costData']['cost']
            tommarow_cost=data_json['costData']["nextCost"]
            all_day=data_json['costData']["allCost"]
            nowcost=str(now_cost)
            todaycost=str(today_cost)
            tommarowcost=str(tommarow_cost)
            thedayafter=str(all_day)

            vendor_data=data_json['vendorData']
            vendorWD=vendor_data['vendorWD']
            print(vendor_data,"-------")                        
            todayOneFlag = vendor_data['todayOneFlag']
            todayTwoFlag = vendor_data['todayTwoFlag']
            openTime = vendor_data['openTime']
            closeTime = vendor_data['closeTime']

            today_flag = vendor_data['todayFlag']


            todayM_msg  = vendor_data['todayM']
            todayE_msg = vendor_data['todayE']
            today_onem_msg= vendor_data['todayOneM']
            todayOneE_msg= vendor_data['todayOneE']
            todayTwoM_msg= vendor_data['todayTwoM']
            todayTwoE_msg=  vendor_data['todayTwoE']



            todayThreeM_msg=vendor_data['todayThreeM']
            todayThreeE_msg=vendor_data['todayThreeE']
            todayFourM_msg=vendor_data['todayFourM']
            todayFourE_msg=vendor_data['todayFourE']
            todayFiveM_msg=vendor_data['todayFiveM']
            todayFiveE_msg=vendor_data['todayFiveE']
            todaySixM_msg=vendor_data['todaySixM']
            todaySixE_msg=vendor_data['todaySixE']



            today = datetime.datetime.today().strftime('%A').upper()
            tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%A').upper()
            day_after_tomorrow = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%A').upper()
            todayThree_Day=(datetime.datetime.today() + datetime.timedelta(days=3)).strftime('%A').upper()
            todayFour_Day=(datetime.datetime.today() + datetime.timedelta(days=4)).strftime('%A').upper()
            todayFive_Day=(datetime.datetime.today() + datetime.timedelta(days=5)).strftime('%A').upper()
            todaySix_Day=(datetime.datetime.today() + datetime.timedelta(days=6)).strftime('%A').upper()
            buttons = []


            print(today,'morning-------',todayM_msg)
            print(today,'evening-------',todayE_msg)
            print(tomorrow,' morning-------',today_onem_msg)
            print(tomorrow,' evening-------',todayOneE_msg)
            print(day_after_tomorrow,' morning-------',todayTwoM_msg)
            print(day_after_tomorrow,' evening-------',todayTwoE_msg)



            print(todayThree_Day,' morning-------',todayThreeM_msg)
            print(todayThree_Day,' evening-------',todayThreeE_msg)
            print(todayFour_Day,'morning-------',todayFourM_msg)
            print(todayFour_Day,' evening-------',todayFourE_msg)
            print(todayFive_Day,' morning-------',todayFiveM_msg)
            print(todayFive_Day,' evening-------',todayFiveE_msg)
            print(todaySix_Day,' morning-------',todaySixM_msg)
            print(todaySix_Day,' evening-------',todaySixE_msg)




            text="*Please* *select* *the* *delivery* *timeslot* (shipping charges)."

            if today_flag == True:
                buttons.append({"title": f"Now({now_cost}﷼)", "payload": "Now"})
            if todayM_msg == "Available":
                buttons.append({"title": f"Today morning({today_cost}﷼)", "payload": "today morning"})
            if todayE_msg == "Available":
                buttons.append({"title": f"Today Evening({today_cost}﷼)", "payload": "today evening"})
            if today_onem_msg == "Available":
                buttons.append({"title": f"Tomorrow morning({tommarow_cost}﷼)", "payload": "tomorrow morning"})
            if todayOneE_msg == "Available":
                buttons.append({"title": f"Tomorrow afternoon({tommarow_cost}﷼)", "payload": "tomorrow evening"})
            if todayTwoM_msg == "Available":
                buttons.append({"title": f"After tomorrow morning({thedayafter}﷼)", "payload": "after morning"})
            if todayTwoE_msg == "Available":
                buttons.append({"title": f"After tomorrow afternoon({thedayafter}﷼)", "payload": "after evening"})

            # --------------------------*new days * ------------------------------------

            
            

            text="*Please* *select* *the* *delivery* *timeslot* (shipping charges)."
            print(text,buttons)

            dispatcher.utter_button_message(text, buttons)
            # dispatcher.utter_message(text=text+output)

            
            return[]
        except TypeError:
            dispatcher.utter_message(Text='Apparently, something went wrong.')
            return[]        






    

class Actiondatetimesubmit(Action):

    def name(self) -> Text:
        return "action_date_time_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global message
           
            message=tracker.latest_message['text']
            print(message)
            cost=[todaycost,tommarowcost,thedayafter]
            print(cost)
            Evening= "2:30 PM - 7:30 PM"
            Morning="8:30 AM - 1:30 PM"
            global delevery_time
            global output_date
            global amount
            delevery_time = ""
            output_date=""
            amount=""
            lowercase_string = message.lower()
            print(lowercase_string,"-----------------------")

            if lowercase_string=='today morning':
                output_date = datetime.datetime.now().date()   
                amount=cost[0]
                delevery_time = "8:30 AM - 1:30 PM"
                return[FollowupAction('submit_date_api')]
            elif lowercase_string=='now':
                output_date = datetime.datetime.now().date()   
                amount=cost[0]
                delevery_time = "Now"
                return[FollowupAction('submit_date_api')]
            elif lowercase_string=='tomorrow morning':
                output_date = datetime.datetime.now().date() + datetime.timedelta(days=1)   
                amount=cost[1]
                delevery_time = "8:30 AM - 1:30 PM"
                return[FollowupAction('submit_date_api')]
            elif lowercase_string=='after morning':
                output_date = datetime.datetime.now().date() + datetime.timedelta(days=2)
                amount=cost[2]
                delevery_time = "8:30 AM - 1:30 PM"
                return[FollowupAction('submit_date_api')]
            elif lowercase_string=='today evening':
                print('today evening')
                output_date = datetime.datetime.now().date()   
                amount=cost[0] 
                delevery_time = "2:30 PM - 7:30 PM"
                return[FollowupAction('submit_date_api')]
            elif lowercase_string=='tomorrow evening':
                print('tomorrow evening')
                output_date = datetime.datetime.now().date() + datetime.timedelta(days=1)   
                amount=cost[1]
                delevery_time = "2:30 PM - 7:30 PM"
                return[FollowupAction('submit_date_api')]
            elif lowercase_string=='after evening':
                print('after evening')
                output_date = datetime.datetime.now().date() + datetime.timedelta(days=2)
                amount=cost[2]
                delevery_time = "2:30 PM - 7:30 PM"
                return[FollowupAction('submit_date_api')]
            # -----------------------------------------------------    
            else:
                dispatcher.utter_message(Text='Please select correct timeslot.')

            print(output_date,'------------------date')                        
            print(amount,"------------amount")
            print(delevery_time,"delivery time")  
            
        
            return[]



class Actionsubmit_date_api(Action):
    
    #@check_login
    def name(self) -> Text:
        return "submit_date_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            payload="{\"query\":\"mutation {\\n  setShippingFee(\\n    cart_id: \\\""+cart_id+"\\\",\\n    shipping_amount: \\\""+amount+"\\\",\\n    sign_in: true\\n    ) {\\n    success\\n    message\\n     \\n  }\\n}\\n\",\"variables\":{}}"
            headers = {
              'Authorization': 'Bearer {}'.format(token),
              'Content-Type': 'application/json',
              'Cookie': 'PHPSESSID=bde39jglclcrt46qca9ss294c5; private_content_version=0ede2c5b2d40d90755a5ccd7cae756dc'
            }
            print(payload,"------->>>>>>>>-----amount payload")
            response = requests.request("POST", url, headers=headers, data=payload)
            data=response.json()
            print(data,"------->>>>>>>>>>>-------amount updated ")
            print(output_date,"------->>>>>>>>----output date")
            global convert_date
            convert_date=str(output_date)
            new=datetime.datetime.strptime(convert_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            # ----------------------------------------second_api---------------------------
            lat=str(number_list[0])
            longtitude=str(number_list[1])
            print(lat,longtitude)
            payload="{\"query\":\"query {\\n  updateQuote(\\n      quote_id: \\\""+cart_id+"\\\",\\n  delivery_date: \\\""+new+"\\\",\\n   delivery_time: \\\""+delevery_time+"\\\",\\n    lat: \\\""+lat+"\\\",\\n     lng: \\\""+longtitude+"\\\") {\\n    success\\n    \\n  }\\n}\",\"variables\":{}}"
            headers = {
              'Content-Type': 'application/json'
            }
            print(payload,"---------->>>>>>>>>>>>>>>>>>>>----------today update payload")    
            response = requests.request("POST", url, headers=headers, data=payload)
            data=response.json()
            print(data,"------->>>>>>>>>>>>>-------today update qote")
            buttons = []
            message="Are you sure, you want to place an order?"
            # Create a button for "Yes"
            button_yes = {
                "title": "Yes",
                "payload": "Yes"
            }
            buttons.append(button_yes)

            # Create a button for "No"
            button_no = {
                "title": "No",
                "payload": "No"
            }
            buttons.append(button_no)

            # Print the list of buttons
            print(buttons)
            dispatcher.utter_button_message(message, buttons)    
        
            return[]
            # return[FollowupAction('place_order_submit')]

class Actionplaceorder(Action):
    
    #@check_login
    def name(self) -> Text:
        return "place_order_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global data1
        print(email,"------------------------------------------")
        shipping_url = "https://cargoarabia.com/rest/V1/carts/mine/estimate-shipping-methods"

        payload = json.dumps({
          "address": {
            "city": provincecity,
            "country_id": "SA",
            "firstname": first_name,
            "lastname": last_name,
            "postcode": postcode,
            "region": "Riyadh Province",
            "save_in_address_book": 0,
            "street": [
              road
            ],
            "telephone": "+"+mobile
          }
        })
        headers = {
          'Authorization': 'Bearer {}'.format(token),
          'Content-Type': 'application/json',
          'Cookie': 'PHPSESSID=2ejoiel7m0f2d8uuiruqi9v2ij; private_content_version=54a7f0f3e683de57fd73894bcd7702fe'
        }
        print(payload,"shipping url")
        response = requests.request("POST", shipping_url, headers=headers, data=payload)
        data=response.json()
        print(data,"-------shipping url")



        payment_info_url = "https://cargoarabia.com/rest/V1/carts/mine/payment-information"

        payload = json.dumps({
          "billingAddress": {
            "firstname": first_name,
            "lastname": last_name,
            "city": provincecity,
            "region": "Riyadh Province",
            "postcode": postcode,
            "telephone": "+"+mobile,
            "country_id": "SA",
            "street": [
              road
            ],
            "save_in_address_book": 0
          },
          "cartId": conver_string,
          "paymentMethod": {
            "method": "cashondelivery",
            "additional_data": None,
            "po_number": None
          },
          "email": email
        })
        headers = {
          'Authorization': 'Bearer {}'.format(token),
          'Content-Type': 'application/json',
          'Cookie': 'PHPSESSID=lhbfu37pue7im0dlpqn1h4cp1o; private_content_version=922fb156a11589d0546da2c78d6d4035'
        }
        print(payload,'---------------------------')
        response1 = requests.request("POST", payment_info_url, headers=headers, data=payload)        
        data1=response1.json()
        print(data1,"----------- payement info")

        

        payload="{\"query\":\"query  {\\n  orderDetails(id: "+data1+", sms: true) {\\n    success\\n    increment_id\\n    customer_name\\n    created_at\\n    discount_amount \\n  }\\n}\",\"variables\":{}}"
        headers = {
          'Authorization': 'Bearer {}'.format(token),
          'Content-Type': 'application/json',
          'Cookie': 'private_content_version=019c6f005d7e441271ca7fedf27f9f52'
        }
        print(payload,"------- order 1")
        response2 = requests.request("POST", url, headers=headers, data=payload)
        data2=response.json()
        print(data2,"--------get order details")
        print(convert_date)


        new=datetime.datetime.strptime(convert_date, "%Y-%m-%d").strftime("%d/%m/%Y")#------ changing date format
        # print(latitude,longitude,"---------------------------------------------")
        lat=str(number_list[0])
        longtitude=str(number_list[1])
        print(lat,longtitude)
        payload="{\"query\":\"query\\r\\n{\\r\\n  updateOrder(\\r\\norder_id: "+data1+",\\r\\n    delivery_date: \\\""+new+"\\\",\\r\\n    delivery_time:\\\""+delevery_time+"\\\",\\r\\n    lat: \\\""+lat+"\\\", \\r\\n  lng: \\\""+longtitude+"\\\") {\\r\\n    success\\r\\n  }\\r\\n}\",\"variables\":{}}"
        headers = {
          'Authorization': 'Bearer {}'.format(token),
          'Content-Type': 'application/json',
          'Cookie': 'PHPSESSID=473ae58gvlscaklc7scv9i9u8k; private_content_version=58e79661308c916a52b235df81e46d71'
        }
        print(payload,"---------------------------------------------payload of update order")
        response4 = requests.request("POST", url, headers=headers, data=payload)
        print(response4,"update url")
        
        print(response4.text,"--update")
        mine_url = "https://cargoarabia.com/rest/V1/carts/mine"

        payload={}
        headers = {
          'Authorization': 'Bearer {}'.format(token),
          'Cookie': 'PHPSESSID=2ejoiel7m0f2d8uuiruqi9v2ij; private_content_version=54a7f0f3e683de57fd73894bcd7702fe'
        }
        response = requests.request("POST", mine_url, headers=headers, data=payload)

        
        # dispatcher.utter_message(text='Hello {},\nYour order has been placed.\nPlease open this link to track the status.\nhttps://cargoarabia.com/track-order/{}\nBest Regards!\nTeam CargoArabia.'.format(first_name,data1))
        print('----------------------------',first_name)
        global name
        name=first_name
        print('---------------------------',last_name)
        return[FollowupAction('action_reset_slot')]


class ActionResetSlot(Action):
    def name(self) -> Text:
        return "action_reset_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('reset slot function')

        dispatcher.utter_message(text='Hello {},\nYour order has been placed.\nPlease open this link to track the status.\nhttps://cargoarabia.com/track-order/{}\nBest Regards!\nTeam CargoArabia.'.format(name,data1))
        return [AllSlotsReset()]

class ActionResetSlot1(Action):
    def name(self) -> Text:
        return "action_reset_slot1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        print(intent)
        if intent=='exit':
            print('inside if')
            return [AllSlotsReset(),FollowupAction('action_hello_world')]
        else:
            print('reset slot function11111111111111')

            return [AllSlotsReset()] 
