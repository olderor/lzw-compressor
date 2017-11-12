# Telegram Bot
Select a mode: /compress /decompress or /compare and send a file.<br/>
Or just send a link (or few links) and it will compress all (href parameters) .txt files on that page.
<br/>
# Console app
Run [main.py](./lzw-compressor/main.py)<br />
First parameter is command (either "compress", "decompress" or "compare").<br />
1) "compress" command - needs two more parameters: input filename and output filename. It will compress input file into the file with selected output filename.
2) "decompress" command - needs two more parameters: input filename and output filename. It will decompress input file into the file with selected output filename.
3) "compare" command - needs two more parameters: first filename and second filename. You can use this command to compare a content of two files. It will print True to the console if the content is the same, False if it differs.
