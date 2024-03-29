import os


def read_file(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text


def read_binary_file(filename):
    file = open(filename, 'rb')
    text = file.read()
    file.close()
    return text


def write_file(filename, content, encoding):
    file = open(filename, 'w', encoding=encoding)
    file.write(content)
    file.close()


def write_binary_file(filename, content):
    file = open(filename, 'wb')
    file.write(content)
    file.close()


def compare_files_content(filenames):
    if len(filenames) < 2:
        return True
    content = read_binary_file(filenames[0])
    for i in range(1, len(filenames)):
        to_compare = read_binary_file(filenames[i])
        if content != to_compare:
            return False
    return True


def create_directory_if_not_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_name(path):
    return os.path.basename(path).split('.')[0]


def get_directory_name(path):
    return get_name(os.path.dirname(path))
