from typing import Literal

from pydantic import BaseModel


class Config(BaseModel):
    animeapi_key: str = ""
    """AnimeAPI key (starts with ank_), from https://animeapi.ai/dashboard/api-keys"""
    animeapi_model: Literal["anime", "ultra", "ultra-max"] = "anime"
    """Default model. anime $0.003, ultra $0.01, ultra-max $0.02 per image."""
    animeapi_orientation: Literal["portrait", "square", "landscape"] = "portrait"
    """Default image shape. Same price for every shape."""
    animeapi_enhance: bool = True
    """Let AnimeAPI rewrite plain-language prompts into tags (anime model)."""
    animeapi_cooldown: int = 30
    """Seconds each user must wait between images. 0 turns the limit off."""
    animeapi_allow_model_override: bool = False
    """Let users pick a model with -m. Off so users cannot choose a more expensive model."""
    animeapi_show_prompt: bool = False
    """Also send the tags the model actually received."""
    animeapi_language: Literal["zh", "en", "ja"] = "zh"
    """Language of the bot's replies."""
    animeapi_timeout: int = 120
    """Seconds to wait for AnimeAPI."""
