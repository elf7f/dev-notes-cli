from devnotes.utils import slugify_title


def test_slugify_english_title() -> None:
    assert slugify_title("MySQL Index Notes") == "mysql-index-notes"


def test_slugify_cjk_title_keeps_characters() -> None:
    assert slugify_title("Redis 缓存击穿总结") == "Redis-缓存击穿总结"
