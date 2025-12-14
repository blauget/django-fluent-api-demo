"""
Data models for the SDK.
These models represent the data structures that are returned by the API.

TODO: Consider adding separate request models (CreateXxxRequest, UpdateXxxRequest)
"""
from typing import Optional, List, Dict, Any

try:
    from typing import TypedDict  # Python 3.8+
except ImportError:
    from typing_extensions import TypedDict  # Python < 3.8


# ============================================================================
# RESPONSE MODELS (what the API returns)
# ============================================================================

class ClientData(TypedDict, total=False):
    """Data model for a Client (response from the API)."""
    id: Optional[int]
    name: str
    email: str


class ItemData(TypedDict, total=False):
    """Data model for an Item (response from the API)."""
    id: Optional[int]
    name: str
    sku: str
    price: str  # IA Notation: DecimalField se serializa como string en JSON


class InvoiceItemData(TypedDict, total=False):
    """Data model for an Invoice Item (response from the API)."""
    id: Optional[int]
    invoice: int
    item: int
    quantity: int


class InvoiceData(TypedDict, total=False):
    """Data model for an Invoice (response from the API)."""
    id: Optional[int]
    client: int
    date: str  # IA Notation: DateField se serializa como string en formato ISO
    items: List[InvoiceItemData]


class PaginatedResponse(TypedDict):
    """Data model for a paginated response."""
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Dict[str, Any]]
