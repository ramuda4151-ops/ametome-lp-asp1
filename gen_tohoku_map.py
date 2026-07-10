#!/usr/bin/env python3
# 東北地方の地図をSVGで生成するスクリプト（gen_kanto_map.pyと同スタイル / lp3用）

import os

svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 460" width="500" height="460">
  <defs>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="rgba(0,0,0,0.3)"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="500" height="460" fill="#e8f4ff" rx="12"/>

  <!-- 海 -->
  <rect width="500" height="460" fill="#b8d8f0" rx="12"/>

  <!-- 陸地ベース（東北周辺） -->
  <ellipse cx="250" cy="215" rx="205" ry="200" fill="#e8e8d0"/>

  <!-- 北海道（薄め） -->
  <polygon points="150,15 380,10 395,50 160,55"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="275" y="40" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">北海道</text>

  <!-- 青森県 -->
  <polygon points="135,70 250,60 365,70 370,115 300,105 250,125 200,105 130,115"
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="250" y="95" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">青森県</text>

  <!-- 秋田県 -->
  <polygon points="130,115 200,105 250,125 245,215 165,225 120,190"
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="185" y="172" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">秋田県</text>

  <!-- 岩手県 -->
  <polygon points="250,125 300,105 370,115 380,200 355,235 250,230 245,215"
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="312" y="178" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">岩手県</text>

  <!-- 山形県 -->
  <polygon points="120,190 165,225 245,215 240,295 225,310 150,315 110,265"
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="180" y="268" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">山形県</text>

  <!-- 宮城県 -->
  <polygon points="245,215 250,230 355,235 360,290 300,310 240,295"
           fill="#004c8c" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="300" y="270" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">宮城県</text>

  <!-- 福島県 -->
  <polygon points="150,315 225,310 240,295 300,310 360,290 385,330 370,375 220,385 135,360"
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="260" y="345" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">福島県</text>

  <!-- 新潟県（薄め） -->
  <polygon points="70,280 110,265 150,315 135,360 100,380 60,340 55,305"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="100" y="328" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">新潟県</text>

  <!-- 関東（薄め） -->
  <polygon points="135,360 220,385 370,375 375,403 145,400"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="262" y="396" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">関東</text>

  <!-- 東北エリア強調の枠線 -->
  <polygon points="135,70 250,60 365,70 370,115 380,200 355,235 360,290 385,330 370,375 220,385 135,360 150,315 110,265 120,190 130,115"
           fill="none" stroke="#ff6b00" stroke-width="3" stroke-dasharray="8,4" opacity="0.8"/>

  <!-- タイトル -->
  <rect x="10" y="412" width="480" height="38" fill="rgba(0,76,140,0.85)" rx="6"/>
  <text x="250" y="436" font-family="Noto Sans JP, sans-serif" font-size="15" font-weight="bold" fill="white" text-anchor="middle">東北地方全域対応！近隣エリアもご相談ください</text>
</svg>'''

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'map_tohoku.svg')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("東北地図SVG生成完了: " + out_path)
