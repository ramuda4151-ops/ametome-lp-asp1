#!/usr/bin/env python3
# 福岡県周辺（北部九州）の地図をSVGで生成するスクリプト（gen_tohoku_map.pyと同スタイル / lp4用）

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

  <!-- 陸地ベース（九州周辺） -->
  <ellipse cx="235" cy="250" rx="200" ry="185" fill="#e8e8d0"/>

  <!-- 山口県（薄め・本州側） -->
  <polygon points="300,20 470,15 480,60 320,70"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="395" y="47" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">山口県</text>

  <!-- 福岡県（対応エリア・強調） -->
  <polygon points="160,120 230,95 310,105 345,140 330,185 280,210 210,215 150,185 140,150"
           fill="#004c8c" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="243" y="160" font-family="Noto Sans JP, sans-serif" font-size="15" font-weight="bold" fill="white" text-anchor="middle">福岡県</text>

  <!-- 佐賀県（薄め） -->
  <polygon points="140,150 150,185 210,215 195,255 120,250 95,200"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="152" y="222" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">佐賀県</text>

  <!-- 長崎県（薄め） -->
  <polygon points="95,200 120,250 110,290 55,295 35,245 60,210"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="78" y="258" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">長崎県</text>

  <!-- 大分県（薄め） -->
  <polygon points="330,185 345,140 420,150 440,220 400,265 335,250 320,215"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="382" y="207" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">大分県</text>

  <!-- 熊本県（薄め） -->
  <polygon points="195,255 280,210 320,215 335,250 320,320 240,345 180,320 175,280"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="255" y="290" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">熊本県</text>

  <!-- 宮崎県（薄め） -->
  <polygon points="335,250 400,265 395,350 330,385 320,320"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="360" y="315" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">宮崎県</text>

  <!-- 鹿児島県（薄め） -->
  <polygon points="180,320 240,345 320,320 330,385 250,410 175,385"
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="252" y="378" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">鹿児島県</text>

  <!-- 福岡県強調の枠線 -->
  <polygon points="160,120 230,95 310,105 345,140 330,185 280,210 210,215 150,185 140,150"
           fill="none" stroke="#ff6b00" stroke-width="3" stroke-dasharray="8,4" opacity="0.8"/>

  <!-- タイトル -->
  <rect x="10" y="412" width="480" height="38" fill="rgba(0,76,140,0.85)" rx="6"/>
  <text x="250" y="436" font-family="Noto Sans JP, sans-serif" font-size="15" font-weight="bold" fill="white" text-anchor="middle">福岡県全域対応！近隣エリアもご相談ください</text>
</svg>'''

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'map_fukuoka.svg')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("福岡地図SVG生成完了: " + out_path)
