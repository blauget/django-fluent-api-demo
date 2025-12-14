"""
SDK para Invoice System API.

Use exmaples:
    >>> from sdk import InvoiceSystemClient
    >>> client = InvoiceSystemClient()
    >>> client.clients.create(name="Juan", email="juan@example.com")
    >>> client.items.list()
    >>> client.invoices.get(1)
"""

from .client import InvoiceSystemClient
from .models import (
    ClientData,
    ItemData,
    InvoiceData,
    InvoiceItemData,
    PaginatedResponse,
)

__all__ = [
    # Main client
    'InvoiceSystemClient',
    
    # Response models
    'ClientData',
    'ItemData',
    'InvoiceData',
    'InvoiceItemData',
    'PaginatedResponse',
]

__version__ = '1.0.0'

