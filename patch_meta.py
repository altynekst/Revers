import sys
p, new = sys.argv[1], sys.argv[2].strip()
old = b"https://t.me/noomiunlock"
nb = new.encode()
if len(nb) != len(old):
    sys.exit(f"длина {len(nb)}, нужно {len(old)}")
data = open(p, "rb").read()
c = data.count(old)
if c == 0:
    sys.exit("старая ссылка не найдена")
open(p, "wb").write(data.replace(old, nb))
print("OK заменено:", c, "->", nb.decode())
