# Viettel Tech Blog Images — skill cho Claude Code

Tạo **thumbnail isometric** và **ảnh minh họa trong bài** cho Tech Blog Viettel Cloud (viettelcloud.vn/tech-blog):
đúng kích thước đo từ trang, đúng 5 màu thương hiệu Viettel, dựng bằng HTML/SVG và render bằng Chrome headless,
có script mô phỏng 7 khung hiển thị của trang và kiểm tra màu/dung lượng trước khi giao.

Trang hướng dẫn đầy đủ (GitHub Pages): `docs/index.html` → bật Pages với source **main / docs**.

![Thumbnail mẫu](docs/assets/thumb-namespace.webp)

## Cài đặt

Yêu cầu: [Claude Code](https://claude.com/claude-code), Google Chrome (hoặc Chromium/Edge, đặt `CHROME_BIN` nếu ở đường dẫn lạ),
Python 3 với Pillow (`pip3 install pillow`). Không cần npm. Font FS PF BeauSans Pro là font nội bộ, không kèm theo; thiếu font ảnh dùng Roboto.

```bash
# Cách A: clone rồi copy — tên thư mục phải giữ nguyên "viettel-techblog-images"
git clone https://github.com/minhnhat0202-bit/techblog-images.git
cp -R techblog-images/skill/viettel-techblog-images ~/.claude/skills/

# Cách B: tải dist/viettel-techblog-images.zip, giải nén vào ~/.claude/skills/

# Cách C: một dòng
curl -fsSL https://raw.githubusercontent.com/minhnhat0202-bit/techblog-images/main/install.sh | bash

# Kiểm tra môi trường
python3 ~/.claude/skills/viettel-techblog-images/scripts/render.py --check-env
```

## Dùng

Mở Claude Code trong thư mục dự án, ra lệnh bằng tiếng Việt hoặc tiếng Anh. Skill tự kích hoạt khi nhắc tới ảnh cho bài Tech Blog:

```
https://viettelcloud.vn/tech-blog/3/140  tạo bộ ảnh minh họa phù hợp cho bài này
Thumbnail cho bài về Load Balancer, kiểu isometric, nền lưới chấm
Kiểm tra xem thumb.png có hợp với khung hiển thị của Tech Blog không
```

Kết quả lưu tại `./techblog-images/<tên-bài>/`: thumbnail `.webp` + `.png`, các `fig0N.png`, file HTML nguồn để sửa và render lại,
ảnh xem trước 7 khung, và `GHI-CHU-CHEN-ANH.md` ghi vị trí chèn từng hình kèm alt text.

## Quy chuẩn

| Loại | Kích thước | Vì sao |
|---|---|---|
| Thumbnail | 1500×1000 (3:2), vùng an toàn 1000×760 giữa | Trang crop `object-fit: cover` trong 7 khung tỷ lệ 1:1 → 1.91:1 |
| Ảnh trong bài | rộng 1688, cao 950/1126/844/1266 | Cột nội dung 844 px, 2× cho Retina; mobile 358 px nên chữ ≥ 36 px |

Màu: chỉ `EE0033`, `000000`, `44494D`, `B5B4B4`, `F2F2F2` và tint/shade; một điểm nhấn đỏ mỗi hình. Không xanh/tím/cam/vàng.

## Cấu trúc repo

```
skill/viettel-techblog-images/   skill (copy nguyên thư mục này vào ~/.claude/skills/)
  SKILL.md                       quy trình cho Claude
  references/                    số đo trang, style guide, phong cách isometric, prompt AI
  assets/templates/              thumbnail.html, inline.html
  assets/icons/                  16 icon line-art SVG
  assets/examples/               ảnh mẫu + scene isometric mẫu
  scripts/                       iso.py, render.py, preview_crops.py, check_image.py, fit_thumb.py
docs/                            landing page (GitHub Pages) + ảnh
dist/                            bản đóng gói .zip và .skill
install.sh                       cài một dòng
```

## Đóng gói lại sau khi sửa skill

```bash
cd skill && zip -qr ../dist/viettel-techblog-images.zip viettel-techblog-images -x '*/__pycache__/*' && cp ../dist/viettel-techblog-images.zip ../dist/viettel-techblog-images.skill
```

Dùng nội bộ Viettel Cloud / VTNet. Bộ quy chuẩn màu thuộc Tập đoàn Viettel; font thương hiệu không phân phối kèm.
