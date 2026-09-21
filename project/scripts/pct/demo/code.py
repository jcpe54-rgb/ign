# -*- coding: utf-8 -*-
"""Fuente DEMO unica del Overview.

Este modulo solo representa la fuente. No conoce Views, Repeaters ni Templates.
"""

HORIZON_MINUTES = 480

LINES = [
    {"id": "L1", "caseInCount": 6425, "caseOutCount": 6355,
     "counter5MinAgo": 6150, "state": "running", "faultCode": 0,
     "stops": []},
    {"id": "L2", "caseInCount": 6100, "caseOutCount": 6050,
     "counter5MinAgo": 6050, "state": "stopped", "faultCode": 0,
     "stops": [(90, 22), (310, 25), (455, 25)]},
    {"id": "L3", "caseInCount": 6250, "caseOutCount": 6180,
     "counter5MinAgo": 5986, "state": "running", "faultCode": 0,
     "stops": [(130, 8), (350, 13)]},
    {"id": "L4", "caseInCount": 6000, "caseOutCount": 5950,
     "counter5MinAgo": 5769, "state": "running", "faultCode": 0,
     "stops": []},
    {"id": "L5", "caseInCount": 6300, "caseOutCount": 6230,
     "counter5MinAgo": 6029, "state": "running", "faultCode": 0,
     "stops": [(55, 5), (125, 7), (210, 9), (315, 11), (410, 15)]},
    {"id": "L6", "caseInCount": 4750, "caseOutCount": 4700,
     "counter5MinAgo": 4700, "state": "stopped", "faultCode": "FC-014",
     "stops": [(100, 10), (245, 12), (446, 34)]},
    {"id": "L7", "caseInCount": 5800, "caseOutCount": 5760,
     "counter5MinAgo": 5760, "state": "inactive", "faultCode": 0,
     "stops": None},
    {"id": "L8", "caseInCount": 6300, "caseOutCount": 6250,
     "counter5MinAgo": 6250, "state": "inactive", "faultCode": 0,
     "stops": None},
    {"id": "L9", "caseInCount": 6150, "caseOutCount": 6105,
     "counter5MinAgo": 5917, "state": "running", "faultCode": 0,
     "stops": [(260, 31)]},
    {"id": "L10", "caseInCount": 4497, "caseOutCount": 4427,
     "counter5MinAgo": 4251, "state": "running", "faultCode": 0,
     "stops": [(145, 9), (370, 11)]}
]

PALLET_COUNTS = {
    "P1": {"L1": 87, "L2": 100},
    "P2": {"L3": 94, "L4": 70},
    "P3": {"L5": 68, "L6": 74},
    "P4": {"L7": 0, "L8": 0},
    "P5": {"L9": 96, "L10": 76}
}

SHIFT = {
    "current": {
        "id": "DEMO_CURRENT",
        "name": "Turno demo",
        "accumulatedCases": 93220
    },
    "previous": {
        "id": "DEMO_PREVIOUS",
        "name": "Turno anterior",
        "accumulatedCases": 151840
    },
    "supervisor": None,
    "updatedAt": None
}


def get_snapshot():
    """Entrega una copia nueva para impedir que el normalizador mute el DEMO."""
    import copy
    return copy.deepcopy({
        "horizonMinutes": HORIZON_MINUTES,
        "lines": LINES,
        "palletCounts": PALLET_COUNTS,
        "shift": SHIFT
    })
