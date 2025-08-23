# -*- coding: utf-8 -*-
import os
import time

from dotenv import load_dotenv
from loguru import logger

from get_regions_tree import get_regions_tree
from regions import get_wordstat_by_regions
from regions_utils import pretty_regions

load_dotenv(dotenv_path='.env')

OAuth = os.getenv('OAuth')


def tests():
    """
    Главная функция скрипта для получения региональной статистики по ключевым словам.

    Работа скрипта:
        1. Загружает полный список регионов с помощью функции get_regions_tree().
        2. Для каждого ключевого слова из списка keywords:
            - Получает статистику по регионам через API Яндекс.Вордстат
              с помощью get_wordstat_by_regions().
            - Форматирует и выводит результаты с помощью pretty_regions().
        3. Делает паузу в 1 секунду между запросами, чтобы избежать превышения лимитов API.

    Входные данные:
        - Список ключевых слов keywords задается внутри функции main().
        - OAuth-токен для доступа к API импортируется из keys.py.

    Логирование:
        - Выводит информацию о текущем обрабатываемом ключевом слове.
        - Ошибки получения данных выводятся через print() и loguru.

    Ограничения:
        - Пауза между запросами установлена в 1 секунду, можно менять в зависимости
          от лимитов API.
        - Функция работает только с региональным типом "cities" по умолчанию.

    Пример использования:
        Запуск скрипта:
            python main.py
        Результат:
            Вывод региональной статистики для каждого ключевого слова
            в читаемом формате с топ-10 регионов.
    """
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
    tests()
