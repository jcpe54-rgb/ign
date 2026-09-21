# -*- coding: utf-8 -*-
"""Calculos de produccion compartidos por la capa de normalizacion."""


def _number(value):
    """Convierte un valor numerico a float; devuelve None si no es valido."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def tons_from_cases(cases, bale_weight_kg):
    """Convierte fardos a toneladas sin imponer redondeo de presentacion."""
    cases_value = _number(cases)
    weight_value = _number(bale_weight_kg)
    if cases_value is None or weight_value is None:
        return None
    if cases_value < 0 or weight_value <= 0:
        return None
    return cases_value * weight_value / 1000.0


def speed_ton_h(counter_now, counter_before, elapsed_minutes, bale_weight_kg):
    """Calcula Ton/h protegiendo faltantes, resets e intervalos invalidos."""
    now_value = _number(counter_now)
    before_value = _number(counter_before)
    elapsed_value = _number(elapsed_minutes)
    weight_value = _number(bale_weight_kg)

    if (now_value is None or before_value is None or
            elapsed_value is None or weight_value is None):
        return None
    if elapsed_value <= 0 or weight_value <= 0:
        return None
    if now_value < before_value:
        return None

    delta_cases = now_value - before_value
    tons = tons_from_cases(delta_cases, weight_value)
    if tons is None:
        return None
    return tons * (60.0 / elapsed_value)
