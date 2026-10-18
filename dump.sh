#!/usr/bin/env bash
set -e
rm -rf d dumpout i2d; mkdir -p d dumpout
unzip -q "$1" 'lib/*' 'assets/bin/Data/Managed/Metadata/global-metadata.dat' -d d
SO=$(ls d/lib/arm64-v8a/libil2cpp.so 2>/dev/null || ls d/lib/armeabi-v7a/libil2cpp.so)
echo "SO=$SO"
V=https://github.com/Perfare/Il2CppDumper/releases/download/v6.7.46
curl -sL -o i2d.zip "$V/Il2CppDumper-net6-v6.7.46.zip"
unzip -q -o i2d.zip -d i2d
export DOTNET_ROLL_FORWARD=Major
MD="$PWD/d/assets/bin/Data/Managed/Metadata/global-metadata.dat"
OUT="$PWD/dumpout"; SOP="$PWD/$SO"
python3 -c "import struct;b=open('$MD','rb').read(8);print('metadata:',b[:4].hex(),'version',struct.unpack('<i',b[4:8])[0])"
file "$SOP" 2>/dev/null || true
(cd i2d && printf '\n' | dotnet Il2CppDumper.dll "$SOP" "$MD" "$OUT") > dumpout/dumper.log 2>&1 || true
grep -v "^   at " dumpout/dumper.log | head -40
ls -la dumpout
grep -n -i -E "class [A-Za-z0-9_.]*(Grab|Hand|Hook|Bar|Controller|Climb|Trick|Localiz|Language|Translat)" dumpout/dump.cs | head -200 > dumpout/find.txt
wc -l dumpout/find.txt
