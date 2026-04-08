#!/usr/bin/env python3
"""
Generate premium print-ready RuangKu QR assets.
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
SHORT_URL = "kuker24.github.io/Ruangku"

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
def vertical_gradient(w: int, h: int, top=(8, 21, 43), mid=(14, 34, 66), bottom=(9, 18, 36)) -> Image.Image:
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


def add_rounded_shadow(
    base: Image.Image,
    box,
    *,
    radius: int,
    color=(0, 0, 0, 120),
    blur: int = 18,
    offset: tuple[int, int] = (0, 12),
):
    x1, y1, x2, y2 = box
    ox, oy = offset
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x1 + ox, y1 + oy, x2 + ox, y2 + oy), radius=radius, fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


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
    """Draw text with subtle dark stroke for stronger readability."""
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

    # Ambient background glows
    draw_glow_circle(canvas, (W - 170, 330), 430, color=(37, 99, 235), alpha=140, blur=90)
    draw_glow_circle(canvas, (260, H - 320), 460, color=(124, 58, 237), alpha=110, blur=95)
    draw_glow_circle(canvas, (W // 2, H // 2 + 340), 300, color=(245, 158, 11), alpha=70, blur=75)

    draw = ImageDraw.Draw(canvas)

    # Fonts
    f_badge = load_font(34, bold=True)
    f_brand = load_font(104, bold=True)
    f_title = load_font(96, bold=True)
    f_sub = load_font(42, bold=False)
    f_scan = load_font(34, bold=True)
    f_step = load_font(38, bold=False)
    f_step_num = load_font(38, bold=True)
    f_url_label = load_font(30, bold=True)
    f_url = load_font(36, bold=True)
    f_footer = load_font(28, bold=False)

    # Top badge
    badge_text = "RUANGKU • CAMPUS RESERVATION"
    badge_w = int(draw.textlength(badge_text, font=f_badge)) + 84
    badge_h = 74
    badge_x = (W - badge_w) // 2
    badge_y = 82
    rounded_rect(
        draw,
        (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
        26,
        fill=(245, 158, 11, 238),
        outline=(255, 219, 130, 255),
        width=2,
    )
    draw.text((badge_x + 42, badge_y + 18), badge_text, fill=(26, 18, 2), font=f_badge)

    # Headline
    brand_text = "RuangKu"
    brand_w = draw.textlength(brand_text, font=f_brand)
    draw_text_readable(draw, ((W - int(brand_w)) // 2, 182), brand_text, f_brand, fill=(255, 255, 255), stroke_width=3)

    title_text = "SCAN QR UNTUK PINJAM RUANG"
    title_w = draw.textlength(title_text, font=f_title)
    draw_text_readable(draw, ((W - int(title_w)) // 2, 310), title_text, f_title, fill=(255, 255, 255), stroke_width=3)

    sub_text = "Cepat, rapi, profesional — tanpa antre di BAK"
    sub_w = draw.textlength(sub_text, font=f_sub)
    draw_text_readable(draw, ((W - int(sub_w)) // 2, 430), sub_text, f_sub, fill=(238, 246, 255), stroke_width=2)

    # Main glass card
    card = (190, 560, W - 190, 3040)
    add_rounded_shadow(canvas, card, radius=56, color=(0, 0, 0, 125), blur=24, offset=(0, 16))
    rounded_rect(draw, card, 56, fill=(255, 255, 255, 24), outline=(255, 255, 255, 88), width=2)
    draw.line((card[0] + 140, card[1] + 1, card[2] - 140, card[1] + 1), fill=(255, 255, 255, 145), width=2)

    # Instruction strip (high contrast)
    strip = (card[0] + 120, card[1] + 90, card[2] - 120, card[1] + 178)
    rounded_rect(draw, strip, 22, fill=(8, 20, 40, 176), outline=(255, 255, 255, 62), width=2)
    strip_text = "Arahkan kamera HP ke QR berikut"
    strip_w = draw.textlength(strip_text, font=f_sub)
    draw_text_readable(draw, ((W - int(strip_w)) // 2, strip[1] + 22), strip_text, f_sub, fill=(255, 255, 255), stroke_width=2)

    # QR panel (very clean white for scan reliability)
    qr_panel_size = 1360
    qr_panel_x = (W - qr_panel_size) // 2
    qr_panel_y = card[1] + 230
    qr_panel = (qr_panel_x, qr_panel_y, qr_panel_x + qr_panel_size, qr_panel_y + qr_panel_size)

    add_rounded_shadow(canvas, qr_panel, radius=36, color=(0, 0, 0, 95), blur=18, offset=(0, 10))
    rounded_rect(draw, qr_panel, 36, fill=(255, 255, 255, 255), outline=(224, 232, 244, 255), width=5)

    qr_size = 1140
    qr_img = make_qr(FORM_URL, qr_size)
    qr_x = (W - qr_size) // 2
    qr_y = qr_panel_y + (qr_panel_size - qr_size) // 2
    canvas.paste(qr_img, (qr_x, qr_y))

    # Scan badge
    scan_badge = "SCAN ME"
    scan_w = int(draw.textlength(scan_badge, font=f_scan)) + 96
    scan_h = 76
    scan_x = qr_panel[2] - scan_w - 24
    scan_y = qr_panel[1] - 38
    rounded_rect(
        draw,
        (scan_x, scan_y, scan_x + scan_w, scan_y + scan_h),
        25,
        fill=(245, 158, 11, 255),
        outline=(255, 214, 114, 255),
        width=2,
    )
    draw.text((scan_x + 48, scan_y + 18), scan_badge, fill=(27, 18, 2), font=f_scan)

    # Step chips (dark + bright text for readability)
    steps = [
        "Scan QR dengan kamera HP",
        "Isi borang reservasi ruang secara digital",
        "Tunggu konfirmasi dari staf BAK",
    ]
    chip_left = card[0] + 120
    chip_right = card[2] - 120
    chip_h = 132
    chip_gap = 24
    chip_start_y = qr_panel[3] + 88

    for i, txt in enumerate(steps):
        y1 = chip_start_y + i * (chip_h + chip_gap)
        y2 = y1 + chip_h
        chip_box = (chip_left, y1, chip_right, y2)

        add_rounded_shadow(canvas, chip_box, radius=28, color=(0, 0, 0, 82), blur=10, offset=(0, 6))
        rounded_rect(draw, chip_box, 28, fill=(7, 18, 36, 188), outline=(255, 255, 255, 68), width=2)

        # Number bubble
        cx = chip_left + 66
        cy = (y1 + y2) // 2
        r = 34
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(245, 158, 11, 255), outline=(255, 217, 124, 255), width=2)
        num = str(i + 1)
        num_w = draw.textlength(num, font=f_step_num)
        draw.text((cx - num_w / 2, cy - 25), num, fill=(26, 17, 2), font=f_step_num)

        draw_text_readable(draw, (chip_left + 122, y1 + 42), txt, f_step, fill=(250, 253, 255), stroke_width=2)

    # URL fallback panel (highest readability)
    url_box = (card[0] + 130, card[3] - 260, card[2] - 130, card[3] - 108)
    add_rounded_shadow(canvas, url_box, radius=24, color=(0, 0, 0, 90), blur=12, offset=(0, 6))
    rounded_rect(draw, url_box, 24, fill=(255, 255, 255, 244), outline=(220, 228, 238, 255), width=3)

    url_label = "Jika QR tidak terbaca, buka link ini:"
    label_w = draw.textlength(url_label, font=f_url_label)
    draw.text(((W - int(label_w)) // 2, url_box[1] + 26), url_label, fill=(52, 63, 82), font=f_url_label)

    url_w = draw.textlength(SHORT_URL, font=f_url)
    draw.text(
        ((W - int(url_w)) // 2, url_box[1] + 74),
        SHORT_URL,
        fill=(16, 34, 68),
        font=f_url,
        stroke_width=1,
        stroke_fill=(255, 255, 255),
    )

    # Footer
    footer = "RuangKu • Cepat • Transparan • Tanpa Antre"
    footer_w = draw.textlength(footer, font=f_footer)
    draw_text_readable(draw, ((W - int(footer_w)) // 2, H - 90), footer, f_footer, fill=(224, 236, 255), stroke_width=2)

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
    canvas = vertical_gradient(W, H, top=(7, 20, 42), mid=(15, 37, 70), bottom=(8, 17, 35)).convert("RGBA")
    draw_glow_circle(canvas, (W - 180, 260), 330, color=(59, 130, 246), alpha=130, blur=76)
    draw_glow_circle(canvas, (250, H - 200), 340, color=(124, 58, 237), alpha=98, blur=78)

    draw = ImageDraw.Draw(canvas)

    f_title = load_font(82, bold=True)
    f_sub = load_font(36, bold=False)
    f_badge = load_font(30, bold=True)
    f_info = load_font(34, bold=True)
    f_url = load_font(28, bold=False)

    # Main card
    card = (120, 120, W - 120, H - 120)
    add_rounded_shadow(canvas, card, radius=48, color=(0, 0, 0, 120), blur=20, offset=(0, 12))
    rounded_rect(draw, card, 48, fill=(255, 255, 255, 22), outline=(255, 255, 255, 72), width=2)

    title = "SCAN UNTUK RESERVASI"
    tw = draw.textlength(title, font=f_title)
    draw_text_readable(draw, ((W - int(tw)) // 2, 200), title, f_title, fill=(255, 255, 255), stroke_width=3)

    subtitle_strip = (card[0] + 150, 320, card[2] - 150, 402)
    rounded_rect(draw, subtitle_strip, 20, fill=(7, 18, 35, 182), outline=(255, 255, 255, 60), width=2)
    subtitle = "Scan QR untuk isi borang digital"
    sw = draw.textlength(subtitle, font=f_sub)
    draw_text_readable(draw, ((W - int(sw)) // 2, subtitle_strip[1] + 20), subtitle, f_sub, fill=(251, 253, 255), stroke_width=2)

    # QR panel
    panel_size = 1160
    panel_x = (W - panel_size) // 2
    panel_y = 450
    panel = (panel_x, panel_y, panel_x + panel_size, panel_y + panel_size)

    add_rounded_shadow(canvas, panel, radius=30, color=(0, 0, 0, 95), blur=16, offset=(0, 8))
    rounded_rect(draw, panel, 30, fill=(255, 255, 255, 255), outline=(225, 233, 244, 255), width=4)

    qr_size = 980
    qr = make_qr(FORM_URL, qr_size)
    canvas.paste(qr, ((W - qr_size) // 2, panel_y + (panel_size - qr_size) // 2))

    # Corner badge
    badge = "RuangKu"
    bw = int(draw.textlength(badge, font=f_badge)) + 58
    bh = 60
    bx = panel[2] - bw - 18
    by = panel[1] - 30
    rounded_rect(draw, (bx, by, bx + bw, by + bh), 21, fill=(245, 158, 11), outline=(255, 214, 112), width=2)
    draw.text((bx + 30, by + 13), badge, fill=(30, 18, 0), font=f_badge)

    # Bottom readability strip
    info_box = (220, 1660, W - 220, 1774)
    rounded_rect(draw, info_box, 20, fill=(255, 255, 255, 244), outline=(220, 228, 238, 255), width=3)
    info_text = "Scan • Isi Borang Digital • Selesai"
    iw = draw.textlength(info_text, font=f_info)
    draw.text(((W - int(iw)) // 2, info_box[1] + 34), info_text, fill=(19, 37, 70), font=f_info)

    url_text = SHORT_URL
    uw = draw.textlength(url_text, font=f_url)
    draw_text_readable(draw, ((W - int(uw)) // 2, 1808), url_text, f_url, fill=(235, 244, 255), stroke_width=2)

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
