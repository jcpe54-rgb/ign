# -*- coding: utf-8 -*-
"""Fachada publica de datos de Pasta Corta.

La UI consume exclusivamente get_overview_model(). Sustituir DEMO por un
adapter real en otra fase no debe alterar el contrato retornado.
"""

SOURCE = "demo"


def _read_source():
    if SOURCE == "demo":
        return project.pct.demo.get_snapshot()
    raise ValueError("Data source adapter is not configured: %s" % SOURCE)


def get_overview_model():
    """Punto publico unico para construir el modelo completo del Overview."""
    config = project.pct.config.get_config()
    source = _read_source()
    return project.pct.model.build_overview_model(source, config)
