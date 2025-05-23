# Orders API

## Obsah repozitára
flask-orders/
├── app.py - routing + logika API
├── models.py - SQLAlchemy model tabuľky orders
├── schemas.py - Pydantic validácia vstupov/výstupov
├── currency_rates.py - sťahovanie kurzov ČNB a prepočty
├── db.py - inicializácia SQLAlchemy
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md # tento súbor

## Spustenie
### Bez Dockeru:
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
 → beží na http://127.0.0.1:5000

### Docker:
docker compose up --build
 → beží na http://127.0.0.1:8000
 
 
 ## Endpointy

| Metóda & URL                          | Popis                     | Telo (JSON)                                               | Odpoveď            |
| ------------------------------------- | ------------------------- | --------------------------------------------------------- | ------------------ |
| **POST /orders**                      | vytvor objednávku         | `{"customer_name":"Janko","price":10,"currency":"EUR"}` | **201** + objekt   |
| **GET /orders**                       | zoznam objednávok         | –                                                         | **200** + zoznam   |
| **GET /orders?to\_currency=USD**      | objednávky s prepočtom do USD | –                                                         | **200** + zoznam   |
| **GET /orders/⟨id⟩?to\_currency=EUR** | objednávka s prevodom meny    | –                                                         | **200** + objekt   |
| **DELETE /orders/⟨id⟩**               | zmaž objednávku           | –                                                         | **200** + objekt |


