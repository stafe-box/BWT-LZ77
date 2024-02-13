from bitarray import bitarray
from LZ77Compressor import LZ77Compressor
from Bwt import Bwt
import os


class Archiver:
    def __init__(self):
        self.bwt = Bwt('$')  # End of File character
        self.lz77 = LZ77Compressor()

    def compress(self, input_file_path, output_file_path):
        # Apply BWT to the input file
        with open(input_file_path, 'r') as f:
            
            input_text = f.read()
            input_text = input_text.replace('\n',"*")
            bwt_encoded = self.bwt.encode(input_text)
            # print (bwt_encoded)

            # Save intermediate result
            intermediate_path = output_file_path + ".bwt"
            with open(intermediate_path, 'w', encoding='utf-8') as f:
                f.write(''.join(bwt_encoded))

        # Apply LZ77 to the BWT encoded data
        self.lz77.compress(intermediate_path, output_file_path)

        # Clean up intermediate file
        os.remove(intermediate_path)
        Ssrc = os.path.getsize(input_file_path)
        Scomp = os.path.getsize(output_file_path)
        SSR = (1 - Scomp/Ssrc) * 100
        print (f"Compression {SSR:.2f} %")

    def decompress(self, input_file_path, output_file_path):
        # Apply LZ77 decompression
        intermediate_path = input_file_path + ".bwt"
        self.lz77.decompress(input_file_path, intermediate_path)

        # Apply BWT to the decompressed data
        with open(intermediate_path, 'rb') as f:
            bwt_encoded = f.read().decode('utf-8')
        original_text = self.bwt.decode(list(bwt_encoded))
        text = ''.join(original_text)
        text = text.replace('*', '\n')

        # Save the decompressed result
        with open(output_file_path, 'w') as f:
            f.write(text)

        # Clean up intermediate file
        os.remove(intermediate_path)