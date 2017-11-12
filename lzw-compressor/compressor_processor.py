import os
import file_manager
import compressor2 as compressor
from enum import Enum
import math


class CompressingMode(Enum):
    COMPRESS = 1
    DECOMPRESS = 2
    COMPARE = 3


def format_size(size, precision=2):
    suffixes = ["B", "KB", "MB", "GB", "TB"]
    suffix_index = 0
    while size > 1024 and suffix_index < 4:
        suffix_index += 1
        size = size / 1024.0
    return "%.*f %s" % (precision, size, suffixes[suffix_index])


def format_number(number):
    s = "%d" % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + " ".join(reversed(groups))


class CompressorProcessor:

    def __init__(self):
        self.mode = dict()
        self.files = dict()

    @staticmethod
    def get_file_sizes_difference(first, second):
        first_size = os.path.getsize(first)
        second_size = os.path.getsize(second)
        return int(math.ceil((first_size - second_size) * 100 / first_size)), first_size - second_size

    @staticmethod
    def compress(file_path, compressed_file_path):
        data = file_manager.read_binary_file(file_path)
        encoded = compressor.compress(data)
        file_manager.write_binary_file(compressed_file_path, encoded)
        if CompressorProcessor.get_file_sizes_difference(file_path, compressed_file_path)[1] < 0:
            encoded = compressor.copy_to_compress(data)
            file_manager.write_binary_file(compressed_file_path, encoded)


    @staticmethod
    def decompress(file_path, compressed_file_path):
        data = file_manager.read_binary_file(file_path)
        decoded = compressor.decompress(data)
        file_manager.write_binary_file(compressed_file_path, decoded)

    @staticmethod
    def compare(first, second):
        return file_manager.compare_files_content([first, second])

    def process(self, bot, chat_id):
        mode = self.mode[chat_id]
        files = self.files[chat_id]
        if mode == CompressingMode.COMPARE:
            bot.send_message(chat_id, "Comparing...")
            if CompressorProcessor.compare(files[0][0], files[1][0]):
                bot.send_message(chat_id, "The content is the same.")
            else:
                bot.send_message(chat_id, "The content is different.")
        elif mode == CompressingMode.COMPRESS:
            bot.send_message(chat_id, "Compressing...")
            CompressorProcessor.compress(files[0][0], files[0][1])
            doc = open(files[0][1], 'rb')
            bot.send_document(chat_id, doc)
            size_dif = CompressorProcessor.get_file_sizes_difference(files[0][0], files[0][1])
            if size_dif[1] < 0:
                bot.send_message(chat_id, "Compressing done. No data compressed :(")
            else:
                bot.send_message(chat_id, "Compressing done. :)\nSaved " + str(size_dif[0]) + "% = " + format_number(size_dif[1]) + " bytes (" + format_size(size_dif[1]) + ").")
            doc.close()
        else:
            bot.send_message(chat_id, "Decompressing...")
            CompressorProcessor.decompress(files[0][0], files[0][2])
            doc = open(files[0][2], 'rb')
            bot.send_document(chat_id, doc)
            doc.close()
        self.files[chat_id] = []

    def add_file(self, file_path, compressed_file_path, decompressed_file_path, bot, chat_id):
        if chat_id not in self.mode:
            self.mode[chat_id] = CompressingMode.COMPRESS
            bot.send_message(chat_id, "Selected compress mode by default.")
        self.files.setdefault(chat_id, [])
        self.files[chat_id].append((file_path, compressed_file_path, decompressed_file_path))
        if self.mode[chat_id] == CompressingMode.COMPARE:
            if len(self.files[chat_id]) == 2:
                self.process(bot, chat_id)
        else:
            self.process(bot, chat_id)

    def set_mode(self, chat_id, mode):
        self.mode[chat_id] = mode
