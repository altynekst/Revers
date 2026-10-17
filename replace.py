import sys
file_path = 'work/assets/bin/Data/Managed/Metadata/global-metadata.dat'

# Оригинал (13 байт)
old_utf8 = b'NOOMIUNLOCKED'
# Новая строка без пробела, чтобы было ровно 13 байт
new_utf8 = b'crack bytuman'

# Версия для UTF-16 (для Unity)
old_utf16 = 'NOOMIUNLOCKED'.encode('utf-16le')
new_utf16 = 'crack bytuman'.encode('utf-16le')

with open(file_path, 'rb') as f:
    data = f.read()

found = False

if old_utf8 in data:
    data = data.replace(old_utf8, new_utf8)
    print("Найдено и заменено (UTF-8)")
    found = True

if old_utf16 in data:
    data = data.replace(old_utf16, new_utf16)
    print("Найдено и заменено (UTF-16)")
    found = True

if found:
    with open(file_path, 'wb') as f:
        f.write(data)
else:
    print("ОШИБКА: Строка не найдена!")
