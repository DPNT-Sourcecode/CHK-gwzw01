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
        assert checkout_solution.checkout('AAA') == 130
        assert checkout_solution.checkout('AAAA') == 180
        assert checkout_solution.checkout('AAAAA') == 230
        assert checkout_solution.checkout('AAAAAA') == 260

        # Special offers for B (2 for 45)
        assert checkout_solution.checkout('BB') == 45
        assert checkout_solution.checkout('BBB') == 75
        assert checkout_solution.checkout('BBBB') == 90

    def test_checkout_free_offers(self):
        # E offers (2E gets one B free)
        assert checkout_solution.checkout('EEB') == 80
        assert checkout_solution.checkout('EEBB') == 110
        assert checkout_solution.checkout('EEBEEB') == 160
        assert checkout_solution.checkout('EEBEEBB') == 190

    def test_checkout_combined_offers(self):
        # Combined offers
        assert checkout_solution.checkout('AAABB') == 175 # 3A(130) + 2B(45)
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

        

    