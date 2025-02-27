from typing import Tuple

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
        'K': {'price': 70, 'special': [(2, 120)]}, # Changed
        'L': {'price': 90, 'special': None},
        'M': {'price': 15, 'special': None},
        'N': {'price': 40, 'special': None},
        'O': {'price': 10, 'special': None},
        'P': {'price': 50, 'special': [(5, 200)]},
        'Q': {'price': 30, 'special': [(3, 80)]},
        'R': {'price': 50, 'special': None},
        'S': {'price': 20, 'special': None}, # Changed
        'T': {'price': 20, 'special': None},
        'U': {'price': 40, 'special': None},
        'V': {'price': 50, 'special': [(3, 130), (2, 90)]},
        'W': {'price': 20, 'special': None},
        'X': {'price': 17, 'special': None}, # Changed
        'Y': {'price': 20, 'special': None}, # Chaged
        'Z': {'price': 21, 'special': None} # Changed
    }

    # Free offers as an adjacency list/graph
    FREE_OFFERS = {
        'E': [{'trigger_quantity': 2, 'free_sku': 'B', 'free_quantity': 1}],
        'F': [{'trigger_quantity': 2, 'free_sku': 'F', 'free_quantity': 1}],
        'N': [{'trigger_quantity': 3, 'free_sku': 'M', 'free_quantity': 1}],
        'R': [{'trigger_quantity': 3, 'free_sku': 'Q', 'free_quantity': 1}],
        'U': [{'trigger_quantity': 3, 'free_sku': 'U', 'free_quantity': 1}]
    }

    GROUP_DISCOUNT_OFFERS = [
        {
            'group': ['S', 'T', 'X', 'Y', 'Z'],
            'quantity': 3,
            'price': 45
        }
    ]

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
    
    def _apply_group_discount_offers(self, sku_counts: dict) -> Tuple[dict, int]:
        '''
        Apply group discount offers to the given sku_counts.
        Returns an updatd sku_counts dictionary with items used in group offers removed
        and the total discount applied.
        '''
        adjusted_counts = sku_counts.copy()
        total_discount = 0 

        for offer in self.GROUP_DISCOUNT_OFFERS: 
            group_items = {}

            # Collect all items in this group from the basket 
            for sku in offer['group']: 
                if sku in adjusted_counts and adjusted_counts[sku] > 0:
                    group_items[sku] = adjusted_counts[sku]

            # If we have items from this group, apply the offer 
            if group_items:
                # Calculate how many complete sets we can form for this offer 
                total_group_items = sum(group_items.values())
                num_sets = total_group_items // offer['quantity']

                if num_sets > 0:
                    # To favour the customer, we want to use the most expensive items first
                    # for the group discount (to maximize regular-price savings)
                    items_by_price = sorted(
                        [(sku, self.SKU_TABLE[sku]['price'], count)
                         for sku, count in group_items.items()],
                         key=lambda x: x[1],
                         reverse=True
                    )

                    # Track how many items we've used in the offer
                    items_used = 0
                    items_to_remove = {} 
                    regular_price_total = 0

                    # Calculate how many of each  item to use in the offers 
                    while items_used < num_sets * offer['quantity']:
                        for sku, price, count in items_by_price:
                            if items_used >= num_sets * offer['quantity']:
                                break
                            
                            # Use as many of this item as possible for the offer 
                            can_use = min(count, num_sets * offer['quantity'] - items_used)
                            items_to_remove[sku] = items_to_remove.get(sku, 0) + can_use 
                            items_used += can_use 
                            regular_price_total += can_use * price 
                        
                        # Remove the items used in the offers from the adjusted counts 
                        for sku, count in items_to_remove.items():
                            adjusted_counts[sku] -= count 

                        # Calculate the discount (difference between regular price and offer price)
                        discount_total = regular_price_total - (num_sets * offer['price'])
                        total_discount += discount_total

        return adjusted_counts, total_discount
                        
    def total(self) -> int:
        # First, apply free offers (like 2E get 1B free)
        counts_after_free = self._apply_free_offers(self.sku_counts)

        # Then apply group discount offers 
        counts_after_groups, group_discount = self._apply_group_discount_offers(counts_after_free)

        regular_total = 0 
        for sku, count in counts_after_groups.items():
            regular_total += self._calculate_cost_for_sku(sku, count)

        return regular_total - group_discount


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
