# Style guide · Minimalism × màu Viettel cho ảnh Tech Blog

## 1. Bảng màu (chỉ 5 màu Viettel + trắng; tint/shade của chúng được phép, hue khác không)

| Vai trò trong ảnh | HEX | Ghi chú |
|---|---|---|
| Nền | `#FFFFFF` | Thumbnail luôn trắng (nổi trên nền trang trắng nhờ khoảng trống, không cần viền). Ảnh trong bài: trắng; khối cần tách dùng `#F2F2F2` hoặc `#F8F8F9` |
| Nét chính, chữ chính | `#44494D` | Stroke icon, viền node, chữ nhãn. Không dùng đen `#000000` cho nét (quá gắt trên trắng); đen chỉ cho chữ tiêu đề lớn nếu có |
| Nét phụ, hairline, mũi tên | `#B5B4B4` · `#DADBDD` | Đường nối, lưới, khung gom nhóm, phần "chưa nói tới" |
| Mảng xám rất nhạt | `#F2F2F2` · `#F8F8F9` | Nền node phụ, vùng gom nhóm; không viền |
| **Điểm nhấn** | `#EE0033` | Một chi tiết duy nhất: bộ phận của icon (chân chip, mũi tên, chấm), node đang bàn tới, vạch ngắn. Fill đặc hoặc stroke, không gradient |
| Đỏ nhạt (hiếm) | `#FFD9E0` | Nền của node đỏ khi cần chữ đỏ trên nền nhạt; không dùng trên thumbnail |

Tỷ lệ gợi ý trên thumbnail: trắng ≥ 75%, xám 2–20%, **đỏ 0.3–10%** — line-art chỉ cần 0.3–2% đỏ là đủ nhận diện, mảng đỏ đặc
không quá 10% (`check_image.py` đo giúp). Ảnh trong bài: đỏ ≤ 20%.

Cấm: xanh dương, xanh lá, tím, cam, vàng, gradient nhiều màu, ảnh stock. Logo bên thứ ba (Kubernetes, NVIDIA, MySQL…)
không chèn bản màu gốc; viết tên dạng chữ (`K8s`, `vLLM`) hoặc vẽ lại hình khối một màu `#44494D`.

## 2. Nét và hình

- Line-art: `fill="none" stroke="#44494D" stroke-linecap="round" stroke-linejoin="round"`. Độ dày nét đồng nhất trong một
  ảnh: thumbnail 14–16 px trên canvas 1500 (template đặt `--stroke:5.2` trong viewBox 200 × scale 3 của `--art-size:600px`);
  ảnh trong bài 10–12 px. Icon trong `assets/icons` vẽ ở stroke 7 nhưng template ghi đè bằng `--stroke`.
- Hình học cơ bản: chữ nhật bo góc nhỏ (rx = 2–3% cạnh), tròn, lục giác, đường thẳng. Góc bo đồng nhất.
- Fill đặc chỉ cho điểm nhấn đỏ và cho mảng xám nhạt nền. Không bóng, không viền kép, không texture, không 3D/isometric.
- Khoảng trống là vật liệu chính: thumbnail art chiếm 45–60% chiều cao canvas; quanh nó trống. Ảnh trong bài lề ≥ 80 px.
- Một họa tiết thương hiệu được phép (tùy chọn, không bắt buộc): **cung tròn mảnh** xám `#DADBDD` stroke 8–10 px bao quanh
  icon, hở một đoạn (như thumbnail GPU hiện có trên trang) — gợi khung hội thoại của brand mà vẫn tối giản. Không dùng
  khung hội thoại đầy đủ hay họa tiết mảng lặp trên nền trắng (brand guideline cấm họa tiết mảng trên nền trắng trơn).

## 2b. Nền thumbnail (template có sẵn, đổi class trên `<body>`)

Nền trắng trơn bị người dùng chê "đơn điệu" (06/10/2026), nên template có lớp nền công nghệ **mờ**: gradient hướng tâm
trắng → `#F4F4F5` ở rìa, cộng một họa tiết xám nhạt (`#CFD0D2`–`#E3E4E6`) được mask mờ dần về tâm để vùng quanh icon
luôn sạch. Bốn biến thể:

| Class | Họa tiết | Khi dùng |
|---|---|---|
| `bg-circuit` (mặc định) | vài đường mạch hairline + chấm nối ở 4 góc, 2 chấm đỏ nhỏ | hầu hết bài hạ tầng/cloud; rõ "công nghệ" nhất, vẫn thưa |
| `bg-dots` | lưới chấm 46 px | bài khái niệm, dữ liệu, AI |
| `bg-grid` | lưới ô vuông 60 px | kiến trúc, sơ đồ, quy hoạch tài nguyên |
| `bg-hex` | tổ ong hairline | Kubernetes/container (tránh khi icon chính cũng là lục giác — bị rối) |
| `bg-none` | trắng trơn | khi người dùng muốn tối giản tuyệt đối |

Quy tắc: họa tiết chỉ dùng xám trong bảng màu, độ tương phản với nền ≤ 10%, không chạm vùng an toàn bằng nét đậm, không
dùng họa tiết thương hiệu (khung hội thoại) lặp trên nền trắng. PNG có gradient nặng 250–400 KB → **giao bản WebP**
(`--webp`, ~15–30 KB); `check_image.py` chấp nhận PNG nặng khi có WebP đạt bên cạnh. Ảnh trong bài không dùng nền
họa tiết (sơ đồ cần nền phẳng để đọc).

## 3. Chữ

- Font: `"FS PF BeauSans Pro", Roboto, Arial, sans-serif`. Trên máy không có BeauSans, Roboto cho kết quả gần nhất với web.
- Thumbnail: tối đa một "từ khóa" ≤ 4 ký tự đặt trong/cạnh icon (GPU, K8s, S3, API, LLM), weight 700, cỡ 120–180 px, màu
  `#44494D`. Không tiêu đề bài, không câu, không logo Viettel Cloud (trang đã có header).
- Ảnh trong bài: kicker in hoa 28 px giãn 0.08em màu `#B5B4B4` góc trên trái (ví dụ `HÌNH 2 · LUỒNG REQUEST`); nhãn node
  36–44 px weight 500; chữ phụ 30 px `#B5B4B4`. ≤ 3 từ mỗi nhãn, ≤ 7 node mỗi hình. Dài hơn ⇒ tách hình.

## 4. Ẩn dụ theo chủ đề (chọn một, đừng ghép ba)

| Chủ đề | Hình | Chi tiết đỏ gợi ý |
|---|---|---|
| Cloud nói chung, IaaS | đám mây nét đơn | một chấm/mũi tên vào mây |
| Compute, VM, server | chữ nhật xếp 2–3 tầng, mỗi tầng 1 chấm | chấm của tầng đang bàn |
| GPU, AI, LLM, inference | chip vuông có chân ra 4 phía, chữ GPU/LLM giữa | chân chip (như tiền lệ trên trang) |
| Kubernetes, container orchestration | 3–7 lục giác xếp tổ ong | lục giác trung tâm |
| Container, Docker | hộp (cube nét) hoặc 3 hộp xếp | một hộp |
| Load balancer, routing, gateway | một node trái → 3 node phải qua mũi tên | node trái hoặc mũi tên được chọn |
| Object storage, S3, backup | 3 đĩa chồng / thùng; backup thêm mũi tên vòng + đồng hồ | mũi tên vòng |
| Database, SQL | trụ (cylinder) nét | nắp trụ |
| Network, VPC, CDN | các chấm nối hairline, một chấm to | chấm to |
| Security, firewall, IAM | khiên + tick hoặc khóa | tick / thân khóa |
| Monitoring, observability | đường xung (pulse) trong khung | đỉnh xung |
| API, microservices | hai khối với khớp nối `{ }` | khớp nối |
| Serverless, function | tia sét trong mây | tia sét |
| CI/CD, pipeline, DevOps | mũi tên vòng ∞ hoặc 3 bước nối nhau | bước đang bàn |
| Migration, hybrid cloud | hai mây nối mũi tên, một mây nét đứt | mũi tên |
| Cost, FinOps | đồng hồ đo (gauge) hoặc biểu đồ cột 3 cột | cột được nhấn |
| Case study, khách hàng | tòa nhà nét đơn + mây nhỏ | mây |

Nguyên tắc: khi bài có nhiều khái niệm, thumbnail lấy khái niệm **xuất hiện trong tiêu đề**; các khái niệm còn lại để ảnh
trong bài.

## 5. Icon có sẵn (`assets/icons/`, viewBox 0 0 200 200, stroke 7, `stroke="currentColor"`, phần nhấn class `acc`)

`cloud` · `server` · `chip` · `database` · `storage` · `container` · `k8s` · `loadbalancer` · `shield` · `network` ·
`lock` · `monitor` · `backup` · `api` · `serverless` · `pipeline`.

Cách dùng trong HTML: dán nội dung file vào `<div class="art">…</div>`; CSS template đã đặt `color:#44494D` và
`.acc{stroke:#EE0033}` (hoặc `fill:#EE0033` cho phần tử có class `acc fill`). Đổi kích thước bằng biến `--art-size`.
Thêm chữ vào icon chip: `<text class="kw" x="100" y="112">GPU</text>` (CSS `.kw` có sẵn).

Tự vẽ icon mới: giữ đúng hệ (viewBox 200, stroke 7, bo tròn, lưới 10 px, chừa 20 px lề trong viewBox). Kiểm tra bằng cách
render thumbnail rồi nhìn ở preview 86×86.

## 6. Bố cục ảnh trong bài (template `inline.html`)

- Luồng trái → phải cho pipeline/request flow; trên → dưới cho phân tầng (client / edge / cluster). Không sơ đồ chéo.
- Node: chữ nhật bo 12 px, viền 3 px `#44494D`, nền trắng; node phụ `.soft` nền `#F2F2F2` không viền; node nhấn `.hl` nền
  `#EE0033` chữ trắng — **một `.hl` mỗi hình** (hai khi so sánh "trước/sau" cố ý).
- Mũi tên: hairline 3 px `#B5B4B4`, đầu mũi tên tam giác nhỏ; mũi tên nhấn đỏ 4 px chỉ khi nó là chủ đề.
- Gom nhóm: khung hairline nét đứt `#DADBDD` bo 16 px, nhãn nhóm in hoa nhỏ ở góc trên trái khung.
- So sánh hai phương án: hai cột cách nhau một hairline dọc, tiêu đề cột in hoa; phương án được khuyến nghị có một vạch đỏ ngắn trên tiêu đề.
- Số thứ tự bước: chữ trần đỏ `01 02 03` weight 700 (không hình tròn nền).
- Không screenshot thô; nếu phải minh họa UI, vẽ lại wireframe nét xám.

## 7. Không làm

- Không ảnh stock, không ảnh chụp, không 3D isometric, không gradient, không bóng, không glow.
- Không hơn một màu nhấn; không logo màu của bên thứ ba; không logo Viettel/Viettel Cloud trong ảnh (trang đã có).
- Không chữ dài trên thumbnail; không chữ < 36 px trên ảnh trong bài.
- Không để chi tiết quan trọng ngoài vùng an toàn 1000×760 của thumbnail.
- Không xuất ảnh > 1500 px rộng cho thumbnail hoặc > 250 KB; ảnh trong bài không > 500 KB.
- Không chỉnh sửa PNG đã render bằng tay; sửa HTML và render lại để lần sau tái tạo được.
