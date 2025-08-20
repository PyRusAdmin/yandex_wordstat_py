# -*- coding: utf-8 -*-
import os
import time

import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv(dotenv_path='.env')

OAuth = os.getenv('OAuth')


def create_wordstat_report(keyword: str):
    """
    Получение данных по ключевому слову из Wordstat API (v1)
    """
    url = "https://api.wordstat.yandex.net/v1/topRequests"
    headers = {
        "Authorization": f"Bearer {OAuth}",
        "Content-Type": "application/json",
    }

    payload = {
        "phrase": keyword,
        "numPhrases": 20,  # по умолчанию 50, максимум 2000
        "devices": ["all"],  # можно: all, desktop, phone, tablet
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


def pretty_regions(data: dict) -> str:
    if not data or 'regions' not in data:
        return "Нет данных о регионах"

    result = [f"📊 Региональная статистика для: {data['requestPhrase']}"]
    result.append(f"🔢 Всего показов: {data.get('totalCount', 0):,}")
    result.append("\n📍 Топ регионов:")

    for region in data.get('regions', [])[:10]:  # Ограничиваем 10 регионами
        result.append(f"   • {region['regionId']} — {region['count']:,}")

    return "\n".join(result)


def main():
    # Использование:
    keywords = ["маркетинг"]

    for keyword in keywords:
        logger.info(f"Запрос: {keyword}")

        # Получаем данные по регионам (города)
        region_data = get_wordstat_by_regions(keyword, "cities")
        print(region_data)
        if region_data:
            print(pretty_regions(region_data))

        time.sleep(1)

if __name__ == "__main__":
    main()