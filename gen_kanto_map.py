#!/usr/bin/env python3
# 関東地方の地図をSVGで生成するスクリプト

svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 420" width="500" height="420">
  <defs>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="rgba(0,0,0,0.3)"/>
    </filter>
  </defs>
  
  <!-- 背景 -->
  <rect width="500" height="420" fill="#e8f4ff" rx="12"/>
  
  <!-- 海 -->
  <rect width="500" height="420" fill="#b8d8f0" rx="12"/>
  
  <!-- 陸地ベース（関東周辺） -->
  <ellipse cx="250" cy="200" rx="220" ry="180" fill="#e8e8d0"/>

  <!-- 群馬県 -->
  <polygon points="120,80 200,70 220,100 210,140 160,150 120,130" 
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="165" y="115" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">群馬県</text>

  <!-- 栃木県 -->
  <polygon points="200,70 290,65 310,100 300,145 220,140 210,100" 
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="255" y="108" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">栃木県</text>

  <!-- 茨城県 -->
  <polygon points="290,65 370,75 390,120 370,180 320,195 300,145 310,100" 
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="340" y="135" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">茨城県</text>

  <!-- 埼玉県 -->
  <polygon points="160,150 210,140 220,140 300,145 290,185 240,200 190,195 155,185" 
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="228" y="172" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">埼玉県</text>

  <!-- 千葉県 -->
  <polygon points="300,145 320,195 370,180 400,210 390,260 350,300 310,290 280,250 270,210 290,185" 
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="340" y="235" font-family="Noto Sans JP, sans-serif" font-size="13" font-weight="bold" fill="white" text-anchor="middle">千葉県</text>

  <!-- 東京都 -->
  <polygon points="190,195 240,200 270,210 260,240 230,250 195,240 175,220" 
           fill="#004c8c" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="225" y="225" font-family="Noto Sans JP, sans-serif" font-size="12" font-weight="bold" fill="white" text-anchor="middle">東京都</text>

  <!-- 神奈川県 -->
  <polygon points="175,220 195,240 230,250 260,240 265,275 240,295 200,300 165,285 150,260 155,235" 
           fill="#0068b7" stroke="#fff" stroke-width="2" filter="url(#shadow)"/>
  <text x="207" y="268" font-family="Noto Sans JP, sans-serif" font-size="12" font-weight="bold" fill="white" text-anchor="middle">神奈川県</text>

  <!-- 山梨県（薄め） -->
  <polygon points="120,130 160,150 155,185 150,260 120,265 90,240 85,200 95,160" 
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="120" y="205" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">山梨県</text>

  <!-- 長野県（薄め） -->
  <polygon points="60,80 120,80 120,130 95,160 85,200 60,195 40,160 45,120" 
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="80" y="140" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">長野県</text>

  <!-- 静岡県（薄め） -->
  <polygon points="90,240 120,265 150,260 165,285 200,300 240,295 250,330 200,360 150,355 100,330 80,295 75,265" 
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="165" y="330" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">静岡県</text>

  <!-- 福島県（薄め） -->
  <polygon points="120,30 290,20 290,65 200,70 120,80" 
           fill="#7aadcc" stroke="#fff" stroke-width="1.5"/>
  <text x="205" y="50" font-family="Noto Sans JP, sans-serif" font-size="11" fill="white" text-anchor="middle" opacity="0.9">福島県</text>

  <!-- 関東エリア強調の枠線 -->
  <polygon points="120,80 200,70 290,65 310,100 370,75 390,120 370,180 400,210 390,260 350,300 310,290 280,250 265,275 240,295 200,300 165,285 150,260 155,235 175,220 190,195 155,185 160,150 120,130"
           fill="none" stroke="#ff6b00" stroke-width="3" stroke-dasharray="8,4" opacity="0.8"/>

  <!-- タイトル -->
  <rect x="10" y="375" width="480" height="38" fill="rgba(0,76,140,0.85)" rx="6"/>
  <text x="250" y="399" font-family="Noto Sans JP, sans-serif" font-size="15" font-weight="bold" fill="white" text-anchor="middle">関東地方全域対応！近隣エリアもご相談ください</text>
</svg>'''

with open('/home/ubuntu/ametome-lp/img/map_kanto.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("関東地図SVG生成完了")
