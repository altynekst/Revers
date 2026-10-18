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
(cd i2d && printf '\n' | dotnet Il2CppDumper.dll "$SOP" "$MD" "$OUT") 2>&1 | tail -25
ls -la dumpout
grep -n -i -E "class [A-Za-z0-9_.]*(Grab|Hand|Hook|Bar|Controller|Climb|Trick|Localiz|Language|Translat)" dumpout/dump.cs | head -200 > dumpout/find.txt
wc -l dumpout/find.txt
