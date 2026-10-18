import sys, os, re, UnityPy
d = sys.argv[1]
pats = [b"unlock", b"noomi", b"crack", b"tuman"]
pats16 = [p.decode().encode("utf-16le") for p in pats]
files = sorted(f for f in os.listdir(d) if re.fullmatch(r"(level\d+|sharedassets\d+\.assets)", f))
for f in files:
    try: env = UnityPy.load(f"{d}/{f}")
    except Exception as e:
        print(f, "ERR", e); continue
    names = {}
    for o in env.objects:
        if o.type.name == "GameObject":
            try: names[o.path_id] = o.read_typetree().get("m_Name", "")
            except Exception: pass
    print(f"=== {f}: объектов {len(list(env.objects))}")
    for o in env.objects:
        t = o.type.name
        try: raw = bytes(o.get_raw_data())
        except Exception: continue
        low = raw.lower()
        hit = [p.decode() for p in pats if p in low] + [p.decode("utf-16le")+"(u16)" for p in pats16 if p in low]
        if t in ("TextMesh",):
            try:
                tr = o.read_typetree(); print(f"  [TextMesh] id={o.path_id} text={tr.get('m_Text')!r}")
            except Exception: pass
        if hit and t != "GameObject":
            go = None
            try: go = o.read_typetree().get("m_GameObject", {}).get("m_PathID")
            except Exception: pass
            ctx = ""
            for p in pats + pats16:
                i = low.find(p)
                if i >= 0:
                    ctx = raw[max(0, i-20): i+60]; break
            print(f"  {t} id={o.path_id} go={go} '{names.get(go,'')}' hit={hit} ctx={ctx!r}")
        elif hit and t == "GameObject":
            print(f"  GameObject id={o.path_id} name={names.get(o.path_id)!r} hit={hit}")
