#!/usr/bin/env python3
"""
日本地図SVGを生成する（関東地方を強調表示）
"""

svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
  <defs>
    <style>
      .japan-base { fill: #c8dff0; stroke: #7ab0d0; stroke-width: 0.8; }
      .kanto { fill: #004c8c; stroke: #002a5e; stroke-width: 1.2; }
      .kanto-label { fill: white; font-family: "Noto Sans JP", sans-serif; font-size: 11px; font-weight: bold; text-anchor: middle; }
      .region-label { fill: #555; font-family: "Noto Sans JP", sans-serif; font-size: 9px; text-anchor: middle; }
      .pref-label { fill: white; font-family: "Noto Sans JP", sans-serif; font-size: 7px; text-anchor: middle; }
      .note-text { fill: #004c8c; font-family: "Noto Sans JP", sans-serif; font-size: 11px; font-weight: bold; text-anchor: middle; }
      .note-sub { fill: #555; font-family: "Noto Sans JP", sans-serif; font-size: 9px; text-anchor: middle; }
    </style>
    <!-- 関東ハイライト用グロー -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="400" height="500" fill="#e8f4fd" rx="12"/>

  <!-- ===== 日本列島（簡略化シルエット） ===== -->

  <!-- 北海道 -->
  <path class="japan-base" d="M 240 30 L 270 25 L 310 35 L 330 50 L 320 70 L 295 80 L 270 75 L 250 65 L 235 50 Z"/>
  <!-- 北海道 東部 -->
  <path class="japan-base" d="M 310 35 L 340 30 L 355 45 L 345 60 L 325 65 L 310 55 Z"/>

  <!-- 東北 -->
  <path class="japan-base" d="M 265 85 L 285 82 L 300 90 L 305 110 L 300 130 L 285 140 L 270 135 L 258 120 L 255 100 Z"/>

  <!-- ===== 関東（強調） ===== -->
  <!-- 茨城 -->
  <path class="kanto" d="M 295 145 L 315 140 L 325 155 L 320 175 L 305 180 L 290 170 L 285 155 Z" filter="url(#glow)"/>
  <!-- 栃木 -->
  <path class="kanto" d="M 270 140 L 290 138 L 295 155 L 285 170 L 268 168 L 260 155 L 262 143 Z" filter="url(#glow)"/>
  <!-- 群馬 -->
  <path class="kanto" d="M 248 140 L 268 138 L 270 155 L 262 168 L 245 165 L 238 152 L 240 142 Z" filter="url(#glow)"/>
  <!-- 埼玉 -->
  <path class="kanto" d="M 252 170 L 270 168 L 285 170 L 288 185 L 278 195 L 258 193 L 248 182 Z" filter="url(#glow)"/>
  <!-- 千葉 -->
  <path class="kanto" d="M 295 175 L 320 175 L 335 185 L 338 205 L 325 220 L 308 225 L 295 215 L 290 198 L 290 182 Z" filter="url(#glow)"/>
  <!-- 東京 -->
  <path class="kanto" d="M 258 193 L 278 193 L 288 200 L 285 215 L 268 218 L 252 210 L 250 198 Z" filter="url(#glow)"/>
  <!-- 神奈川 -->
  <path class="kanto" d="M 250 215 L 270 218 L 290 215 L 295 230 L 280 242 L 258 240 L 245 228 Z" filter="url(#glow)"/>
  <!-- 山梨（関東近隣） -->
  <path class="kanto" d="M 225 195 L 248 192 L 252 210 L 245 228 L 228 225 L 218 210 L 220 198 Z" filter="url(#glow)"/>

  <!-- 関東ラベル -->
  <text class="kanto-label" x="284" y="192">関東エリア</text>
  <text class="kanto-label" x="284" y="205">対応中！</text>

  <!-- 都道府県ラベル -->
  <text class="pref-label" x="307" y="163">茨城</text>
  <text class="pref-label" x="277" y="156">栃木</text>
  <text class="pref-label" x="254" y="155">群馬</text>
  <text class="pref-label" x="268" y="184">埼玉</text>
  <text class="pref-label" x="313" y="200">千葉</text>
  <text class="pref-label" x="268" y="210">東京</text>
  <text class="pref-label" x="268" y="232">神奈川</text>
  <text class="pref-label" x="234" y="213">山梨</text>

  <!-- ===== 中部・東海 ===== -->
  <path class="japan-base" d="M 220 200 L 238 198 L 240 215 L 228 228 L 210 230 L 198 218 L 200 205 Z"/>
  <path class="japan-base" d="M 195 220 L 210 215 L 225 228 L 220 245 L 205 250 L 190 240 L 188 228 Z"/>
  <path class="japan-base" d="M 175 235 L 195 230 L 205 245 L 198 262 L 180 265 L 165 255 L 162 242 Z"/>

  <!-- 長野 -->
  <path class="japan-base" d="M 200 165 L 225 162 L 235 178 L 228 198 L 210 200 L 195 190 L 193 175 Z"/>

  <!-- 新潟 -->
  <path class="japan-base" d="M 200 130 L 230 125 L 248 138 L 242 155 L 225 160 L 205 158 L 195 145 Z"/>

  <!-- ===== 近畿 ===== -->
  <path class="japan-base" d="M 148 255 L 168 250 L 178 265 L 172 282 L 155 285 L 140 275 L 138 262 Z"/>
  <path class="japan-base" d="M 128 265 L 148 260 L 155 278 L 148 295 L 130 298 L 115 288 L 112 273 Z"/>
  <path class="japan-base" d="M 110 275 L 130 270 L 138 285 L 130 302 L 112 305 L 98 295 L 95 280 Z"/>

  <!-- ===== 中国地方 ===== -->
  <path class="japan-base" d="M 80 285 L 110 280 L 115 295 L 105 312 L 85 315 L 68 305 L 65 292 Z"/>
  <path class="japan-base" d="M 55 295 L 78 290 L 85 305 L 78 322 L 58 325 L 42 315 L 40 300 Z"/>

  <!-- ===== 四国 ===== -->
  <path class="japan-base" d="M 100 320 L 130 315 L 148 325 L 145 345 L 125 352 L 100 348 L 85 338 L 85 325 Z"/>

  <!-- ===== 九州 ===== -->
  <path class="japan-base" d="M 50 315 L 78 310 L 88 325 L 82 345 L 62 355 L 40 350 L 28 335 L 30 320 Z"/>
  <!-- 九州南部 -->
  <path class="japan-base" d="M 38 348 L 62 352 L 68 370 L 55 385 L 35 382 L 22 368 L 25 352 Z"/>

  <!-- 沖縄（小さく） -->
  <ellipse class="japan-base" cx="60" cy="430" rx="18" ry="8"/>
  <ellipse class="japan-base" cx="38" cy="445" rx="10" ry="5"/>

  <!-- ===== 地方ラベル ===== -->
  <text class="region-label" x="285" y="60">北海道</text>
  <text class="region-label" x="283" y="115">東北</text>
  <text class="region-label" x="210" y="175">中部</text>
  <text class="region-label" x="138" y="280">近畿</text>
  <text class="region-label" x="78" y="300">中国</text>
  <text class="region-label" x="115" y="338">四国</text>
  <text class="region-label" x="55" y="338">九州</text>
  <text class="region-label" x="58" y="445">沖縄</text>

  <!-- ===== 注記テキスト ===== -->
  <text class="note-text" x="200" y="470">関東エリアを中心に対応中</text>
  <text class="note-sub" x="200" y="486">関東近隣の方もご相談ください</text>

  <!-- 関東エリア強調の枠線 -->
  <ellipse cx="280" cy="190" rx="70" ry="65" fill="none" stroke="#ff6600" stroke-width="2.5" stroke-dasharray="6,3" opacity="0.8"/>
</svg>'''

with open('/home/ubuntu/ametome-lp/img/map_japan.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("SVG map generated successfully!")
