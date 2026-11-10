import time
from typing import Dict, Optional, Set, Tuple

from nonebot import get_plugin_config, logger, on_command, require
from nonebot.adapters import Event, Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import UniMessage  # noqa: E402

from .client import MAX_PROMPT, MODELS, ORIENTATIONS, AnimeAPIError, download, generate  # noqa: E402
from .config import Config  # noqa: E402
from .messages import text  # noqa: E402

__plugin_meta__ = PluginMetadata(
    name="AnimeAPI 动漫图片生成",
    description="使用 AnimeAPI 生成动漫图片：每张 $0.003，预付 $5 起，无订阅 / Anime image generation at $0.003 per image",
    usage=(
        "/anime <提示词>  生成一张动漫图片\n"
        "/anime -o landscape <提示词>  指定画幅 portrait | square | landscape\n"
        "/anime -m ultra <提示词>  指定模型（需开启 ANIMEAPI_ALLOW_MODEL_OVERRIDE）"
    ),
    type="application",
    homepage="https://github.com/animeapi-ai/nonebot-plugin-animeapi",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"author": "AnimeAPI <contact@animeapi.ai>"},
)

config = get_plugin_config(Config)

_last_use: Dict[str, float] = {}
_in_flight: Set[str] = set()

anime = on_command("anime", aliases={"animeapi"}, priority=10, block=True)


def _parse(raw: str) -> Tuple[str, Optional[str], Optional[str]]:
    """Split leading -m/-o options from the prompt."""
    tokens = raw.split()
    model: Optional[str] = None
    orientation: Optional[str] = None
    while len(tokens) >= 2 and tokens[0] in ("-m", "--model", "-o", "--orientation"):
        flag, value = tokens[0], tokens[1].lower()
        if flag in ("-m", "--model"):
            model = value
        else:
            orientation = value
        tokens = tokens[2:]
    return " ".join(tokens).strip(), model, orientation


@anime.handle()
async def handle_anime(matcher: Matcher, event: Event, args: Message = CommandArg()) -> None:
    lang = config.animeapi_language
    prompt, model_arg, orientation_arg = _parse(args.extract_plain_text().strip())

    if not prompt:
        await matcher.finish(text(lang, "no_prompt"))
    if len(prompt) > MAX_PROMPT:
        await matcher.finish(text(lang, "too_long"))
    if not config.animeapi_key.strip():
        await matcher.finish(text(lang, "no_key"))

    model = config.animeapi_model
    if model_arg:
        if model_arg not in MODELS:
            await matcher.finish(text(lang, "bad_model"))
        if not config.animeapi_allow_model_override and model_arg != config.animeapi_model:
            await matcher.finish(text(lang, "model_locked"))
        model = model_arg  # type: ignore[assignment]
    orientation = config.animeapi_orientation
    if orientation_arg:
        if orientation_arg not in ORIENTATIONS:
            await matcher.finish(text(lang, "bad_orientation"))
        orientation = orientation_arg  # type: ignore[assignment]

    user = event.get_user_id()
    if user in _in_flight:
        await matcher.finish(text(lang, "busy_user"))
    if config.animeapi_cooldown > 0:
        wait = _last_use.get(user, 0) + config.animeapi_cooldown - time.monotonic()
        if wait > 0:
            await matcher.finish(text(lang, "cooldown", seconds=int(wait) + 1))

    _in_flight.add(user)
    try:
        result = await generate(
            key=config.animeapi_key.strip(),
            prompt=prompt,
            model=model,
            orientation=orientation,
            enhance=config.animeapi_enhance,
            timeout=config.animeapi_timeout,
        )
    except AnimeAPIError as exc:
        logger.warning(f"AnimeAPI generation failed: {exc.status} {exc.code} {exc.message}")
        if exc.status == 402:
            reply = text(lang, "no_balance")
        elif exc.status == 401:
            reply = text(lang, "invalid_key")
        elif exc.code in ("MODERATION_BLOCKED", "PROVIDER_REJECTED"):
            reply = text(lang, "rejected", reason=exc.message)
        elif exc.status in (429, 503):
            reply = text(lang, "busy")
        elif exc.code == "NETWORK":
            reply = text(lang, "network")
        else:
            reply = text(lang, "failed", reason=exc.message)
        await matcher.finish(reply)
    finally:
        _in_flight.discard(user)

    _last_use[user] = time.monotonic()
    logger.info(
        f"AnimeAPI image for {user} in {result.generation_time_ms}ms: {result.image_url} "
        f"(balance ${result.balance_usd:.3f})"
    )

    try:
        raw, mimetype = await download(result.image_url)
        suffix = "png" if "png" in (mimetype or result.image_url) else "webp"
        message = UniMessage.image(raw=raw, mimetype=mimetype, name=f"animeapi.{suffix}")
    except Exception as exc:  # the URL still works for platforms that fetch it themselves
        logger.warning(f"Could not download the AnimeAPI image, sending its URL instead: {exc!r}")
        message = UniMessage.image(url=result.image_url)
    if config.animeapi_show_prompt and result.enhanced_prompt:
        message = message + UniMessage.text("\n" + result.enhanced_prompt)
    await message.send()
