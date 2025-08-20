# -*- coding: utf-8 -*-
import requests
from loguru import logger


def get_wordstat_by_regions(keyword: str, OAuth, region_type: str = "cities"):
    """
    Получает статистику по регионам для ключевой фразы
    """
    payload = {
        "phrase": keyword,
        "regionType": region_type,  # all, cities, regions, countries
    }
    HEADERS = {
        "Authorization": f"Bearer {OAuth}",
        "Content-Type": "application/json",
    }
    URL_REGIONS = "https://api.wordstat.yandex.net/v1/regions"  # Для статистики по регионам
    try:
        response = requests.post(URL_REGIONS, json=payload, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"❌ {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка запроса: {e}")
        return None
