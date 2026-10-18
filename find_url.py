import os, re, sys, UnityPy
root = sys.argv[1]
P = [b'noomimoded', 'noomimoded'.encode('utf-16le'), b't.me/', 't.me/'.encode('utf-16le'), b'telegram.me']
skip = ('.so', '.dex', '.png', '.jpg', '.ogg', '.wav', '.mp3', '.ttf', '.otf', '.arsc')
def ctx(b, m): return b[max(0, m.start()-30): m.end()+50]
def raw_hits(tag, b):
    for pt in P:
        for m in list(re.finditer(re.escape(pt), b, re.I))[:2]:
            print("RAW", tag, m.start(), ctx(b, m))
for dp, _, fs in os.walk(root):
    for n in fs:
        p = os.path.join(dp, n); rel = os.path.relpath(p, root)
        if n.lower().endswith(skip): continue
        try: b = open(p, 'rb').read()
        except Exception: continue
        raw_hits(rel, b)
        if not (rel.startswith('assets/bin/Data') or rel.startswith('assets/aa') or n.endswith(('.bundle', '.assets', '.unity3d'))):
            continue
        try: env = UnityPy.load(p)
        except Exception: continue
        for o in env.objects:
            try: rb = bytes(o.get_raw_data())
            except Exception: continue
            if any(re.search(re.escape(pt), rb, re.I) for pt in P):
                try: nm = o.read_typetree().get('m_Name', '')
                except Exception: nm = ''
                print("OBJ", rel, o.type.name, o.path_id, repr(nm))
                raw_hits(f"{rel}#{o.path_id}", rb)
print("СКАН ЗАВЕРШЁН")
