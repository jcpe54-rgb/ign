"""Fachada unica de datos para las Views principales.

Cambiar ``SOURCE`` y la funcion ``_read_source`` es el unico punto necesario
para introducir adapters de Tags, Historian o Named Queries en otra fase.
"""

SOURCE = "demo"


def _read_source():
    if SOURCE == "demo":
        return project.pct.demo.get_snapshot()
    raise ValueError("Data source adapter is not configured: %s" % SOURCE)


def get_overview_model():
    config = project.pct.config.get_config()
    source = _read_source()
    raw_by_id = dict((item["id"], item) for item in source["lines"])
    lines = []
    for line_config in config["lines"]:
        raw = raw_by_id[line_config["id"]]
        counts = source["palletCounts"][line_config["palletizerId"]]
        raw["palletCount"] = counts.get(line_config["id"], 0)
        lines.append(project.pct.model.normalize_line(
            raw, line_config, config, raw.get("timeline", [])))

    palletizers = []
    for item in config["palletizers"]:
        palletizers.append(project.pct.model.normalize_palletizer(
            item, source["palletCounts"][item["id"]]))

    return {
        "lines": lines,
        "palletizers": palletizers,
        "shift": source["shift"],
        "kpis": {
            "operatingLines": sum(1 for line in lines
                                  if line["state"] == "running"),
            "totalLines": config["lineCount"],
            "activePalletizers": sum(1 for item in palletizers
                                      if item["state"] == "active"),
            "totalPalletizers": config["palletizerCount"]
        }
    }
