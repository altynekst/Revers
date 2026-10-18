import sys, struct, UnityPy
d, level, old, new = sys.argv[1:5]
path = f"{d}/{level}"
env = UnityPy.load(path)
def enc(s):
    b = s.encode()
    return struct.pack("<I", len(b)) + b + b"\x00" * ((4 - len(b) % 4) % 4)
oe, ne = enc(old), enc(new)
cnt = 0
for o in env.objects:
    raw = bytes(o.get_raw_data())
    if oe in raw:
        n = raw.count(oe); cnt += n
        print("FOUND", o.type.name, "id", o.path_id, "x", n)
        print("HEAD", raw[:64].hex())
        o.set_raw_data(raw.replace(oe, ne))
if not cnt: sys.exit("строка не найдена в " + level)
open(path, "wb").write(env.file.save())
print("OK заменено:", cnt)
