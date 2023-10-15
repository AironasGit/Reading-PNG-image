def read_chunk(file):
    chunk_length = int(file.read(4).hex(), 16) # First 4 bytes of a chunk describe its length
    chunk_type = file.read(4).decode('ascii') # Following 4 bytes of a chunk describe its type
    chunk_data = file.read(chunk_length).hex()
    chunk_crc = file.read(4)
    return chunk_type, chunk_data

def get_png_file_chunks(file_path):
    pngSignature = b'\x89PNG\r\n\x1a\n'
    with open(file_path, 'rb') as file: # Opening the file in binary mode
        signature = file.read(8) # First 8 bytes is always the PNG signature
        if signature != pngSignature:
            raise Exception('Not PNG file')
        chunks = []
        while True:
            chunk_type, chunk_data = read_chunk(file)
            chunks.append((chunk_type, chunk_data))
            if chunk_type == 'IEND': # Last chunk is always 'IEND'
                break
    return chunks

def unpack_IHDR_data(IHDR_data):
    width = int(IHDR_data[:8], 16) # Width = 4 bytes
    height = int(IHDR_data[8:16], 16) # Height = 4 bytes
    bit_depth = int(IHDR_data[16:18], 16) # Bit depth = 1 byte
    color_type = int(IHDR_data[18:20], 16) # Color type = 1 byte
    compression_method = int(IHDR_data[20:22], 16) # Compression method = 1 byte
    filter_method = int(IHDR_data[22:24], 16) # Filter method = 1 byte
    interlace_method = int(IHDR_data[24:26], 16) # Interlace method = 1 byte
    # The PNG specification only supports 0 as the compression method and 0 as the filter method
    if compression_method != 0:
        raise Exception('invalid compression method')
    if filter_method != 0:
        raise Exception('invalid filter method')
    #if color_type != 6:
    #    raise Exception('we only support truecolor with alpha')
    #if bit_depth != 8:
    #    raise Exception('we only support a bit depth of 8')
    #if interlace_method != 0:
    #    raise Exception('we only support no interlacing')
    return width, height, bit_depth, color_type, compression_method, filter_method, interlace_method

def main():
    file_path = 'C:/Users/Aironas/Downloads/Rank.PNG'
    chunks = get_png_file_chunks(file_path)

    _, IHDR_data = chunks[0] # First chunk is always 'IHDR'
    width, height, bit_depth, color_type, compression_method, filter_method, interlace_method = unpack_IHDR_data(IHDR_data)
    IDAT_data = ''.join(chunk_data for chunk_type, chunk_data in chunks if chunk_type == 'IDAT')
    print(IDAT_data[len(IDAT_data) - 4:])
if __name__ == '__main__':
    main()