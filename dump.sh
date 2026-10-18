#!/usr/bin/env bash
set +e
APK="$1"
rm -rf d dumpout tools; mkdir -p d dumpout tools
unzip -q "$APK" 'lib/*' 'assets/bin/Data/*' -d d
SO=$(ls "$PWD"/d/lib/arm64-v8a/libil2cpp.so 2>/dev/null || ls "$PWD"/d/lib/armeabi-v7a/libil2cpp.so)
MD="$PWD/d/assets/bin/Data/Managed/Metadata/global-metadata.dat"
UV=$(strings -n 6 d/assets/bin/Data/globalgamemanagers | grep -oE '[0-9]{4}\.[0-9]+\.[0-9]+[fpab][0-9]+' | head -1)
echo "SO=$SO"; echo "Unity=$UV"
RX='Grab|Hand|Hook|Bar|Controller|Climb|Trick|Localiz|Language|Translat|Release|Noomi|Telegram'
strings -n 4 "$MD" | grep -E "$RX" | sort -u | head -600 > dumpout/names.txt
echo "имён из метаданных: $(wc -l < dumpout/names.txt)"
URL=$(curl -sL https://api.github.com/repos/SamboyCoding/Cpp2IL/releases/latest | jq -r '.assets[].browser_download_url' | grep -iE 'linux' | head -1)
echo "Cpp2IL: $URL"
cd tools && curl -sL -o c2i.bin "$URL"
case "$URL" in *.zip) unzip -q -o c2i.bin -d c2i ;; *) mkdir c2i; cp c2i.bin c2i/Cpp2IL ;; esac
BIN=$(find c2i -type f -iname 'Cpp2IL*' ! -name '*.dll' ! -name '*.pdb' ! -name '*.json' | head -1)
chmod +x "$BIN"; echo "BIN=$BIN"; cd ..
export DOTNET_ROLL_FORWARD=Major DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
timeout 900 "tools/$(realpath --relative-to=tools "$BIN")" --game-path "$APK" --output-as diffable-cs --output-root dumpout/c2i > dumpout/c2i.log 2>&1
echo "--- попытка 1 (APK): код $?"; tail -15 dumpout/c2i.log
if [ -z "$(find dumpout/c2i -name '*.cs' 2>/dev/null | head -1)" ]; then
  timeout 900 "tools/$(realpath --relative-to=tools "$BIN")" --game-path "$PWD/d" --force-binary-path "$SO" --force-metadata-path "$MD" --force-unity-version "$UV" --output-as diffable-cs --output-root dumpout/c2i > dumpout/c2i2.log 2>&1
  echo "--- попытка 2 (файлы): код $?"; tail -15 dumpout/c2i2.log
fi
N=$(find dumpout/c2i -name '*.cs' 2>/dev/null | wc -l); echo "файлов .cs: $N"
{
  echo "=== ФАЙЛЫ КЛАССОВ ==="; find dumpout/c2i -name '*.cs' 2>/dev/null | grep -iE "$RX" | head -150
  echo "=== МЕТОДЫ ==="; grep -rhn -iE "(Grab|Release|Hook|Trick|Climb|SetLanguage|GetLocalized)[A-Za-z]*\(" dumpout/c2i 2>/dev/null | head -150
  echo "=== ИМЕНА ИЗ МЕТАДАННЫХ ==="; head -250 dumpout/names.txt
} > dumpout/find.txt
(cd dumpout && zip -qr all.zip c2i names.txt find.txt *.log 2>/dev/null)
ls -la dumpout | head -20
