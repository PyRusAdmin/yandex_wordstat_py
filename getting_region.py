# -*- coding: utf-8 -*-
from loguru import logger

from get_regions_tree import get_regions_tree
from keys import OAuth
from regions import get_wordstat_by_regions
from regions_utils import pretty_regions


def parse_region_tree(node, region_map):
    """
    Рекурсивно обходит дерево регионов (value -> label)
    """
    if isinstance(node, dict):
        if "value" in node and "label" in node:
            region_map[int(node["value"])] = node["label"]  # ID приводим к int
        if "children" in node and node["children"]:
            for child in node["children"]:
                parse_region_tree(child, region_map)
    elif isinstance(node, list):
        for item in node:
            parse_region_tree(item, region_map)


def main():
    # Сначала загружаем названия регионов
    region_names = get_regions_tree(OAuth=OAuth)
    # Затем запрашиваем статистику
    keyword = "курсы"
    data = get_wordstat_by_regions(keyword, OAuth, "cities")
    if data:
        print(pretty_regions(keyword, data, region_names))
    else:
        logger.error("❌ Не удалось получить статистику по регионам")


if __name__ == "__main__":
    main()
