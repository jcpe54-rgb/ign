"""Calculos de produccion compartidos por todos los adapters y Views."""


def tons_from_cases(cases, bale_weight_kg):
    """Convierte fardos a toneladas sin imponer redondeo de presentacion."""
    if cases is None:
        return None
    return cases * bale_weight_kg / 1000.0


def speed_ton_h(counter_now, counter_before, elapsed_minutes, bale_weight_kg):
    """Calcula velocidad y protege resets, faltantes e intervalos invalidos.

    Un resultado ``None`` expresa que no existe una muestra calculable. Esto
    evita confundir falta de datos con una velocidad real de cero.
    """
    if counter_now is None or counter_before is None:
        return None
    if elapsed_minutes is None or elapsed_minutes <= 0:
        return None
    delta_cases = counter_now - counter_before
    if delta_cases < 0:
        return None
    return tons_from_cases(delta_cases, bale_weight_kg) * (60.0 / elapsed_minutes)
