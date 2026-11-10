import asyncio
from dataclasses import dataclass
from typing import Optional, Tuple

import httpx

API_URL = "https://animeapi.ai/api/generate"
MODELS = ("anime", "ultra", "ultra-max")
ORIENTATIONS = ("portrait", "square", "landscape")
MAX_PROMPT = 1000


@dataclass
class Generated:
    image_url: str
    enhanced_prompt: str
    balance_usd: float
    generation_time_ms: int


class AnimeAPIError(Exception):
    def __init__(self, message: str, status: int = 0, code: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code


async def generate(
    *,
    key: str,
    prompt: str,
    model: str,
    orientation: str,
    enhance: bool,
    allow_nsfw: bool,
    timeout: float = 120,
) -> Generated:
    """Generate one image. Retries once when AnimeAPI says a retry can succeed."""
    payload = {
        "prompt": prompt,
        "model": model,
        "orientation": orientation,
        "enhance": enhance,
        "allowNSFW": allow_nsfw,
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in (1, 2):
            try:
                res = await client.post(API_URL, json=payload, headers={"Authorization": f"Bearer {key}"})
            except httpx.HTTPError as exc:
                raise AnimeAPIError(str(exc) or exc.__class__.__name__, code="NETWORK") from exc
            try:
                data = res.json()
            except ValueError:
                data = {}
            if res.is_success and data.get("image_url"):
                return Generated(
                    image_url=data["image_url"],
                    enhanced_prompt=data.get("enhanced_prompt", ""),
                    balance_usd=float(data.get("balance_usd", 0)),
                    generation_time_ms=int(data.get("generation_time_ms", 0)),
                )
            error = data.get("error")
            message = error if isinstance(error, str) else (error or {}).get("message") or f"HTTP {res.status_code}"
            code = data.get("code") or ""
            nsfw_blocked = not allow_nsfw and "nsfw" in message.lower()
            if nsfw_blocked:
                raise AnimeAPIError(message, res.status_code, "NSFW_BLOCKED")
            retryable = data.get("retryable") is True or res.status_code in (500, 503)
            if retryable and attempt == 1:
                try:
                    wait = float(res.headers.get("Retry-After", 3))
                except ValueError:
                    wait = 3.0
                await asyncio.sleep(min(wait, 10))
                continue
            raise AnimeAPIError(message, res.status_code, code)
    raise AnimeAPIError("unreachable")


async def download(url: str, timeout: float = 60) -> Tuple[bytes, Optional[str]]:
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        res = await client.get(url)
        res.raise_for_status()
        return res.content, res.headers.get("content-type")
