import os
import math
from PIL import Image, ImageDraw, ImageFilter

SRC_PATH = r"C:\Users\Vivek Chaurasiya\.gemini\antigravity\brain\a5c74d64-3f55-4531-bfee-ffbe3300e046\student_saarthi_logo_mark_1794556039245.jpg"
OUT_DIR = r"D:\Student Saarthi\static\images\logo"
STATIC_DIR = r"D:\Student Saarthi\static"

os.makedirs(OUT_DIR, exist_ok=True)

img = Image.open(SRC_PATH).convert("RGBA")
width, height = img.size

# 1. Create transparent background version of the emblem
# Background is dark navy (~ [0, 15, 40])
transparent_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
pixels = img.load()
trans_pixels = transparent_img.load()

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        # Calculate brightness / distance from dark navy
        # Background color around (3, 16, 42)
        bg_dist = math.sqrt((r - 3)**2 + (g - 16)**2 + (b - 42)**2)
        
        # Max brightness
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        
        if bg_dist < 28 and lum < 26:
            # Completely background
            trans_pixels[x, y] = (0, 0, 0, 0)
        elif bg_dist < 60 and lum < 45:
            # Transition edge - smooth feather
            alpha = int(255 * ((bg_dist - 28) / (60 - 28)))
            trans_pixels[x, y] = (r, g, b, max(0, min(255, alpha)))
        else:
            trans_pixels[x, y] = (r, g, b, 255)

# Save transparent version
trans_path = os.path.join(OUT_DIR, "logo-mark-transparent.png")
transparent_img.save(trans_path, "PNG")
print(f"Saved: {trans_path}")

# 2. Save full square emblem (for app icons and rich previews)
square_path = os.path.join(OUT_DIR, "logo-mark.png")
img.save(square_path, "PNG")
print(f"Saved: {square_path}")

# 3. Create a modern squircle/app-icon version (with sleek rounded corners)
app_icon = img.resize((512, 512), Image.Resampling.LANCZOS)
mask = Image.new("L", (512, 512), 0)
draw = ImageDraw.Draw(mask)
draw.rounded_rectangle([(0, 0), (512, 512)], radius=110, fill=255)

app_icon_rounded = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
app_icon_rounded.paste(app_icon, (0, 0), mask=mask)

app_icon_path = os.path.join(OUT_DIR, "logo-512.png")
app_icon_rounded.save(app_icon_path, "PNG")
print(f"Saved: {app_icon_path}")

# 4. Apple Touch Icon (180x180)
apple_touch = img.resize((180, 180), Image.Resampling.LANCZOS)
apple_touch_path = os.path.join(OUT_DIR, "apple-touch-icon.png")
apple_touch.save(apple_touch_path, "PNG")
print(f"Saved: {apple_touch_path}")

# 5. Favicon PNGs
fav_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
fav_32_path = os.path.join(OUT_DIR, "favicon-32x32.png")
fav_32.save(fav_32_path, "PNG")
print(f"Saved: {fav_32_path}")

fav_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
fav_16_path = os.path.join(OUT_DIR, "favicon-16x16.png")
fav_16.save(fav_16_path, "PNG")
print(f"Saved: {fav_16_path}")

# 6. Generate multi-resolution favicon.ico
ico_path_static = os.path.join(STATIC_DIR, "favicon.ico")
ico_path_logo = os.path.join(OUT_DIR, "favicon.ico")

# Using the high-res image to create crisp icons at 16, 32, 48, 64
img.save(
    ico_path_static,
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
)
img.save(
    ico_path_logo,
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
)
print(f"Saved: {ico_path_static}")
print(f"Saved: {ico_path_logo}")

print("All raster logo assets successfully generated!")
