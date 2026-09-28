#!/usr/bin/env bash
# Install the toolchain that rebuilds the chapter PDFs identically to the released ones.
# Tested 28 Sep 2026 on Ubuntu 24.04 (Claude Code cloud container). See source/BUILD.md.
# Run as root (or with sudo) from anywhere:  bash source/setup-toolchain.sh
set -euo pipefail

apt-get update -qq || true                      # a failing third-party PPA is harmless here
apt-get install -y -qq pandoc poppler-utils fonts-dejavu-core fonts-dejavu-extra

# pypdf needs a working `cryptography`; the distro copy is broken on this image, so pip's wins.
pip install -q --ignore-installed cryptography
pip install -q pypdf pillow

# Playwright must match the Chromium on disk. The cloud container ships chromium-1194 in
# /opt/pw-browsers, which is Playwright 1.56.0. Elsewhere, install any version and then run
# `playwright install chromium`.
if [ -d /opt/pw-browsers/chromium-1194 ]; then
  pip install -q playwright==1.56.0
else
  pip install -q playwright && playwright install chromium
fi

# Fonts: exactly the faces the released PDFs embed. Poppins SemiBold/Medium/Italic are left out on
# purpose: the original machine did not have them, so weight 600 fell back to Bold. Installing them
# changes heading line breaks and moves page numbers away from the ones the visual review cites.
F=/usr/share/fonts/truetype/google; mkdir -p "$F"
G=https://raw.githubusercontent.com/google/fonts/main/ofl
for f in poppins/Poppins-Regular.ttf poppins/Poppins-Bold.ttf poppins/Poppins-BoldItalic.ttf \
         "lora/Lora%5Bwght%5D.ttf" "lora/Lora-Italic%5Bwght%5D.ttf"; do
  curl -sSfL -o "$F/$(basename "$f")" "$G/$f"
done
rm -f "$F"/Poppins-SemiBold.ttf "$F"/Poppins-Medium.ttf "$F"/Poppins-Italic.ttf
fc-cache -f >/dev/null
echo "toolchain ready: $(pandoc --version | head -1); playwright $(pip show playwright | sed -n 's/^Version: //p')"
