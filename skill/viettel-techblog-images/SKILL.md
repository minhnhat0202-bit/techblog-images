---
name: viettel-techblog-images
description: >
  Tạo ảnh thumbnail và ảnh minh họa trong bài cho Tech Blog Viettel Cloud (viettelcloud.vn/tech-blog) theo phong cách
  MINIMALISM và đúng 5 màu chuẩn Viettel (EE0033, 000000, 44494D, B5B4B4, F2F2F2). Kích thước đã đo trực tiếp từ trang:
  thumbnail 1500×1000 (3:2, vùng an toàn giữa vì trang crop object-fit cover từ 1:1 đến 1.91:1), ảnh trong bài rộng 1688
  (2× cột nội dung 844px). Dựng ảnh bằng HTML/SVG rồi render qua Chrome headless (không cần npm), có script xem trước
  thumbnail ở đúng 7 khung hiển thị của trang và script kiểm tra kích thước/dung lượng/màu. Dùng BẤT CỨ KHI NÀO người dùng
  cần ảnh cho bài Tech Blog / blog kỹ thuật Viettel Cloud: "ảnh thumbnail cho bài", "ảnh bìa bài viết", "ảnh minh họa
  Kubernetes/LLM/Storage…", "ảnh đại diện bài tech blog", "sơ đồ kiến trúc cho bài viết", "banner bài blog", "vẽ hình cho
  bài", kể cả khi chỉ đưa tiêu đề/dàn ý bài và nói "làm ảnh cho đẹp", "theo chuẩn Viettel", "tối giản". Cũng dùng để
  kiểm tra/sửa ảnh thumbnail có sẵn bị crop mất chủ thể, sai tỷ lệ, sai màu, hoặc để viết prompt cho công cụ AI tạo ảnh
  (Figma generate_image, Gemini, Midjourney) theo đúng brand.
---

# Viettel Cloud Tech Blog · Ảnh thumbnail & ảnh minh họa (minimalism, màu Viettel)

Skill biến một chủ đề bài viết thành ảnh dùng ngay trên viettelcloud.vn/tech-blog: **thumbnail** (ảnh đại diện trong
danh sách bài) và **ảnh minh họa trong bài** (sơ đồ, hình khái niệm, so sánh). Ảnh được dựng bằng HTML + SVG trên
template có sẵn, render ra PNG/WebP bằng Google Chrome headless (`scripts/render.py`), rồi xem trước đúng cách trang
crop (`scripts/preview_crops.py`) và kiểm tra (`scripts/check_image.py`). Không cần cài npm; chỉ cần Chrome và Python 3
với Pillow (`scripts/render.py --check-env` báo thiếu gì).

## 1. Hai loại ảnh và kích thước (đo từ trang ngày 06/10/2026 — chi tiết ở `references/site-specs.md`)

| Loại | Kích thước xuất | Vì sao | Định dạng |
|---|---|---|---|
| **Thumbnail** | **1500 × 1000 px** (3:2) | Trang hiển thị thumbnail qua `object-fit: cover` trong 7 khung có tỷ lệ 1:1 → 1.91:1 (386×290, 287×210, 253×188, 414×290, 398×208, 86×86, mobile 358×210). 3:2 là tâm của dải tỷ lệ đó; khung lớn nhất là 414×290 nên 1500 px đủ cho màn 2× | WebP chất lượng 85 (ưu tiên, <250 KB) + PNG gốc |
| **Ảnh trong bài** | **rộng 1688 px**, cao tùy nội dung: 16:9 → 1688×950, 3:2 → 1688×1126, 2:1 → 1688×844, 4:3 → 1688×1266 | Cột nội dung bài rộng 844 px desktop; ảnh hiển thị full chiều rộng cột; 1688 = 2× cho màn Retina. Mobile co còn 358 px nên chữ trong ảnh phải lớn | PNG (sơ đồ, nét) hoặc WebP (có mảng ảnh), <500 KB |
| Ảnh chia sẻ mạng xã hội (khi được hỏi) | 1200 × 630 | Chuẩn Open Graph | PNG/JPG |

**Vùng an toàn của thumbnail**: mọi chủ thể, chữ, chi tiết quan trọng nằm trong **khung giữa 1000 × 760 px**
(x 250→1250, y 120→880). Phần ngoài khung chỉ dành cho nền, họa tiết tràn, mảng màu — vì khung 86×86 (sidebar "Xem nhiều
nhất") cắt còn hình vuông giữa, còn khung 398×208 cắt mất ~22% chiều cao trên/dưới. Thumbnail **không hiển thị trên trang
chi tiết bài** (chỉ trong danh sách/sidebar/bài liên quan), nên nó cần "nhận ra trong 1 giây ở cỡ nhỏ" hơn là kể chuyện.

## 2. Phong cách: thumbnail ISOMETRIC GRADIENT (mặc định) · ảnh trong bài minimalism phẳng

Người dùng đã chọn (06/10/2026): **thumbnail** dựng theo phong cách Isometric Gradient — khối 3D đẳng cự, mặt khối gradient
trong tint đỏ/xám Viettel, bóng mềm, nền công nghệ mờ (`references/iso-style.md`, thư viện `scripts/iso.py`). **Ảnh
trong bài** giữ bố cục sơ đồ phẳng để nhãn đọc được, nhưng node dùng biến thể `raised` (khối nổi nhẹ: gradient, cạnh dày
dưới, bóng mềm — mặc định trong `inline.html`) cho cùng tông với thumbnail. Line-art phẳng cho thumbnail vẫn có (template mặc định) khi
người dùng yêu cầu "tối giản tuyệt đối". Các quy tắc màu dưới đây áp dụng cho cả hai.

Đọc `references/style-guide.md` trước khi dựng (ngắn, ~150 dòng) — nó chứa bảng màu, nét vẽ, bố cục, bảng ẩn dụ chủ đề →
hình, và danh sách "không làm". Tóm tắt để không quên:

- **Màu**: chỉ 5 màu Viettel + trắng và tint của chúng. Nền trắng `#FFFFFF` (hoặc xám `#F2F2F2` khi cần tách khối).
  Nét chính xám than `#44494D`, nét phụ/hairline `#B5B4B4` hoặc `#DADBDD`, **đỏ `#EE0033` cho đúng một điểm nhấn**
  (một bộ phận của icon, một node trong sơ đồ, một vạch). Không xanh dương, tím, cam, vàng — kể cả logo công nghệ bên
  thứ ba: vẽ lại dạng đơn sắc hoặc thay bằng hình khối/chữ (ví dụ "K8s" thay logo Kubernetes màu xanh).
- **Nét**: line-art stroke đều, bo tròn đầu nét, độ dày ≈ 1% chiều rộng canvas (thumbnail 14–16 px, ảnh trong bài 10–12 px).
  Không gradient, không bóng đổ, không 3D, không ảnh chụp, không họa tiết nền lặp.
- **Bố cục thumbnail**: một ẩn dụ duy nhất, đặt giữa, chiếm 45–60% chiều cao; nhiều khoảng trống. Tối đa một chữ/ký
  hiệu ngắn (≤ 4 ký tự như "GPU", "K8s", "S3") đặt trong icon; không đặt tiêu đề bài vào thumbnail (tiêu đề đã hiện bên cạnh).
- **Bố cục ảnh trong bài**: kicker nhỏ góc trên trái (tùy chọn), vùng hình ở giữa, chữ ≥ 36 px tại 1688 (đọc được ở 844),
  nhãn ≤ 3 từ; luồng trái → phải hoặc trên → dưới; node được bàn tới trong đoạn văn là node đỏ duy nhất.
- **Font**: `FS PF BeauSans Pro` (font nội bộ Viettel, đã cài trên máy tác giả) → fallback `Roboto` (font của website) →
  Arial. Chữ in hoa giãn 0.08em cho nhãn, chữ thường cho mọi thứ khác.

## 3. Quy trình

### Bước 1 · Hiểu bài và chọn ẩn dụ
Hỏi (hoặc suy ra từ tiêu đề/dàn ý) ba điều: chủ đề kỹ thuật chính, "điểm mới" của bài (cái gì đáng tô đỏ), cần
thumbnail hay ảnh trong bài hay cả hai (và bao nhiêu hình, mỗi hình minh họa đoạn nào). Chọn ẩn dụ từ bảng trong
`style-guide.md §4` (Kubernetes → cụm lục giác, Load balancer → một node tỏa ba nhánh, LLM/GPU → chip, Storage → đĩa
xếp chồng, Security → khiên + tick…). Nếu bài có nhiều hình, giữ cùng độ dày nét, cùng cỡ chữ, cùng vị trí kicker để
cả bài "cùng một tay vẽ". Với 1–2 ảnh, không cần hỏi lại — làm luôn rồi đưa người dùng xem.

### Bước 2 · Dựng HTML từ template
Thumbnail isometric: viết một `scene.py` nhỏ (xem `iso-style.md §2–3`, mẫu ở `assets/examples/scene-namespace.py`) sinh
SVG bằng `scripts/iso.py`, rồi dán vào `<div class="art">` của `thumbnail.html` với `--art-size` 740–800 px. Thumbnail
line-art và ảnh trong bài: dùng template trực tiếp như dưới.
**Nơi lưu:** mọi file (HTML nguồn, PNG, WebP, preview) lưu trong **thư mục đang làm việc của dự án**, tại
`./techblog-images/<slug>/` — không lưu vào scratchpad, `/tmp`, hay `~/.claude/...` để người dùng tìm thấy ngay trong Finder. Nếu người dùng chỉ đường dẫn khác thì theo đó. Khi giao, nêu đường dẫn đầy đủ và `open` thư mục đó.
Copy template vào thư mục này và sửa phần được đánh dấu `<!-- EDIT -->`:
- `assets/templates/thumbnail.html` — canvas 1500×1000, có sẵn vùng an toàn, biến CSS màu/nét, 3 biến thể bố cục
  (`icon-center` mặc định · `icon-keyword` icon + chữ ngắn · `icon-arc` icon trong cung tròn mảnh như thumbnail GPU hiện
  có trên trang) và 5 lớp nền công nghệ mờ (`bg-circuit` mặc định · `bg-dots` · `bg-grid` · `bg-hex` · `bg-none`, xem
  `style-guide.md §2b`; nền có gradient nên luôn giao WebP). Dán SVG icon vào `<div class="art">`.
- `assets/templates/inline.html` — canvas rộng 1688, cao đặt bằng class `h-16x9 | h-3x2 | h-2x1 | h-4x3`; có sẵn CSS
  cho sơ đồ: `.node`, `.node.hl` (đỏ), `.node.soft` (xám nhạt), `.row/.col`, `.arrow` (SVG mũi tên), `.kicker`, `.caption`,
  `.group` (khung hairline gom nhóm), `.step` (số thứ tự đỏ chữ trần).
- Icon có sẵn: `assets/icons/*.svg` (viewBox 0 0 200 200, stroke `currentColor`, phần nhấn mang class `acc` → đỏ).
  Danh sách và cách ghép ở `style-guide.md §5`. Thiếu icon thì **tự vẽ SVG cùng ngôn ngữ**: hình học cơ bản, stroke 7
  trong viewBox 200, `stroke-linecap="round" stroke-linejoin="round" fill="none"`. Thư viện 188 icon Tập đoàn (PNG, 1 màu)
  nằm ở `~/.claude/skills/viettel-slides/assets/icons/png/` nếu cần icon nghiệp vụ; tra `references/icons.md` của skill đó.

### Bước 3 · Render
```bash
python3 ~/.claude/skills/viettel-techblog-images/scripts/render.py thumb.html --preset thumb --out techblog-<slug>-thumb.png --webp
python3 ~/.claude/skills/viettel-techblog-images/scripts/render.py fig01.html --preset inline-16x9 --out techblog-<slug>-fig01.png
# preset khác: inline-3x2 | inline-2x1 | inline-4x3 | og | custom WxH (--size 1688x1400)
# --safe : vẽ đè khung vùng an toàn (chỉ để kiểm tra, không giao file này)
```
Script tìm Chrome ở `/Applications/Google Chrome.app` (hoặc `$CHROME_BIN`), chờ font tải xong, xuất PNG đúng pixel; `--webp`
xuất thêm WebP q85 và báo dung lượng.

### Bước 4 · Kiểm tra bằng mắt và bằng script (bắt buộc trước khi giao)
```bash
python3 .../scripts/preview_crops.py techblog-<slug>-thumb.png --out preview.png   # thumbnail trong 7 khung thật của trang
python3 .../scripts/check_image.py techblog-<slug>-thumb.png --kind thumb          # kích thước, dung lượng, màu lạ, % đỏ, vùng an toàn
python3 .../scripts/check_image.py techblog-<slug>-fig01.png --kind inline
```
Mở PNG và `preview.png` bằng tool Read để nhìn. Những lỗi hay gặp và cách sửa:
- Chủ thể bị cắt ở khung 86×86 hoặc 398×208 → giảm `--art-size` hoặc dời vào vùng an toàn; chủ thể quá nhỏ (< 35% chiều cao) → tăng `--art-size` (mặc định 600px).
- `check_image` báo "màu ngoài bảng" > 0.5% → có hue lạ (thường do logo hoặc anti-alias của màu không chuẩn); đổi về
  `#44494D`/`#EE0033`.
- Đỏ > 12% diện tích thumbnail → không còn là "điểm nhấn"; line-art thường chỉ 0.3–2%. Đỏ = 0% → thiếu nhận diện, thêm một chi tiết đỏ.
- Chữ trong ảnh trong bài < 36 px → phóng to hoặc bỏ chữ, chuyển sang caption dưới ảnh trong CMS.
- Ảnh > 250 KB (thumb) / 500 KB (inline) → dùng WebP, bỏ texture, giảm chi tiết.

### Bước 5 · Giao
Trả về đường dẫn đầy đủ (trong thư mục dự án) + kích thước + dung lượng, chạy `open <thư mục>` để Finder hiện ngay, và
một dòng mô tả alt text gợi ý cho CMS. Đặt tên
`techblog-<slug>-thumb.webp` (và `.png`), `techblog-<slug>-fig01.png`, `fig02`… Nếu người dùng muốn chỉnh, sửa HTML và render
lại — không chỉnh tay trên PNG.

## 4. Khi người dùng muốn ảnh "vẽ bằng AI" (tranh minh họa, không phải sơ đồ)
Đọc `references/ai-prompts.md`: prompt mẫu cho Figma `generate_image` (MCP có sẵn trong môi trường này), Gemini/Imagen,
Midjourney, kèm hậu kỳ bắt buộc (resize/crop về 1500×1000, kiểm tra màu bằng `check_image.py`, vì model hay thêm hue
xanh/tím). Ưu tiên vẫn là HTML/SVG — nó đúng màu tuyệt đối, sửa được từng chi tiết và nhất quán giữa các bài.

## 5. Khi được yêu cầu kiểm tra/sửa ảnh có sẵn
Chạy `preview_crops.py` + `check_image.py` lên ảnh gốc, chỉ ra khung nào mất chủ thể, màu nào ngoài bảng, rồi đề xuất:
(a) crop/pad về 3:2 với `scripts/fit_thumb.py` (giữ chủ thể giữa, pad bằng trắng/F2F2F2), hoặc (b) vẽ lại theo template nếu
ảnh gốc là ảnh stock nhiều màu. Nêu rõ với người dùng ảnh stock nhiều màu không đạt chuẩn tối giản dù có crop đúng.

## 6. Tệp trong skill
- `references/site-specs.md` — số đo đầy đủ: API, 61 thumbnail hiện có (phân bố tỷ lệ/định dạng), 7 khung hiển thị, cột
  nội dung, font/màu của trang, cách CMS nhúng ảnh (Quill, nhiều ảnh base64).
- `references/style-guide.md` — bảng màu, nét, bố cục, ẩn dụ theo chủ đề, icon có sẵn, danh sách không làm.
- `references/iso-style.md` — phong cách Isometric Gradient: bảng mặt khối, primitives, ẩn dụ theo chủ đề.
- `references/ai-prompts.md` — prompt cho công cụ sinh ảnh + hậu kỳ.
- `assets/templates/thumbnail.html`, `assets/templates/inline.html` — template HTML.
- `assets/examples/` — ảnh mẫu đã render: thumbnail isometric (namespace, GPU), ảnh trong bài `raised`, 3 biến thể line-art, preview crop, bảng icon; `scene-namespace.py` mẫu cảnh iso.
- `assets/icons/*.svg` — icon line-art (cloud, server, chip, database, storage, container, k8s, lb, shield, network, lock, monitor, backup, api, serverless, pipeline).
- `scripts/iso.py` (primitives isometric → SVG), `scripts/render.py` (HTML → PNG/WebP), `scripts/preview_crops.py` (mô phỏng 7 khung), `scripts/check_image.py` (kiểm tra),
  `scripts/fit_thumb.py` (đưa ảnh có sẵn về 3:2).
