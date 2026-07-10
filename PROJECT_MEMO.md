# アメトメ LP プロジェクトメモ

## ASPとパスの対応（重要・必ず参照）

| パス | ASP名 | 対応エリア |
|---|---|---|
| `/lp1/` | マスター | 関東 |
| `/lp1/a/` | **felmat（フェルマット）** | 関東 |
| `/lp1/b/` | **レントラックス** | 関東 |
| `/lp3/` | マスター | 東北 |
| `/lp3/a/` | **felmat（フェルマット）** | 東北 |
| `/lp3/b/` | **レントラックス** | 東北 |

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

## lp3（東北版）について

lp1をベースに2026-07-10作成。**lp1には一切変更を加えないこと。**

lp1からの変更点:

- 対応エリアを東北6県に変更（h1、選ばれる理由、対応エリアセクション）
- 地図: `img/map_tohoku.svg`（`gen_tohoku_map.py` で生成）
- お客様の声の県名を宮城・福島・青森に変更
- 「雨漏り診断士が直接対応」訴求5箇所に注釈を追加:
  「※お問い合わせの状況により、雨漏り診断士以外のスタッフが対応する場合があります。」
  （クラス `shindanshi-note`、スタイルはlp3/index.htmlの`<head>`内に定義）
- ASP識別子: `data/*.json` に `asp_key` を追加（`a_tohoku` / `b_tohoku` / `tohoku_default`）。
  GAS通知の `asp:` 欄でlp1と区別できる
- 電話番号・felmatキー（I11242X）・レントラックスct3タグはlp1と同一を流用（広告主確認済み・暫定）

### 通知系の状態（TODO）

- 通知メッセージ冒頭: `【アメトメ】"東北"専用`（lp3専用GAS `gas_code_lp3.js` に実装済み）
- **暫定: lp3のgasUrlはlp1と同じGASを向いている**（東北用LINEグループが未作成のため。
  Gmail＋既存LINEグループに届き、`asp: a_tohoku` 等で判別可能）
- 東北用LINEグループができたら:
  1. `gas_code_lp3.js` を新規GASプロジェクトとしてデプロイ（手順はファイル冒頭コメント参照）
  2. スクリプトプロパティに `LINE_CHANNEL_ACCESS_TOKEN` / `LINE_GROUP_ID` / `DRIVE_FOLDER_ID` を設定
  3. `lp3/index.html` の `gasUrl`（2箇所）を新URLに差し替え → `cd lp3 && python3 build.py` → push
