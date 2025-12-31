from functools import lru_cache

@lru_cache(maxsize=128)
def prompt_cache(key: str):
    return key