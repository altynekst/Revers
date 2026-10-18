import sys, UnityPy
data_dir = sys.argv[1]
level = sys.argv[2] if len(sys.argv) > 2 else "level1"
env = UnityPy.load(f"{data_dir}/{level}")
objs = list(env.objects)
names, tr_of_go, meshes = {}, {}, []
for o in objs:
    if o.type.name == "GameObject":
        names[o.path_id] = o.read_typetree().get("m_Name", "")
for o in objs:
    t = o.type.name
    try: tree = o.read_typetree()
    except Exception: continue
    go = tree.get("m_GameObject", {}).get("m_PathID")
    if t == "Transform":
        tr_of_go[go] = (o.path_id, tree["m_LocalPosition"], tree["m_LocalScale"])
    elif t == "MeshFilter":
        m = tree["m_Mesh"]
        meshes.append((go, m["m_FileID"], m["m_PathID"]))
    elif t in ("TextMesh", "TextMeshPro"):
        print(f"[TEXT] go={go} '{names.get(go)}' -> {tree.get('m_Text') or tree.get('m_text')!r}")
print("GO_id | имя | mesh(file,id) | transform_id | pos | scale")
for go, fid, pid in meshes:
    tid, pos, sc = tr_of_go.get(go, (None, {}, {}))
    p = tuple(round(pos.get(k, 0), 2) for k in "xyz"); s = tuple(round(sc.get(k, 0), 2) for k in "xyz")
    print(go, "|", names.get(go, "?"), "|", (fid, pid), "|", tid, "|", p, "|", s)
print("Меши в файле:")
for o in objs:
    if o.type.name == "Mesh":
        tr = o.read_typetree()
        print(" id=%s name=%r вершин=%s" % (o.path_id, tr.get("m_Name"), tr.get("m_VertexData", {}).get("m_VertexCount")))
