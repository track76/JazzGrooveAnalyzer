# M70 — Beat Reference Reconstruction

## Problema

L'attuale BeatReferenceBuilder costruisce un BeatReference
per ogni ElementaryMetricEvent copiandone il timestamp.

Conseguenze:

ElementaryMetricEvent
        ↓
BeatReference(timestamp = event.timestamp)
        ↓
MetricOffset = 0 ms

La visualizzazione scientifica produce quindi una
traiettoria completamente piatta.

## Contraddizione

La documentazione di BeatReference afferma:

"It is inferred from the recognised metric structure."

Questa affermazione non è rispettata
dall'implementazione corrente.

## Decisione

BeatReference NON deve essere derivato direttamente
dagli ElementaryMetricEvents.

BeatReference deve essere ricostruito dalla
struttura metrica dell'ensemble.

## Stato

Nessuna implementazione.

Prima viene definita la teoria,
poi verrà modificata la pipeline.
