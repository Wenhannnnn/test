#Start of skeleton code
import csv
#Open the binary input file
input_file = open("binaryFileC_74.bin", 'rb')
FRAME_SIZE = 26
data_frames = []
frame_number = 1
#Read the first byte and loop as long as
#there is always another byte available
byte = input_file.read(1)
Framestart = False
output_file_path = "output.csv"
temperature_table = {
    0xA0: 30.0, 0xA1: 30.1, 0xA2: 30.2, 0xA3: 30.3, 0xA4: 30.4, 0xA5: 30.5, 0xA6: 30.6, 0xA7: 30.7,
    0xA8: 30.8, 0xA9: 30.9, 0xAA: 31.0, 0xAB: 31.1, 0xAC: 31.2, 0xAD: 31.3, 0xAE: 31.4, 0xAF: 31.5,
    0xB0: 31.6, 0xB1: 31.7, 0xB2: 31.8, 0xB3: 31.9, 0xB4: 32.0, 0xB5: 32.1, 0xB6: 32.2, 0xB7: 32.3,
    0xB8: 32.4, 0xB9: 32.5, 0xBA: 32.6, 0xBB: 32.7, 0xBC: 32.8, 0xBD: 32.9, 0xBE: 33.0, 0xBF: 33.1,
    0xC0: 33.2, 0xC1: 33.3, 0xC2: 33.4, 0xC3: 33.5, 0xC4: 33.6, 0xC5: 33.7, 0xC6: 33.8, 0xC7: 33.9,
    0xC8: 34.0, 0xC9: 34.1, 0xCA: 34.2, 0xCB: 34.3, 0xCC: 34.4, 0xCD: 34.5, 0xCE: 34.6, 0xCF: 34.7,
    0xD0: 34.8, 0xD1: 34.9, 0xD2: 35.0, 0xD3: 35.1, 0xD4: 35.2, 0xD5: 35.3, 0xD6: 35.4, 0xD7: 35.5,
    0xD8: 35.6, 0xD9: 35.7, 0xDA: 35.8, 0xDB: 35.9, 0xDC: 36.0, 0xDD: 36.1, 0xDE: 36.2, 0xDF: 36.3,
    
}
def lookup_temperature(byte_value):
    if byte_value in temperature_table:
        return temperature_table[byte_value]
    else:
        return None
    
while byte:
    print("Byte value is (hexidecimal): " + str(byte))
    print("Byte value is (decimal): " + str(int.from_bytes(byte)))
    if byte == b'~':
        # Read the next byte to check if it's also the start of a frame
        next_byte = input_file.read(1)
        if next_byte == b'~':
            Framestart = True

            input_file.seek(-2, 1)
            frame_bytes = input_file.read(FRAME_SIZE)
            checksum = 255 - (sum(frame_bytes[:-1]) % 256 )

            if checksum == frame_bytes[-1]:
                # Store the frame in the list along with its number
                data_frames.append((frame_number, frame_bytes))
                byte_str = ', '.join(str(byte) for byte in frame_bytes)
                print(f"Data frame {frame_number}: {byte_str}")
            else:
                print(f"Frame {frame_number} has incorrect checksum and will be discarded.")
            frame_number += 1
        else:
            print(f"Frame {frame_number} has incorrect harder and will be discarded.")
            frame_number += 1

    
    #
    #
    # add decoding method here
    #
    #

    #Get the next byte from the file and repeat
    byte = input_file.read(1)


#Must be end of the file so close the file
print("End of file reached")
input_file.close()

#解码

# 创建一个列表，用于存储处理后的信息
processed_frames = []

for frame in data_frames:
    frame_bytes = frame[1]

    # 解析每个byte
    byte1_char = chr(frame_bytes[0])  # 第1个byte转换成ASCII字符
    byte2_char = chr(frame_bytes[1])  # 第2个byte转换成ASCII字符
    byte3_decimal = frame_bytes[2]
    byte4_decimal = frame_bytes[3]
    byte5_decimal = frame_bytes[4]
    byte6_decimal = frame_bytes[5]
    byte7_decimal = frame_bytes[6]
    # byte3_to_7_decimal = int.from_bytes(frame_bytes[2:7], byteorder='big')  # 第3至第7个byte转换成10进制数
    byte8_char = chr(frame_bytes[7])  # 第8个byte转换成ASCII字符
    byte9_to_10_uint16 = int.from_bytes(frame_bytes[8:10], byteorder='big')  # 第9至第10个byte转换成16位无符号整数
    byte11_to_12_uint16 = int.from_bytes(frame_bytes[10:12], byteorder='big')  # 第11至第12个byte转换成16位无符号整数
    byte13_to_14_uint16 = int.from_bytes(frame_bytes[12:14], byteorder='little')  # 第13至第14个byte转换成16位无符号整数
    byte15_hex = lookup_temperature(frame_bytes[14])  # 第15个byte查表
    byte16_hex = lookup_temperature(frame_bytes[15])  # 第16个byte转换成16进制
    byte17_char = chr(frame_bytes[16])  # 第17个byte转换成ASCII字符
    byte18_to_25_uint64 = int.from_bytes(frame_bytes[17:25], byteorder='big')  # 第18至第25个byte转换成64位无符号整数
    byte26_decimal = frame_bytes[25]  # 第26个byte转换成10进制数

   # 将处理后的信息存储到列表中
    processed_frame_info = [
        byte1_char, byte2_char, byte3_decimal,byte4_decimal,byte5_decimal,byte6_decimal,byte7_decimal, byte8_char,
        byte9_to_10_uint16, byte11_to_12_uint16, byte13_to_14_uint16,
        byte15_hex, byte16_hex, byte17_char, byte18_to_25_uint64,
        byte26_decimal
    ]
    processed_frames.append(processed_frame_info)
    for frame_info in processed_frames:
        print(", ".join(str(item) for item in frame_info))
        print()  # 每个帧输出完成后换行
#End of skeleton code
with open(output_file_path, 'w', newline='') as csvfile:
    # 创建CSV写入对象
    csv_writer = csv.writer(csvfile)

    # 遍历处理后的每个帧信息
    for frame_info in processed_frames:
        # 将每个帧信息写入CSV文件
        csv_writer.writerow(frame_info)
    print("CSV文件写入完成:", output_file_path)