#!/usr/bin/env bash
set -euo pipefail
IN=$1; LEVEL=$2; TID=$3
rm -rf work out; mkdir -p work out
unzip -q "$IN" "assets/bin/Data/$LEVEL" -d work
python3 patch_level.py work/assets/bin/Data "$LEVEL" "$TID"
cp "$IN" out/tmp.apk
(cd work && zip -q -0 ../out/tmp.apk "assets/bin/Data/$LEVEL")
zip -q -d out/tmp.apk 'META-INF/*.SF' 'META-INF/*.RSA' 'META-INF/*.DSA' 'META-INF/MANIFEST.MF' || true
BT=$(ls -d "$ANDROID_HOME"/build-tools/* | sort -V | tail -1)
"$BT/zipalign" -p -f 4 out/tmp.apk out/aligned.apk
[ -f debug.keystore ] || keytool -genkeypair -keystore debug.keystore -storepass android -keypass android -alias k -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=dev"
"$BT/apksigner" sign --ks debug.keystore --ks-pass pass:android --key-pass pass:android --out out/patched.apk out/aligned.apk
"$BT/apksigner" verify out/patched.apk && echo BUILD_OK
