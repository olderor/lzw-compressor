import sys
from compressor_processor import CompressorProcessor
from page_compressor import PageProcessor
import re
import codecs


ESCAPE_SEQUENCE_RE = re.compile(r"""
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )""", re.UNICODE | re.VERBOSE)


def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')
    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


command = sys.argv[1]

if command == "compress":
    paths = list(map(lambda p: p.encode('utf-8').decode('unicode_escape'), sys.argv[2:]))
    if len(paths) == 0:
        print("Warning! No files selected to compress.")
    else:
        CompressorProcessor.compress_files(paths, "./", 'archive')

elif command == "decompress":
    archive = sys.argv[2]
    CompressorProcessor.decompress(archive, "./archive/")

elif command == "compare":
    print(CompressorProcessor.compare(sys.argv[2], sys.argv[3]))
elif command == "download":
    paths = PageProcessor.download(sys.argv[2], sys.argv[3])
    print("Downloaded " + str(len(paths)) + " files.")
    for path in paths:
        print(path)
    print("Done.")
elif command == "compress_link":
    PageProcessor.compress(sys.argv[2])
else:
    print("undefined command")
