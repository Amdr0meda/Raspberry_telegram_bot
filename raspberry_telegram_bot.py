#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import
#time.sleep(60)

import os
import re
import socket
import telebot
from telebot import types
from requests import get

#Aqui debes poner entre las '' el token de tu bot
TOKEN = '2053244546:AAFStUOfSbBIw7_9rXMD7hyYNfc905ZsGvQ'

bot = telebot.TeleBot(TOKEN)

#Lista de comandos que tiene el bot, esta se mostrará en la ayuda
commands = {
            'about': 'Información sobre el bot y creador',
            'ayuda': 'Lista de comandos disponibles',
            'reiniciar': 'Reinicia la Raspberry',
            'apagar': 'Apaga la Raspberry',
            'exec': 'Ejecuta un comando por terminal',
            'temperatura': 'Temperatura del procesador',
            'usb': 'Dispositivos conectados a puertos USB',
            'red': 'Visualiza la conf de la red e interfaces',
            'ping': 'Realiza ping, comprueba la conexión',
            'memoria': 'Uso y capacidad de las memorias',
            'liberar': 'Vacia la memoria swap',
            'ip_privada': 'Expone la IP privada', 
            'ip_publica': 'Expone la IP publica',
            'hostname': 'Muestra el nombre del equipo'
}

#Comando /start cuando se inicia el bot
@bot.message_handler(commands=['start'])
def command_help(m):
    name = m.from_user.first_name
    bot.send_message(m.chat.id, '¡Hola ' + name + '! Este bot es desarrollado por Amdr0meda, para ver la guia de uso y más información visita:')
    bot.send_message(m.chat.id, 'https://github.com/Amdr0meda/Raspberry_telegram_bot')
    bot.send_message(m.chat.id, 'Utiliza /ayuda ver los comandos disponibles')

#Comando /about información del bot y codigo
@bot.message_handler(commands=['about'])
def command_long_text(m):
    if m.chat.id == 287453931:
        about_bot = 'Este bot es desarrollado por Amdr0meda, para ver la guia de uso y más información visita el repositorio del proyecto en:\n\n https://github.com/Amdr0meda/Raspberry_telegram_bot'
        bot.send_message(m.chat.id, about_bot)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /ayuda que responde enviando un texto con los comandos disponibles
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    if m.chat.id == 287453931:
        help_text = 'Lista de comandos disponibles.\n\n'
        for key in commands:
            help_text += '/' + key + ' - '
            help_text += commands[key] + '\n'
        bot.send_message(m.chat.id, help_text)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /reiniciar reinicia la Raspberry
@bot.message_handler(commands=['reiniciar'])
def command_long_text(m):
    if m.chat.id == 287453931:
        bot.send_message(m.chat.id, 'Reiniciando, recibirás un mensaje cuando se complete.')
        os.system('sudo shutdown -r now')
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /apagar apaga la Raspberry
@bot.message_handler(commands=['apagar'])
def command_long_text(m):
    if m.chat.id == 287453931:
        bot.send_message(m.chat.id, 'Reiniciando, recibirás un mensaje cuando se complete.')
        os.system('sudo shutdown -r now')
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /ip_privada que muestra la ip privada del equipo
@bot.message_handler(commands=['ip_privada'])
def command_long_text(m):
    if m.chat.id == 287453931:
        f = os.popen('hostname -I')
        ip_private = f.read()
        bot.send_message(m.chat.id, 'Tu direccion IP privada es: ')
        bot.send_message(m.chat.id, ip_private)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /ip_publica que muestra la ip publica del equipo
@bot.message_handler(commands=['ip_publica'])
def command_long_text(m):
    if m.chat.id == 287453931:
        ip_public = get('https://api.ipify.org').text
        bot.send_message(m.chat.id, 'Tu direccion IP publica es: ')
        bot.send_message(m.chat.id, ip_public)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /hostame muestra el nombre del equipo
@bot.message_handler(commands=['hostname'])
def command_long_text(m):
    if m.chat.id == 287453931:
        hostname = socket.gethostname()
        bot.send_message(m.chat.id, 'El nombre de tu equipo es:')
        bot.send_message(m.chat.id, hostname)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /exec que responde ejecutando X comando en la terminal
@bot.message_handler(commands=['exec'])
def command_long_text(m):
    if m.chat.id == 287453931:
        bot.send_message(m.chat.id, 'Resultado del comando:')
        f = os.popen(m.text[len('/exec '):])
        result = f.read()
        bot.send_message(m.chat.id, result)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /temperatura muestra la temperatura del procesador y un comentario
@bot.message_handler(commands=['temperatura'])
def command_long_text(m):
    if m.chat.id == 287453931:
        f = os.popen('vcgencmd measure_temp')
        dump = f.read()
        cleaned = re.sub(r"[temp='C]","", dump)
        temperature = cleaned.rstrip()
        if (temperature <= '40'):
            bot.send_message(m.chat.id,'Temperatura normal: ' + temperature + ' °C')
        elif (temperature <= '50'):
            bot.send_message(m.chat.id,'Temperatura alta: ' + temperature + ' °C')
        else:
            bot.send_message(m.chat.id,'Temperatura muy alta: ' + temperature + ' °C')
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /usb muestra los dispositivos conectados a puertos USB
@bot.message_handler(commands=['usb'])
def command_long_text(m):
    if m.chat.id == 287453931:
        f = os.popen('lsusb')
        result = f.read()
        bot.send_message(m.chat.id, result)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /red Visualiza la conf de la red y sus interfaces
@bot.message_handler(commands=['red'])
def command_long_text(m):
    if m.chat.id == 287453931:
        f = os.popen('ifconfig')
        result = f.read()
        bot.send_message(m.chat.id, result)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /ping con un ping a Google 2 veces
@bot.message_handler(commands=['ping'])
def command_long_text(m):
    if m.chat.id == 287453931:
        f = os.popen('ping www.google.com -c 1')
        result = f.read()
        bot.send_message(m.chat.id, 'El resultado del ping a www.google.com es: \n\n' + result)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /memoria muestra el uso y capacidad de las memorias
@bot.message_handler(commands=['memoria'])
def command_long_text(m):
    if m.chat.id == 287453931:
        f = os.popen('free -m')
        result = f.read()
        bot.send_message(m.chat.id, '(Memoria mostrada en megabytes)')
        bot.send_message(m.chat.id, result)
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Comando /memoria muestra el uso y capacidad de las memorias
@bot.message_handler(commands=['liberar'])
def command_long_text(m):
    if m.chat.id == 287453931:
        f = os.popen('sudo swapoff -a ; sudo swapon -a')
        bot.send_message(m.chat.id, 'La memoria swap ha sido liberada')
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

#Texto para cuando el usuario escribe cualquier comando / palabra que no este declarada
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    if m.chat.id == 287453931:
        bot.send_message(m.chat.id, 'No te entiendo, escribe /ayuda para ver los comandos disponibles')
    else:
        bot.send_message(m.chat.id, 'No estas autorizado. Utiliza /about para obtener mas información')

bot.infinity_polling()