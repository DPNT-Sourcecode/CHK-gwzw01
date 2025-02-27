from solutions.CHK import checkout_solution

class TestCheckout():
    def test_checkout_basic(self):
        # Empty string should cost 0
        assert checkout_solution.checkout('') == 0

        # Single items
        assert checkout_solution.checkout('A') == 50
        assert checkout_solution.checkout('B') == 30
        assert checkout_solution.checkout('C') == 20
        assert checkout_solution.checkout('D') == 15
        assert checkout_solution.checkout('E') == 40 

    def test_checkout_special_offers(self):
        # Special offers for A (3 for 130)
        assert checkout_solution.checkout('AAA') == 130 # 3A offer 
        assert checkout_solution.checkout('AAAA') == 180 # 3A(130) + 1A(50)
        assert checkout_solution.checkout('AAAAA') == 200 # 5A offer
        assert checkout_solution.checkout('AAAAAA') == 250 # 5A(200) + 1A(50)
        assert checkout_solution.checkout('AAAAAAA') == 300 # 5A(200) + 2A(100)
        assert checkout_solution.checkout('AAAAAAAA') == 330 # 5A(200) + 3A(130)

        # Verify we're using the most favourable combination for A
        assert checkout_solution.checkout('AAAAAAAAAA') == 400 # 2 x 5A offers better than 3 x 3A + A

        # Special offers for B (2 for 45)
        assert checkout_solution.checkout('BB') == 45
        assert checkout_solution.checkout('BBB') == 75
        assert checkout_solution.checkout('BBBB') == 90

    def test_self_referential_free_offers(self):
        assert checkout_solution.checkout('FFF') == 20 # 2F(20) + 1 free. Exactly one group
        assert checkout_solution.checkout('FFFF') == 30 # 3F(30) + 1 free. Still only 1 complete group
        assert checkout_solution.checkout('FFFFFF') == 40 # 4F(40) + 2 free. 2 complete groups
        assert checkout_solution.checkout('FFFFFFFF') == 60 # 6F(60) + 2 free. 2 groups + 2 remainder

        # Test self-referential for U (buy 3U get 1U free)
        assert checkout_solution.checkout('UUU') == 120 # 3U(120)
        assert checkout_solution.checkout('UUUU') == 120 # 3U(120) + 1 free. Exactly one group
        assert checkout_solution.checkout('UUUUU') == 160 # 4U(140) + 1 free. 1 complete group + 1 remainder
        assert checkout_solution.checkout('UUUUUUUU') == 240 # 6U(240) + 2 free. 2 groups
        

    def test_checkout_combined_offers(self):
        # Combined special and free offers
        assert checkout_solution.checkout('AAAAAEEB') == 280 # 5A(200) + 2E(80)
        assert checkout_solution.checkout('EEBAAB') == 210 # 2E(80) + 2A(100) + 1B(30)
        assert checkout_solution.checkout('ABCDEABCDEFFF') == 300 # 2A(100) + 1B(30) + 2C(40) + 2D(30) + 2E(80) + 2F(20)

    def test_checkout_invalid_input(self):
        # Invalid inputs should return -1
        assert checkout_solution.checkout('a') == -1 # lowercase 
        assert checkout_solution.checkout('-') == -1 # Special char 
        assert checkout_solution.checkout('ABCa') == -1 # mixed valid/invalid
        assert checkout_solution.checkout('   ') == -1 # spaces
        assert checkout_solution.checkout(None) == -1 # None
        assert checkout_solution.checkout(123) == -1 # non-string

    def test_complex_combinations(self):
        # Test combination of multiple offers
        assert checkout_solution.checkout('AAAAAEEBAAABBB') == 485  # 5A(200) + 3A(130) + 2E(80) + 1 free B + 2B(45) + B(30)
        
        # Complex test with H and K offers
        assert checkout_solution.checkout('HHHHHHHHHHKK') == 230  # 10H(80) + 2K(150)
        
        # Complex test with P, Q, and R offers
        assert checkout_solution.checkout('PPPPPQQQRRR') == 330  # 5P(200) + 3Q(80) + 3R(50) + 1 free Q
        
        # Complex test with multiple free offers
        assert checkout_solution.checkout('EEBNNMRRQ') == 230  # 2E(80) + 1 free B + 2N(80) + 1M(15) + 2R(100) + 1Q(30) - not enough N for free M
        
        # Test with all types of offers (pricing special offers, free item offers, self-referential)
        assert checkout_solution.checkout('AAAAABBEEFFFHHHHHKKKNNNMPPPPPQQQRRRUVVV') == 1020
        # 5A(200) + 2B(45) + 2E(80) + 1 free B + 2F(20) + 1 free F + 5H(45) + 2K(150) + 3N(120) + 1 free M + 5P(200) + 2Q(60) + 1 free Q (from R) + 3R(150) + 1U(40) + 3V(130)

    def test_all_items(self):
        # One of each item
        assert checkout_solution.checkout('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == 965

        

    
