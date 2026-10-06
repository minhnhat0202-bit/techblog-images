# Số đo trang Tech Blog Viettel Cloud (quét ngày 06/10/2026)

Nguồn: tải 56 bài qua API công khai, đo 61 thumbnail + 67 ảnh trong bài, render trang bằng Chrome headless ở viewport
1440 px và 390 px để đo khung hiển thị thật. Số liệu có thể thay đổi khi website đổi giao diện — nếu nghi ngờ, chạy lại
phần "Cách đo lại" cuối file.

## 1. Kiến trúc trang (để biết ảnh đi đâu)

- Nuxt 2 SPA; dữ liệu bài từ `GET https://viettelcloud.vn/api/landingpage/tech-blog?language=1|2&limit=20&page=N`
  (1 = tiếng Việt, 2 = tiếng Anh); chi tiết `GET /api/landingpage/tech-blog/{id}?language=1`.
- Mỗi bài có `translations[].image_url` (thumbnail, một ảnh cho mỗi ngôn ngữ) và `translations[].content` (HTML từ
  trình soạn thảo Quill — class `ql-align-center`). Ảnh thumbnail lưu tại `https://os.viettelcloud.vn/cmp-cms/<hash>.<ext>`.
- Ảnh trong bài: 38/67 là **data URI base64** dán thẳng vào HTML (nặng, không cache); số còn lại hotlink từ nguồn ngoài
  (googleusercontent, solutions.viettel.vn, cdn.tgdd.vn…). ⇒ Khi giao ảnh trong bài, giao **file** để biên tập viên tải lên
  qua `/api/upload` của CMS, không khuyến khích dán base64.
- Route bài: `/tech-blog/{category_id}/{id}`; danh mục: Dành cho Người mới, Nhà quản lý, Nhà phát triển, Case Study.

## 2. Khung hiển thị thumbnail (desktop 1440 px, trừ khi ghi khác)

Tất cả dùng `object-fit: cover; object-position: center`, không bo góc, hover `scale(1.1)`, cùng một file ảnh cho mọi khung.

| Khung | Ở đâu | Kích thước hiển thị | Tỷ lệ | Pixel cần (2×) |
|---|---|---|---|---|
| Bài nổi bật ("Được đề xuất") | đầu trang /tech-blog | 386 × 290 | 1.33 | 772 × 580 |
| Lưới bài 3 cột | /tech-blog | 287 × 210 | 1.37 | 574 × 420 |
| Danh sách bài (ảnh trái, chữ phải) | /tech-blog phần dưới | 253 × 188 | 1.35 | 506 × 376 |
| "Nội dung liên quan" | cuối trang chi tiết | 414 × 290 | 1.43 | 828 × 580 |
| "Xem nhiều nhất" / "Tin mới nhất" bài đầu | sidebar trang chi tiết | 398 × 208 | 1.91 | 796 × 416 |
| "Xem nhiều nhất" các bài sau | sidebar | 86 × 86 | 1.00 | 172 × 172 |
| Mobile 390 px, mọi danh sách | /tech-blog | 358 × 210 (và 324×208, 356×290) | 1.70 | 716 × 420 |
| Trang chủ, khối tin (`h-[260px]`) | / | rộng cột × 260 | ~1.4–1.6 | — |

Suy ra:
- Dải tỷ lệ 1.00 → 1.91. Ảnh 3:2 (1.5) bị cắt tối đa 33% chiều rộng (khung 1:1) hoặc 22% chiều cao (khung 1.91).
- **Vùng an toàn trên canvas 1500×1000**: giao của khung 1:1 (1000×1000 giữa) và khung 1.91 (1500×785 giữa) = 1000×785
  giữa; làm tròn **1000 × 760** (x 250–1250, y 120–880) để có lề.
- Khung lớn nhất 414×290 ⇒ 1500 px thừa cho 2× (828 px). Không cần quá 1500; ảnh 2000+ chỉ tốn dung lượng.
- Khung 86×86: chủ thể phải nhận ra được khi co xuống ~60 px ⇒ ẩn dụ đơn, nét dày, tương phản cao.

## 3. Thumbnail hiện có trên trang (61 ảnh của 56 bài)

| Chỉ số | Kết quả |
|---|---|
| Kích thước | từ 48×48 (SVG) đến 2186×1437; trung vị ~800×450 |
| Tỷ lệ | ~16:9 (1.75–1.95): 23 ảnh · 3:2 (1.45–1.6): 14 · 1:1: 8 · 4:3–5:4: 4 · dọc (<1): 2 · còn lại rải rác |
| Định dạng | PNG ~24 · JPG/JPEG ~22 · WebP ~12 · SVG 1 |
| Dung lượng | 2 KB → 6.4 MB (một JPG 611×408 nặng 6.4 MB); đa số 20–300 KB |
| Phong cách | Hỗn hợp: ảnh stock nhiều màu (tím, xanh), logo công nghệ (MySQL, Kubernetes), ảnh chụp, vài sơ đồ. Bài mới
nhất (10/2026, "GPU-hours into tokens") dùng SVG line-art xám than + đỏ Viettel trên nền trắng, có cung tròn xám mảnh —
đây là tiền lệ gần nhất với chuẩn tối giản của skill này. |

Kết luận: không có chuẩn kích thước thống nhất trên trang; skill chọn 1500×1000 (3:2) vì nằm giữa dải tỷ lệ khung hiển
thị, và chuẩn hóa phong cách theo tiền lệ line-art mới nhất.

## 4. Ảnh trong bài

| Chỉ số | Kết quả |
|---|---|
| Cột nội dung | **844 px** desktop (1440), **358 px** mobile (390). Ảnh hiển thị ở chiều rộng tự nhiên nếu ≤ 844, lớn hơn thì co về 844; `object-fit: fill` (không crop) |
| Ảnh hiện có | 67 ảnh; rộng 183 → 2362 px; sơ đồ ngang (2048×930, 1902×725), ảnh chụp 1928×1283, ảnh màn hình dọc 497×741, băng ngang mảnh (1390×208 — bảng/biểu đồ chụp màn hình) |
| Chữ thân bài | Roboto 16 px / line-height 24 px; h1 30 px; nền trắng |
| Căn | Đa số `ql-align-center`; có caption in nghiêng dưới ảnh ("Hình 1. …") |

Suy ra: xuất **1688 px rộng** (2× 844). Chữ trong ảnh ≥ 36 px tại 1688 ⇒ 18 px hiển thị desktop, ~7.6 px mobile — vẫn
nhỏ trên mobile, nên nhãn phải ngắn và nội dung quan trọng nói trong caption. Sơ đồ ngang (2:1, 16:9) đọc tốt hơn sơ đồ
dọc trên mobile vì không chiếm cả màn.

## 5. Màu/font của giao diện (để ảnh "cùng tông" với trang)

- Đỏ nav/CTA `#EE0033`; icon SVG header dùng `#be0129` (đỏ sẫm) — ảnh vẫn dùng `#EE0033` chuẩn brand.
- Chữ xám than, tag nền `#F2F2F2`, nền trắng, hairline xám nhạt. Font web: Roboto, Arial.
- Header banner Tech Blog là ảnh chụp tòa nhà Viettel tông xám xanh — ảnh thumbnail nền trắng sẽ nổi, không đánh nhau.

## 6. Cách đo lại (khi nghi ngờ giao diện đã đổi)

```bash
# 1. thumbnail hiện có
curl -s -A Mozilla/5.0 "https://viettelcloud.vn/api/landingpage/tech-blog?language=1&limit=20&page=1" | python3 -c "
import json,sys; [print(t['image_url']) for i in json.load(sys.stdin)['results'] for t in i['translations'] if t.get('image_url')]"
# 2. khung hiển thị thật: Chrome headless + playwright-core (npm i playwright-core; channel 'chrome'), đo getBoundingClientRect của <img>
#    có src chứa os.viettelcloud.vn ở viewport 1440 và 390 trên /tech-blog và một trang /tech-blog/{cat}/{id}.
```
