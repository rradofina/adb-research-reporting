from pathlib import Path
from PIL import Image, ImageDraw

src = Path("tmp/pdf_render_v1")
out = Path("tmp/pdf_contact_v1")
out.mkdir(parents=True, exist_ok=True)
paths = sorted(src.glob("page-*.png"))
cols, rows = 4, 2
thumb_w, thumb_h = 330, 430
pad, label_h = 18, 24
for sheet_idx in range(0, len(paths), cols * rows):
    batch = paths[sheet_idx:sheet_idx + cols * rows]
    canvas = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (thumb_h + label_h + pad) + pad), "#D9E1E5")
    draw = ImageDraw.Draw(canvas)
    for j, p in enumerate(batch):
        im = Image.open(p).convert("RGB")
        im.thumbnail((thumb_w, thumb_h))
        x = pad + (j % cols) * (thumb_w + pad) + (thumb_w - im.width) // 2
        y = pad + (j // cols) * (thumb_h + label_h + pad)
        canvas.paste(im, (x, y))
        draw.text((x, y + im.height + 3), p.stem, fill="#17365D")
    canvas.save(out / f"contact-{sheet_idx // (cols * rows) + 1:02d}.png")
print(f"Created {len(list(out.glob('contact-*.png')))} contact sheets")
