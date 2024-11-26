import struct
import os

def conv_utf8_to_utf32(input_file, output_file):
    try:
        input_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', input_file)
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', output_file)

        with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'wb') as outfile:
            bom = 0x0000FEFF
            outfile.write(struct.pack('<I', bom))
            for line in infile:
                utf32_chars = [struct.pack('<I', ord(char)) for char in line]
                outfile.writelines(utf32_chars)

    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
    except Exception as e:
        print(f"Erro ao converter '{input_file}' para UTF-32: {e}")


def conv_utf32_to_utf8(input_file, output_file):
    input_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', input_file)
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', output_file)
    
    with open(input_path, 'rb') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        infile.read(4)
        
        while True:
            utf32_bytes = infile.read(4)
            if not utf32_bytes:
                break
            
            utf32_char = struct.unpack('<I', utf32_bytes)[0]
            outfile.write(chr(utf32_char))

