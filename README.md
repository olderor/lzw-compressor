# Telegram Bot
Select a mode: /compress /decompress /download or /compare and send a file.<br/>
Or just send a link (or few links) and it will compress all (href parameters) .txt files on that page.
<br/>
# Console app
Run [main.py](./lzw-compressor/main.py)<br />
First parameter is command (either "compress", "decompress" or "compare").<br />
1) "compress" command - needs one or more parameters: paths to files to archive. It will compress files into archive and save it in the current directory with name 'archive.LUL'.<br />
2) "decompress" command - needs one parameter - path to archive. It will decompress all files from archive into current directory.<br />
3) "compare" command - needs two more parameters: first filename and second filename. You can use this command to compare a content of two files. It will print True to the console if the content is the same, False if it differs.
