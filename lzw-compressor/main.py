import sys
import file_manager
import compressor


input_filename = sys.argv[1]
output_filename = sys.argv[2]
command = sys.argv[3]

if command == "compress":
    data = file_manager.read_file(input_filename)
    encoded = compressor.compress(data)
    file_manager.write_binary_file(output_filename, encoded)

elif command == "decompress":
    data = file_manager.read_binary_file(input_filename)
    decoded = compressor.decompress(data)
    file_manager.write_file(output_filename, decoded[1], decoded[0])

elif command == "compare":
    print(file_manager.compare_files_content([input_filename, output_filename]))

else:
    print("undefined command")
