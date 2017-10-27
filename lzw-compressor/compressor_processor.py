import sys
import file_manager
import compressor
from enum import Enum


class CompressingMode(Enum):
    COMPRESS = 1
    DECOMPRESS = 2
    COMPARE = 3


class CompressorProcessor:

    def __init__(self):
        self.mode = dict()
        self.files = dict()

    @staticmethod
    def compress(file_path, compressed_file_path):
        data = file_manager.read_binary_file(file_path)
        encoded = compressor.compress(data)
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
            if self.compare(files[0][0], files[1][0]):
                bot.send_message(chat_id, "The content is the same.")
            else:
                bot.send_message(chat_id, "The content is different.")
        elif mode == CompressingMode.COMPRESS:
            bot.send_message(chat_id, "Compressing...")
            self.compress(files[0][0], files[0][1])
            doc = open(files[0][1], 'rb')
            bot.send_document(chat_id, doc)
            doc.close()
        else:
            bot.send_message(chat_id, "Decompressing...")
            self.decompress(files[0][0], files[0][2])
            doc = open(files[0][2], 'rb')
            bot.send_document(chat_id, doc)
            doc.close()
        self.files[chat_id] = []

    def add_file(self, file_path, compressed_file_path, decompressed_file_path, bot, chat_id):
        if chat_id not in self.mode:
            self.mode[chat_id] = CompressingMode.COMPRESS
            bot.send_message(chat_id, "Selected compress mode by defauld.")
        self.files.setdefault(chat_id, [])
        self.files[chat_id].append((file_path, compressed_file_path, decompressed_file_path))
        if self.mode[chat_id] == CompressingMode.COMPARE:
            if len(self.files[chat_id]) == 2:
                self.process(bot, chat_id)
        else:
            self.process(bot, chat_id)

    def set_mode(self, chat_id, mode):
        self.mode[chat_id] = mode
