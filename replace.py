import sys
file_path = 'work/assets/bin/Data/Managed/Metadata/global-metadata.dat'
old_str = b'NOOMIUNLOCKED'  # 13 символов
# \x00 в конце - это нулевой байт (заглушка). Вместе с '!' получается ровно 14.
# Но так как мы не можем менять длину, мы просто заменим 13 байт на 13 байт.
# 'Crack by tuman' - это 14 символов. 
# 'Crack by tuma' - 13 символов.
new_str = b'Crack by tuma' 

with open(file_path, 'rb') as f:
    data = f.read()

if old_str in data:
    data = data.replace(old_str, new_str)
    with open(file_path, 'wb') as f:
        f.write(data)
    print("Строка заменена!")
else:
    print("Строка не найдена!")
