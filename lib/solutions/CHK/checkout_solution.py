
SKU_TABLE = {
    'A': {'price': 50, 'special': (3, 130)},
    'B': {'price': 30, 'special': (2, 45)},
    'C': {'price': 20, 'special': None},
    'D': {'price': 15, 'special': None},
    'E': {'price': 40, 'special': None}
}

def calculate_cost_for_sku(sku, count):
    if sku not in SKU_TABLE:
        raise ValueError(f"Invalid SKU: {sku}")
    
    item_info = SKU_TABLE[sku]
    total_price = 0

    if item_info['special'] is None:
        total_price = item_info['price'] * count
    else:
        # The price for items with special offers is 
        # calculated by first calculating how many full offers we can apply
        # and then adding the cost of the remaining items. 
        # For example, if the special offer is 3 for 130, and we have 5 items,
        # we can apply the offer once, and then add the cost of the remaining 2 items. 
        num_offers = count // item_info['special'][0]
        total_price = num_offers * item_info['special'][1]
        remaining_items = count % item_info['special'][0]
        total_price += remaining_items * item_info['price']

    return total_price

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    '''
    This function calculates the total cost of a given string of SKUs.
    If the input string is invalid, the function returns -1.
    '''
    # We presume that the input string is a sequence of characters,
    # where each character is a valid SKU.
    
    # Ensure that the input string contains valid SKUs.
    for sku in skus: 
        if sku not in SKU_TABLE:
            return -1
        
    # Now we start processing the input. We will create a map
    # of sku's to the number of occurences in the input string. 
    sku_counts = {}
    for sku in skus: 
        sku_counts[sku] = sku_counts.get(sku, 0) + 1

    total_cost = 0
    for sku, count in sku_counts.items():
        total_cost += calculate_cost_for_sku(sku, count)

    return total_cost


