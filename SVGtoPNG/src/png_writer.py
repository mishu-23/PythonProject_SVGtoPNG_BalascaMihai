import zlib
from struct import pack

def write_png(canvas, file_path):
    height, width, _= canvas.shape
    print(f"Writing PNG with dimensions ({width}, {height})")
    png_header = b'\x89PNG\r\n\x1a\n'

    #parametri pentru IHDR chunk
    color_type = 6
    bit_depth = 16
    compression = 0
    filter_method = 0
    interlace = 0

    print(f"PNG file {file_path} written successfully.")


    ihdr = pack('>IIBBBBB', width, height, bit_depth, color_type, compression, filter_method, interlace)
    ihdr_chunk = create_chunk(b'IHDR', ihdr)
    data = b''.join(b'\x00' + row.tobytes() for row in canvas)
    compressed_data = zlib.compress(data)
    idat_chunk = create_chunk(b'IDAT', compressed_data)
    iend_chunk = create_chunk(b'IEND', b'')
    with open(file_path, 'wb') as f:
        f.write(png_header)
        f.write(ihdr_chunk)
        f.write(idat_chunk)
        f.write(iend_chunk)

def create_chunk(chunk_type, data):
    length = len(data)
    crc = zlib.crc32(chunk_type, length) & 0xffffffff
    return pack('>I', length) + chunk_type + data + pack('>I', crc)