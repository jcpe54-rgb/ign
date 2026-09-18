"""Configuracion unica de la capa de datos de Pasta Corta.

Los ``tagPath`` quedan deliberadamente sin valor hasta que se confirmen las
rutas reales. Los IDs L1-L10 son contratos internos, no nombres de Tags.
"""

APP_CONFIG = {
    "baleWeightKg": 12,
    "speedWindowMinutes": 5,
    "lineCount": 10,
    "palletizerCount": 5,
    "lines": [
        {"id": "L1", "name": "L1", "tagPath": None, "palletizerId": "P1"},
        {"id": "L2", "name": "L2", "tagPath": None, "palletizerId": "P1"},
        {"id": "L3", "name": "L3", "tagPath": None, "palletizerId": "P2"},
        {"id": "L4", "name": "L4", "tagPath": None, "palletizerId": "P2"},
        {"id": "L5", "name": "L5", "tagPath": None, "palletizerId": "P3"},
        {"id": "L6", "name": "L6", "tagPath": None, "palletizerId": "P3"},
        {"id": "L7", "name": "L7", "tagPath": None, "palletizerId": "P4"},
        {"id": "L8", "name": "L8", "tagPath": None, "palletizerId": "P4"},
        {"id": "L9", "name": "L9", "tagPath": None, "palletizerId": "P5"},
        {"id": "L10", "name": "L10", "tagPath": None, "palletizerId": "P5"}
    ],
    "palletizers": [
        {"id": "P1", "name": "P1", "lineIds": ["L1", "L2"]},
        {"id": "P2", "name": "P2", "lineIds": ["L3", "L4"]},
        {"id": "P3", "name": "P3", "lineIds": ["L5", "L6"]},
        {"id": "P4", "name": "P4", "lineIds": ["L7", "L8"]},
        {"id": "P5", "name": "P5", "lineIds": ["L9", "L10"]}
    ],
    # Los sufijos se resolveran contra tagPath exclusivamente en el adapter.
    "signals": {
        "state": None,
        "faultCode": None,
        "caseInCount": None,
        "caseOutCount": None,
        "operatingMode": None,
        "operatingState": None,
        "sku": None,
        "workOrder": None,
        "networkStatus": None,
        "powerOnTime": None
    },
    # Estructuras configurables; los horarios no se declaran como definitivos.
    "shifts": [],
    "groups": [],
    "supervisors": []
}


def get_config():
    """Devuelve una copia para impedir mutaciones accidentales globales."""
    import copy
    return copy.deepcopy(APP_CONFIG)
