#!/usr/bin/python
import telebot
import re
import config
from shutil import copyfile
from os import path

bot = telebot.TeleBot(config.token)

@bot.message_handler(func=lambda message: message.from_user.first_name == config.user_name,  
                     content_types=['audio','document', 'video', 'photo'])
def download1(message):
    attachment = get_attachment(message)
    
    print(message)
    
    telegram_file_path = bot.get_file(attachment.file_id).file_path
    downloaded_file = bot.download_file(telegram_file_path)
    
    save_path = get_save_path(attachment, message.content_type)
    save_file(save_path, downloaded_file)

    
def get_attachment(message):
    if message.content_type == 'audio':
        return message.audio
    if message.content_type == 'document':
        return message.document
    if message.content_type == 'video':
        return message.video
    if message.content_type == 'photo':
        return message.photo[-1]
  
def get_save_path(attachment, content_type):
    if content_type == 'photo':
        save_path = config.save_folder + 'photo.jpg'
    else:
        save_path = config.save_folder + attachment.file_name
    
    counter = 1
    while path.exists(save_path):
        if counter == 1:
            save_path += f' ({counter})'
        else:
            save_path = re.sub(r'\(\d+\)', f'({counter})', save_path)
        counter += 1
        
    return save_path   
  
def save_file(path, file):
    with open(path,'wb') as new_file:
        new_file.write(file)

   
bot.polling()
