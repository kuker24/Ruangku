#!/usr/bin/env python3
"""
Generate print-ready RuangKu QR assets.
Outputs:
- assets/qr/RuangKu_QR_Poster_A4.png
- assets/qr/RuangKu_QR_Poster_A4.pdf
- assets/qr/RuangKu_QR_Sticker_Square.png
- assets/qr/RuangKu_QR_Plain.png
"""

from __future__ import annotations

import os
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FORM_URL = "https://kuker24.github.io/Ruangku/"

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "assets" / "qr"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------
# Font helpers
# -------------------------
def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# -------------------------
# Drawing helpers
# -------------------------
def vertical_gradient(w: int, h: int, top=(11, 29, 58), mid=(17, 42, 79), bottom=(10, 20, 42)) -> Image.Image:
    img = Image.new("RGB", (w, h), top)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        if t < 0.55:
            tt = t / 0.55
            r = int(top[0] + (mid[0] - top[0]) * tt)
            g = int(top[1] + (mid[1] - top[1]) * tt)
            b = int(top[2] + (mid[2] - top[2]) * tt)
        else:
            tt = (t - 0.55) / 0.45
            r = int(mid[0] + (bottom[0] - mid[0]) * tt)
            g = int(mid[1] + (bottom[1] - mid[1]) * tt)
            b = int(mid[2] + (bottom[2] - mid[2]) * tt)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img


def draw_glow_circle(base: Image.Image, center: tuple[int, int], radius: int, color=(59, 130, 246), alpha=110, blur=70):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


def make_qr(url: str, target_size: int) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=18,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img.resize((target_size, target_size), Image.Resampling.NEAREST)


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_text_readable(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    *,
    fill: tuple[int, int, int] = (255, 255, 255),
    stroke_fill: tuple[int, int, int] = (8, 18, 36),
    stroke_width: int = 2,
):
    """Draw text with subtle dark stroke so it stays readable on bright gradients."""
    draw.text(xy, text, fill=fill, font=font, stroke_width=stroke_width, stroke_fill=stroke_fill)


def save_with_dpi(image: Image.Image, png_path: Path, pdf_path: Path, dpi=300):
    image_rgb = image.convert("RGB")
    image_rgb.save(png_path, format="PNG", dpi=(dpi, dpi), optimize=True)
    image_rgb.save(pdf_path, format="PDF", resolution=dpi)


# -------------------------
# Asset 1: A4 wall poster
# -------------------------
def generate_a4_poster():
    # A4 portrait @ 300 DPI
    W, H = 2480, 3508
    canvas = vertical_gradient(W, H).convert("RGBA")

    # ambient glows
    draw_glow_circle(canvas, (W - 220, 360), 400, color=(37, 99, 235), alpha=130, blur=85)
    draw_glow_circle(canvas, (300, H - 350), 420, color=(124, 58, 237), alpha=100, blur=95)
    draw_glow_circle(canvas, (W // 2, H // 2 + 250), 260, color=(245, 158, 11), alpha=65, blur=70)

    draw = ImageDraw.Draw(canvas)

    # Top brand area
    f_brand = load_font(98, bold=True)
    f_sub = load_font(40, bold=False)
    f_title = load_font(92, bold=True)
    f_desc = load_font(42, bold=False)
    f_steps = load_font(34, bold=False)
    f_footer = load_font(26, bold=False)
    f_pill = load_font(34, bold=True)

    # Brand title
    brand_text = "RuangKu"
    brand_w = draw.textlength(brand_text, font=f_brand)
    draw.text(((W - brand_w) // 2, 150), brand_text, fill=(255, 255, 255), font=f_brand)

    sub_text = "Sistem Reservasi Ruang Kampus Digital"
    sub_w = draw.textlength(sub_text, font=f_sub)
    draw_text_readable(draw, ((W - sub_w) // 2, 268), sub_text, f_sub, fill=(246, 250, 255), stroke_width=2)

    # Main heading
    h_text = "SCAN UNTUK RESERVASI"
    h_w = draw.textlength(h_text, font=f_title)
    draw.text(((W - h_w) // 2, 390), h_text, fill=(255, 255, 255), font=f_title)

    # Glass card container
    card_margin_x = 210
    card_top = 560
    card_bottom = 2940
    card_box = (card_margin_x, card_top, W - card_margin_x, card_bottom)

    # card shadow
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    rounded_rect(sd, (card_box[0] + 8, card_box[1] + 20, card_box[2] + 8, card_box[3] + 20), 48, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(shadow)

    # card body
    rounded_rect(draw, card_box, 48, fill=(255, 255, 255, 22), outline=(255, 255, 255, 70), width=2)

    # subtle highlight line
    draw.line((card_box[0] + 130, card_top + 1, card_box[2] - 130, card_top + 1), fill=(255, 255, 255, 130), width=2)

    # Instruction text above QR
    top_desc = "Gunakan kamera HP untuk scan QR code ini"
    top_desc_w = draw.textlength(top_desc, font=f_desc)
    draw_text_readable(draw, ((W - top_desc_w) // 2, card_top + 92), top_desc, f_desc, fill=(255, 255, 255), stroke_width=2)

    # White QR panel for max readability
    qr_panel_size = 1320
    qr_panel_x = (W - qr_panel_size) // 2
    qr_panel_y = card_top + 210
    qr_panel = (qr_panel_x, qr_panel_y, qr_panel_x + qr_panel_size, qr_panel_y + qr_panel_size)

    rounded_rect(draw, qr_panel, 32, fill=(255, 255, 255), outline=(235, 239, 248), width=3)

    # QR code itself
    qr_size = 1120
    qr_img = make_qr(FORM_URL, qr_size)
    qr_x = (W - qr_size) // 2
    qr_y = qr_panel_y + (qr_panel_size - qr_size) // 2
    canvas.paste(qr_img, (qr_x, qr_y))

    # Orange scan pill
    pill_text = "SCAN ME"
    pill_w = int(draw.textlength(pill_text, font=f_pill)) + 90
    pill_h = 72
    pill_x = qr_panel[2] - pill_w - 24
    pill_y = qr_panel[1] - 36
    rounded_rect(draw, (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), 24, fill=(245, 158, 11), outline=(255, 205, 96), width=2)
    draw.text((pill_x + 44, pill_y + 16), pill_text, fill=(20, 15, 0), font=f_pill)

    # Steps section
    step_y = qr_panel[3] + 92
    steps = [
        "1) Scan QR dengan kamera HP",
        "2) Isi formulir reservasi RuangKu",
        "3) Tunggu konfirmasi dari staf BAK via WhatsApp",
    ]
    for i, text in enumerate(steps):
        draw_text_readable(draw, (card_box[0] + 120, step_y + i * 72), text, f_steps, fill=(248, 252, 255), stroke_width=2)

    # Footer note
    footer = "RuangKu • Cepat • Transparan • Tanpa Antre"
    footer_w = draw.textlength(footer, font=f_footer)
    draw_text_readable(draw, ((W - footer_w) // 2, card_bottom - 98), footer, f_footer, fill=(232, 240, 255), stroke_width=2)

    # Save
    png_path = OUT_DIR / "RuangKu_QR_Poster_A4.png"
    pdf_path = OUT_DIR / "RuangKu_QR_Poster_A4.pdf"
    save_with_dpi(canvas, png_path, pdf_path)
    return png_path, pdf_path


# -------------------------
# Asset 2: Sticker/Square
# -------------------------
def generate_square_sticker():
    W, H = 2000, 2000
    canvas = vertical_gradient(W, H, top=(10, 28, 56), mid=(18, 42, 77), bottom=(8, 18, 36)).convert("RGBA")
    draw_glow_circle(canvas, (W - 180, 240), 300, color=(59, 130, 246), alpha=120, blur=72)
    draw_glow_circle(canvas, (260, H - 180), 320, color=(124, 58, 237), alpha=95, blur=75)

    draw = ImageDraw.Draw(canvas)
    f_title = load_font(78, bold=True)
    f_sub = load_font(38, bold=False)
    f_badge = load_font(30, bold=True)

    # Card
    card = (130, 140, W - 130, H - 140)
    rounded_rect(draw, card, 44, fill=(255, 255, 255, 20), outline=(255, 255, 255, 66), width=2)

    title = "Reservasi Ruang"
    tw = draw.textlength(title, font=f_title)
    draw.text(((W - tw) // 2, 220), title, fill=(255, 255, 255), font=f_title)

    subtitle = "Scan QR untuk isi Google Form"
    sw = draw.textlength(subtitle, font=f_sub)
    draw_text_readable(draw, ((W - sw) // 2, 320), subtitle, f_sub, fill=(250, 252, 255), stroke_width=2)

    # QR panel
    panel = (370, 430, W - 370, H - 370)
    rounded_rect(draw, panel, 28, fill=(255, 255, 255), outline=(235, 239, 248), width=3)

    qr_size = 1120
    qr = make_qr(FORM_URL, qr_size)
    canvas.paste(qr, ((W - qr_size) // 2, (H - qr_size) // 2 + 40))

    badge = "RuangKu"
    bw = int(draw.textlength(badge, font=f_badge)) + 56
    bh = 58
    bx = panel[2] - bw - 18
    by = panel[1] - 30
    rounded_rect(draw, (bx, by, bx + bw, by + bh), 20, fill=(245, 158, 11), outline=(255, 209, 106), width=2)
    draw.text((bx + 28, by + 12), badge, fill=(30, 18, 0), font=f_badge)

    out = OUT_DIR / "RuangKu_QR_Sticker_Square.png"
    canvas.convert("RGB").save(out, dpi=(300, 300), optimize=True)
    return out


# -------------------------
# Asset 3: plain QR
# -------------------------
def generate_plain_qr():
    qr = make_qr(FORM_URL, 1600)
    out = OUT_DIR / "RuangKu_QR_Plain.png"
    qr.save(out, dpi=(300, 300), optimize=True)
    return out


def main():
    p_png, p_pdf = generate_a4_poster()
    s_png = generate_square_sticker()
    q_png = generate_plain_qr()

    print("✅ Generated QR assets:")
    print(f"- {p_png}")
    print(f"- {p_pdf}")
    print(f"- {s_png}")
    print(f"- {q_png}")


if __name__ == "__main__":
    main()
