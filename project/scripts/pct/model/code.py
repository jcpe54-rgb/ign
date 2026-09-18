"""Normalizacion del contrato consumido por Views y Templates."""


def _communication(ready=True, no_data=False, error=False):
    return {"ready": ready, "noData": no_data, "error": error}


def normalize_line(raw, line_config, config, timeline):
    speed = project.pct.calculations.speed_ton_h(
        raw.get("caseOutCount"), raw.get("counter5MinAgo"),
        config["speedWindowMinutes"], config["baleWeightKg"])
    state = raw.get("state", "noData")
    no_data = state == "noData"
    return {
        "id": line_config["id"],
        "name": line_config["name"],
        "state": state,
        "hasFault": raw.get("faultCode", 0) != 0,
        "faultCode": raw.get("faultCode", 0),
        "caseInCount": raw.get("caseInCount"),
        "caseOutCount": raw.get("caseOutCount"),
        "speedTonH": None if speed is None else round(speed, 2),
        "palletCount": raw.get("palletCount", 0),
        "operatingMode": raw.get("operatingMode"),
        "operatingState": raw.get("operatingState", state),
        "sku": raw.get("sku"),
        "workOrder": raw.get("workOrder"),
        "networkStatus": raw.get("networkStatus", "connected"),
        "powerOnTime": raw.get("powerOnTime"),
        "downtime": {
            "stopCount": 0 if raw.get("stops") is None else len(raw["stops"]),
            "stoppedMinutes": 0 if raw.get("stops") is None else
                              sum(item[1] for item in raw["stops"]),
            "timeline": timeline
        },
        "quality": _communication(not no_data, no_data, False)
    }


def normalize_palletizer(item, counts):
    line1, line2 = item["lineIds"]
    pallets1 = counts.get(line1, 0)
    pallets2 = counts.get(line2, 0)
    return {
        "id": item["id"], "name": item["name"], "state": "active"
        if pallets1 + pallets2 > 0 else "inactive",
        "line1": line1, "line2": line2,
        "palletsLine1": pallets1, "palletsLine2": pallets2,
        "totalPallets": pallets1 + pallets2,
        "communication": _communication()
    }
