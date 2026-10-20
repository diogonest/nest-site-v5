import os, collections, math
from vectorizer import decode_png, trace_mask_to_loops, loops_to_path_d

UPLOADS = "/Users/diogooliveirasantos/.gemini/antigravity/brain/84b2eeb3-c6f4-43ff-8f65-a7640df5e7eb/.user_uploaded"
IMG_DIR = "/Users/diogooliveirasantos/Downloads/JOBS/DIOGO NEST/Nest-site-v5/img"

def vectorize_logo(in_path, out_svg_path, colors_spec, pad=16, epsilon=1.0):
    w, h, recon = decode_png(in_path)
    
    # Global bounding box of non-background content
    min_x, max_x, min_y, max_y = w, 0, h, 0
    for y in range(h):
        for x in range(w):
            idx = (y * w + x) * 4
            r, g, b, a = recon[idx:idx+4]
            if a < 30 or (r > 242 and g > 242 and b > 242):
                continue
            min_x = min(min_x, x); max_x = max(max_x, x)
            min_y = min(min_y, y); max_y = max(max_y, y)

    crop_x1 = max(0, min_x - pad)
    crop_y1 = max(0, min_y - pad)
    crop_x2 = min(w, max_x + 1 + pad)
    crop_y2 = min(h, max_y + 1 + pad)
    cw = crop_x2 - crop_x1
    ch = crop_y2 - crop_y1

    svg_paths = []
    for name, hex_fill, match_fn in colors_spec:
        mask = []
        for y in range(crop_y1, crop_y2):
            row = []
            for x in range(crop_x1, crop_x2):
                idx = (y * w + x) * 4
                r, g, b, a = recon[idx:idx+4]
                row.append(match_fn(r, g, b, a))
            mask.append(row)
        
        loops = trace_mask_to_loops(mask, cw, ch)
        path_d = loops_to_path_d(loops, epsilon=epsilon, offset_x=0, offset_y=0)
        if path_d:
            svg_paths.append(f'<path fill="{hex_fill}" fill-rule="evenodd" d="{path_d}"/>')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {ch}" width="{cw}" height="{ch}">
  {' '.join(svg_paths)}
</svg>'''
    with open(out_svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[SVG] {os.path.basename(out_svg_path)}: {cw}x{ch}, {os.path.getsize(out_svg_path)} bytes")

# 1. Vargas: dark text, red face, orange face
def vargas():
    in_p = f"{UPLOADS}/media_1792434196755.png"
    def is_text(r, g, b, a):
        return a > 40 and r < 80 and g < 80 and b < 80 and not (r > 240 and g > 240 and b > 240)
    def is_orange(r, g, b, a):
        return a > 40 and r > 180 and g > 60 and g < 150 and b < 90
    def is_red(r, g, b, a):
        return a > 40 and r > 120 and g < 65 and b < 65 and not is_text(r, g, b, a)
    colors = [
        ("dark", "#333333", is_text),
        ("orange", "#F15A24", is_orange),
        ("red", "#B83232", is_red),
    ]
    vectorize_logo(in_p, f"{IMG_DIR}/logo-vargas.svg", colors, pad=16, epsilon=1.0)

# 2. Prime: black text/contour, bright red, dark red
def prime():
    in_p = f"{UPLOADS}/media_1792433261498.png"
    def is_black(r, g, b, a):
        return a > 40 and r < 60 and g < 60 and b < 60
    def is_bright_red(r, g, b, a):
        return a > 40 and r > 180 and g < 40 and b < 40
    def is_dark_red(r, g, b, a):
        return a > 40 and r >= 100 and r <= 180 and g < 40 and b < 40
    colors = [
        ("black", "#000000", is_black),
        ("bright_red", "#ED1C24", is_bright_red),
        ("dark_red", "#B81414", is_dark_red),
    ]
    vectorize_logo(in_p, f"{IMG_DIR}/logo-prime.svg", colors, pad=16, epsilon=1.0)

# 3. Habitar: black text, cyan icon and subtitle
def habitar():
    in_p = f"{UPLOADS}/media_1792433278336.png"
    def is_black(r, g, b, a):
        return a > 40 and r < 60 and g < 60 and b < 60 and not (r > 240 and g > 240 and b > 240)
    def is_cyan(r, g, b, a):
        return a > 40 and r < 80 and g > 80 and b > 120 and not (r > 240 and g > 240 and b > 240)
    colors = [
        ("black", "#0E0E0E", is_black),
        ("cyan", "#0088A8", is_cyan),
    ]
    vectorize_logo(in_p, f"{IMG_DIR}/logo-habitar.svg", colors, pad=16, epsilon=1.0)

# 4. Solydus: black text, grey text, light green, dark green
def solydus():
    in_p = f"{UPLOADS}/media_1792433288615.png"
    def is_black(r, g, b, a):
        return a > 40 and r < 50 and g < 50 and b < 50
    def is_grey(r, g, b, a):
        return a > 40 and abs(r - g) < 20 and abs(g - b) < 20 and r >= 100 and r <= 160
    def is_light_green(r, g, b, a):
        return a > 40 and g > 130 and g > r and g > b
    def is_dark_green(r, g, b, a):
        return a > 40 and g >= 70 and g <= 130 and g > r and g > b and not is_black(r, g, b, a)
    colors = [
        ("black", "#0A0A0A", is_black),
        ("grey", "#7D8285", is_grey),
        ("light_green", "#3CA837", is_light_green),
        ("dark_green", "#007A33", is_dark_green),
    ]
    vectorize_logo(in_p, f"{IMG_DIR}/logo-solydus.svg", colors, pad=16, epsilon=1.0)

# 5. My Home: dark teal bird and text
def myhome():
    in_p = f"{UPLOADS}/media_1792433353841.png"
    def is_teal(r, g, b, a):
        return a > 40 and r < 120 and g < 130 and b < 130 and not (r > 230 and g > 230 and b > 230)
    colors = [
        ("teal", "#2C4C48", is_teal),
    ]
    vectorize_logo(in_p, f"{IMG_DIR}/logo-myhome.svg", colors, pad=16, epsilon=1.0)

if __name__ == "__main__":
    vargas()
    prime()
    habitar()
    solydus()
    myhome()
    print("All 5 logos vectorized.")
