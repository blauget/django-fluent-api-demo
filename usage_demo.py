"""
Usage demo for the Invoice System SDK.
"""

from sdk import InvoiceSystemClient

# Initialize the client
client = InvoiceSystemClient(
    base_url='http://127.0.0.1:8000/api/v1/',
    # token='your-token-here'  # Optional
)

print("=" * 60)
print("DEMO: SDK Invoice System")
print("=" * 60)

try:
    # ========================================================================
    # CLIENTS
    # ========================================================================
    print("\nCLIENT MANAGEMENT")
    print("-" * 60)
    
    # Create a client (fluent and typed method)
    print("\n1. Creating a client...")
    new_client = client.clients.create(
        name="Juan",
        email="juan@example.com"
    )
    print(f"   Client created: {new_client}")
    
    # List all clients
    print("\n2. Listing all clients...")
    clients = client.clients.list()
    print(f"   Total clients: {len(clients) if isinstance(clients, list) else 'N/A'}")
    
    # Get a specific client
    if new_client.get('id'):
        print(f"\n3. Getting client ID {new_client['id']}...")
        client_data = client.clients.get(new_client['id'])
        print(f"   Client: {client_data}")
        
        # Search by email
        print("\n4. Searching client by email...")
        found_client = client.clients.get_by_email("juan@example.com")
        if found_client:
            print(f"   Client found: {found_client['name']}")
        
        # Update client
        print("\n5. Updating client...")
        updated = client.clients.update(
            client_id=new_client['id'],
            name="Juan Carlos Pérez",
            email="juancarlos@example.com"
        )
        print(f"   Client updated: {updated['name']}")
    
    # ========================================================================
    # ITEMS
    # ========================================================================
    print("\n\nITEM MANAGEMENT")
    print("-" * 60)
    
    # Create an item
    print("\n1. Creating an item...")
    new_item = client.items.create(
        name="Laptop Dell XPS",
        sku="LAP-DELL-XPS-001",
        price="1299.99"
    )
    print(f"   Item created: {new_item}")
    
    # List items
    print("\n2. Listing items...")
    items = client.items.list()
    print(f"   Total items: {len(items) if isinstance(items, list) else 'N/A'}")
    
    # Search by SKU
    if new_item.get('id'):
        print("\n3. Searching item by SKU...")
        found_item = client.items.get_by_sku("LAP-DELL-XPS-001")
        if found_item:
            print(f"   Item found: {found_item['name']} - ${found_item['price']}")
    
    # ========================================================================
    # INVOICES
    # ========================================================================
    print("\n\nINVOICE MANAGEMENT")
    print("-" * 60)
    
    if new_client.get('id'):
        # Create an invoice
        print("\n1. Creating an invoice...")
        new_invoice = client.invoices.create(client_id=new_client['id'])
        print(f"   Invoice created: {new_invoice}")
        
        # Get invoices from a client
        print("\n2. Getting client invoices...")
        client_invoices = client.invoices.get_by_client(new_client['id'])
        print(f"   Client invoices: {len(client_invoices)}")
        
        # Get a specific invoice
        if new_invoice.get('id'):
            print(f"\n3. Getting invoice ID {new_invoice['id']}...")
            invoice = client.invoices.get(new_invoice['id'])
            print(f"   Invoice: {invoice}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)

except Exception as e:
    print(f"\nUnexpected error: {e}")
    import traceback
    traceback.print_exc()
