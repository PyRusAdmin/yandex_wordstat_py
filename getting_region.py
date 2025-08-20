# -*- coding: utf-8 -*-
import os
from rich.json import JSON
import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv(dotenv_path='.env')

OAuth = os.getenv('OAuth')


def get_wordstat_by_regions(keyword: str, region_type: str = "cities"):
    url = "https://api.wordstat.yandex.net/v1/getRegionsTree"
    headers = {
        "Authorization": f"Bearer {OAuth}",
        "Content-Type": "application/json",
    }
    payload = {
        "phrase": keyword,
        "regionType": region_type,  # cities, countries, districts, regions
        "devices": ["all"],
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Проверка статуса ответа
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка при получении регионов: {e}")
        return None


def main():
    response = get_wordstat_by_regions("дизайн", "cities")
    print(response)



if __name__ == "__main__":
    main()
