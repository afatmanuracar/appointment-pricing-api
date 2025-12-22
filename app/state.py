# app/state.py
_MEMBERS: dict[str, object] = {}
_CLASSES: dict[str, object] = {}
_CLASS_COUNTS: dict[str, int] = {}
_RESERVATIONS: dict[str, object] = {}

def reset_state() -> None:
    _MEMBERS.clear()
    _CLASSES.clear()
    _CLASS_COUNTS.clear()
    _RESERVATIONS.clear()
