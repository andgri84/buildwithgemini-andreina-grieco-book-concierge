# My agent: Andreina Grieco Book Concierge

One-liner: Un agente conversazionale che aiuta i lettori a scoprire e acquistare i romanzi fantasy di Andreina Grieco ("La Regina Cambiante", "Yohnna e il Baluardo dei Deserti", "Yohnna e le Lacrime di Israfil") con box esclusive, copie autografate, card da collezione, dediche personalizzate e calcolo dinamico delle spedizioni.

Tool coverage:
- Memory: Ricorda il nome del lettore per la dedica personalizzata, preferenze di lettura/trope, carrello/box selezionata e recapiti di spedizione.
- Tools:
  - `list_boxes()`: Restituisce il catalogo dinamico delle 6 box con prezzi base, contenuti (libri + card) e opzioni.
  - `get_book_details(title)`: Schede dettagliate su trama, ambientazione e personaggi per ciascun libro.
  - `calculate_shipping(box_id, shipping_method)`: Calcola il totale in base al metodo scelto (Poste Non Tracciato incluso nel prezzo base, Poste Tracciato +2€, formula Vinted con sconto di 3€ sul prezzo base per compensare la spedizione Vinted).
  - `save_order(customer_name, dedication_name, shipping_address, box_id, shipping_method, payment_preference, contact_info)`: Salva l'ordine nel database dinamico e genera il riepilogo con istruzioni di pagamento (PayPal / Bonifico) o finalizzazione contatto (Instagram, Vinted, Email).
- Catalog/UI: Catalogo interattivo renderizzato come schede/card per le 6 Box:
  1. Box Baluardo (Yohnna 1 o Yohnna 2 + card): 14 €
  2. Box Principessa (La Regina Cambiante + 2 card): 18 €
  3. Box Regina (La Regina Cambiante + 5 card): 20 €
  4. Box Troni e Deserti (La Regina Cambiante + Yohnna 1 + card): 32 €
  5. Box Sovrano delle Sabbie (Yohnna 1 + Yohnna 2 + card): 26 €
  6. Box Imperatrice (Tutti e 3 i libri + tutte le card): 30 €
- Image gen: Generazione anteprima visiva della card o della dedica calligrafica personalizzata.
- Sandbox: Calcolo quote Vinted (acconto PayPal = Prezzo Box − 3€; annuncio Vinted riservato = 1€ + spedizione Vinted ~3€, così il lettore non paga due volte la spedizione e il totale resta allineato).

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch (pick what fits): Calcolo quote Vinted, database Firestore per persistenza ordini, tracciamento Cloud Trace.
