from flask import Flask, request
import requests
import json
from flask import jsonify

temp_access_token = 'EAAKhhIdZCSLoBAB6HAEiquF12KlVpJDiiwdoZAwBFixjBrTihEzpIop79Pdo2ZCiq8ZBiGfCiQw9JZAFZArSuTU0ary5EnbigsxUD1ETCO1AiZAQ4LZCG7aCcGqqVOBaeedw8rRrK0S82BmtwktBWzOUwDCUAWJfo6vAvJgm4vXnmSl6DPl2QZAot'
sender_phone_id = '112458745121003'
ngrok_link = 'http://211a-2402-8100-303a-9814-189a-719c-e8d7-be1a.ngrok-free.app/webhooks/rest/webhook'

app = Flask(__name__)

def send_reply(phone_number_id, to, reply_message):
    url = f'https://graph.facebook.com/v15.0/{phone_number_id}/messages'
    headers = {
        "Authorization": f"Bearer {temp_access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": reply_message}
    }
    respone = requests.post(url, headers=headers, data=json.dumps(data))
    print(respone.text)

def send_button_menu(phone_number_id, to, reply_message, button_list):
    url = f'https://graph.facebook.com/v15.0/{phone_number_id}/messages'
    headers = {
        "Authorization": f"Bearer {temp_access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": reply_message
            },
            "action": {
                "buttons": button_list
            }
        }
    }
    respone = requests.post(url, headers=headers, data=json.dumps(data))
    print(respone.text)

def send_main_menu(phone_number_id, to, reply_message, button_list):
    url = f'https://graph.facebook.com/v15.0/{phone_number_id}/messages'
    headers = {
        "Authorization": f"Bearer {temp_access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {
                "text": reply_message
            },
            "action": {
                "button": "Options",
                "sections": [
                    {
                        "title": "Options",
                        "rows": button_list
                    }
                ]
            }
        }
    }
    respone = requests.post(url, headers=headers, data=json.dumps(data))
    print(respone.text)

def send_products_list(phone_number_id, to, reply_message, p_list):
    url = f'https://graph.facebook.com/v15.0/{phone_number_id}/messages'
    headers = {
        "Authorization": f"Bearer {temp_access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {
                "text": reply_message
            },
            "action": {
                "button": "Options",
                "sections": [
                    {
                        "title": "Options",
                        "rows": p_list
                    }
                ]
            }
        }
    }
    respone = requests.post(url, headers=headers, data=json.dumps(data))
    print(respone.text)

@app.route('/incoming', methods=['GET','POST'])
def incoming():
    # print(request.json['entry'])
    # return jsonify({'message': 'success'}), 200
    if request.method == 'POST':
        entries = request.json['entry']
        for entry in entries:

            for change in entry.get("changes", []):
                value = change.get("value")
                if value is not None:
                    phone_number_id = value.get(
                        "metadata", {}).get("phone_number_id")
                    if phone_number_id == sender_phone_id:
                        if value.get("messages") is not None:
                            for message in value.get("messages"):
                                from_number = message.get("from")
                                print(message.get("type"),"456789------------")
                                if message.get("type") == "text":
                                    message_text = message.get("text", {}).get("body")
                                    print("first if")
                                    if any(digit in message_text for digit in ['1', '2', '3', '4' , '5', '6', '7', '8', '9', '10', '11', '12', '13']) and len(message_text) <= 2:
                                        message_text = message_text.replace('10', 'todayfoure_msg').replace('11', 'todayfivem_msg').replace('12', 'todayfivee_msg').replace('13', 'todaysixm_msg').replace('14', 'todaysixe_msg').replace('1', 'Now').replace('2', 'tomorrow morning').replace('3', 'after morning').replace('4', 'today evening').replace('5', 'tomorrow evening').replace('6', 'after evening').replace('7', 'todaythreem_msg').replace('8', 'todaythreee_msg').replace('9', 'todayfourm_msg')
                                    response = requests.post(ngrok_link, json={'message': message_text})
                                    print(message_text,"54-----------")
                                    print(response,"----response-------")
                                    print(response.json(),"1-------------------- printing response from json")
                                    rasa_response = response.json()
                                    reply_text = rasa_response[0]['text']
                                    print(reply_text)
                                    if 'Please enter your last name.' in reply_text or 'Please enter your email.' in reply_text or 'Thanks for registering with us, Click Next to proceed further?' in reply_text:
                                        send_reply(phone_number_id, from_number, reply_text)     

                                    elif 'yes' in message_text:
                                        print('ok4')
                                        buttonStr = ''
                                        for itmInd, itm in enumerate(rasa_response[0]['buttons']):
                                            buttonStr = buttonStr + f"*{itmInd+1}* {itm['title']}\n"
                                        # send_main_menu(phone_number_id, from_number, reply_text, buttonList)
                                        reply_text = f'{reply_text}\n{buttonStr}'
                                        print(reply_text)
                                        send_reply(phone_number_id, from_number, buttonStr)
                                        print("above yes not")

                                    elif 'Store' in reply_text:
                                        print('ok1------------------------------------------',reply_text)
                                        buttonList = []
                                        for itmInd, itm in enumerate(rasa_response[0]['buttons']):
                                            tempDict = {
                                                'id': f'ID_1_{itmInd+1}',
                                                'title': f"{itm['title'][:21]}..."
                                            }
                                            buttonList.append(tempDict)
                                        send_main_menu(phone_number_id, from_number, reply_text, buttonList)

                                    # elif 'quantity' in reply_text:
                                    #     print('ok2')
                                    #     send_reply(phone_number_id, from_number, reply_text)
                                            # print('987')
                                            # print('above locaion')

                                    elif 'location' in reply_text:
                                        print('ok3-------------------------------------------------------',reply_text)
                                        send_reply(phone_number_id, from_number, reply_text)
                                        print('above yes')


                                    elif 'you want to place an order' in reply_text:
                                        buttonList = []
                                        for itmInd, itm in enumerate(rasa_response[0]['buttons']):
                                            if len(itm['title']) >= 19:
                                                tempDict = {
                                                    "type": "reply",
                                                    "reply": {
                                                        "id": f"ID_4_{itm['payload']}",
                                                        "title": f"{itm['title'][:19]}..."
                                                    }
                                                }
                                            else:
                                                tempDict = {
                                                    "type": "reply",
                                                    "reply": {
                                                        "id": f"ID_4_{itm['payload']}",
                                                        "title": f"{itm['title'][:19]}"
                                                    }
                                                }
                                            buttonList.append(tempDict)
                                        send_button_menu(phone_number_id, from_number, reply_text, buttonList)


                                        print('interactive1')
                                elif message.get("type") == 'interactive' and message.get("interactive").get("type") == "button_reply":
                                    if message.get("interactive").get("type") == "button_reply":
                                        if 'ID_4' in message.get("interactive").get("button_reply").get("id"):
                                            message_text = message.get("interactive").get("button_reply").get("id").replace('ID_4_', '')
                                            response = requests.post(ngrok_link, json={'message': message_text})
                                            rasa_response = response.json()
                                            reply_text = rasa_response[0]['text']
                                            print(message_text,"-----------")
                                            print(response,"----response-------")
                                            print(response.json(),"-------------------- printing response from json")
                                            send_reply(phone_number_id, from_number, reply_text)

                                elif message.get("type") == 'interactive' and message.get("interactive").get("type") == "list_reply":
                                    if message.get("interactive").get("type") == "list_reply":
                                        if 'ID_1' in message.get("interactive").get("list_reply").get("id"):
                                            # if message.get("interactive").get("list_reply").get("id") == 'ID_1_1':
                                                message_text = message.get("interactive").get("list_reply").get("id").replace('ID_1_', '')
                                                response = requests.post(ngrok_link, json={'message': message_text})
                                                rasa_response = response.json()
                                                reply_text = rasa_response[0]['text']
                                                products_list = rasa_response[0]['buttons']
                                                buttonList = []
                                                for itmInd, itm in enumerate(products_list):
                                                    tempDict = {
                                                        'id': f"ID_2_{itm['payload']}",
                                                        'title': f"{itm['title'][:21]}..."
                                                    }
                                                    buttonList.append(tempDict)
                                                print(message_text,"-----------")
                                                print(response,"----response-------")
                                                print(response.json(),"-------------------- printing response from json")
                                                send_products_list(phone_number_id, from_number, reply_text, buttonList)
                                        elif 'ID_2' in message.get("interactive").get("list_reply").get("id"):
                                            message_text = message.get("interactive").get("list_reply").get("id").replace('ID_2_', '')
                                            response = requests.post(ngrok_link, json={'message': message_text})
                                            rasa_response = response.json()
                                            reply_text = rasa_response[0]['text']
                                            print(message_text,"-----------")
                                            print(response,"----response-------")
                                            print(response.json(),"-------------------- printing response from json")
                                            # send_reply(phone_number_id, from_number, reply_text)
                                            buttonList = []
                                            for itm in range(1, 11):
                                                # print(itm)
                                                tempDict = {
                                                    'id': f"ID_4_{itm} units",
                                                    'title': f"{itm}"
                                                }
                                                buttonList.append(tempDict)
                                            send_main_menu(phone_number_id, from_number, reply_text, buttonList)

                                        # elif 'ID_3' in message.get("interactive").get("list_reply").get("id"):
                                        #     message_text = message.get("interactive").get("list_reply").get("id").replace('ID_3_', '')
                                        #     response = requests.post(ngrok_link, json={'message': message_text})
                                        #     rasa_response = response.json()
                                        #     reply_text = rasa_response[0]['text']
                                        #     print(message_text,"-----------")
                                        #     print(response,"----response-------")
                                        #     print(response.json(),"-------------------- printing response from json")
                                        #     buttonList = []
                                        #     for itmInd, itm in enumerate(rasa_response[0]['buttons']):
                                        #         if len(itm['title']) >= 19:
                                        #             tempDict = {
                                        #                 "type": "reply",
                                        #                 "reply": {
                                        #                     "id": f"ID_4_{itm['payload']}",
                                        #                     "title": f"{itm['title'][:19]}..."
                                        #                 }
                                        #             }
                                        #         else:
                                        #             tempDict = {
                                        #                 "type": "reply",
                                        #                 "reply": {
                                        #                     "id": f"ID_4_{itm['payload']}",
                                        #                     "title": f"{itm['title'][:19]}"
                                        #                 }
                                        #             }
                                        #         buttonList.append(tempDict)
                                        #     send_button_menu(phone_number_id, from_number, reply_text, buttonList)

                                        elif 'ID_4' in message.get("interactive").get("list_reply").get("id"):
                                            message_text = message.get("interactive").get("list_reply").get("id").replace('ID_4_', '')
                                            response = requests.post(ngrok_link, json={'message': message_text})
                                            rasa_response = response.json()
                                            print(message_text,"-----------")
                                            print(response,"----response-------")
                                            print(response.json(),"-------------------- printing response from json")
                                            reply_text = rasa_response[0]['text']

                                            send_reply(phone_number_id, from_number, reply_text)

                                elif message.get("type") == 'location':
                                    latitude = message.get("location").get("latitude")
                                    longitude = message.get("location").get("longitude")
                                    # print({'LocationData': {'lat': latitude, 'long': longitude}})
                                    response = requests.post(ngrok_link, json={
                                                                    "sneder":"rasa",
                                                                    "message": f"lat: {latitude}, long: {longitude}, mob_num: {27647828232}",
                                                                    })
                                    print({                         '1'"2"
                                                                    "sneder":"rasa",
                                                                    "message": f"lat: {latitude}, long: {longitude}, mob_num:{27647828232}",
                                                                    })
                                    rasa_response = response.json()
                                    reply_text = rasa_response[0]['text']
                                    print(latitude, longitude, "-----------")
                                    print(response,"----response-------")
                                    print(response.json(),"-------------------- printing response from json")
                                    # send_reply(phone_number_id, from_number, reply_text)
                                    print('inside else in location')
                                    buttonStr = ''
                                    if 'Please enter your first name.' in reply_text:
                                        send_reply(phone_number_id, from_number, reply_text)
                                    elif 'Sorry, we are not operating in this location.' in reply_text:
                                        send_reply(phone_number_id, from_number, reply_text)
                                    else:
                                        for itmInd, itm in enumerate(rasa_response[0]['buttons']):
                                            buttonStr = buttonStr + f"*{itmInd+1}* {itm['title']}\n"
                                        # send_main_menu(phone_number_id, from_number, reply_text, buttonList)
                                    reply_text = f'{reply_text}\n{buttonStr}\n'
                                    print(reply_text)
                                    send_reply(phone_number_id, from_number, buttonStr)


        return jsonify({'message': 'success'}), 200

    else:
        if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == 'token':
            return request.args.get('hub.challenge')
        else:
            return 'Invalid verification token'

if __name__ == '__main__':
    app.run(debug=True)