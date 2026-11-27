"""Script per re-importare il database Firestore esportato in qualsiasi nuovo progetto GCP o emulatore."""

import json
import os
import sys
from google.cloud import firestore

# Sostituisci con il tuo nuovo project ID se deployi altrove
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-03-9513a337097b")

def main():
    print(f"Importing data into Firestore project: {PROJECT_ID}...")
    db = firestore.Client(project=PROJECT_ID)

    with open("firestore_export.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Libri
    for book in data.get("catalog_books", []):
        db.collection("catalog_books").document(book["id"]).set(book)
        print(f"  ✓ Book: {book['id']}")

    # 2. Box
    for box in data.get("catalog_boxes", []):
        db.collection("catalog_boxes").document(box["id"]).set(box)
        print(f"  ✓ Box: {box['id']}")

    # 3. Ordini
    for order in data.get("book_orders", []):
        db.collection("book_orders").document(order["order_id"]).set(order)
        print(f"  ✓ Order: {order['order_id']}")

    print("Import completato con successo!")

if __name__ == "__main__":
    main()
