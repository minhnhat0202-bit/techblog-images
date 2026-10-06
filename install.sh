#!/usr/bin/env bash
# Cài skill viettel-techblog-images vào ~/.claude/skills (Claude Code).
# Dùng: curl -fsSL https://raw.githubusercontent.com/minhnhat0202-bit/techblog-images/main/install.sh | bash
set -euo pipefail
REPO="${REPO:-https://github.com/minhnhat0202-bit/techblog-images}"
DEST="${HOME}/.claude/skills"
TMP="$(mktemp -d)"
echo "→ Tải skill từ ${REPO} …"
curl -fsSL "${REPO}/archive/refs/heads/main.zip" -o "${TMP}/repo.zip"
unzip -q "${TMP}/repo.zip" -d "${TMP}"
SRC="$(find "${TMP}" -type d -path '*/skill/viettel-techblog-images' | head -1)"
[ -n "${SRC}" ] || { echo "Không tìm thấy thư mục skill trong gói tải về"; exit 1; }
mkdir -p "${DEST}"
rm -rf "${DEST}/viettel-techblog-images"
cp -R "${SRC}" "${DEST}/viettel-techblog-images"
rm -rf "${TMP}"
echo "✓ Đã cài vào ${DEST}/viettel-techblog-images"
echo "→ Kiểm tra môi trường:"
python3 "${DEST}/viettel-techblog-images/scripts/render.py" --check-env || true
echo "Mở Claude Code trong thư mục dự án và thử: \"Làm thumbnail cho bài về Object Storage trên Tech Blog Viettel Cloud\""
