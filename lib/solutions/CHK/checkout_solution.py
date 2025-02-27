
SKU_TABLE = {
    'A': {'price': 50, 'special': [(3, 130), (5, 200)]},
    'B': {'price': 30, 'special': [(2, 45)]},
    'C': {'price': 20, 'special': []},
    'D': {'price': 15, 'special': []},
}

def calculate_price(sku, count):
    price = 0 
    if sku not in SKU_TABLE:
        raise ValueError(f"Invalid SKU: {sku}")
    
    price = SKU_TABLE[sku]['price']
    
# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    # we presume that the input string is a sequence of characters,
    # where each character is a valid SKU.

    # Let's start by validating the input.
    if not isinstance(skus, str):
        raise ValueError("Input must be a string")
    
    # Ensure that the input string contains valid SKUs.
    for sku in skus: 
        if sku not in SKU_TABLE:
            raise ValueError(f"Invalid SKU: {sku}")
        
    # Now we start processing the input. We will create a map
    # of sku's to the number of occurences in the input string. 
    sku_counts = {}
    for sku in skus: 
        sku_counts[sku] = sku_counts.get(sku, 0) + 1


