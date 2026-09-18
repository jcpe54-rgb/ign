# Capa de datos — Fase 06

## Flujo y responsabilidades

La arquitectura respeta el flujo **fuente → normalización/cálculo → modelo →
View principal → params → templates**. `project.pct.data.get_overview_model()`
es la fachada que debe invocar la View principal una sola vez; los componentes
hijos deben recibir por `params` porciones del objeto normalizado.

| Recurso de Project Library | Responsabilidad |
| --- | --- |
| `project.pct.config` | Único origen de parámetros, líneas, rutas configurables y asociaciones. |
| `project.pct.demo` | Única fuente DEMO y construcción de timelines. |
| `project.pct.calculations` | Conversión a toneladas y velocidad para intervalos regulares o irregulares. |
| `project.pct.model` | Contratos normalizados de línea y paletizador. |
| `project.pct.data` | Fachada y selección del adapter de fuente. |

Los módulos son recursos de Project Library compatibles con el runtime Jython
de Ignition Perspective 8.1.26. No se modifican las Views en esta fase.

## Contratos entregados

Una línea expone `id`, `name`, `state`, `hasFault`, `faultCode`, contadores de
entrada/salida, `speedTonH`, pallets, modo y estado operacional separados, SKU,
orden, red, encendido, `downtime` y `quality`. `quality` distingue `ready`,
`noData` y `error`; por ello falta de comunicación no se interpreta como paro.

Un paletizador expone `id`, `name`, `state`, IDs de sus dos líneas, pallets por
línea, total y comunicación. Sus pallets proceden de un conteo propio y nunca
se vuelven a sumar desde `caseOutCount`.

El turno expone `shift` (incluidos grupo y supervisor), `current` y `previous`.
Inicio y fin permanecen sin horario definitivo y no existe cierre automático.
Esto deja el límite de turno en el futuro adapter/servicio, mientras el
histórico podrá persistirse independientemente del reinicio visible.

## Sustitución de DEMO

En una fase posterior se implementarán adapters con la misma forma cruda para:

1. lecturas actuales de Tags usando el `tagPath` y las señales de configuración;
2. ventanas y timelines mediante Tag Historian;
3. acumulados e históricos mediante Named Queries/PostgreSQL.

La selección actualmente centralizada en `project.pct.data._read_source()` se
cambiará para delegar en esos adapters. El normalizador, el modelo devuelto,
las Views y los params de templates conservarán su contrato.
