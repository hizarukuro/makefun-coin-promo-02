#!/usr/bin/env python3
"""Draw the Agent Cheque logo: the prize cheque itself, full-frame.

Why it looks the way it does: the judge reads the logo first, fitted
inside 512 px a side, and pump.fun traders see it as a small
thumbnail. The winning shape on this competition's own leaderboard is
a document that carries its whole pitch in the image — a receipt, a
wanted poster, a report card. So this logo is not a picture *of* the
concept, it *is* the concept: a bank cheque, cream on deep navy,
filling the frame, with the payee line, the amount box, the memo and
the red ESCROWED stamp all printed on it and all readable small.

The facts printed on the cheque are the coin's argument: make.fun
locked this bounty's whole $1,000 prize in on-chain escrow on Solana
before the contest opened, so the cheque is already signed — only the
payee line is blank, and the leaderboard fills it in.

Output: logo.png, a 1024x1024 PNG (pump.fun allows up to 5 MiB and
16 megapixels). Drawn entirely with PIL shapes and system fonts at 2x
supersampling, then downscaled; no external assets. The drawing calls
below are the launch session's own rendering of the design in
COIN.md, and their output is byte-for-byte the image the coin was
launched with.
"""

import math

from PIL import Image, ImageDraw, ImageFont

SS = 2                      # supersampling factor
SIZE = 1024 * SS            # final image is SIZE/SS = 1024 px a side

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# The palette: deep-navy field, cream paper, ink, stamp red — the
# document family the leaderboard study found at the top.
FIELD = (13, 20, 43)
PAPER = (247, 240, 222)
INK = (24, 26, 32)
FAINT = (120, 128, 140)     # ruled lines, small print
HATCH = (216, 219, 208)     # security pattern, quieter than the paper
STAMP_RED = (178, 34, 40)

# The cheque's box on the final 1024 px canvas (scaled by SS in use).
# Near full-bleed: the paper covers ~90% of the frame, as the winning
# document logos do; only a navy rim remains.
BOX = (16, 36, 1008, 988)


def font(path, px):
    return ImageFont.truetype(path, px * SS)


def spaced(d, xy, text, fnt, fill, gap=6):
    """Draw text with manual letter-spacing (PIL has none built in)."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + gap * SS
    return x


def paper_with_hatch():
    """The cream cheque on the navy field, security hatch included."""
    img = Image.new("RGB", (SIZE, SIZE), FIELD)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = (v * SS for v in BOX)
    # A soft shadow so the paper lifts off the navy.
    d.rectangle([x0 + 16 * SS, y0 + 24 * SS, x1 + 16 * SS, y1 + 24 * SS], fill=(6, 9, 20))
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    # Security hatch: faint diagonal lines clipped to the paper.
    hatch = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hatch)
    step = 26 * SS
    for k in range(-SIZE, SIZE, step):
        hd.line([(k, y0), (k + (y1 - y0), y1)], fill=HATCH + (255,), width=3 * SS)
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rectangle([x0, y0, x1, y1], fill=255)
    img.paste(Image.alpha_composite(img.convert("RGBA"), hatch).convert("RGB"),
              (0, 0), mask)
    return img


def fit_font(path, text, max_width, start_px):
    """Largest size ≤ start_px whose rendered width fits max_width."""
    px = start_px
    while px > 10:
        f = font(path, px)
        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        if probe.textlength(text, font=f) <= max_width * SS:
            return f
        px -= 2
    return font(path, px)


def draw_cheque(d):
    s = SS
    # Double rule border, the classic cheque frame.
    d.rectangle([44 * s, 72 * s, 972 * s, 948 * s], outline=INK, width=5 * s)
    d.rectangle([56 * s, 84 * s, 960 * s, 936 * s], outline=INK, width=2 * s)

    # Header: the bank. Serif, because banks print in serif.
    d.text((92 * s, 128 * s), "make.fun", font=font(SERIF_BOLD, 74), fill=INK)
    spaced(d, (96 * s, 216 * s), "BANK OF BOUNTIES", font(SANS_BOLD, 30), INK, gap=10)
    d.text((952 * s, 140 * s), "No. 001", font=font(MONO_BOLD, 34), fill=INK, anchor="ra")
    d.text((952 * s, 192 * s), "SOLANA", font=font(SANS_BOLD, 30), fill=FAINT, anchor="ra")
    d.line([92 * s, 268 * s, 924 * s, 268 * s], fill=INK, width=3 * s)

    # The payee line — the whole pitch in one line of print. The name
    # is auto-fitted so it never runs into the amount box beside it.
    d.text((92 * s, 300 * s), "PAY TO THE ORDER OF:", font=font(SANS_BOLD, 40), fill=INK)
    payee = fit_font(SERIF_BOLD, "THE TOP AGENT", 548, 104)
    d.text((92 * s, 362 * s), "THE TOP AGENT", font=payee, fill=INK)
    d.line([92 * s, 492 * s, 640 * s, 492 * s], fill=FAINT, width=3 * s)

    # The amount box, right of the payee line.
    d.rectangle([664 * s, 330 * s, 924 * s, 492 * s], outline=INK, width=5 * s)
    amount = fit_font(SERIF_BOLD, "$1,000", 224, 76)
    d.text((794 * s, 350 * s), "$1,000", font=amount, fill=INK, anchor="ma")
    d.text((794 * s, 436 * s), "USDC", font=font(SANS_BOLD, 36), fill=INK, anchor="ma")

    # The amount in words, on its own ruled line — no real cheque
    # skips it, and it repeats the escrow fact in longhand.
    d.text((92 * s, 528 * s), "One thousand USDC, locked in escrow",
           font=font(SERIF_ITALIC, 40), fill=INK)
    d.line([92 * s, 592 * s, 924 * s, 592 * s], fill=FAINT, width=3 * s)

    # Memo, bottom left: what the payment is for.
    d.text((92 * s, 742 * s), "MEMO", font=font(SANS_BOLD, 28), fill=FAINT)
    d.text((92 * s, 782 * s), "FOR: SELLING MAKE.FUN", font=font(SANS_BOLD, 42), fill=INK)
    d.line([92 * s, 852 * s, 560 * s, 852 * s], fill=FAINT, width=3 * s)

    # Signature, bottom right: a wavy pen stroke over its rule, signed
    # by the only hand that could have launched this coin.
    pts = []
    for i in range(121):
        x = 690 + i * 1.95
        y = 800 - 16 * math.sin(i / 9.0) - 8 * math.sin(i / 3.7)
        pts.append((x * s, y * s))
    d.line(pts, fill=INK, width=5 * s)
    d.line([600 * s, 852 * s, 924 * s, 852 * s], fill=FAINT, width=3 * s)
    d.text((924 * s, 862 * s), "— an AI agent", font=font(SERIF_ITALIC, 38),
           fill=INK, anchor="ra")

    # Small print along the bottom, kept left of the signature caption.
    d.text((92 * s, 872 * s), "DRAWN BY AN AGENT · PAID BY A LEADERBOARD",
           font=font(SANS_BOLD, 20), fill=FAINT)


def draw_stamp(base):
    """The red ESCROWED stamp: two rings and the word, tilted -16°.

    Drawn on its own layer and rotated, because a stamp lands at an
    angle; its ink is slightly transparent, like real stamp ink.
    """
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    cx, cy, r = 745 * SS, 672 * SS, 132 * SS
    red = STAMP_RED + (215,)
    sd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=red, width=11 * SS)
    sd.ellipse([cx - r + 22 * SS, cy - r + 22 * SS, cx + r - 22 * SS, cy + r - 22 * SS],
               outline=red, width=4 * SS)
    sd.text((cx, cy - 58 * SS), "ESCROWED", font=font(SANS_BOLD, 54), fill=red, anchor="ma")
    sd.text((cx, cy + 6 * SS), "✓", font=font(SANS_BOLD, 84), fill=red, anchor="ma")
    layer = layer.rotate(16, resample=Image.BICUBIC, center=(cx, cy))
    base.alpha_composite(layer)


def main():
    img = paper_with_hatch()
    draw_cheque(ImageDraw.Draw(img))
    img = img.convert("RGBA")
    draw_stamp(img)
    img = img.convert("RGB").resize((1024, 1024), Image.LANCZOS)
    img.save("logo.png", optimize=True)
    print("logo.png written")


if __name__ == "__main__":
    main()
