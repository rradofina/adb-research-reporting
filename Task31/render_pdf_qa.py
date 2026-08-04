from __future__ import annotations

import argparse
from pathlib import Path

import fitz
from PIL import Image, ImageDraw


def render(pdf_path: Path, render_dir: Path, contact_dir: Path) -> tuple[int, int]:
    render_dir.mkdir(parents=True, exist_ok=True)
    contact_dir.mkdir(parents=True, exist_ok=True)

    document = fitz.open(pdf_path)
    for page_number, page in enumerate(document, start=1):
        pixmap = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
        pixmap.save(render_dir / f"page-{page_number:03d}.png")

    paths = sorted(render_dir.glob("page-*.png"))
    cols, rows = 4, 2
    thumb_w, thumb_h = 330, 430
    pad, label_h = 18, 24
    for sheet_index in range(0, len(paths), cols * rows):
        batch = paths[sheet_index : sheet_index + cols * rows]
        width = cols * (thumb_w + pad) + pad
        height = rows * (thumb_h + label_h + pad) + pad
        canvas = Image.new("RGB", (width, height), "#D9E1E5")
        draw = ImageDraw.Draw(canvas)
        for index, path in enumerate(batch):
            with Image.open(path).convert("RGB") as image:
                image.thumbnail((thumb_w, thumb_h))
                x = pad + (index % cols) * (thumb_w + pad) + (thumb_w - image.width) // 2
                y = pad + (index // cols) * (thumb_h + label_h + pad)
                canvas.paste(image, (x, y))
                draw.text((x, y + image.height + 3), path.stem, fill="#17365D")
        canvas.save(contact_dir / f"contact-{sheet_index // (cols * rows) + 1:02d}.png")

    return len(paths), len(list(contact_dir.glob("contact-*.png")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("render_dir", type=Path)
    parser.add_argument("contact_dir", type=Path)
    args = parser.parse_args()
    pages, contacts = render(args.pdf, args.render_dir, args.contact_dir)
    print(f"{args.pdf}: rendered {pages} pages and created {contacts} contact sheets")
