from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 1200, 630
FONT_REGULAR = "/System/Library/Fonts/Avenir.ttc"
FONT_MEDIUM = "/System/Library/Fonts/Avenir Next.ttc"


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS
    )
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def fit_trimmed(path: Path, height: int) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    if bounds:
        image = image.crop(bounds)
    width = round(image.width * height / image.height)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def tracking_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    spacing: int,
) -> None:
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        x += round(draw.textlength(char, font=font)) + spacing


background = cover(Image.open(ROOT / "social-preview-background.png").convert("RGB"), (WIDTH, HEIGHT))
canvas = background.convert("RGBA")

# Use the authoritative transparent pouch renders so all package typography stays exact.
# The side pouches rotate away from the centered peach pouch to form a compact fan.
products = [
    ("oreha-grape-transparent.png", 470, 600, 70, 12),
    ("oreha-honey-lemon-transparent.png", 470, 822, 70, -12),
    ("oreha-peach-transparent.png", 460, 782, 58, 0),
]

for filename, height, x, y, angle in products:
    pouch = fit_trimmed(ROOT / filename, height)
    if angle:
        pouch = pouch.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_shape = Image.new("RGBA", pouch.size, (0, 0, 0, 0))
    shadow_shape.putalpha(pouch.getchannel("A"))
    shadow_shape = shadow_shape.filter(ImageFilter.GaussianBlur(18))
    shadow.alpha_composite(shadow_shape, (x + 14, y + 22))
    canvas = Image.alpha_composite(canvas, shadow)
    canvas.alpha_composite(pouch, (x, y))

draw = ImageDraw.Draw(canvas)
brand = ImageFont.truetype(FONT_MEDIUM, 132, index=5)
support = ImageFont.truetype(FONT_REGULAR, 46, index=0)

tracking_text(draw, (42, 132), "OREHA", brand, (246, 246, 243, 255), 13)
draw.text((49, 322), "Japanese performance jelly", font=support, fill=(211, 216, 217, 255))
draw.text((49, 389), "for serious endurance.", font=support, fill=(211, 216, 217, 255))

canvas.convert("RGB").save(ROOT / "social-preview.png", quality=94, optimize=True)
