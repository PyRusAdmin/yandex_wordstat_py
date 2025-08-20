# -*- coding: utf-8 -*-
import requests
from loguru import logger

from getting_region import parse_region_tree


def get_regions_tree(OAuth):
    """
    Получает полный список регионов (ID -> название)
    """
    try:
        URL_REGIONS_TREE = "https://api.wordstat.yandex.net/v1/getRegionsTree"  # Для списка регионов
        HEADERS = {
            "Authorization": f"Bearer {OAuth}",
            "Content-Type": "application/json",
        }
        response = requests.post(URL_REGIONS_TREE, headers=HEADERS)
        response.raise_for_status()
        print("RAW response:", response.text)
        tree = response.json()
        if not tree:
            logger.error("❌ Ответ от /v1/getRegionsTree пустой")
            return {}
        region_map = {}
        parse_region_tree(tree, region_map)
        logger.success(f"✅ Загружено {len(region_map)} регионов")
        return region_map

    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке дерева регионов: {e}")
        return {}
