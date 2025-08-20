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
