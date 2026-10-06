# Prompt cho công cụ sinh ảnh AI (khi người dùng muốn tranh minh họa thay vì sơ đồ)

Dùng khi bài cần hình "có không khí" (ví dụ case study, bài quan điểm) mà ẩn dụ line-art chưa đủ. Vẫn phải ra ảnh tối
giản, đúng màu; model thường thêm xanh/tím và chữ lỗi, nên hậu kỳ là bắt buộc.

## 1. Công cụ sẵn có trong môi trường
- **Figma MCP `generate_image`** (server claude.ai Figma): tạo ảnh từ prompt, có thể tải về bằng `download_assets`.
  Yêu cầu tỷ lệ 3:2 (thumbnail) hoặc 16:9 (ảnh trong bài) rồi resize về đúng pixel.
- Gemini / Imagen, Midjourney, DALL·E: người dùng tự chạy với prompt bên dưới, gửi lại file.

## 2. Khung prompt (tiếng Anh cho model; điền phần trong ngoặc)

```
Minimalist flat vector illustration for a cloud-computing tech blog thumbnail.
Subject: [one metaphor, e.g. "a single abstract GPU chip seen from above with pins on four sides"].
Style: thin uniform line art, rounded stroke ends, generous white space, no shading, no gradient, no 3D, no texture,
no background scene, no people, no text, no logos.
Colors: pure white background #FFFFFF; lines in dark gray #44494D; one small accent in Viettel red #EE0033
[say which part is red, e.g. "only the chip pins are red"]; optional light gray #B5B4B4 thin arc around the subject.
Strictly no blue, purple, orange, yellow or green anywhere.
Composition: subject centered, occupying about half of the frame height; aspect ratio 3:2.
```
Ảnh trong bài: đổi dòng cuối thành `aspect ratio 16:9, subject centered, wide margins` và mô tả tối đa 3 phần tử nối
bằng mũi tên.

Biến thể Midjourney thêm: `--ar 3:2 --style raw --no text,logo,blue,purple,gradient,shadow,3d`.

## 3. Hậu kỳ bắt buộc
```bash
python3 ~/.claude/skills/viettel-techblog-images/scripts/fit_thumb.py ai.png --out techblog-<slug>-thumb.png --webp   # pad/crop về 1500×1000, nền trắng
python3 ~/.claude/skills/viettel-techblog-images/scripts/check_image.py techblog-<slug>-thumb.png --kind thumb
python3 ~/.claude/skills/viettel-techblog-images/scripts/preview_crops.py techblog-<slug>-thumb.png --out preview.png
```
- "Màu ngoài bảng" > 0.5% ⇒ model lệch hue; thử lại prompt (nhấn mạnh "monochrome gray line art, single red accent") hoặc
  chuyển sang đường HTML/SVG.
- Có chữ lỗi/logo ⇒ bỏ, sinh lại với `no text`.
- Nhiều ảnh trong cùng bài ⇒ cùng một prompt khung, chỉ đổi dòng Subject, để nét và tông giống nhau.

## 4. Khi nào không dùng AI
Sơ đồ kiến trúc, luồng request, bảng so sánh, bất cứ hình nào có nhãn/chữ ⇒ luôn dựng bằng `inline.html` (chính xác, sửa
được). Thumbnail cho bài hướng dẫn kỹ thuật ⇒ icon line-art từ template nhanh và nhất quán hơn AI.
