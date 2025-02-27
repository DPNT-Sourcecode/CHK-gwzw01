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
        assert checkout_solution.checkout('FFF') == 20 # 2F

    def test_checkout_combined_offers(self):
        # Combined special and free offers
        assert checkout_solution.checkout('AAAAAEEB') == 280 # 5A(200) + 2E(80)
        assert checkout_solution.checkout('EEBAAB') == 210 # 2E(80) + 2A(100) + 1B(30)
        assert checkout_solution.checkout('ABCDEABCDE') == 280 # 2A(100) + 1B(30) + 2C(40) + 2D(30) + 2E(80)

    def test_checkout_invalid_input(self):
        # Invalid inputs should return -1
        assert checkout_solution.checkout('a') == -1 # lowercase 
        assert checkout_solution.checkout('X') == -1 # invalid SKU 
        assert checkout_solution.checkout('-') == -1 # Special char 
        assert checkout_solution.checkout('ABCa') == -1 # mixed valid/invalid
        assert checkout_solution.checkout('   ') == -1 # spaces
        assert checkout_solution.checkout(None) == -1 # None
        assert checkout_solution.checkout(123) == -1 # non-string

        

    


