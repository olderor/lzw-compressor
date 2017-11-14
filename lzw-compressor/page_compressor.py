import requests
from tqdm import tqdm
from parser import Parser
from compressor_processor import *
from file_manager import create_directory_if_not_exists
from urllib.parse import urljoin, urlparse, unquote
import shutil


ALLOWED_TEXT_FORMATS = [".txt"]


class PageProcessor:

    @staticmethod
    def download(url, directory_path):
        if directory_path[-1] != "/":
            directory_path += "/"
        content = PageProcessor.get_page_content(url)
        text_files_links = PageProcessor.find_links_to_text_files(content)
        if len(text_files_links) == 0:
            return
        create_directory_if_not_exists(directory_path)
        paths = []
        for link in text_files_links:
            full_url = urljoin(url, link)
            filename = unquote(PageProcessor.get_file_name_from_url(link))
            file_path = directory_path + filename
            PageProcessor.download_text_file(full_url, directory_path)
            paths.append(file_path)
        return paths

    @staticmethod
    def download_files(url, chat_id, bot):
        content = PageProcessor.get_page_content(url)
        text_files_links = PageProcessor.find_links_to_text_files(content)
        if len(text_files_links) == 0:
            bot.send_message(chat_id, "No text files found on that page (" + url + ").")
            return
        bot.send_message(chat_id, "Downloading " + str(len(text_files_links)) + " text files:\n" + "\n".join(
            map(lambda l: unquote(PageProcessor.get_file_name_from_url(l)), text_files_links)))
        directory_path = "./data/" + str(chat_id) + "/links/"
        create_directory_if_not_exists(directory_path)
        paths = []
        for link in text_files_links:
            full_url = urljoin(url, link)
            filename = unquote(PageProcessor.get_file_name_from_url(link))
            file_path = directory_path + filename
            PageProcessor.download_text_file(full_url, directory_path)
            paths.append(file_path)
        return paths

    @staticmethod
    def send_files(paths, chat_id, bot):
        for path in paths:
            with open(path, 'rb') as doc:
                bot.send_document(chat_id, doc)

    @staticmethod
    def compress(url):
        host = urlparse(url).hostname
        temp_directory = "./temp/"
        paths = PageProcessor.download(url, temp_directory)
        compressed_filename = CompressorProcessor.compress_files(paths, "./", host)
        shutil.rmtree(temp_directory)
        return compressed_filename

    @staticmethod
    def process_url(url, mode, chat_id, bot):
        if mode == CompressingMode.DOWNLOAD:
            paths = PageProcessor.download_files(url, chat_id, bot)
            PageProcessor.send_files(paths, chat_id, bot)
            return
        host = urlparse(url).hostname
        paths = PageProcessor.download_files(url, chat_id, bot)
        directory_path = "./data/" + str(chat_id) + "/links/"
        bot.send_message(chat_id, "Downloaded " + str(len(paths)) + " text files. Now compressing...")
        compressed_filename = CompressorProcessor.compress_files(paths, directory_path, host)
        PageProcessor.send_files([compressed_filename], chat_id, bot)
        size_dif = CompressorProcessor.get_file_sizes_difference(paths, compressed_filename)
        if size_dif[1] < 0:
            bot.send_message(chat_id, "Compressing done. No data compressed :(")
        else:
            bot.send_message(chat_id, "Compressing done. :)\nSaved " + str(size_dif[0]) + "% = " + format_number(size_dif[1]) + " bytes (" + format_size(size_dif[1]) + ").")

    @staticmethod
    def get_file_name_from_url(url):
        filename = url.split('/')[-1]
        return filename

    @staticmethod
    def download_text_file(link_to_file, directory_path):
        filename = unquote(PageProcessor.get_file_name_from_url(link_to_file))
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
