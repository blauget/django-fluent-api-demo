"""
SDK para Invoice System API.

Un SDK moderno y tipado que implementa patrones de diseño de SDKs profesionales
como OpenAI y AWS SDK v2.

Ejemplo de uso:
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
    CreateClientRequest,
    UpdateClientRequest,
    CreateItemRequest,
    UpdateItemRequest,
    CreateInvoiceRequest,
    UpdateInvoiceRequest,
    PaginatedResponse,
)

__all__ = [
    # Cliente principal
    'InvoiceSystemClient',
    
    # Modelos
    'ClientData',
    'ItemData',
    'InvoiceData',
    'InvoiceItemData',
    'CreateClientRequest',
    'UpdateClientRequest',
    'CreateItemRequest',
    'UpdateItemRequest',
    'CreateInvoiceRequest',
    'UpdateInvoiceRequest',
    'PaginatedResponse',
]

__version__ = '1.0.0'

