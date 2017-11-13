import telebot
import logging
from parser import Parser
from page_compressor import PageProcessor
from compressor_processor import *
from file_manager import create_directory_if_not_exists


TOKEN = "450503576:AAGBzxaZDaPyrP4Fuu-3J8_I47raOpsavfM"
ADMIN_CHAT_ID = 152550720
BANNED_USERS = [] #('Dmytro', 'Nazarenko')]


bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
compressor_proc = CompressorProcessor()


def messages_filter(handler):
    def handle(message):
        for user in BANNED_USERS:
            if message.from_user.first_name == user[0] and \
                            message.from_user.last_name == user[1]:
                return
        handler(message)

    return handle


def message_logger(handler):
    def handle(message):
        try:
            username = "usernameNone"
            if message.from_user.username:
                username = message.from_user.username
            first_name = "first_nameNone"
            if message.from_user.first_name:
                first_name = message.from_user.first_name
            last_name = "last_nameNone"
            if message.from_user.last_name:
                last_name = message.from_user.last_name

            bot.send_message(ADMIN_CHAT_ID,
                         "Got message from " + username +
                         " (" + first_name + " " + last_name + ").")
            bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
        except Exception as e:
            logger.error(str(e))
        handler(message)

    return handle


@bot.message_handler(commands=["compress"])
@message_logger
@messages_filter
def select_compress_mode(message):
    compressor_proc.set_mode(message.chat.id, CompressingMode.COMPRESS)
    bot.send_message(message.chat.id, "Selected compress mode. Now send a file to compress.")


@bot.message_handler(commands=["decompress"])
@message_logger
@messages_filter
def select_compress_mode(message):
    compressor_proc.set_mode(message.chat.id, CompressingMode.DECOMPRESS)
    bot.send_message(message.chat.id, "Selected decompress mode. Now send a compressed file.")


@bot.message_handler(commands=["compare"])
@message_logger
@messages_filter
def select_compress_mode(message):
    compressor_proc.set_mode(message.chat.id, CompressingMode.COMPARE)
    bot.send_message(message.chat.id, "Selected comparing mode. Now send two files to compare its content.")


@bot.message_handler(commands=["download"])
@message_logger
@messages_filter
def select_compress_mode(message):
    compressor_proc.set_mode(message.chat.id, CompressingMode.DOWNLOAD)
    bot.send_message(message.chat.id, "Selected downloading mode. Now send a link to text files.")


@bot.message_handler(commands=["help"])
@message_logger
@messages_filter
def help(message):
    bot.send_message(message.chat.id,
"""Select a mode: /compress /decompress or /compare and send me a file.\n
Or just send me a link and I will compress all .txt files listed on that page.""")


@bot.message_handler(content_types=["text"])
@message_logger
@messages_filter
def undefined_text(message):
    links = Parser.find_urls(message.text)
    if len(links) == 0:
        bot.reply_to(message,
"""Select a mode: /compress /decompress or /compare and send me a file.\n
Or just send me a link and I will compress all .txt files listed on that page.""")
        return
    bot.reply_to(message, "Links found:\n" + "\n".join(links) + "\nParsing pages...")
    for link in links:
        try:
            PageProcessor.process_url(link, compressor_proc.get_mode(message.chat.id), message.chat.id, bot)
        except Exception as e:
            bot.send_message(message.chat.id, e)


@bot.message_handler(content_types=['document'])
@message_logger
@messages_filter
def handle_docs(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        directory = "./data/" + str(chat_id) + "/document/"
        src = directory + message.document.file_name
        create_directory_if_not_exists(src)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Document successfully uploaded.")
        compressor_proc.add_file(src, directory, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['photo'])
@message_logger
@messages_filter
def handle_photo(message):
    try:
        chat_id = message.chat.id
        directory = "./data/" + str(chat_id) + "/photo/"
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        file_name = file_info.file_path.replace("/", "_")
        downloaded_file = bot.download_file(file_info.file_path)
        src = directory + file_name
        create_directory_if_not_exists(src)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Photo successfully uploaded.")
        compressor_proc.add_file(src, directory, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['video'])
@message_logger
@messages_filter
def handle_video(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.video.file_id)
        file_name = file_info.file_path.replace("/", "_")
        downloaded_file = bot.download_file(file_info.file_path)
        directory = "./data/" + str(chat_id) + "/video/"
        src = directory + file_name
        create_directory_if_not_exists(src)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Video successfully uploaded.")
        compressor_proc.add_file(src, directory, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['audio'])
@message_logger
@messages_filter
def handle_audio(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.audio.file_id)
        file_name = file_info.file_path.replace("/", "_")
        downloaded_file = bot.download_file(file_info.file_path)
        directory = "./data/" + str(chat_id) + "/audio/"
        src = directory + file_name
        create_directory_if_not_exists(src)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Audio successfully uploaded.")
        compressor_proc.add_file(src, directory, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['sticker'])
@message_logger
@messages_filter
def handle_sticker(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.sticker.file_id)
        file_name = file_info.file_path.replace("/", "_")
        downloaded_file = bot.download_file(file_info.file_path)
        directory = "./data/" + str(chat_id) + "/sticker/"
        src = directory + file_name
        create_directory_if_not_exists(src)
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Sticker successfully uploaded.")
        compressor_proc.add_file(src, directory, bot, chat_id)
    except Exception as e:
        bot.reply_to(message, e)

if __name__ == '__main__':
    bot.polling(none_stop=False, interval=0, timeout=20)
