# -*- coding: utf-8 -*-
import time

from loguru import logger

from getting_region import get_regions_tree
from keys import OAuth
from regions import get_wordstat_by_regions


def pretty_wordstat(data: dict) -> str:
    lines = []
    lines.append(f"📊 Запрос: {data['requestPhrase']}")
    lines.append(f"🔢 Общая частота: {data['totalCount']:,}".replace(",", " "))
    lines.append("\n✨ Топ запросы:")
    for item in data.get("topRequests", []):
        lines.append(f"   • {item['phrase']} — {item['count']:,}".replace(",", " "))
    lines.append("\n🔗 Ассоциации:")
    for item in data.get("associations", []):
        lines.append(f"   • {item['phrase']} — {item['count']:,}".replace(",", " "))
    return "\n".join(lines)


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
