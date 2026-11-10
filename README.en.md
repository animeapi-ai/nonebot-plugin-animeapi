# nonebot-plugin-animeapi

Anime image generation for [NoneBot2](https://nonebot.dev) bots, powered by [AnimeAPI](https://animeapi.ai), one of the cheapest anime image APIs: **$0.003 per image**, prepaid balance from $5 that never expires, no subscription. New accounts get 3 free images, no card needed.

[简体中文](README.md) · **English** · [日本語](README.ja.md)

## Install

With nb-cli (recommended):

```sh
nb plugin install nonebot-plugin-animeapi
```

Or install with your package manager and add `plugins = ["nonebot_plugin_animeapi"]` under `[tool.nonebot]` in `pyproject.toml`:

```sh
pip install nonebot-plugin-animeapi
```

## Configure

Put your key (starts with `ank_`) in `.env`. Create one at <https://animeapi.ai/dashboard/api-keys>:

```dotenv
ANIMEAPI_KEY=ank_xxxxxxxx
```

| Setting | Default | What it does |
| --- | --- | --- |
| `ANIMEAPI_KEY` | empty | Your AnimeAPI key (required) |
| `ANIMEAPI_MODEL` | `anime` | `anime` $0.003, `ultra` $0.01, `ultra-max` $0.02 per image |
| `ANIMEAPI_ORIENTATION` | `portrait` | `portrait`, `square` or `landscape`; same price |
| `ANIMEAPI_ENHANCE` | `true` | Rewrite plain prompts into tags (anime model) |
| `ANIMEAPI_COOLDOWN` | `30` | Seconds each user must wait between images; `0` disables the limit |
| `ANIMEAPI_ALLOW_MODEL_OVERRIDE` | `false` | Let users choose a model with `-m`. Off so users cannot pick a more expensive model |
| `ANIMEAPI_SHOW_PROMPT` | `false` | Also send the tags the model received |
| `ANIMEAPI_LANGUAGE` | `zh` | Language of the bot's replies: `zh`, `en` or `ja` |
| `ANIMEAPI_TIMEOUT` | `120` | Seconds to wait for AnimeAPI |

AnimeAPI does not generate adult content. Explicit prompts are refused and not charged.

## Use

```
/anime a girl with a red umbrella at a rainy bus stop
/anime -o landscape a shrine in autumn, falling leaves
/anime -m ultra a cafe chalkboard that reads OPEN LATE
```

Write the prompt in plain words; AnimeAPI rewrites it into tags for the anime model. `/animeapi` is an alias. The command prefix follows your `COMMAND_START`.

Images are sent through [nonebot-plugin-alconna](https://github.com/nonebot/plugin-alconna), so the plugin works with OneBot, QQ, Telegram, Discord, Kook, Feishu and the other adapters it supports.

## Messages your users may see

| Situation | Reply |
| --- | --- |
| Balance is empty | Tells the bot owner to add funds at <https://animeapi.ai/dashboard/billing> |
| Key is wrong or revoked | Tells the bot owner to check the key |
| The model refused the prompt | Shows the reason; nothing is charged |
| Too soon after the last image | Shows how many seconds are left |
| AnimeAPI is busy | Asks to try again in a few seconds; failed images are refunded |

## Links

- AnimeAPI: <https://animeapi.ai> · [Docs](https://animeapi.ai/docs) · [API reference](https://animeapi.ai/docs/api-reference)
- Licence: [MIT](LICENSE)
