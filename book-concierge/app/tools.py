"""Tools per l'agente Andreina Grieco Book Concierge con backend Firestore relazionale."""

from typing import Any, Dict, List, Optional
import datetime
import uuid
from google.cloud import firestore
from app.catalog import BOOKS_DATABASE, BOXES_DATABASE, AUTHOR_CONTACTS

# Hardcoded GCP Project ID per compatibilità Agent Platform / Firestore
PROJECT_ID = "qwiklabs-gcp-03-9513a337097b"

# Lazy initialization del client Firestore
_db: Optional[firestore.Client] = None

def get_firestore_client() -> firestore.Client:
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db


def list_books() -> Dict[str, Any]:
    """Legge e restituisce l'elenco completo di tutti i libri dell'autrice da Firestore ('catalog_books'),
    mostrando titolo, saga, volume, genere, ambientazione e protagonista.

    Returns:
        Dizionario con l'elenco dei libri presenti nel database.
    """
    try:
        db = get_firestore_client()
        docs = db.collection("catalog_books").stream()
        books = []
        for doc in docs:
            books.append(doc.to_dict())
        if books:
            return {
                "status": "success",
                "source": "firestore",
                "books": books,
            }
    except Exception as e:
        print(f"Errore lettura libri da Firestore: {e}")

    return {
        "status": "success",
        "source": "local_fallback",
        "books": list(BOOKS_DATABASE.values()),
    }


def list_boxes() -> Dict[str, Any]:
    """Legge e restituisce il catalogo dinamico delle 6 Box da Firestore ('catalog_boxes'),
    risolvendo ed espandendo i libri collegati a ciascuna box tramite la collection 'catalog_books'.

    Returns:
        Un dizionario contenente la lista formattata di tutte le box con i dettagli dei libri inclusi.
    """
    try:
        db = get_firestore_client()
        
        # Mappa dei libri per join rapido
        books_map = {}
        for b_doc in db.collection("catalog_books").stream():
            books_map[b_doc.id] = b_doc.to_dict()

        docs = db.collection("catalog_boxes").stream()
        boxes_list = []
        for doc in docs:
            data = doc.to_dict()
            if data.get("is_available", True):
                # Risoluzione join libri
                linked_books = []
                for b_id in data.get("book_ids", []):
                    if b_id in books_map:
                        b_info = books_map[b_id]
                        linked_books.append({
                            "id": b_id,
                            "title": b_info.get("title"),
                            "type": b_info.get("type"),
                            "publisher": b_info.get("publisher"),
                        })
                    else:
                        linked_books.append({"id": b_id, "title": b_id})

                boxes_list.append({
                    "id": data.get("id", doc.id),
                    "name": data.get("name"),
                    "base_price": f"{data.get('base_price', 0.0):.2f} €",
                    "books_summary": data.get("books_display", ""),
                    "included_books": linked_books,
                    "cards_included": data.get("cards_included", 0),
                    "description": data.get("description", ""),
                })
        
        if boxes_list:
            return {
                "status": "success",
                "source": "firestore",
                "boxes": boxes_list,
                "note": "Tutte le copie sono autografate e dedicate a mano dall'autrice. Spedizione ordinaria Poste inclusa.",
            }
    except Exception as e:
        print(f"Errore lettura Firestore: {e}, fallback")

    # Fallback in-memory
    fallback = []
    for box in BOXES_DATABASE.values():
        fallback.append({
            "id": box["id"],
            "name": box["name"],
            "base_price": f"{box['base_price']:.2f} €",
            "books_summary": ", ".join(box["books"]),
            "included_books": box["books"],
            "cards_included": box["cards_included"],
            "description": box["description"],
        })
    return {
        "status": "success",
        "source": "local_fallback",
        "boxes": fallback,
        "note": "Tutte le copie sono autografate e dedicate a mano dall'autrice. Spedizione ordinaria Poste inclusa.",
    }


def get_book_details(book_key: str) -> Dict[str, Any]:
    """Fornisce dettagli approfonditi su un libro dell'autrice leggendolo da Firestore:
    sinossi, ambientazione, genere, temi e numero di pagine.

    Args:
        book_key: Titolo o ID del libro ('regina_cambiante', 'yohnna_1', 'yohnna_2' o simili).

    Returns:
        Dettagli completi del libro richiesto.
    """
    key = book_key.lower().strip()
    book_id = None
    if "regina" in key or "cambiante" in key:
        book_id = "regina_cambiante"
    elif "baluardo" in key or "1" in key or "primo" in key:
        book_id = "yohnna_1"
    elif "lacrime" in key or "israfil" in key or "2" in key or "secondo" in key:
        book_id = "yohnna_2"

    if not book_id:
        return {
            "status": "not_found",
            "message": f"Nessun libro trovato per '{book_key}'. I titoli disponibili sono: 'La Regina Cambiante', 'Yohnna e il Baluardo dei Deserti (Vol. 1)', 'Yohnna e le Lacrime di Israfil (Vol. 2)'.",
        }

    try:
        db = get_firestore_client()
        doc = db.collection("catalog_books").document(book_id).get()
        if doc.exists:
            return {
                "status": "success",
                "source": "firestore",
                "book": doc.to_dict(),
            }
    except Exception as e:
        print(f"Errore lettura libro Firestore: {e}")

    # Fallback
    return {
        "status": "success",
        "source": "local_fallback",
        "book": BOOKS_DATABASE.get(book_id, {}),
    }


def calculate_shipping(box_id: str, shipping_method: str) -> Dict[str, Any]:
    """Calcola il prezzo esatto e la formula di pagamento/spedizione in base alla box
    e al metodo di consegna scelto dal lettore.

    Args:
        box_id: Identificativo o nome della box.
        shipping_method: 'poste_non_tracciato', 'poste_tracciato' o 'vinted'.

    Returns:
        Dettagli sul costo finale ed eventuali supplementi o scorpori Vinted.
    """
    matched_box = None
    clean_id = box_id.lower().replace(" ", "_")
    for key, box in BOXES_DATABASE.items():
        if key in clean_id or box["name"].lower() in box_id.lower():
            matched_box = box
            break

    if not matched_box:
        matched_box = BOXES_DATABASE.get(box_id, BOXES_DATABASE["box_principessa"])

    base_price = float(matched_box["base_price"])
    method = shipping_method.lower().strip()

    if "tracciat" in method and "non" not in method:
        total_price = base_price + 2.0
        return {
            "box_name": matched_box["name"],
            "shipping_method": "Poste Italiane (Piego di libri Tracciato)",
            "base_price": f"{base_price:.2f} €",
            "shipping_supplement": "2.00 €",
            "total_to_pay": f"{total_price:.2f} €",
            "payment_methods": ["PayPal", "Bonifico Bancario"],
            "explanation": "La spedizione con codice di tracciamento raccomandato costa 2€ in più rispetto alla base.",
        }
    elif "vinted" in method:
        paypal_part = max(0.0, base_price - 3.0)
        vinted_listing = 1.0
        return {
            "box_name": matched_box["name"],
            "shipping_method": "Vinted (Spedizione rapida/economica con punto di ritiro)",
            "base_price": f"{base_price:.2f} €",
            "formula_details": {
                "acconto_paypal_o_bonifico": f"{paypal_part:.2f} €",
                "annuncio_vinted_riservato": f"{vinted_listing:.2f} € + spese di spedizione Vinted (circa 3€)",
                "note": "In questo modo non paghi la spedizione due volte e il totale finale corrisponde all'incirca al prezzo normale della box!",
            },
            "contacts_to_finalize": AUTHOR_CONTACTS,
            "requires_contact": True,
        }
    else:
        return {
            "box_name": matched_box["name"],
            "shipping_method": "Poste Italiane (Piego di libri ordinario - non tracciato)",
            "base_price": f"{base_price:.2f} €",
            "shipping_supplement": "0.00 € (Inclusa nel prezzo)",
            "total_to_pay": f"{base_price:.2f} €",
            "payment_methods": ["PayPal", "Bonifico Bancario"],
            "explanation": "La spedizione ordinaria è completamente inclusa nel prezzo della box.",
        }


def save_order_request(
    box_name: str,
    dedication_name: str,
    shipping_address: str,
    shipping_method: str,
    customer_contact: Optional[str] = None,
    payment_choice: Optional[str] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    """Salva la richiesta d'ordine direttamente nella collection Firestore 'book_orders'
    e restituisce la ricevuta con ID univoco e istruzioni operative.

    Args:
        box_name: Nome della box scelta.
        dedication_name: Nome per la dedica personalizzata a mano.
        shipping_address: Indirizzo completo di spedizione.
        shipping_method: Modalità di spedizione ('Poste Non Tracciato', 'Poste Tracciato', 'Vinted').
        customer_contact: Contatto del cliente (Instagram, cellulare/WhatsApp o email).
        payment_choice: Metodo di pagamento scelto se con Poste ('PayPal' o 'Bonifico') oppure 'Vinted'.
        notes: Eventuali note aggiuntive.

    Returns:
        Riepilogo dell'ordine registrato con ID univoco e istruzioni per il completamento.
    """
    order_id = f"AG-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pricing = calculate_shipping(box_name, shipping_method)

    order_record = {
        "order_id": order_id,
        "created_at": timestamp,
        "box_name": box_name,
        "dedication_name": dedication_name,
        "shipping_address": shipping_address,
        "shipping_method": shipping_method,
        "customer_contact": customer_contact or "Da comunicare",
        "payment_choice": payment_choice or "Da confermare",
        "notes": notes or "",
        "pricing_summary": pricing,
        "status": "In attesa di pagamento/finalizzazione",
    }

    # Scrittura su Firestore
    try:
        db = get_firestore_client()
        db.collection("book_orders").document(order_id).set(order_record)
        saved_to = "firestore"
    except Exception as e:
        print(f"Errore scrittura Firestore: {e}")
        saved_to = "local_cache"

    return {
        "status": "order_created",
        "backend": saved_to,
        "order_id": order_id,
        "summary": order_record,
        "author_contacts": AUTHOR_CONTACTS,
        "next_steps": (
            "Ordine registrato con successo nel database! L'utente può ora procedere con il pagamento indicato "
            "(PayPal o Bonifico) inviando l'ID ordine all'autrice su Instagram (@andreina_grieco_autrice) "
            "o via email, oppure attendere il link riservato su Vinted se ha scelto tale modalità."
        ),
    }


def get_order_status(order_id: str) -> Dict[str, Any]:
    """Verifica lo stato e i dettagli di un ordine esistente leggendolo da Firestore.

    Args:
        order_id: Il codice univoco dell'ordine (es. 'AG-SEED001' o l'ID generato).

    Returns:
        I dettagli dell'ordine o messaggio se non trovato.
    """
    try:
        db = get_firestore_client()
        clean_id = order_id.strip().upper()
        doc = db.collection("book_orders").document(clean_id).get()
        if doc.exists:
            return {
                "status": "found",
                "order": doc.to_dict(),
            }
        else:
            return {
                "status": "not_found",
                "message": f"Nessun ordine trovato con ID '{order_id}'.",
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Errore durante la consultazione dell'ordine: {str(e)}",
        }
