
SKU_TABLE = {
    'A': {'price': 50, 'special': (3, 130)},
    'B': {'price': 30, 'special': (2, 45)},
    'C': {'price': 20, 'special': None},
    'D': {'price': 15, 'special': None},
}

def calculate_cost_for_sku(sku, count):
    if sku not in SKU_TABLE:
        raise ValueError(f"Invalid SKU: {sku}")
    
    item_info = SKU_TABLE[sku]
    total_price = 0
    remaining_items = count

    # Calculate how many times we can apply this offer. 
    num_offers = remaining_items // offer_qty 
    total_price += num_offers * offer_price 
    remaining_items -= num_offers * offer_qty


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



