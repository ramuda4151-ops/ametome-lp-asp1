# アメトメ LP プロジェクトメモ

## ASPとパスの対応（重要・必ず参照）

| パス | ASP名 |
|---|---|
| `/lp1/a/` | **felmat（フェルマット）** |
| `/lp1/b/` | **レントラックス** |

## サイト構成

- リポジトリ: https://github.com/ramuda4151-ops/ametome-lp-asp1
- 公開URL: https://asp.amamori-tometai.com/
- マスターLP: https://asp.amamori-tometai.com/lp1/
- felmat用LP: https://asp.amamori-tometai.com/lp1/a/
- レントラックス用LP: https://asp.amamori-tometai.com/lp1/b/

## ファイル構成

- `lp1/index.html` … マスターテンプレート
- `lp1/data/a.json` … felmat用設定（コールトラッキング: fmcall方式）
- `lp1/data/b.json` … レントラックス用設定（コールトラッキング: ct3方式）
- `lp1/a/index.html` … felmat用LP（build.pyで生成）
- `lp1/b/index.html` … レントラックス用LP（build.pyで生成）
- `style.css` … 全LP共通スタイル
- `lp1/build.py` … ASP別HTML生成スクリプト

## 主な仕様メモ

- felmatのコールトラッキングは `fmcall_atag_tel='ON'` で `href="tel:..."` を自動書き換え
- `id="fmcall"` の要素は作らない（テキスト書き換え防止のため）
- サンクスページURL: `thanks.html`（各ASPディレクトリからの相対パス）
- フォームタイプボタン色: ティール `#2a8a7a`（選択時: `#1d6b5e`）
