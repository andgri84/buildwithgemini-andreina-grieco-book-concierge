"""Seed script for Firestore collections: catalog_books, catalog_boxes, and book_orders."""

from google.cloud import firestore
import datetime

# Hardcoded GCP Project ID as requested
PROJECT_ID = "qwiklabs-gcp-03-9513a337097b"
BUCKET_BASE_URL = f"https://storage.googleapis.com/andreina-grieco-book-concierge-9513a337097b"

db = firestore.Client(project=PROJECT_ID)

SEEDED_BOOKS = [
    {
        "id": "regina_cambiante",
        "title": "La Regina Cambiante",
        "author": "Andreina Grieco",
        "publisher": "Plesio Editore",
        "saga": None,
        "volume_number": None,
        "type": "Standalone",
        "genre": "Dark / Epic Fantasy storico",
        "setting": "Regno di Campania, fine Settecento",
        "cover_url": f"{BUCKET_BASE_URL}/covers/regina_cambiante.jpg",
        "thumbnail_url": f"{BUCKET_BASE_URL}/thumbnails/regina_cambiante.jpg",
        "synopsis": (
            "Sul finire del Settecento, il Regno di Campania vive nel terrore dei cambianti, "
            "mutanti emarginati capaci di evolvere e trasformarsi a seconda dei loro desideri reconditi. "
            "La principessa Valeria è stata addestrata a combatterli, ma quando il fratello usurpa il trono, "
            "scopre che lei stessa sta mutando. Per padroneggiare i suoi poteri dovrà affidarsi al feroce "
            "Demone del Lago Fusaro, la cui unica intenzione è trasformare il suo addestramento in un inferno."
        ),
        "protagonist": "Principessa Valeria",
        "themes": ["Metamorfosi", "Lotta per il trono", "Mostro vs Umano", "Segreti dinastici"],
        "pages": 320,
    },
    {
        "id": "yohnna_1",
        "title": "Yohnna e il Baluardo dei Deserti",
        "author": "Andreina Grieco",
        "publisher": "Edikit",
        "saga": "La Saga di Yohnna",
        "volume_number": 1,
        "type": "Saga (Vol. 1)",
        "genre": "Epic Fantasy / Desert Fantasy",
        "setting": "Le vaste e spietate terre sabbiose del Baluardo",
        "cover_url": f"{BUCKET_BASE_URL}/covers/yohnna_1.jpg",
        "thumbnail_url": f"{BUCKET_BASE_URL}/thumbnails/yohnna_1.jpg",
        "synopsis": (
            "Primo volume della saga che vede protagonista il giovane Yohnna alle prese con le sfide, "
            "i misteri e la difesa estrema del Baluardo tra le sabbie aride e le minacce che incombono "
            "sulle terre del deserto."
        ),
        "protagonist": "Yohnna",
        "themes": ["Viaggio dell'eroe", "Sopravvivenza e baluardo", "Destino e sabbie"],
        "pages": 280,
    },
    {
        "id": "yohnna_2",
        "title": "Yohnna e le Lacrime di Israfil",
        "author": "Andreina Grieco",
        "publisher": "Edikit",
        "saga": "La Saga di Yohnna",
        "volume_number": 2,
        "type": "Saga (Vol. 2)",
        "genre": "Epic Fantasy / Desert Fantasy",
        "setting": "Oltre il deserto, il richiamo e il mito di Israfil",
        "cover_url": f"{BUCKET_BASE_URL}/covers/yohnna_2.jpg",
        "thumbnail_url": f"{BUCKET_BASE_URL}/thumbnails/yohnna_2.jpg",
        "synopsis": (
            "Secondo volume che porta a compimento e approfondisce l'arco narrativo di Yohnna, "
            "rivelando la natura e il mistero delle Lacrime di Israfil e le conseguenze delle scelte "
            "fatte al Baluardo."
        ),
        "protagonist": "Yohnna",
        "themes": ["Mito e rivelazione", "Conflitto epico", "Evoluzione spirituale e sacrifici"],
        "pages": 310,
    },
]

SEEDED_BOXES = [
    {
        "id": "box_baluardo",
        "name": "Box Baluardo",
        "base_price": 14.0,
        "book_ids": ["yohnna_1", "yohnna_2"],
        "book_choice_mode": "one_of",
        "books_display": "Yohnna 1 (oppure Yohnna 2 per chi ha già l'1)",
        "cards_included": 1,
        "is_available": True,
        "description": "Un volume singolo a scelta tra Yohnna 1 o Yohnna 2 con copia autografata, dedica personalizzata e 1 card da collezione.",
    },
    {
        "id": "box_principessa",
        "name": "Box Principessa",
        "base_price": 18.0,
        "book_ids": ["regina_cambiante"],
        "book_choice_mode": "all",
        "books_display": "La Regina Cambiante",
        "cards_included": 2,
        "is_available": True,
        "description": "Copia autografata de La Regina Cambiante con dedica personalizzata + 2 card da collezione esclusive.",
    },
    {
        "id": "box_regina",
        "name": "Box Regina",
        "base_price": 20.0,
        "book_ids": ["regina_cambiante"],
        "book_choice_mode": "all",
        "books_display": "La Regina Cambiante",
        "cards_included": 5,
        "is_available": True,
        "description": "Copia autografata de La Regina Cambiante con dedica personalizzata + set completo di 5 card da collezione.",
    },
    {
        "id": "box_troni_deserti",
        "name": "Box Troni e Deserti",
        "base_price": 32.0,
        "book_ids": ["regina_cambiante", "yohnna_1"],
        "book_choice_mode": "all",
        "books_display": "La Regina Cambiante + Yohnna e il Baluardo dei Deserti (Vol. 1)",
        "cards_included": 3,
        "is_available": True,
        "description": "Entrambi gli esordi autografati con dedica personalizzata + selezione di 3 card da collezione.",
    },
    {
        "id": "box_sovrano_sabbie",
        "name": "Box Sovrano delle Sabbie",
        "base_price": 26.0,
        "book_ids": ["yohnna_1", "yohnna_2"],
        "book_choice_mode": "all",
        "books_display": "Yohnna e il Baluardo dei Deserti (Vol. 1) + Yohnna e le Lacrime di Israfil (Vol. 2)",
        "cards_included": 2,
        "is_available": True,
        "description": "La duologia completa di Yohnna autografata con dedica personalizzata + 2 card da collezione della saga.",
    },
    {
        "id": "box_imperatrice",
        "name": "Box Imperatrice",
        "base_price": 30.0,
        "book_ids": ["regina_cambiante", "yohnna_1", "yohnna_2"],
        "book_choice_mode": "all",
        "books_display": "Tutti e 3 i libri (La Regina Cambiante + Yohnna 1 + Yohnna 2)",
        "cards_included": 7,
        "is_available": True,
        "description": "L'intera bibliografia autografata (tutti e 3 i libri) + set completo di 7 card da collezione.",
    },
]

SEEDED_ORDERS = [
    {
        "order_id": "AG-SEED001",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "customer_name": "Chiara Rossi",
        "dedication_name": "A Chiara, che la regina guidi il tuo cammino!",
        "box_id": "box_regina",
        "box_name": "Box Regina",
        "book_ids": ["regina_cambiante"],
        "shipping_address": "Corso Vittorio Emanuele 45, 80121 Napoli",
        "shipping_method": "Poste Italiane Tracciato",
        "total_price": 22.0,
        "payment_status": "Pagato",
        "payment_method": "PayPal",
        "contact_info": "@chiara_fantasy",
    },
    {
        "order_id": "AG-SEED002",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "customer_name": "Davide Moretti",
        "dedication_name": "A Davide, fiero guardiano delle sabbie",
        "box_id": "box_sovrano_sabbie",
        "box_name": "Box Sovrano delle Sabbie",
        "book_ids": ["yohnna_1", "yohnna_2"],
        "shipping_address": "Piazza Maggiore 3, 40124 Bologna",
        "shipping_method": "Vinted",
        "total_price": 26.0,
        "payment_status": "Acconto ricevuto / In attesa di acquisto su Vinted",
        "payment_method": "Vinted + PayPal",
        "contact_info": "vinted: davidem_reads",
    },
]

def seed():
    print(f"Seeding Firestore in project: {PROJECT_ID}...")
    
    # 1. Seed books table (collection 'catalog_books') with cover_url & thumbnail_url
    books_ref = db.collection("catalog_books")
    for book in SEEDED_BOOKS:
        books_ref.document(book["id"]).set(book)
        print(f"  ✓ Book seeded: {book['id']} ({book['title']})")
        print(f"     Cover:     {book['cover_url']}")
        print(f"     Thumbnail: {book['thumbnail_url']}")

    # 2. Seed boxes table (collection 'catalog_boxes')
    boxes_ref = db.collection("catalog_boxes")
    for box in SEEDED_BOXES:
        boxes_ref.document(box["id"]).set(box)
        print(f"  ✓ Box seeded: {box['id']} ({box['name']}) -> {box['book_ids']}")
        
    # 3. Seed orders table (collection 'book_orders')
    orders_ref = db.collection("book_orders")
    for order in SEEDED_ORDERS:
        orders_ref.document(order["order_id"]).set(order)
        print(f"  ✓ Order seeded: {order['order_id']} for {order['customer_name']}")

    print("Firestore seeding with covers & thumbnails completed successfully!")

if __name__ == "__main__":
    seed()
