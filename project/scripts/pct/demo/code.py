"""Fuente DEMO unica, sin dependencias de componentes Perspective."""

HORIZON_MINUTES = 480


def _timeline(stops):
    """Genera segmentos contiguos; cada duracion de paro se conserva exacta."""
    segments = []
    cursor = 0
    for start, duration in stops:
        if start > cursor:
            segments.append({"state": "running", "startMinute": cursor,
                             "durationMinutes": start - cursor})
        segments.append({"state": "stopped", "startMinute": start,
                         "durationMinutes": duration})
        cursor = start + duration
    if cursor < HORIZON_MINUTES:
        segments.append({"state": "running", "startMinute": cursor,
                         "durationMinutes": HORIZON_MINUTES - cursor})
    return segments


def _inactive_timeline():
    return [{"state": "inactive", "startMinute": 0,
             "durationMinutes": HORIZON_MINUTES}]


# counter5MinAgo hace explicito el origen de cada velocidad DEMO. El codigo de
# falla es opaco: unicamente se aplica la regla contractual de cero/no cero.
LINES = [
    {"id": "L1", "caseOutCount": 11620, "counter5MinAgo": 11415,
     "state": "running", "faultCode": 0, "stops": []},
    {"id": "L2", "caseOutCount": 9840, "counter5MinAgo": 9840,
     "state": "stopped", "faultCode": 0, "stops": [(90, 22), (310, 25)]},
    {"id": "L3", "caseOutCount": 10950, "counter5MinAgo": 10756,
     "state": "running", "faultCode": 0, "stops": [(130, 8), (350, 13)]},
    {"id": "L4", "caseOutCount": 10380, "counter5MinAgo": 10199,
     "state": "running", "faultCode": 0, "stops": []},
    {"id": "L5", "caseOutCount": 10760, "counter5MinAgo": 10559,
     "state": "running", "faultCode": 0,
     "stops": [(55, 5), (125, 7), (210, 9), (315, 11), (410, 15)]},
    {"id": "L6", "caseOutCount": 8920, "counter5MinAgo": 8920,
     "state": "fault", "faultCode": 1,
     "stops": [(100, 10), (245, 12), (390, 12)]},
    {"id": "L7", "caseOutCount": 0, "counter5MinAgo": 0,
     "state": "inactive", "faultCode": 0, "stops": None},
    {"id": "L8", "caseOutCount": 0, "counter5MinAgo": 0,
     "state": "inactive", "faultCode": 0, "stops": None},
    {"id": "L9", "caseOutCount": 10540, "counter5MinAgo": 10352,
     "state": "running", "faultCode": 0, "stops": [(260, 31)]},
    {"id": "L10", "caseOutCount": 10210, "counter5MinAgo": 10034,
     "state": "running", "faultCode": 0, "stops": [(145, 9), (370, 11)]}
]

PALLET_COUNTS = {
    "P1": {"L1": 87, "L2": 100},
    "P2": {"L3": 94, "L4": 70},
    "P3": {"L5": 68, "L6": 74},
    "P4": {"L7": 0, "L8": 0},
    "P5": {"L9": 96, "L10": 76}
}

SHIFT = {
    "shift": {"id": "DEMO", "name": "Turno demo", "start": None,
              "end": None, "group": None, "supervisor": None},
    "current": {"accumulatedCases": 93220, "accumulatedTons": 1118.64,
                "palletCount": 665},
    "previous": {"accumulatedCases": 151840,
                 "accumulatedTons": 1822.08}
}


def get_snapshot():
    """Entrega datos fuente nuevos para que el normalizador no mute el DEMO."""
    import copy
    snapshot = copy.deepcopy({"lines": LINES,
                              "palletCounts": PALLET_COUNTS,
                              "shift": SHIFT})
    for line in snapshot["lines"]:
        line["timeline"] = timeline_for(line)
    return snapshot


def timeline_for(raw_line):
    if raw_line["stops"] is None:
        return _inactive_timeline()
    return _timeline(raw_line["stops"])
