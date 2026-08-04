# M70 — Beat Reconstruction Engine

## Obiettivo

Ricostruire i BeatReference a partire dagli
ElementaryMetricEvents osservati.

Il BeatReference rappresenta il beat teorico
dell'ensemble.

Non rappresenta un evento osservato.

## Input

tuple[ElementaryMetricEvent]

## Output

tuple[BeatReference]

## Responsabilità

- ricostruire la griglia metrica teorica;
- generare BeatReference indipendenti dagli eventi;
- preservare l'ordine temporale;
- produrre un riferimento utilizzabile dal
  MetricClusterBuilder.

## Non responsabilità

- clustering;
- costruzione dei Pulse;
- ricostruzione della InternalMetricTimeline;
- visualizzazione.

## Stato

Placeholder.
L'algoritmo scientifico verrà definito
prima dell'implementazione.
