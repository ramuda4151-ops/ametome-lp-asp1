#!/usr/bin/env python3
"""
lp1/build.py
マスターHTML（lp1/index.html）をベースに、各ASPディレクトリのindex.htmlを生成するスクリプト。

使い方:
  cd /home/ubuntu/ametome-lp-asp1/lp1
  python3 build.py

マスター（lp1/index.html）を修正したら、このスクリプトを実行して
git add . && git commit && git push するだけで全ASPに反映される。
"""

import os
import re

MASTER_PATH = os.path.join(os.path.dirname(__file__), 'index.html')
ASP_DIRS = ['a', 'b']  # 追加するASPはここに追記するだけ

def build_asp(asp_key, master_html):
    """マスターHTMLからASP別HTMLを生成する"""
    html = master_html

    # LP設定ローダーのaspKeyを固定値に書き換える（JSONフェッチ不要にする）
    # 元のローダーをASP固定版に置き換え
    loader_pattern = r'<!-- LP設定ローダー.*?<!-- End LP設定ローダー -->'
    fixed_loader = f"""  <!-- LP設定ローダー（ASP: {asp_key}） -->
  <script>
  (function() {{
    var aspKey = '{asp_key}';
    var base = '/lp1/';

    // JSONを同期的に取得
    var xhr = new XMLHttpRequest();
    xhr.open('GET', base + 'data/' + aspKey + '.json', false);
    try {{ xhr.send(); }} catch(e) {{}}

    var config = {{}};
    if (xhr.status === 200) {{
      try {{ config = JSON.parse(xhr.responseText); }} catch(e) {{}}
    }}

    window.__LP_CONFIG__ = config;

    // コールトラッキングスクリプトを動的挿入
    if (config.call_tracking_scripts && config.call_tracking_scripts.length > 0) {{
      config.call_tracking_scripts.forEach(function(s) {{
        var el = document.createElement('script');
        if (s.type === 'inline') {{
          el.textContent = s.content;
        }} else {{
          el.src = s.src;
          if (s.async) el.async = true;
        }}
        document.currentScript.parentNode.insertBefore(el, document.currentScript.nextSibling);
      }});
    }}

    // DOMContentLoaded後に電話番号表示・リンクを更新
    document.addEventListener('DOMContentLoaded', function() {{
      var cfg = window.__LP_CONFIG__ || {{}};
      var tel = cfg.tel || '0120-094-956';
      var telRaw = cfg.tel_raw || '01200940956';
      var mode = cfg.tel_mode || 'plain';

      if (mode === 'plain') {{
        document.querySelectorAll('.lp-tel-display').forEach(function(el) {{
          el.textContent = tel;
        }});
        document.querySelectorAll('.lp-tel-link').forEach(function(el) {{
          if (el.tagName === 'A') el.href = 'tel:' + telRaw;
        }});
      }} else if (mode === 'fmcall') {{
        document.querySelectorAll('.lp-tel-display').forEach(function(el) {{
          el.id = 'fmcall';
          el.textContent = tel;
        }});
        document.querySelectorAll('.lp-tel-link').forEach(function(el) {{
          if (el.tagName === 'A') el.href = 'tel:' + telRaw;
        }});
      }} else if (mode === 'ct3') {{
        document.querySelectorAll('.lp-tel-display').forEach(function(el) {{
          el.classList.add('ct3_telno');
          el.textContent = '-';
        }});
        document.querySelectorAll('.lp-tel-link').forEach(function(el) {{
          if (el.tagName === 'A') el.href = '#';
          el.classList.add('telno');
        }});
      }}

      // thanksUrlをJSONから設定
      window.__LP_THANKS_URL__ = cfg.thanks_url || 'thanks.html';
    }});
  }})();
  </script>
  <!-- End LP設定ローダー -->"""

    html = re.sub(loader_pattern, fixed_loader, html, flags=re.DOTALL)

    # thanksUrlをJSONから取得するように修正
    html = html.replace(
        "var thanksUrl = window.__LP_CONFIG__ ? window.__LP_CONFIG__.thanks_url : 'thanks.html';",
        "var thanksUrl = window.__LP_THANKS_URL__ || (window.__LP_CONFIG__ ? window.__LP_CONFIG__.thanks_url : 'thanks.html');"
    )

    return html

def main():
    with open(MASTER_PATH, 'r', encoding='utf-8') as f:
        master_html = f.read()

    base_dir = os.path.dirname(MASTER_PATH)

    for asp_key in ASP_DIRS:
        asp_dir = os.path.join(base_dir, asp_key)
        os.makedirs(asp_dir, exist_ok=True)
        output_path = os.path.join(asp_dir, 'index.html')

        built_html = build_asp(asp_key, master_html)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(built_html)

        print(f"✓ {asp_key}/index.html を生成しました ({len(built_html)} bytes)")

    print("\nビルド完了！次のコマンドでデプロイしてください:")
    print("  cd /home/ubuntu/ametome-lp-asp1")
    print("  git add lp1/ && git commit -m 'build: ASP別HTMLを再生成' && git push origin master")

if __name__ == '__main__':
    main()
