"""
SDK Client for the Invoice System API.

These SDK try to implement the following patterns:
- Client Library Pattern: Centralized client with nested resources
- Resource-Oriented Design: Each resource is an independent class
- Fluent API: Discoverable and easy to use API
- Strong Typing: Strong typing with Type Hints and data models
"""
import requests
from typing import Optional, Dict, Any, List, Union
from urllib.parse import urljoin

# TODO: Improve error handling with custom exceptions
from .models import (
    ClientData,
    ItemData,
    InvoiceData,
    InvoiceItemData,
    PaginatedResponse,
)


class BaseResource:
    """
    Base class for all resources of the API.
    
    Implement the standard CRUD operations and provides a base
    for specific methods for each resource.
    """
    
    def __init__(self, client: 'InvoiceSystemClient'):
        """
        Initialize the resource.
        
        Args:
            client: The main client instance
        """
        self.client = client
        self.endpoint_path = ""
    
    def _build_url(self, resource_id: Optional[Union[int, str]] = None) -> str:
        """
        Build the full URL for the resource.
        
        Args:
            resource_id: Optional ID of the specific resource
            
        Returns:
            Built URL
        """
        path = f"{self.endpoint_path}/"
        if resource_id:
            path = f"{path}{resource_id}/"
        return urljoin(self.client.base_url, path)
    
    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs
    ) -> Union[List[Dict[str, Any]], PaginatedResponse]:
        """
        List all resources.
        
        Args:
            page: Page number (for pagination)
            page_size: Page size
            **kwargs: Additional filtering parameters
            
        Returns:
            List of resources or paginated response
        """
        params = kwargs.copy()
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['page_size'] = page_size
        
        return self.client._request('GET', self._build_url(), params=params)
    
    def get(self, resource_id: Union[int, str]) -> Dict[str, Any]:
        """
        Get a specific resource by ID.
        
        Args:
            resource_id: ID of the resource to get
            
        Returns:
            The resource data
            
        Raises:
            NotFoundError: If the resource does not exist
        """
        return self.client._request('GET', self._build_url(resource_id))
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new resource.
        
        Args:
            data: Data of the resource to create
            
        Returns:
            The created resource data
            
        Raises:
            ValidationError: If the data is invalid
        """
        return self.client._request('POST', self._build_url(), json=data)
    
    def update(
        self,
        resource_id: Union[int, str],
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing resource.
        
        Args:
            resource_id: ID of the resource to update
            data: Data to update (partial)
            
        Returns:
            The updated resource data
            
        Raises:
            NotFoundError: If the resource does not exist
            ValidationError: If the data is invalid
        """
        return self.client._request('PATCH', self._build_url(resource_id), json=data)
    
    def delete(self, resource_id: Union[int, str]) -> bool:
        """
        Delete a resource.
        
        Args:
            resource_id: ID of the resource to delete
            
        Returns:
            True if the resource was deleted
            
        Raises:
            NotFoundError: If the resource does not exist
        """
        return self.client._request('DELETE', self._build_url(resource_id))


# ============================================================================
# SPECIFIC RESOURCES
# ============================================================================

class ClientsResource(BaseResource):
    """
    Client resource.
    
    Provide specific methods for operations with clients.
    """
    
    def __init__(self, client: 'InvoiceSystemClient'):
        super().__init__(client)
        self.endpoint_path = "clients"
    
    def create(self, name: str, email: str) -> ClientData:
        """
        Create a new client.
        
        Args:
            name: Client name
            email: Client email
            
        Returns:
            The created client data
        """
        data = {
            "name": name,
            "email": email
        }
        return super().create(data)
    
    def update(
        self,
        client_id: Union[int, str],
        name: Optional[str] = None,
        email: Optional[str] = None
    ) -> ClientData:
        """
        Update an existing client.
        
        Args:
            client_id: Client ID
            name: New name (optional)
            email: New email (optional)
            
        Returns:
            The updated client data
        """
        data: Dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if email is not None:
            data["email"] = email
        
        return super().update(client_id, data)
    
    def get_by_email(self, email: str) -> Optional[ClientData]:
        """
        Search a client by email.
        
        Args:
            email: Email of the client to search
            
        Returns:
            The client data if exists, None otherwise
        """
        results = self.list(email=email)
        if isinstance(results, dict) and 'results' in results:
            clients = results['results']
        else:
            clients = results if isinstance(results, list) else []
        
        for client in clients:
            if client.get('email') == email:
                return client
        return None


class ItemsResource(BaseResource):
    """
    Item resource.
    
    Provide specific methods for operations with items.
    """
    
    def __init__(self, client: 'InvoiceSystemClient'):
        super().__init__(client)
        self.endpoint_path = "items"
    
    def create(self, name: str, sku: str, price: Union[str, float]) -> ItemData:
        """
        Create a new item.
        
        Args:
            name: Item name
            sku: Unique SKU of the item
            price: Item price (can be string or float)
            
        Returns:
            The created item data
        """
        data = {
            "name": name,
            "sku": sku,
            "price": str(price)
        }
        return super().create(data)
    
    def update(
        self,
        item_id: Union[int, str],
        name: Optional[str] = None,
        sku: Optional[str] = None,
        price: Optional[Union[str, float]] = None
    ) -> ItemData:
        """
        Update an existing item.
        
        Args:
            item_id: Item ID
            name: New name (optional)
            sku: New SKU (optional)
            price: New price (optional)
            
        Returns:
            The updated item data
        """
        data: Dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if sku is not None:
            data["sku"] = sku
        if price is not None:
            data["price"] = str(price)
        
        return super().update(item_id, data)
    
    def get_by_sku(self, sku: str) -> Optional[ItemData]:
        """
        Search an item by SKU.
        
        Args:
            sku: SKU of the item to search
            
        Returns:
            The item data if exists, None otherwise
        """
        results = self.list(sku=sku)
        if isinstance(results, dict) and 'results' in results:
            items = results['results']
        else:
            items = results if isinstance(results, list) else []
        
        for item in items:
            if item.get('sku') == sku:
                return item
        return None


class InvoicesResource(BaseResource):
    """
    Invoice resource.
    
    Provide specific methods for operations with invoices.
    """
    
    def __init__(self, client: 'InvoiceSystemClient'):
        super().__init__(client)
        self.endpoint_path = "invoices"
    
    def create(self, client_id: int, date: Optional[str] = None) -> InvoiceData:
        """
        Create a new invoice.
        
        Args:
            client_id: Client ID
            date: Invoice date in ISO format (optional, uses auto_now_add if not provided)
            
        Returns:
            The created invoice data
        """
        data: Dict[str, Any] = {
            "client": client_id
        }
        if date:
            data["date"] = date
        
        return super().create(data)
    
    def update(
        self,
        invoice_id: Union[int, str],
        client_id: Optional[int] = None,
        date: Optional[str] = None
    ) -> InvoiceData:
        """
        Update an existing invoice.
        
        Args:
            invoice_id: Invoice ID
            client_id: New client ID (optional)
            date: New date in ISO format (optional)
            
        Returns:
            The updated invoice data
        """
        data: Dict[str, Any] = {}
        if client_id is not None:
            data["client"] = client_id
        if date is not None:
            data["date"] = date
        
        return super().update(invoice_id, data)
    
    def get_by_client(self, client_id: int) -> List[InvoiceData]:
        """
        Get all invoices of a client.
        
        Args:
            client_id: Client ID
            
        Returns:
            The list of invoices of the client
        """
        results = self.list(client=client_id)
        if isinstance(results, dict) and 'results' in results:
            return results['results']
        return results if isinstance(results, list) else []


# ============================================================================
# MAIN CLIENT
# ============================================================================

class InvoiceSystemClient:
    """
    Main client to interact with the Invoice System API.
    
    This client implements a resource-oriented design pattern,
    where each resource (clients, items, invoices) is accessible as
    a property of the client.
    
    Use example:
        >>> client = InvoiceSystemClient()
        >>> client.clients.create(name="Juan", email="juan@example.com")
        >>> client.items.list()
        >>> client.invoices.get(1)
    """
    
    def __init__(
        self,
        base_url: str = 'http://127.0.0.1:8000/api/v1/',
        token: Optional[str] = None
    ):
        """
        Initialize the client.
        
        Args:
            base_url: Base URL of the API
            token: Authentication token (optional)
        """
        self.base_url = base_url if base_url.endswith('/') else f"{base_url}/"
        self.session = requests.Session()
        
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "InvoiceSystem-Python-SDK/1.0"
        })
        
        if token:
            self.session.headers["Authorization"] = f"Token {token}"
        
        # Instantiate the resources once
        self._clients: Optional[ClientsResource] = None
        self._items: Optional[ItemsResource] = None
        self._invoices: Optional[InvoicesResource] = None
    
    def _request(self, method: str, url: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]], bool]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            url: Full URL of the request
            **kwargs: Additional arguments for requests
            
        Returns:
            Response from the API (JSON parsed or True for DELETE)
        """
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            if response.status_code == 204:
                return True
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"API Error: {e}")
    
    # ========================================================================
    # PROPERTIES FOR ACCESSING RESOURCES (Fluent API Pattern)
    # ========================================================================
    
    @property
    def clients(self) -> ClientsResource:
        """
        Access to the Clients resource.
        
        Returns:
            Instance of ClientsResource
        """
        if self._clients is None:
            self._clients = ClientsResource(self)
        return self._clients
    
    @property
    def items(self) -> ItemsResource:
        """
        Access to the Items resource.
        
        Returns:
            Instance of ItemsResource
        """
        if self._items is None:
            self._items = ItemsResource(self)
        return self._items
    
    @property
    def invoices(self) -> InvoicesResource:
        """
        Access to the Invoices resource.
        
        Returns:
            Instance of InvoicesResource
        """
        if self._invoices is None:
            self._invoices = InvoicesResource(self)
        return self._invoices
    
    def __repr__(self) -> str:
        """Representation of the client."""
        return f"<InvoiceSystemClient base_url='{self.base_url}'>"
