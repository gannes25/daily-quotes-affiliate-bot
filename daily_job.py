import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import os

# === CONFIG ===
AFFILIATE_LINKS = [
    "https://www.amazon.in/dp/0143453609?tag=your-amazon-id",
    "https://www.flipkart.com/book/p/itmflipkartaffid",
    "https://www.amazon.in/dp/067009711X?tag=your-amazon-id",
    "https://www.flipkart.com/another-product/p/flipkartaffid"
]
AFFILIATE_URL = random.choice(AFFILIATE_LINKS)

FONT_PATH = "assets/fonts/OpenSans-Bold.ttf"
OUTPUT_DIR = "images"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# === FUNCTION: Get a Daily Quote from API ===
def get_quote():
    try:
        res = requests.get("https://zenquotes.io/api/random")
        if res.status_code == 200:
            data = res.json()[0]
            return f"{data['q']} — {data['a']}"
        else:
            return "Stay positive. Work hard. Make it happen. — Anonymous"
    except:
        return "Stay positive. Work hard. Make it happen. — Anonymous"


# === FUNCTION: Create Image ===
def generate_image(quote_text):
    img = Image.new("RGB", (1080, 1080), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    quote_font = ImageFont.truetype(FONT_PATH, 38)
    affiliate_font = ImageFont.truetype(FONT_PATH, 24)

    # Word wrapping
    lines = []
    words = quote_text.split()
    line = ""
    for word in words:
        if draw.textlength(line + word, font=quote_font) < 900:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())

    y_text = 300
    for line in lines:
        draw.text((80, y_text), line, font=quote_font, fill="black")
        y_text += 60

    # Affiliate link
    draw.text((80, 1000), f"Buy Now 👉 {AFFILIATE_URL}", font=affiliate_font, fill="blue")

    filename = os.path.join(OUTPUT_DIR, f"quote_{datetime.now().strftime('%Y%m%d')}.png")
    img.save(filename)
    print(f"✅ Image saved: {filename}")


# === RUN ===
quote = get_quote()
generate_image(quote)
