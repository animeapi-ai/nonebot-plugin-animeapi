# nonebot-plugin-animeapi

[NoneBot2](https://nonebot.dev) ボット向けのアニメ画像生成プラグインです。[AnimeAPI](https://animeapi.ai) を利用します。AnimeAPI は最安クラスのアニメ画像 API です：**1 枚 $0.003**、プリペイド残高は $5 から・無期限、サブスクリプションなし。新規アカウントは無料 3 枚、カード不要。

[简体中文](README.md) · [English](README.en.md) · **日本語**

## インストール

```sh
nb plugin install nonebot-plugin-animeapi
```

または `pip install nonebot-plugin-animeapi` の後、`pyproject.toml` の `[tool.nonebot]` に `plugins = ["nonebot_plugin_animeapi"]` を追加します。

## 設定

`.env` にキー（`ank_` で始まる）を記入します。キーは <https://animeapi.ai/dashboard/api-keys> で作成できます：

```dotenv
ANIMEAPI_KEY=ank_xxxxxxxx
ANIMEAPI_LANGUAGE=ja
```

| 設定 | 既定 | 説明 |
| --- | --- | --- |
| `ANIMEAPI_KEY` | 空 | AnimeAPI のキー（必須） |
| `ANIMEAPI_MODEL` | `anime` | 1 枚 `anime` $0.003、`ultra` $0.01、`ultra-max` $0.02 |
| `ANIMEAPI_ORIENTATION` | `portrait` | `portrait`（縦）、`square`（正方形）、`landscape`（横）。価格は同じ |
| `ANIMEAPI_ENHANCE` | `true` | プロンプトをタグに自動変換（anime モデル） |
| `ANIMEAPI_COOLDOWN` | `30` | ユーザーごとの生成間隔（秒）。`0` で無効 |
| `ANIMEAPI_ALLOW_MODEL_OVERRIDE` | `false` | ユーザーが `-m` でモデルを選べるようにします |
| `ANIMEAPI_SHOW_PROMPT` | `false` | モデルが受け取ったタグも送信 |
| `ANIMEAPI_LANGUAGE` | `zh` | ボットの返信言語：`zh`、`en`、`ja` |
| `ANIMEAPI_TIMEOUT` | `120` | AnimeAPI の応答を待つ秒数 |

AnimeAPI は成人向けコンテンツを生成しません。露骨なプロンプトは拒否され、課金されません。

## 使い方

```
/anime 雨のバス停で赤い傘をさす少女
/anime -o landscape 秋の神社、舞い落ちる紅葉
```

プロンプトは普通の文章で構いません。別名：`/animeapi`。

## リンク

- AnimeAPI：<https://animeapi.ai> · [ドキュメント](https://animeapi.ai/docs) · [API リファレンス](https://animeapi.ai/docs/api-reference)
- ライセンス：[MIT](LICENSE)
