import sys, UnityPy
d, level, tid = sys.argv[1], sys.argv[2], int(sys.argv[3])
sc = [float(x) for x in sys.argv[4:7]] or [0.0, 0.0, 0.0]
path = f"{d}/{level}"
env = UnityPy.load(path)
done = False
for o in env.objects:
    if o.type.name == "Transform" and o.path_id == tid:
        t = o.read_typetree()
        t["m_LocalScale"] = {"x": sc[0], "y": sc[1], "z": sc[2]}
        o.save_typetree(t); done = True
if not done: sys.exit(f"Transform {tid} не найден")
open(path, "wb").write(env.file.save())
print("OK", path)
