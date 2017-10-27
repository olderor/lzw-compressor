import sys
from compressor_processor import CompressorProcessor


input_filename = sys.argv[1]
output_filename = sys.argv[2]
command = sys.argv[3]

if command == "compress":
    CompressorProcessor.compress(input_filename, output_filename)

elif command == "decompress":
    CompressorProcessor.decompress(input_filename, output_filename)

elif command == "compare":
    print(CompressorProcessor.compare(input_filename, output_filename))

else:
    print("undefined command")
