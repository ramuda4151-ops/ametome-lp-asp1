#!/usr/bin/env python3
"""
lp1/build.py
マスターHTML（lp1/index.html）をベースに、各ASPディレクトリのindex.htmlを生成するスクリプト。
JSONの内容をビルド時に直接<head>に焼き込むため、実行時のJSONフェッチが不要。

使い方:
  cd /home/ubuntu/ametome-lp-asp1/lp1
  python3 build.py

マスター（lp1/index.html）を修正したら、このスクリプトを実行して
git add . && git commit && git push するだけで全ASPに反映される。
"""

import os
import re
import json

MASTER_PATH = os.path.join(os.path.dirname(__file__), 'index.html')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ASP_DIRS = ['a', 'b']  # 追加するASPはここに追記するだけ

def build_call_tracking_scripts_html(scripts):
    """call_tracking_scriptsリストからHTMLの<script>タグ群を生成する"""
    lines = []
    for s in scripts:
        if s.get('type') == 'inline':
            lines.append(f'  <script>{s["content"]}</script>')
        elif s.get('type') == 'src':
            async_attr = ' async' if s.get('async') else ''
            lines.append(f'  <script src="{s["src"]}"{async_attr}></script>')
    return '\n'.join(lines)

def build_tel_mode_script(config):
    """tel_modeに応じた電話リンク書き換えスクリプトを生成する"""
    tel_raw = config.get('tel_raw', '01200940956')
    mode = config.get('tel_mode', 'plain')

    if mode == 'plain':
        return f"""  <script>
  document.addEventListener('DOMContentLoaded', function() {{
    document.querySelectorAll('.lp-tel-link').forEach(function(el) {{
      if (el.tagName === 'A') el.href = 'tel:{tel_raw}';
    }});
  }});
  </script>"""
    elif mode == 'fmcall':
        return f"""  <script>
  document.addEventListener('DOMContentLoaded', function() {{
    document.querySelectorAll('.lp-tel-link').forEach(function(el) {{
      if (el.tagName === 'A') el.href = 'tel:{tel_raw}';
    }});
  }});
  </script>"""
    elif mode == 'ct3':
        return f"""  <script>
  document.addEventListener('DOMContentLoaded', function() {{
    document.querySelectorAll('.lp-tel-link').forEach(function(el) {{
      if (el.tagName === 'A') {{
        el.href = 'tel:{tel_raw}';
        el.classList.add('telno');
      }}
    }});
  }});
  </script>"""
    return ''

def build_asp(asp_key, master_html, config):
    """マスターHTMLからASP別HTMLを生成する（JSON焼き込み方式）"""
    html = master_html

    # コールトラッキングスクリプトのHTMLを生成
    ct_scripts_html = build_call_tracking_scripts_html(
        config.get('call_tracking_scripts', [])
    )

    # tel_modeスクリプトを生成
    tel_mode_script = build_tel_mode_script(config)

    # window.__LP_CONFIG__をインラインで設定（GASフォーム送信等で参照するため残す）
    config_json = json.dumps(config, ensure_ascii=False)

    # LP設定ローダー全体をビルド時焼き込み版に置き換え
    loader_pattern = r'<!-- LP設定ローダー.*?<!-- End LP設定ローダー -->'
    fixed_loader = f"""  <!-- LP設定ローダー（ASP: {asp_key}） -->
  <script>window.__LP_CONFIG__ = {config_json};</script>
{ct_scripts_html}
{tel_mode_script}
  <!-- End LP設定ローダー -->"""

    html = re.sub(loader_pattern, fixed_loader, html, flags=re.DOTALL)

    return html

def main():
    with open(MASTER_PATH, 'r', encoding='utf-8') as f:
        master_html = f.read()

    base_dir = os.path.dirname(MASTER_PATH)

    for asp_key in ASP_DIRS:
        # JSONを読み込む
        json_path = os.path.join(DATA_DIR, f'{asp_key}.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        asp_dir = os.path.join(base_dir, asp_key)
        os.makedirs(asp_dir, exist_ok=True)
        output_path = os.path.join(asp_dir, 'index.html')

        built_html = build_asp(asp_key, master_html, config)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(built_html)

        print(f"✓ {asp_key}/index.html を生成しました ({len(built_html)} bytes)")

    print("\nビルド完了！次のコマンドでデプロイしてください:")
    print("  cd /home/ubuntu/ametome-lp-asp1")
    print("  git add lp1/ && git commit -m 'build: ASP別HTMLを再生成' && git push origin master")

if __name__ == '__main__':
    main()
