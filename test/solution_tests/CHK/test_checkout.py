from solutions.CHK.checkout_solution import checkout, Checkout

class TestCheckout():
    '''
    Potential for improvement: use prices directly from SKU_TABLE in checkout_solution.py
    to avoid hardcoding values here. As it stands now, tests become invalidated as soon as price changes,
    even though logic may be sound. But also made complicated by the need to test the logic of the offers.
    '''
    def test_checkout_basic(self):
        # Empty string should cost 0
        assert checkout('') == 0

        # Single items
        assert checkout('A') == Checkout.SKU_TABLE['A']['price']
        assert checkout('B') == Checkout.SKU_TABLE['B']['price']
        assert checkout('C') == Checkout.SKU_TABLE['C']['price']
        assert checkout('D') == Checkout.SKU_TABLE['D']['price']
        assert checkout('E') == Checkout.SKU_TABLE['E']['price']

    def test_checkout_special_offers(self):
        # Special offers for A 
        assert checkout('AAA') == 130 # 3A offer 
        assert checkout('AAAA') == 180 # 3A(130) + 1A(50)
        assert checkout('AAAAA') == 200 # 5A offer
        assert checkout('AAAAAA') == 250 # 5A(200) + 1A(50)
        assert checkout('AAAAAAA') == 300 # 5A(200) + 2A(100)
        assert checkout('AAAAAAAA') == 330 # 5A(200) + 3A(130)

        # Verify we're using the most favourable combination for A
        assert checkout('AAAAAAAAAA') == 400 # 2 x 5A offers better than 3 x 3A + A

        # Special offers for B (2 for 45)
        assert checkout('BB') == 45
        assert checkout('BBB') == 75
        assert checkout('BBBB') == 90

    def test_self_referential_free_offers(self):
        assert checkout('FFF') == 20 # 2F(20) + 1 free. Exactly one group
        assert checkout('FFFF') == 30 # 3F(30) + 1 free. Still only 1 complete group
        assert checkout('FFFFFF') == 40 # 4F(40) + 2 free. 2 complete groups
        assert checkout('FFFFFFFF') == 60 # 6F(60) + 2 free. 2 groups + 2 remainder

        # Test self-referential for U (buy 3U get 1U free)
        assert checkout('UUU') == 120 # 3U(120)
        assert checkout('UUUU') == 120 # 3U(120) + 1 free. Exactly one group
        assert checkout('UUUUU') == 160 # 4U(140) + 1 free. 1 complete group + 1 remainder
        assert checkout('UUUUUUUU') == 240 # 6U(240) + 2 free. 2 groups
        

    def test_checkout_combined_offers(self):
        # Combined special and free offers
        assert checkout('AAAAAEEB') == 280 # 5A(200) + 2E(80)
        assert checkout('EEBAAB') == 210 # 2E(80) + 2A(100) + 1B(30)
        assert checkout('ABCDEABCDEFFF') == 300 # 2A(100) + 1B(30) + 2C(40) + 2D(30) + 2E(80) + 2F(20)

    def test_checkout_invalid_input(self):
        # Invalid inputs should return -1
        assert checkout('a') == -1 # lowercase 
        assert checkout('-') == -1 # Special char 
        assert checkout('ABCa') == -1 # mixed valid/invalid
        assert checkout('   ') == -1 # spaces
        assert checkout(None) == -1 # None
        assert checkout(123) == -1 # non-string

    # def test_complex_combinations(self):
    #     # Test combination of multiple offers
    #     assert checkout('AAAAAEEBAAABBB') == 485  # 5A(200) + 3A(130) + 2E(80) + 1 free B + 2B(45) + B(30)
        
    #     # Complex test with H and K offers
    #     assert checkout('HHHHHHHHHHKK') == 230  # 10H(80) + 2K(150)
        
    #     # Complex test with P, Q, and R offers
    #     assert checkout('PPPPPQQQRRR') == 410  # 5P(200) + 2Q(60) + 3R(150) + 1 free Q
        
    #     # Complex test with multiple free offers
    #     assert checkout('EEBNNMRRQ') == 305  # 2E(80) + 1 free B + 2N(80) + 1M(15) + 2R(100) + 1Q(30) - not enough N for free M
        
    #     # Test with all types of offers (pricing special offers, free item offers, self-referential)
    #     assert checkout('AAAAABBEEFFFHHHHHKKKNNNMPPPPPQQQRRRUVVV') == 1305
    #     # 5A(200) + 1B(30) + 2E(80) + 1 free B + 2F(20) + 1 free F + 5H(45) + 2K(120) + 1K(70) + 3N(120) + 1 free M + 5P(200) + 2Q(60) + 1 free Q (from R) + 3R(150) + 1U(40) + 3V(130)

    def test_all_items(self):
        # One of each item
        assert checkout('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == 882

        

    


