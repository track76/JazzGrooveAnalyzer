# BMIG / DMIG — preregistrazione diagnostica

Protocollo registrato prima dei nuovi fit e delle differenze. Studi e dati precedenti già noti: nessuna rivendicazione di cecità. Nessun metodo congelato come autorità canonica.

Unità primaria: singola misura M33–M48, n=0,1,2,3 corrispondenti ai beat1–4. Si riusa l’eleggibilità per quarto già documentata: nearest-PLP continuo attraverso stanghette, rappresentante dello strumento più vicino al suo PLP; parità eventi risolta da timestamp precedente poi ID. Nessuna nuova selezione dipendente dal fit o dall’altro strumento. 63 Bass e 64 Drum-exclusive interni originali preservati; evento Drum anticipante Q195 fuori dalle 16 misure conservato come contesto, non riassociato. A/B/C restano metadati, non pesi del fit.

Supporto: strumento eleggibile se e solo se almeno 3 quarti distinti su4 osservati. Misura confrontabile se entrambi eleggibili. Nessuna ulteriore esclusione per residuo, segno, periodo o fase. Invalidità numerica (A/T non finiti o T<=0) impedisce uso del fit e viene distinta da insufficienza osservativa.

Fit identico per i due strumenti: T=mediana di tutte le pendenze (t_j−t_i)/(n_j−n_i); A=mediana(t_i−n_i*T). Theil–Sen con intercetto congiunto, nessun sottocampionamento. Mediane pari: media dei due centrali. Tutte le3 o4 osservazioni conservate; nessuna rimozione/iterazione. Input funzione: soltanto timestamp dello strumento e indici n. PLP_time non entra nel fit. Float64; timestamp originali restano stringhe immutate. T insecondi, BPM=60/T, n=0 all’inizio misura.

Tutti i4 punti validi sono stime del modello, anche quando hanno supporto osservato. Con3/4 si ricostruisce esattamente il solo punto senza osservazione: ESTIMATED_GRID_POINT / OBSERVED_ONSET=NO. Nessun punto generato con<=2/4. Extrapolazione se manca beat1 o4 viene marcata. Griglia dell’unico strumento eleggibile può essere mostrata in misura non confrontabile, ma nessun GRID_DELTA o valore primario.

Residui=onset−griglia; mediana, medianaassoluta e massimoassoluto inms. Nessuna soglia di qualità posthoc. Delta=BMIG−DMIG: negativo Bass ahead, positivo Bass behind, zero EXACT. MEASURE_GRID_DELTA=mediana dei4 delta; ogni misura eleggibile contribuisce UN solo valore e peso uguale al globale. Nessuna ponderazione per4/4, numero aggiuntivi o precisione A/B/C. Nessuna indipendenza statistica fra misure assunta e nessun test inferenziale.

Primario: mediana delle mediane misura, Q1/Q3 con quantili lineari, IQR,min,max e segni. Tukeyfences1.5IQR, punti esterni conservati. Sensibilità: solo misure con entrambi4/4, senza modificare la primaria. Stabilità del segno: YES se le due mediane disponibili hanno stesso segnononzero, NO se segniopposti, NOT ENOUGH DATA se sensibilitàvuota o mediana esattamentezero (nessuna soglia NEAR_ZERO). Conclusione primaria usa segnomediana; se sensitività discordante o non valutabile, NO STABLE DIRECTIONAL RESULT con segni descritti separatamente. Nessuna selezione a posteriori della popolazione preferita.

Confronto precedente: BIPG/DIPG primario4misure, mediana su64 punti +8.858ms, mantenuto. Nuova unità=misura e criterio supporto più locale. La deriva non può propagarsi oltre la misura nel nuovo modello; ciò non prova una maggiore accuratezza fisica o un’intenzione esecutiva. Nessuno score, audio, PLP strumentale, correzione, freeze, bootstrap, commit o push.
