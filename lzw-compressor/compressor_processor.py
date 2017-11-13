import os
import file_manager
import compressor2 as compressor
from enum import Enum
import math


ARCHIVE_EXTENSION = ".LUL"
TEXT_FILE_EXTENSION = ".txt"

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
    def get_file_sizes_difference(files, archive):
        first_size = 0
        for file in files:
            first_size += os.path.getsize(file)
        second_size = os.path.getsize(archive)
        return int(math.ceil((first_size - second_size) * 100 / first_size)), first_size - second_size

    # @staticmethod
    # def compress(file_path, source_directory):
        # data = file_manager.read_binary_file(file_path)
        # encoded = compressor.compress(data)
        # file_manager.write_binary_file(compressed_file_path, encoded)
        # if CompressorProcessor.get_file_sizes_difference(file_path, compressed_file_path)[1] < 0:
        #     encoded = compressor.copy_to_compress(data)
        #     file_manager.write_binary_file(compressed_file_path, encoded)

    @staticmethod
    def compress_files(file_paths, source_directory, archive_name):
        archive_name = archive_name + ARCHIVE_EXTENSION
        archive_path = source_directory + archive_name
        encoded = []
        for file_path in file_paths:
            name_bytes = bytearray()
            name = file_manager.get_name(file_path)
            name_bytes.extend(map(ord, name))

            content = file_manager.read_binary_file(file_path)

            compressor.encode(name_bytes, encoded)
            compressor.add_split_code(encoded)
            compressor.encode(content, encoded)
            compressor.add_split_code(encoded)
        encoded.pop()
        compressed = compressor.pack(encoded)
        file_manager.write_binary_file(archive_path, compressed)
        return archive_path

    @staticmethod
    def decompress(file_path, source_directory):
        data = file_manager.read_binary_file(file_path)
        decoded = compressor.decompress(data)
        paths = []
        for document_data in decoded:
            path = source_directory + document_data[0] + TEXT_FILE_EXTENSION
            file_manager.write_binary_file(path, document_data[1])
            paths.append(path)
        return paths

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
            archive_path = CompressorProcessor.compress_files(
                [files[0][0]], files[0][1], file_manager.get_name(files[0][0]))
            doc = open(archive_path, 'rb')
            bot.send_document(chat_id, doc)
            size_dif = CompressorProcessor.get_file_sizes_difference([files[0][0]], archive_path)
            if size_dif[1] < 0:
                bot.send_message(chat_id, "Compressing done. No data compressed :(")
            else:
                bot.send_message(chat_id, "Compressing done. :)\nSaved " + str(size_dif[0]) + "% = " + format_number(size_dif[1]) + " bytes (" + format_size(size_dif[1]) + ").")
            doc.close()
        else:
            bot.send_message(chat_id, "Decompressing...")
            documents = CompressorProcessor.decompress(files[0][0], files[0][1])
            for document in documents:
                with open(document, 'rb') as doc:
                    bot.send_document(chat_id, doc)
        self.files[chat_id] = []

    def add_file(self, file_path, source_directory, bot, chat_id):
        if chat_id not in self.mode:
            self.mode[chat_id] = CompressingMode.COMPRESS
            bot.send_message(chat_id, "Selected compress mode by default.")
        self.files.setdefault(chat_id, [])
        self.files[chat_id].append((file_path, source_directory))
        if self.mode[chat_id] == CompressingMode.COMPARE:
            if len(self.files[chat_id]) == 2:
                self.process(bot, chat_id)
        else:
            self.process(bot, chat_id)

    def set_mode(self, chat_id, mode):
        self.mode[chat_id] = mode
