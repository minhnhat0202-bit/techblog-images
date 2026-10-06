# Phong cách ISOMETRIC GRADIENT cho thumbnail (`scripts/iso.py`)

Người dùng chọn phong cách này ngày 06/10/2026 thay cho line-art phẳng vì "nền trắng + nét đơn nhìn đơn điệu". Đây là
phong cách minh họa 3D đẳng cự (trục x xuống-phải, y xuống-trái, z lên; không phối cảnh), mặt khối tô gradient mềm,
bóng đổ mềm dưới chân — quen thuộc ở landing page cloud/SaaS. Bản Viettel khác bản phổ biến ở một điểm: **gradient chỉ
đi trong tint/shade của 5 màu brand**, không xanh/tím.

## 1. Bảng mặt khối (đã cài trong `iso.py` → `PAL`)

| Palette | Mặt trên | Mặt trái (+y) | Mặt phải (+x) | Dùng cho |
|---|---|---|---|---|
| `white` | FFFFFF→F7F7F8 | EEEEEF→E2E3E5 | DADBDD→CBCCCE | khối nền rất nhẹ, tầng phụ |
| `light` | FFFFFF→F2F2F2 | E4E5E7→D2D3D5 | C8C9CB→B5B4B4 | platform / cluster / sàn |
| `mid` | DADBDD→C4C5C7 | B5B4B4→9D9D9F | 8F9093→6F7377 | vật thể thường (pod, server, đĩa) |
| `dark` | 6B7075→44494D | 44494D→34383B | 2C2F32→1E2124 | vật thể tối để tạo tương phản, ≤ 1–2 khối |
| `red` | FF4D70→EE0033 | EE0033→CC002B | C10029→950020 | **vật thể được nói tới** — một cụm đỏ mỗi hình |

Mặt trên luôn sáng nhất, mặt phải tối nhất (nguồn sáng trên-trái). Viền mặt trên trắng mờ 1.5 px tạo cạnh "bóng".
Bóng chân: ellipse radial `#44494D` opacity 0.2 → 0. Không bóng đổ dài, không glow, không texture trên mặt khối.

## 2. Primitives

```python
from iso import Scene
sc = Scene(unit=70)                 # 1 ô lưới = 70 px
sc.shadow(x, y, w, d)               # bóng dưới footprint
sc.slab(x, y, z, w, d, h, pal)      # tấm mỏng (platform)
sc.cube(x, y, z, w, d, h, pal)      # hộp (server, container, node)
sc.cylinder(x, y, z, r, h, pal)     # trụ (database, storage, disk)
sc.hexprism(x, y, z, r, h, pal)     # lăng trụ lục giác (pod / Kubernetes)
sc.divider(x1, y1, x2, y2, z, color, width, dash)   # vạch trên mặt sàn (ranh giới namespace, lane)
svg = sc.svg(pad=30)                # <svg> hoàn chỉnh, tự tính viewBox; sắp lớp theo (z đáy, x+y)
```
Dán `svg` vào `<div class="art">` của `thumbnail.html`, đặt `--art-size` 740–800 px và bỏ `stroke-width:var(--stroke)`
khỏi `.art svg` (khối không dùng stroke). Nền `bg-circuit` hợp nhất; `bg-dots` cũng được.

## 3. Ẩn dụ isometric theo chủ đề

| Chủ đề | Cảnh |
|---|---|
| Kubernetes / namespace | platform `light` 6×4, divider chia lane, 4–6 `hexprism`, một lane `red` |
| Compute / VM / server | 2–3 `cube` 1×2×0.5 xếp chồng (rack), đèn = `cube` 0.1 đỏ ở mặt trước |
| Storage / database / backup | 2–3 `cylinder` r 0.8 h 0.5 chồng nhau; đĩa trên `red` |
| Load balancer | 1 `cube` `red` phía trước, 3 `cube` `mid` phía sau, `divider` làm đường nối trên sàn |
| Network / VPC | platform, các `cube` nhỏ 0.6 nối bằng `divider` liền, một `cube` `red` |
| GPU / AI | `slab` `dark` 2×2 (chip) trên platform, các `cube` 0.2 `mid` làm chân; chữ không cần |
| Security | `cube` `red` 1×1×1 ở giữa, 4 `slab` `light` mỏng dựng quanh (tường) — vẽ tường bằng cube h cao w mỏng |

Giữ ≤ 10 khối; chủ thể chiếm 45–60% chiều cao canvas; tâm cảnh trùng tâm canvas (vùng an toàn 1000×760).

## 4. Ảnh trong bài đi cùng: biến thể `raised` của `inline.html`
Sơ đồ vẫn phẳng (không dựng khối nghiêng vì nhãn cần đọc được trên mobile), nhưng `<body class="… raised">` biến node thành
khối nổi nhẹ: gradient trắng→F2F2F3, cạnh dày 7 px `#CFD0D2` phía dưới, bóng mềm; node đỏ gradient FF4D70→EE0033 cạnh
`#A80026`; nền radial trắng→F3F3F4. Người dùng duyệt phương án này 06/10/2026 ("hướng 1"). Bỏ class `raised` khi cần phẳng hẳn.

## 4b. Khi nào vẫn dùng line-art phẳng cho thumbnail
- Thumbnail cho bài rất "khái niệm" (ví dụ quy trình, chính sách) không có vật thể vật lý để dựng khối.
- Người dùng nói "tối giản tuyệt đối" / "line-art".

## 5. Thứ tự vẽ và hạn chế của `iso.py`
Thứ tự vẽ là sắp xếp topo trên hộp bao: A vẽ trước B khi A nằm hoàn toàn xa hơn theo trục x hoặc y (tọa độ nhỏ hơn), hoặc
thấp hơn theo z. Đúng cho mọi cảnh gồm hộp/trụ/lăng trụ không giao nhau (đã sửa lỗi 06/10/2026: chân chip hàng sau từng
đè lên thân chip khi còn dùng khóa (z, x+y)). Hộp giao nhau tạo chu trình → phần còn lại xếp theo heuristic; khi đó tách
vật thể thành khối nhỏ không giao nhau. Chưa có chữ trên mặt khối; cần chữ thì dùng biến thể `icon-keyword` của template.
