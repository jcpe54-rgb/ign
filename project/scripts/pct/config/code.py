# -*- coding: utf-8 -*-
"""Configuracion unica de la capa de datos de Pasta Corta.

Los IDs L1-L10 y P1-P5 son contratos internos. Ninguna ruta de Tags real se
declara hasta que sea confirmada en una fase posterior.
"""

APP_CONFIG = {
    "baleWeightKg": 12,
    "speedWindowMinutes": 5,
    "lineCount": 10,
    "palletizerCount": 5,
    "lines": [
        {"id": "L1", "displayName": "L1", "basePath": None, "palletizerId": "P1"},
        {"id": "L2", "displayName": "L2", "basePath": None, "palletizerId": "P1"},
        {"id": "L3", "displayName": "L3", "basePath": None, "palletizerId": "P2"},
        {"id": "L4", "displayName": "L4", "basePath": None, "palletizerId": "P2"},
        {"id": "L5", "displayName": "L5", "basePath": None, "palletizerId": "P3"},
        {"id": "L6", "displayName": "L6", "basePath": None, "palletizerId": "P3"},
        {"id": "L7", "displayName": "L7", "basePath": None, "palletizerId": "P4"},
        {"id": "L8", "displayName": "L8", "basePath": None, "palletizerId": "P4"},
        {"id": "L9", "displayName": "L9", "basePath": None, "palletizerId": "P5"},
        {"id": "L10", "displayName": "L10", "basePath": None, "palletizerId": "P5"}
    ],
    "palletizers": [
        {"id": "P1", "displayName": "P1", "lineIds": ["L1", "L2"]},
        {"id": "P2", "displayName": "P2", "lineIds": ["L3", "L4"]},
        {"id": "P3", "displayName": "P3", "lineIds": ["L5", "L6"]},
        {"id": "P4", "displayName": "P4", "lineIds": ["L7", "L8"]},
        {"id": "P5", "displayName": "P5", "lineIds": ["L9", "L10"]}
    ]
}


def get_config():
    """Devuelve una copia para impedir mutaciones accidentales globales."""
    import copy
    return copy.deepcopy(APP_CONFIG)
