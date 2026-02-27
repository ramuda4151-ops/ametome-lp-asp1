from PIL import Image
import os

# 480x558の比率でクロップ（縦長に近い正方形に近い比率）
target_w = 480
target_h = 558
target_ratio = target_w / target_h  # 約0.860

files = ['hero_v1.jpg', 'hero_v2.jpg', 'hero_v3.jpg', 'hero_v4.jpg']
img_dir = '/home/ubuntu/ametome-lp/img'

for fname in files:
    path = os.path.join(img_dir, fname)
    img = Image.open(path)
    w, h = img.size
    current_ratio = w / h

    if current_ratio > target_ratio:
        # 横が長すぎる → 高さ基準でクロップ
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # 縦が長すぎる → 幅基準でクロップ
        new_h = int(w / target_ratio)
        top = 0  # 上から切る（人物の頭を残す）
        img = img.crop((0, top, w, top + new_h))

    # 960x1116にリサイズ（2倍解像度）
    img = img.resize((960, 1116), Image.LANCZOS)
    out_path = os.path.join(img_dir, fname.replace('.jpg', '_resized.jpg'))
    img.save(out_path, 'JPEG', quality=90)
    print(f"{fname}: {img.size} -> saved to {out_path}")
