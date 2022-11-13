import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from pprint import pprint

vk_session = vk_api.VkApi(token='vk1.a.TO8lbeT088w1K-ChYnWDbAmuJ8zmL4NzwGWT20rd90Wo7-deaPC0LEZ7yozgp3uf1B077ZDh5-njB2BAWa4Zrz5eORc3q8kIpSPXUQcRHxZ2evs86eCqQEu7BBlKmGtmXKDIcT9JyNRzGbySZBBUNhPqHNAWguyYo0qW9oHdSJTxvyL2Y7ovyTI7Lidp1ubEbkj5eYdBLF5lVfGE1rFawQ')
vk = vk_session.get_api()

longpool = VkLongPoll(vk_session)

def send_message(user_id1):
    data = json.loads(json.dumps(ensure_ascii=False, obj = vk_session.method("messages.getConversations", {"group_id": 207042570, "count": 1, "filter":'unanswered'})))
    #pprint.pprint(data['items']['0']['last_message']['attachments']['0']['market']['title'])
    nameTovar = data['items'][0]['last_message']['attachments'][0]['market']['title']
    price = data['items'][0]['last_message']['attachments'][0]['market']['price']['text']

    username = vk_session.method("users.get", {"user_ids":user_id1})[0]['first_name']
    text = f'Здравствуйте, {username}. Оплата {price} по НОМЕРу карты VISA (сбербанк России) 4276 1609 7424 9097 Ольга Васильевна Я. После оплаты чек и вашу почту'


    linkForUploadFileOnServer = vk_session.method("docs.getMessagesUploadServer", {"type":"doc", "peer_id":user_id1})

    vk_session.method("messages.send", {"user_id":user_id1, "message":text,"random_id":0}) #"attachment": SaveFileOnServer(linkForUploadFileOnServer["upload_url"], user_id1)


def SaveFileOnServer(link, usId):
    result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='docs', peer_id=usId)['upload_url'],
                                                  files={'file': open('PythonApplication1.rar', 'rb')}).text)
    
    jsonAnswer = vk.docs.save(file=result['file'], title='title', tags=[])

    vk.messages.send(
        peer_id=usId,
        random_id=0,
        attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
    )


while True:
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                try:
                    if json.loads(json.dumps(ensure_ascii=False, obj = vk_session.method("messages.getConversations", {"group_id": 207042570, "count": 1, "filter":'unanswered'})))['items'][0]['last_message']['attachments'][0]['market']:
                        print('товар')
                        send_message(event.user_id)  
                except:
                    print('просто сообщение')
                #if event.text.lower():
                    #send_message(event.user_id)




