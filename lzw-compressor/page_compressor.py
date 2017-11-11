import requests
from tqdm import tqdm
from parser import Parser
from compressor_processor import *
from file_manager import create_directory_if_not_exists
from urllib.parse import urljoin, urlparse


ALLOWED_TEXT_FORMATS = [".txt"]


class PageCompressor:

    @staticmethod
    def process_url(url, chat_id, bot):
        content = PageCompressor.get_page_content(url)
        text_files_links = PageCompressor.find_links_to_text_files(content)
        if len(text_files_links) == 0:
            bot.send_message(chat_id, "No text files found on that page (" + url + ").")
            return
        bot.send_message(chat_id, "Compressing text files:\n" + "\n".join(text_files_links))
        directory_path = "./data/" + str(chat_id) + "/links/"
        create_directory_if_not_exists(directory_path)
        for link in text_files_links:
            full_url = urljoin(url, link)
            print(full_url)
            filename = PageCompressor.get_file_name_from_url(full_url)
            compressed_filename = "compressed_" + filename
            file_path = directory_path + filename
            compressed_file_path = directory_path + compressed_filename
            PageCompressor.download_text_file(full_url, directory_path)
            CompressorProcessor.compress(file_path, compressed_file_path)
            doc = open(compressed_file_path, 'rb')
            bot.send_document(chat_id, doc)
            doc.close()
            size_dif = CompressorProcessor.get_file_sizes_difference(file_path, compressed_file_path)
            if size_dif < 0:
                bot.send_message(chat_id, "Compressing done. No data compressed :(")
            else:
                bot.send_message(chat_id,
                                 "Compressing done. :)\nSaved " + format_number(size_dif) + " bytes (" + format_size(
                                     size_dif) + ").")

    @staticmethod
    def get_file_name_from_url(url):
        filename = url.split('/')[-1]
        return filename

    @staticmethod
    def download_text_file(link_to_file, directory_path):
        filename = PageCompressor.get_file_name_from_url(link_to_file)
        response = requests.get(link_to_file, stream=True, verify=False)

        with open(directory_path + filename, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

    @staticmethod
    def find_links_to_text_files(content):
        href_links = Parser.find_hrefs(content)
        text_files_links = []
        for link in href_links:
            for text_format in ALLOWED_TEXT_FORMATS:
                if link.endswith(text_format):
                    text_files_links.append(link)
                    break
        return text_files_links

    @staticmethod
    def get_page_content(url):
        return requests.get(url, verify=False).text
