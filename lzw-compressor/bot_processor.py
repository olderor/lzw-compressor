import datetime
import telebot
import os
import logging
from compressor_processor import *

TOKEN = "450503576:AAGBzxaZDaPyrP4Fuu-3J8_I47raOpsavfM"

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
compressor = CompressorProcessor()


def create_directory_if_not_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


@bot.message_handler(commands=["compress"])
def select_compress_mode(message):
    compressor.set_mode(message.chat.id, CompressingMode.COMPRESS)
    bot.send_message(message.chat.id, "Selected compress mode. Now send a file to compress.")


@bot.message_handler(commands=["decompress"])
def select_compress_mode(message):
    compressor.set_mode(message.chat.id, CompressingMode.DECOMPRESS)
    bot.send_message(message.chat.id, "Selected decompress mode. Now send a compressed file.")


@bot.message_handler(commands=["compare"])
def select_compress_mode(message):
    compressor.set_mode(message.chat.id, CompressingMode.COMPARE)
    bot.send_message(message.chat.id, "Selected comparing mode. Now send two files to compare its content.")


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Select a mode: /compress /decompress or /compare and send me a file.")


@bot.message_handler(content_types=["text"])
def undefined_text(message):
    bot.reply_to(message, "Select a mode /compress /decompress or /compare and send me a file.")


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        directory = "./data/" + str(chat_id) + "/document/"
        src = directory + message.document.file_id + "_" + message.document.file_name
        compressed = directory + "compressed_" + message.document.file_id + "_" + message.document.file_name
        decompressed = directory + "decompressed_" + message.document.file_id + "_" + message.document.file_name
        create_directory_if_not_exists(src)
        create_directory_if_not_exists(compressed)
        create_directory_if_not_exists(decompressed)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Document successfully uploaded.")
        compressor.add_file(src, compressed, decompressed, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['photo'], func=lambda message: not message.from_user.is_bot)
def handle_photo(message):
    try:
        chat_id = message.chat.id
        directory = "./data/" + str(chat_id) + "/photo/"
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        file_name = file_info.file_path.replace("/", "_")
        downloaded_file = bot.download_file(file_info.file_path)
        src = directory + photo.file_id + "_" + file_name
        compressed = directory + "compressed_" + photo.file_id + "_" + file_name
        decompressed = directory + "decompressed_" + photo.file_id + "_" + file_name
        create_directory_if_not_exists(src)
        create_directory_if_not_exists(compressed)
        create_directory_if_not_exists(decompressed)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Photo successfully uploaded.")
        compressor.add_file(src, compressed, decompressed, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.video.file_id)
        file_name = file_info.file_path.replace("/", "_")
        downloaded_file = bot.download_file(file_info.file_path)
        directory = "./data/" + str(chat_id) + "/video/"
        src = directory + message.video.file_id + "_" + file_name
        compressed = directory + "compressed_" + message.video.file_id + "_" + file_name
        decompressed = directory + "decompressed_" + message.video.file_id + "_" + file_name
        create_directory_if_not_exists(src)
        create_directory_if_not_exists(compressed)
        create_directory_if_not_exists(decompressed)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Video successfully uploaded.")
        compressor.add_file(src, compressed, decompressed, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.audio.file_id)
        file_name = file_info.file_path.replace("/", "_")
        downloaded_file = bot.download_file(file_info.file_path)
        directory = "./data/" + str(chat_id) + "/audio/"
        src = directory + message.audio.file_id + "_" + file_name
        compressed = directory + "compressed_" + message.audio.file_id + "_" + file_name
        decompressed = directory + "decompressed_" + message.audio.file_id + "_" + file_name
        create_directory_if_not_exists(src)
        create_directory_if_not_exists(compressed)
        create_directory_if_not_exists(decompressed)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Audio successfully uploaded.")
        compressor.add_file(src, compressed, decompressed, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.sticker.file_id)
        file_name = file_info.file_path.replace("/", "_")
        downloaded_file = bot.download_file(file_info.file_path)
        directory = "./data/" + str(chat_id) + "/sticker/"
        src = directory + message.sticker.file_id + "_" + file_name
        compressed = directory + "compressed_" + message.sticker.file_id + "_" + file_name
        decompressed = directory + "decompressed_" + message.sticker.file_id + "_" + file_name
        create_directory_if_not_exists(src)
        create_directory_if_not_exists(compressed)
        create_directory_if_not_exists(decompressed)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Sticker successfully uploaded.")
        compressor.add_file(src, compressed, decompressed, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)

if __name__ == '__main__':
    bot.polling(none_stop=False, interval=0, timeout=20)
