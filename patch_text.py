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
cands = [new, "crack tuman", "by tuman"]
txt = next((c for c in cands if len(c.encode()) <= len(ob)), None)
if txt is None:
    sys.exit("надпись слишком короткая для замены")
nb = txt.encode().ljust(len(ob), b" ")
rep = struct.pack("<I", len(ob)) + nb + pad4(len(ob))
assert len(rep) == len(pat)
open(path, "wb").write(data.replace(pat, rep))
print("OK in-place:", repr(old), "->", repr(nb.decode()))
