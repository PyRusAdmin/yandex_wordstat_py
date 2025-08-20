# -*- coding: utf-8 -*-
from loguru import logger

from get_regions_tree import get_regions_tree
from keys import OAuth
from regions import get_wordstat_by_regions


def _parse_region_tree(node, region_map):
    """
    Рекурсивно обходит дерево регионов (value -> label)
    """
    if isinstance(node, dict):
        if "value" in node and "label" in node:
            region_map[int(node["value"])] = node["label"]  # ID приводим к int
        if "children" in node and node["children"]:
            for child in node["children"]:
                _parse_region_tree(child, region_map)
    elif isinstance(node, list):
        for item in node:
            _parse_region_tree(item, region_map)


def pretty_regions(keyword: str, data: dict, region_names: dict) -> str:
    if not data or 'regions' not in data:
        return "Нет данных о регионах"
    result = [f"📊 Региональная статистика для: '{keyword}'"]
    result.append("\n📍 Топ регионов (по количеству запросов):")
    sorted_regions = sorted(data['regions'], key=lambda x: x['count'], reverse=True)
    for region in sorted_regions[:10]:
        region_id = region['regionId']
        name = region_names.get(region_id, "Неизвестный регион")
        count = f"{region['count']:,}".replace(",", " ")
        share = region['share'] * 100
        affinity = region['affinityIndex']
        result.append(
            f"   • {name} (ID: {region_id}) — {count} запросов "
            f"(доля: {share:.2f}%, индекс: {affinity:.1f})"
        )
    return "\n".join(result)


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
