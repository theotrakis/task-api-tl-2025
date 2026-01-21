# task-api-tl-2025

# Task Management API (Τεχνολογία Λογισμικού 2025-26)

## Στοιχεία φοιτητή
- Ονοματεπώνυμο: TRAKIS THEODOROS
- ΑΜ: inf2022207
- Τμήμα: Πληροφορικής – Ιόνιο Πανεπιστήμιο

## Περιγραφή
Υλοποιήθηκε REST API για διαχείριση tasks.
Κάθε task έχει: `id`, `username`, `title`, `description`, `deadline`.

Αποθήκευση δεδομένων σε JSON αρχείο (`data/tasks.json`) μέσω του `storage.py`.

## Endpoints
- `GET /tasks` : Επιστρέφει όλα τα tasks
- `GET /tasks/<id>` : Επιστρέφει task με βάση το id
- `POST /tasks` : Δημιουργία task
- `DELETE /tasks/<id>` : Διαγραφή task

## Τοπική εκτέλεση
```bash
pip install -r requirements.txt
python app.py
