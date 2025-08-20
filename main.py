# -*- coding: utf-8 -*-
import time

from loguru import logger

from get_regions_tree import get_regions_tree
from keys import OAuth
from regions import get_wordstat_by_regions
from regions_utils import pretty_regions


def main():
    region_names = get_regions_tree(OAuth=OAuth)
    keywords = ["маркетинг", "обучение", "курсы"]
    for keyword in keywords:
        logger.info(f"🔍 Обрабатываем ключевое слово: {keyword}")
        data = get_wordstat_by_regions(keyword, OAuth, "cities")
        if data:
            print(pretty_regions(keyword, data, region_names))
        else:
            print(f"❌ Не удалось получить данные для '{keyword}'")
        time.sleep(1)  # чтобы не превысить лимиты


if __name__ == "__main__":
    main()
