import sys, zipfile, struct
z = zipfile.ZipFile(sys.argv[1])
b = z.read("assets/bin/Data/Managed/Metadata/global-metadata.dat")
san, ver = struct.unpack("<Ii", b[:8])
slo, sls, sdo, sds = struct.unpack("<4i", b[8:24])
print("sanity", hex(san), "version", ver, "entries", sls // 8, "data", sdo, sds, "size", len(b))
n = sls // 8
with open("lits.tsv", "w", encoding="utf-8") as f:
    for i in range(n):
        l, o = struct.unpack("<II", b[slo + 8 * i: slo + 8 * i + 8])
        t = b[sdo + o: sdo + o + l].decode("utf-8", "replace")
        f.write("%d\t%s\n" % (i, t.replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")))
print("written", n)
