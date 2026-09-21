# -*- coding: utf-8 -*-
"""Normalizacion y construccion del contrato del Overview."""

ALLOWED_LINE_STATES = ("running", "stopped", "inactive", "noData")
ALLOWED_TIMELINE_STATES = ("running", "stopped", "inactive")


def _safe_state(value):
    if value in ALLOWED_LINE_STATES:
        return value
    return "noData"


def _fault_present(fault_code):
    return fault_code not in (None, 0, "0", "")


def _build_timeline(raw_line, horizon_minutes):
    state = _safe_state(raw_line.get("state"))
    if state == "inactive":
        return [{
            "state": "inactive",
            "startMinute": 0,
            "durationMinutes": horizon_minutes
        }]

    stops = raw_line.get("stops")
    if stops is None:
        return []

    segments = []
    cursor = 0
    for item in stops:
        try:
            start = int(item[0])
            duration = int(item[1])
        except (TypeError, ValueError, IndexError):
            continue

        if start < cursor or duration <= 0 or start >= horizon_minutes:
            continue

        if start > cursor:
            segments.append({
                "state": "running",
                "startMinute": cursor,
                "durationMinutes": start - cursor
            })

        stop_end = min(start + duration, horizon_minutes)
        segments.append({
            "state": "stopped",
            "startMinute": start,
            "durationMinutes": stop_end - start
        })
        cursor = stop_end

    if cursor < horizon_minutes:
        tail_state = "stopped" if state == "stopped" else "running"
        segments.append({
            "state": tail_state,
            "startMinute": cursor,
            "durationMinutes": horizon_minutes - cursor
        })

    return segments


def _downtime(raw_line, horizon_minutes):
    timeline = _build_timeline(raw_line, horizon_minutes)
    stop_count = 0
    stopped_minutes = 0
    for segment in timeline:
        if segment["state"] == "stopped":
            stop_count += 1
            stopped_minutes += segment["durationMinutes"]

    return {
        "stopCount": stop_count,
        "stoppedMinutes": stopped_minutes,
        "timeline": timeline
    }


def normalize_line(raw_line, line_config, pallet_count, config, horizon_minutes):
    """Normaliza una linea sin exponer detalles de la fuente."""
    state = _safe_state(raw_line.get("state"))
    fault_code = raw_line.get("faultCode", 0)
    has_fault = _fault_present(fault_code)

    speed = project.pct.calculations.speed_ton_h(
        raw_line.get("caseOutCount"),
        raw_line.get("counter5MinAgo"),
        config["speedWindowMinutes"],
        config["baleWeightKg"]
    )

    # visualState es un derivado de presentacion. No reemplaza el estado
    # operativo contractual y nunca se usa en timeline.
    visual_state = state
    if state == "stopped" and has_fault:
        visual_state = "fault"

    return {
        "id": line_config["id"],
        "name": line_config["displayName"],
        "state": state,
        "hasFault": has_fault,
        "faultCode": fault_code,
        "caseInCount": raw_line.get("caseInCount"),
        "caseOutCount": raw_line.get("caseOutCount"),
        "speedTonH": None if speed is None else round(speed, 2),
        "palletCount": pallet_count,
        "downtime": _downtime(raw_line, horizon_minutes),

        # Campos de compatibilidad visual para la conexion posterior.
        "operatingMode": raw_line.get("operatingMode"),
        "operatingState": state,
        "sku": raw_line.get("sku"),
        "wo": raw_line.get("wo"),
        "quality": None if state == "noData" else "good",
        "visualState": visual_state
    }


def normalize_palletizer(item, counts):
    """Normaliza un paletizador a partir de su asociacion configurada."""
    line1 = item["lineIds"][0]
    line2 = item["lineIds"][1]
    pallets1 = counts.get(line1, 0)
    pallets2 = counts.get(line2, 0)
    total = pallets1 + pallets2

    return {
        "id": item["id"],
        "name": item["displayName"],
        "state": "active" if total > 0 else "inactive",
        "line1": line1,
        "line2": line2,
        "palletsLine1": pallets1,
        "palletsLine2": pallets2,
        "totalPallets": total,

        # Compatibilidad visual para la conexion posterior.
        "palletCount": total,
        "quality": "good",
        "visualState": "running" if total > 0 else "inactive"
    }


def _build_groups(config, lines_by_id, palletizers_by_id):
    groups = []
    index = 1
    for palletizer_config in config["palletizers"]:
        line1 = palletizer_config["lineIds"][0]
        line2 = palletizer_config["lineIds"][1]
        groups.append({
            "id": "G%d" % index,
            "lineOdd": lines_by_id[line1],
            "palletizer": palletizers_by_id[palletizer_config["id"]],
            "lineEven": lines_by_id[line2]
        })
        index += 1
    return groups


def _build_kpis(lines, palletizers, shift, config):
    running_lines = sum(1 for line in lines if line["state"] == "running")
    active_palletizers = sum(
        1 for item in palletizers if item["state"] == "active"
    )

    current_cases = shift.get("current", {}).get("accumulatedCases")
    previous_cases = shift.get("previous", {}).get("accumulatedCases")
    current_tons = project.pct.calculations.tons_from_cases(
        current_cases, config["baleWeightKg"]
    )
    previous_tons = project.pct.calculations.tons_from_cases(
        previous_cases, config["baleWeightKg"]
    )

    return [
        {
            "id": "operatingLines",
            "label": "LÍNEAS OPERANDO",
            "value": "%d de %d" % (running_lines, config["lineCount"]),
            "unit": ""
        },
        {
            "id": "activePalletizers",
            "label": "PALETIZADORES ACTIVOS",
            "value": "%d de %d" % (
                active_palletizers, config["palletizerCount"]
            ),
            "unit": ""
        },
        {
            "id": "previousShift",
            "label": "TURNO ANTERIOR",
            "value": previous_cases,
            "unit": "Fardos"
        },
        {
            "id": "previousProduction",
            "label": "PRODUCCIÓN ANTERIOR",
            "value": None if previous_tons is None else round(previous_tons, 2),
            "unit": "Ton"
        },
        {
            "id": "currentShift",
            "label": "TURNO ACTUAL",
            "value": current_cases,
            "unit": "Fardos"
        },
        {
            "id": "accumulatedProduction",
            "label": "PRODUCCIÓN ACUMULADA",
            "value": None if current_tons is None else round(current_tons, 2),
            "unit": "Ton"
        }
    ]


def build_overview_model(source, config):
    """Construye una sola vez el modelo completo consumible por Overview."""
    raw_by_id = dict((item["id"], item) for item in source["lines"])
    horizon_minutes = source.get("horizonMinutes", 480)

    lines = []
    lines_by_id = {}
    for line_config in config["lines"]:
        line_id = line_config["id"]
        raw_line = raw_by_id.get(line_id, {"id": line_id, "state": "noData"})
        counts = source["palletCounts"].get(line_config["palletizerId"], {})
        line = normalize_line(
            raw_line,
            line_config,
            counts.get(line_id, 0),
            config,
            horizon_minutes
        )
        lines.append(line)
        lines_by_id[line_id] = line

    palletizers = []
    palletizers_by_id = {}
    for item in config["palletizers"]:
        palletizer = normalize_palletizer(
            item,
            source["palletCounts"].get(item["id"], {})
        )
        palletizers.append(palletizer)
        palletizers_by_id[item["id"]] = palletizer

    shift = source.get("shift", {})
    return {
        "lines": lines,
        "palletizers": palletizers,
        "groups": _build_groups(config, lines_by_id, palletizers_by_id),
        "kpis": _build_kpis(lines, palletizers, shift, config),
        "context": {
            "shift": shift.get("current", {}),
            "supervisor": shift.get("supervisor"),
            "updatedAt": shift.get("updatedAt")
        }
    }
