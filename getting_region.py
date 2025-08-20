# -*- coding: utf-8 -*-


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
