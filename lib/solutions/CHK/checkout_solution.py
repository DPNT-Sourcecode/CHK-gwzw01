class Checkout:
    # Class attributes. Shared by all instances.
    SKU_TABLE = {
        'A': {'price': 50, 'special': [(5, 200), (3, 130)]}, # Larger quantities first
        'B': {'price': 30, 'special': [(2, 45)]},
        'C': {'price': 20, 'special': None},
        'D': {'price': 15, 'special': None},
        'E': {'price': 40, 'special': None},
        'F': {'price': 10, 'special': None},
        'G': {'price': 20, 'special': None},
        'H': {'price': 10, 'special': [(10, 80), (5, 45)]},
        'I': {'price': 35, 'special': None},
        'J': {'price': 60, 'special': None},
        'K': {'price': 80, 'special': [(2, 120)]},
        'L': {'price': 90, 'special': None},
        'M': {'price': 15, 'special': None},
        'N': {'price': 40, 'special': None},
        'O': {'price': 10, 'special': None},
        'P': {'price': 50, 'special': [(5, 200)]},
        'Q': {'price': 30, 'special': [(3, 80)]},
        'R': {'price': 50, 'special': None},
        'S': {'price': 20, 'special': None},
        'T': {'price': 20, 'special': None},
        'U': {'price': 40, 'special': None},
        'V': {'price': 50, 'special': [(3, 130), (2, 90)]},
        'W': {'price': 20, 'special': None},
        'X': {'price': 17, 'special': None},
        'Y': {'price': 20, 'special': None},
        'Z': {'price': 21, 'special': None}
    }

    # Free offers as an adjacency list/graph
    FREE_OFFERS = {
        'E': [{'trigger_quantity': 2, 'free_sku': 'B', 'free_quantity': 1}],
        'F': [{'trigger_quantity': 2, 'free_sku': 'F', 'free_quantity': 1}],
        'N': [{'trigger_quantity': 3, 'free_sku': 'M', 'free_quantity': 1}],
        'R': [{'trigger_quantity': 3, 'free_sku': 'Q', 'free_quantity': 1}],
        'U': [{'trigger_quantity': 3, 'free_sku': 'U', 'free_quantity': 1}]
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

                        # Calculate how many items customer actually pays for
                        # For "buy 2 get 1 free", customer pays for 2/3 of total items
                        # Formula: total_paid = ceil(total_count * (trigger_quantity / (trigger_quantity + free_quantity)))

                        total_group_size = trigger_quantity + free_quantity 
                        full_groups = original_count // total_group_size 
                        remainder = original_count % total_group_size 

                        # Pay for full groups (2 out of every 3)
                        items_to_pay = full_groups * trigger_quantity 

                        # For remainder items, pay up to trigger_quantity 
                        items_to_pay += min(remainder, trigger_quantity)

                        adjusted_counts[free_sku] = items_to_pay

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
