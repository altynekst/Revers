import sys, struct
d, level, old, new = sys.argv[1:5]
path = f"{d}/{level}"
data = open(path, "rb").read()
def pad4(n): return b"\x00" * ((4 - n % 4) % 4)
ob = old.encode()
pat = struct.pack("<I", len(ob)) + ob + pad4(len(ob))
cnt = data.count(pat)
if cnt != 1:
    sys.exit(f"нужно ровно 1 совпадение, найдено {cnt}")
nb = new.encode()
room = len(pat) - 4
if len(nb) > room:
    sys.exit(f"не влезает: {len(nb)} > {room} символов")
while 4 + len(nb) + len(pad4(len(nb))) < len(pat):
    nb += b" "
rep = struct.pack("<I", len(nb)) + nb + pad4(len(nb))
assert len(rep) == len(pat), (len(rep), len(pat))
open(path, "wb").write(data.replace(pat, rep))
print("OK in-place:", repr(old), "->", repr(nb.decode()))
