"""Which stated numbers may appear as text, and from which ledger row.

`paper/numbers_ledger.md` is the only source of numbers a figure may state.
Every figure builder formats a number through `stated()`, which returns the
text only when the (figure, key) pair has a ledger row here; otherwise it
returns None, the builder omits the text, and `pending()` lists the number
for MANIFEST.md as NEEDS LEDGER ROW with its committed source.

Plotted positions read from committed files are data, not stated numbers.

SHOW_PENDING stays False until the owner adds the rows; flipping it to True
is the only change needed once they exist (and the row IDs go in LEDGERED).
"""

from __future__ import annotations

SHOW_PENDING = False

_PENDING: list[dict] = []


def stated(value_text: str, row: str | None, *, figure: str, what: str, source: str):
    """Return value_text if `row` names a ledger row; else record it as pending."""
    if row:
        return value_text
    _PENDING.append(dict(figure=figure, what=what, value=value_text, source=source))
    return value_text if SHOW_PENDING else None


def pending() -> list[dict]:
    return list(_PENDING)


def reset():
    _PENDING.clear()
