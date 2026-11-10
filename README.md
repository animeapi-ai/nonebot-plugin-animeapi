# nonebot-plugin-animeapi

为 [NoneBot2](https://nonebot.dev) 机器人提供动漫图片生成，由 [AnimeAPI](https://animeapi.ai) 驱动。AnimeAPI 是最便宜的动漫图片 API 之一：**每张 $0.003**，预付余额 $5 起、永不过期，无订阅。新账号免费 3 张，无需绑卡。

**简体中文** · [English](README.en.md) · [日本語](README.ja.md)

## 安装

使用 nb-cli（推荐）：

```sh
nb plugin install nonebot-plugin-animeapi
```

或使用包管理器安装后，在 `pyproject.toml` 的 `[tool.nonebot]` 中加入 `plugins = ["nonebot_plugin_animeapi"]`：

```sh
pip install nonebot-plugin-animeapi
```

## 配置

在 `.env` 中填写密钥（以 `ank_` 开头），密钥在 <https://animeapi.ai/dashboard/api-keys> 创建：

```dotenv
ANIMEAPI_KEY=ank_xxxxxxxx
```

| 配置项 | 默认 | 说明 |
| --- | --- | --- |
| `ANIMEAPI_KEY` | 空 | AnimeAPI 密钥（必填） |
| `ANIMEAPI_MODEL` | `anime` | 每张 `anime` $0.003、`ultra` $0.01、`ultra-max` $0.02 |
| `ANIMEAPI_ORIENTATION` | `portrait` | `portrait`（竖）、`square`（方）、`landscape`（横），价格相同 |
| `ANIMEAPI_ENHANCE` | `true` | 自动把提示词改写为标签（anime 模型） |
| `ANIMEAPI_COOLDOWN` | `30` | 每位用户两次生成之间的间隔（秒），`0` 为不限制 |
| `ANIMEAPI_ALLOW_MODEL_OVERRIDE` | `false` | 是否允许用户用 `-m` 选择模型。默认关闭，避免用户选用更贵的模型 |
| `ANIMEAPI_SHOW_PROMPT` | `false` | 同时发送模型实际收到的标签 |
| `ANIMEAPI_LANGUAGE` | `zh` | 机器人回复语言：`zh`、`en`、`ja` |
| `ANIMEAPI_TIMEOUT` | `120` | 等待 AnimeAPI 的秒数 |

AnimeAPI 不生成成人内容。露骨的提示词会被拒绝，且不收费。

## 使用

```
/anime 雨天公交站打着红伞的女孩
/anime -o landscape 秋天的神社，落叶纷飞
/anime -m ultra a cafe chalkboard that reads OPEN LATE
```

直接用自然语言描述即可，AnimeAPI 会自动改写为 anime 模型使用的标签。指令别名：`/animeapi`。命令前缀取决于你的 `COMMAND_START`。

通过 [nonebot-plugin-alconna](https://github.com/nonebot/plugin-alconna) 发送图片，支持 OneBot、QQ、Telegram、Discord、Kook、飞书等适配器。

## 用户可能看到的提示

| 情况 | 回复 |
| --- | --- |
| 余额不足 | 提示管理员前往 <https://animeapi.ai/dashboard/billing> 充值 |
| 密钥无效或已撤销 | 提示管理员检查密钥 |
| 模型拒绝了提示词 | 显示原因，不扣费 |
| 冷却中 | 显示剩余秒数 |
| AnimeAPI 繁忙 | 提示稍后重试；失败的图片会退款 |

## 链接

- AnimeAPI：<https://animeapi.ai> · [文档](https://animeapi.ai/docs) · [API 参考](https://animeapi.ai/docs/api-reference)
- 许可证：[MIT](LICENSE)
