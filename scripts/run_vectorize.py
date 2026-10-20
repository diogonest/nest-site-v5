import os, collections, math
from vectorizer import decode_png, trace_mask_to_loops, loops_to_path_d

def vectorize_logo(in_path, out_svg_path, colors_spec, pad=20, epsilon=1.2):
    # colors_spec is a list of (color_name, hex_color, match_func)
    w, h, recon = decode_png(in_path)
    
    # First find global bounding box of all content
    min_x, max_x, min_y, max_y = w, 0, h, 0
    for y in range(h):
        for x in range(w):
            idx = (y * w + x) * 4
            r, g, b, a = recon[idx:idx+4]
            if a < 30 or (r > 245 and g > 245 and b > 245):
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
        # build mask for cropped region
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
    print(f"Generated {out_svg_path} ({cw}x{ch}, {len(svg_paths)} paths, size={os.path.getsize(out_svg_path)} bytes)")

print("run_vectorize.py ready.")
