# M70.5 — Beat Grid Reconstruction

## Obiettivo

Ricostruire una griglia metrica teorica utilizzando:

- Beat seeds
- Beat period

## Input

- ElementaryMetricEvents
- Beat seeds
- Beat period

## Output

tuple[BeatReference]

## Principi

- i BeatReference non coincidono necessariamente
  con gli ElementaryMetricEvents;

- gli ElementaryMetricEvents vengono proiettati
  sulla griglia metrica ricostruita;

- la griglia deve essere deterministica e
  riproducibile.

## Effetto atteso

La rappresentazione scientifica non mostrerà più
offset prossimi a zero, ma offset positivi e
negativi rispetto alla griglia ricostruita.

Questo costituirà la prima validazione reale
dell'algoritmo di ricostruzione metrica.

## Initial Grid Reconstruction

The first beat grid is reconstructed from:

grid[0] = first beat seed

grid[n] = grid[n-1] + estimated period

The beat grid is therefore independent from
small local deviations of subsequent beat seeds.

