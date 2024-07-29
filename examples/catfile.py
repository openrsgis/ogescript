with open(file_path, 'rb') as f:
    data = f.read()

# 计算帧数
frame_size = 1040
frame_num = len(data) // frame_size

# 裁剪每帧的帧头，使其为1024帧长
new_data = b''
for i in range(frame_num):
    start = i * frame_size + 16  # 裁剪帧头，从第16个字节开始
    end = (i + 1) * frame_size
    new_data += data[start:end]

# 写入新文件
new_file_path = 'new_file.bin'
with open(new_file_path, 'wb') as f:
    f.write(new_data)