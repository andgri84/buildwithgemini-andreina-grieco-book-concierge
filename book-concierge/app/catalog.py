"""Database dinamico dei libri, box e ordini per Andreina Grieco Book Concierge."""

from typing import Any, Dict, List, Optional
import datetime
import uuid

# Catalogo dei Libri
BOOKS_DATABASE: Dict[str, Dict[str, Any]] = {
    "regina_cambiante": {
        "id": "regina_cambiante",
        "title": "La Regina Cambiante",
        "author": "Andreina Grieco",
        "publisher": "Plesio Editore",
        "type": "Standalone",
        "genre": "Dark / Epic Fantasy storico",
        "setting": "Regno di Campania, fine Settecento",
        "synopsis": (
            "Sul finire del Settecento, il Regno di Campania vive nel terrore dei cambianti, "
            "mutanti emarginati capaci di evolvere e trasformarsi a seconda dei loro desideri reconditi. "
            "La principessa Valeria è stata addestrata a combatterli, ma quando il fratello usurpa il trono, "
            "scopre che lei stessa sta mutando. Per padroneggiare i suoi poteri dovrà affidarsi al feroce "
            "Demone del Lago Fusaro, la cui unica intenzione è trasformare il suo addestramento in un inferno."
        ),
        "themes": ["Metamorfosi", "Lotta per il trono", "Mostro vs Umano", "Segreti dinastici"],
        "pages": 320,
    },
    "yohnna_1": {
        "id": "yohnna_1",
        "title": "Yohnna e il Baluardo dei Deserti",
        "volume": 1,
        "author": "Andreina Grieco",
        "publisher": "Edikit",
        "type": "Saga di Yohnna (Vol. 1)",
        "genre": "Epic Fantasy / Desert Fantasy",
        "setting": "Le vaste e spietate terre sabbiose del Baluardo",
        "synopsis": (
            "Primo volume della saga che vede protagonista il giovane Yohnna alle prese con le sfide, "
            "i misteri e la difesa estrema del Baluardo tra le sabbie aride e le minacce che incombono "
            "sulle terre del deserto."
        ),
        "themes": ["Viaggio dell'eroe", "Sopravvivenza e baluardo", "Destino e sabbie"],
        "pages": 280,
    },
    "yohnna_2": {
        "id": "yohnna_2",
        "title": "Yohnna e le Lacrime di Israfil",
        "volume": 2,
        "author": "Andreina Grieco",
        "publisher": "Edikit",
        "type": "Saga di Yohnna (Vol. 2)",
        "genre": "Epic Fantasy / Desert Fantasy",
        "setting": "Oltre il deserto, il richiamo e il mito di Israfil",
        "synopsis": (
            "Secondo volume che porta a compimento e approfondisce l'arco narrativo di Yohnna, "
            "rivelando la natura e il mistero delle Lacrime di Israfil e le conseguenze delle scelte "
            "fatte al Baluardo."
        ),
        "themes": ["Mito e rivelazione", "Conflitto epico", "Evoluzione spirituale e sacrifici"],
        "pages": 310,
    },
}

# Catalogo delle Box Speciali con Card da Collezione e Copie Autografate
BOXES_DATABASE: Dict[str, Dict[str, Any]] = {
    "box_baluardo": {
        "id": "box_baluardo",
        "name": "Box Baluardo",
        "base_price": 14.0,
        "books": ["Yohnna e il Baluardo dei Deserti (Vol. 1) OPPURE Yohnna e le Lacrime di Israfil (Vol. 2)"],
        "cards_included": 1,
        "description": (
            "Un volume singolo della saga a scelta tra Yohnna 1 (per iniziare) o Yohnna 2 (se hai già il primo), "
            "copia autografata con dedica personalizzata + card da collezione esclusiva in omaggio."
        ),
    },
    "box_principessa": {
        "id": "box_principessa",
        "name": "Box Principessa",
        "base_price": 18.0,
        "books": ["La Regina Cambiante (Standalone)"],
        "cards_included": 2,
        "description": (
            "Il romanzo 'La Regina Cambiante' autografato con dedica personalizzata + 2 card da collezione "
            "dei personaggi in omaggio."
        ),
    },
    "box_regina": {
        "id": "box_regina",
        "name": "Box Regina",
        "base_price": 20.0,
        "books": ["La Regina Cambiante (Standalone)"],
        "cards_included": 5,
        "description": (
            "L'edizione speciale di 'La Regina Cambiante' autografata con dedica personalizzata + set completo "
            "di ben 5 card da collezione dei personaggi e ambientazioni in omaggio."
        ),
    },
    "box_troni_deserti": {
        "id": "box_troni_deserti",
        "name": "Box Troni e Deserti",
        "base_price": 32.0,
        "books": [
            "La Regina Cambiante (Standalone)",
            "Yohnna e il Baluardo dei Deserti (Vol. 1)",
        ],
        "cards_included": 3,
        "description": (
            "L'incontro dei due universi dell'autrice: entrambi i libri d'esordio autografati con dedica "
            "personalizzata + selezione di card da collezione."
        ),
    },
    "box_sovrano_sabbie": {
        "id": "box_sovrano_sabbie",
        "name": "Box Sovrano delle Sabbie",
        "base_price": 26.0,
        "books": [
            "Yohnna e il Baluardo dei Deserti (Vol. 1)",
            "Yohnna e le Lacrime di Israfil (Vol. 2)",
        ],
        "cards_included": 2,
        "description": (
            "La saga completa di Yohnna (Vol. 1 e Vol. 2) autografata con dedica personalizzata + card da collezione."
        ),
    },
    "box_imperatrice": {
        "id": "box_imperatrice",
        "name": "Box Imperatrice",
        "base_price": 30.0,
        "books": [
            "La Regina Cambiante (Standalone)",
            "Yohnna e il Baluardo dei Deserti (Vol. 1)",
            "Yohnna e le Lacrime di Israfil (Vol. 2)",
        ],
        "cards_included": 7,
        "description": (
            "L'intera bibliografia dell'autrice (tutti e 3 i libri autografati con dedica personalizzata) "
            "+ set supremo con tutte le card da collezione."
        ),
    },
}

# Archivio ordini in memoria / mock database (pronto per Firestore)
ORDERS_DATABASE: List[Dict[str, Any]] = []

AUTHOR_CONTACTS = {
    "instagram": "@andreina_grieco_autrice",
    "vinted": "andreinagrieco_libri",
    "email": "andreina.grieco.autrice@gmail.com",
    "paypal": "paypal.me/andreinagrieco",
    "iban": "IT00X0000000000000000000000 (disponibile su richiesta)",
}
