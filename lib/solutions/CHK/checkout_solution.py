class Checkout:
    # Class attributes. Shared by all instances.
    SKU_TABLE = {
        'A': {'price': 50, 'special': [(5, 200), (3, 130)]}, # Larger quantities first
        'B': {'price': 30, 'special': [(2, 45)]},
        'C': {'price': 20, 'special': None},
        'D': {'price': 15, 'special': None},
        'E': {'price': 40, 'special': None},
        'F': {'price': 10, 'special': None}
    }

    # We can think of free offers as an adjacency list/graph, where
    # the edge from one node to another represents a free offer, and 
    # only applies when the trigger_quantity of the source node is met.
    FREE_OFFERS = {
        'E': [{'trigger_quantity': 2, 'free_sku': 'B', 'free_quantity': 1}],
        'F': [{'trigger_quantity': 2, 'free_sku': 'F', 'free_quantity': 1}]
    }

    def __init__(self, sku_string: str):
        self.sku_counts = self._scan(sku_string)

    def _scan(self, sku_string: str):
        '''
        Scans the input string and returns a dictionary of sku's to the number of occurences.
        '''
        if not isinstance(sku_string, str):
            raise ValueError("Input must be a string")

        sku_counts = {}
        for sku in sku_string:
            if sku not in self.SKU_TABLE: 
                raise ValueError(f"Invalid SKU: {sku}")
            sku_counts[sku] = sku_counts.get(sku, 0) + 1
        return sku_counts

    def _calculate_cost_for_sku(self, sku, count):
        if sku not in self.SKU_TABLE:
            raise ValueError(f"Invalid SKU: {sku}")
        
        item_info = self.SKU_TABLE[sku]
        total_price = 0
        remaining_items = count

        if item_info['special'] is None:
            total_price = item_info['price'] * count
        else:
            # apply special offers in order (largest quantities first) 
            for offer_qty, offer_price in sorted(item_info['special'], key=lambda x: x[0], reverse=True):
                num_offers = remaining_items // offer_qty 
                total_price += num_offers * offer_price
                remaining_items -= num_offers * offer_qty 
            
            # Add remaining items at regular price
            total_price += remaining_items * item_info['price']

        return total_price
    
    def _apply_free_offers(self, sku_counts: dict) -> dict:
        '''
        Apply free offers to the given sku_counts, which effectively deducts
        the free_quantity of the free_sku from the sku_counts. Applied before 
        calculating the total cost.
        '''
        # Deep copy to prevent side effects.
        adjusted_counts = sku_counts.copy()

        # Look for items that trigger free offers.
        for trigger_sku, offers in self.FREE_OFFERS.items():
            if trigger_sku in sku_counts:
                for offer in offers: 
                    free_sku = offer['free_sku']

                    if free_sku == trigger_sku and free_sku in adjusted_counts:
                        trigger_quantity = offer['trigger_quantity']
                        free_quantity = offer['free_quantity']

                        original_count = sku_counts[trigger_sku]

                        
                    elif free_sku in adjusted_counts: 

                        # Calculate how many free items can be given 
                        num_triggers = sku_counts[trigger_sku] // offer['trigger_quantity']
                        free_items = num_triggers * offer['free_quantity']
                        adjusted_counts[free_sku] = max(0, adjusted_counts[free_sku] - free_items)
                    

        return adjusted_counts
    
    def total(self) -> int:
        counts_to_pay = self._apply_free_offers(self.sku_counts)

        total = 0
        for sku, count in counts_to_pay.items():
            total += self._calculate_cost_for_sku(sku, count)
        return total


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    '''
    This function calculates the total cost of a given string of SKUs.
    If the input string is invalid, the function returns -1.
    '''
    try: 
        checkout = Checkout(skus)
        return checkout.total()
    except ValueError:
        return -1




