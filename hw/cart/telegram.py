import requests
from telegram import Bot
from decimal import Decimal
from .cart import Cart

def get_chat_id(bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['result']:
            chat_id = data['result'][0]['message']['chat']['id']
            return chat_id
        
        else:
            print('No updated found ')
            
    else:   
        print(f'No updates found{response.status_code}')
        
        
async def send_message(bot_token, chat_id, text): 
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=text)
    

chat_id = get_chat_id('6728546633:AAG-Qk1fSeD7qrxGqL7Qp8Lx95I9a_Z-AsU')

async def main(text):
    await send_message('6728546633:AAG-Qk1fSeD7qrxGqL7Qp8Lx95I9a_Z-AsU', chat_id, text)





