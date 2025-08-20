# -*- coding: utf-8 -*-
import time

import requests
from loguru import logger

from keys import OAuth


def create_wordstat_report(keyword: str):
    """
    Получение данных по ключевому слову из Wordstat API (v1)
    """
    url = "https://api.wordstat.yandex.net/v1/regions"
    headers = {
        "Authorization": f"Bearer {OAuth}",
        "Content-Type": "application/json",
    }
    payload = {
        "phrase": keyword,
        "regionType": "all",
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        logger.debug("📊 Ответ Wordstat:", data)
        return data
    else:
        logger.error(f"❌ Ошибка Wordstat {response.status_code}: {response.text}")
        return None


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


def pretty_regions(keyword: str, data: dict) -> str:
    if not data or 'regions' not in data:
        return "Нет данных о регионах"
    result = [f"📊 Региональная статистика для: '{keyword}'"]
    result.append("\n📍 Топ регионов (по количеству запросов):")
    # Сортируем по убыванию count
    sorted_regions = sorted(data['regions'], key=lambda x: x['count'], reverse=True)
    for region in sorted_regions[:10]:
        region_id = region['regionId']
        count = f"{region['count']:,}".replace(",", " ")
        share = region['share'] * 100
        affinity = region['affinityIndex']
        result.append(f"   • ID {region_id} — {count} запросов (доля: {share:.2f}%, индекс: {affinity:.1f})")
    return "\n".join(result)


def main():
    keywords = ["маркетинг", "обучение", "курсы"]
    for keyword in keywords:
        logger.info(f"🔍 Обрабатываем ключевое слово: {keyword}")
        region_data = create_wordstat_report(keyword)
        if region_data:
            print(pretty_regions(keyword, region_data))
        else:
            print(f"❌ Не удалось получить данные для '{keyword}'")
        time.sleep(1)  # чтобы не превысить лимиты


if __name__ == "__main__":
    main()
