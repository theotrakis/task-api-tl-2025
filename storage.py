from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

# Βρίσκουμε τον φάκελο του project (εκεί που είναι το storage.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Φτιάχνουμε τη διαδρομή: task_api/data/tasks.json
DATA_PATH = os.getenv("TASKS_FILE", os.path.join(BASE_DIR, "data", "tasks.json"))



def ensure_data_file() -> None:
    """
    Βεβαιώνεται ότι υπάρχει ο φάκελος data/ και το αρχείο tasks.json.
    Αν δεν υπάρχουν, τα δημιουργεί.
    """
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_tasks() -> List[Dict[str, Any]]:
    """
    Διαβάζει όλα τα tasks από το JSON αρχείο και τα επιστρέφει σαν λίστα.
    """
    ensure_data_file()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ασφάλεια: αν για κάποιο λόγο δεν είναι list, επιστρέφουμε κενό
    if not isinstance(data, list):
        return []

    return data


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """
    Αποθηκεύει τη λίστα tasks στο JSON αρχείο.
    """
    ensure_data_file()

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def next_id(tasks: List[Dict[str, Any]]) -> int:
    """
    Επιστρέφει το επόμενο διαθέσιμο id.
    Αν δεν υπάρχουν tasks -> 1
    Αλλιώς -> max(id) + 1
    """
    if not tasks:
        return 1

    max_id = 0
    for t in tasks:
        try:
            tid = int(t.get("id", 0))
            if tid > max_id:
                max_id = tid
        except (TypeError, ValueError):
            # αν κάποιο task έχει λάθος id, το αγνοούμε
            continue

    return max_id + 1


def find_task(tasks: List[Dict[str, Any]], task_id: int) -> Optional[Dict[str, Any]]:
    """
    Βρίσκει και επιστρέφει task με συγκεκριμένο id.
    Αν δεν βρεθεί, επιστρέφει None.
    """
    for t in tasks:
        try:
            if int(t.get("id", -1)) == task_id:
                return t
        except (TypeError, ValueError):
            continue

    return None
