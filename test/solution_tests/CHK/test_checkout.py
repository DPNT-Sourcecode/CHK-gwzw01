from solutions.CHK import checkout_solution

class TestCheckout():
    def test_calculate_cost_for_sku(self):
        assert checkout_solution.calculate_cost_for_sku('A', 1) == 50
        assert checkout_solution.calculate_cost_for_sku('A', 2) == 100
        assert checkout_solution.calculate_cost_for_sku('A', 3) == 130
        assert checkout_solution.calculate_cost_for_sku('A', 4) == 180
        assert checkout_solution.calculate_cost_for_sku('A', 5) == 230
        assert checkout_solution.calculate_cost_for_sku('A', 6) == 260

        assert checkout_solution.calculate_cost_for_sku('C', 1) == 20
        assert checkout_solution.calculate_cost_for_sku('C', 2) == 40
        assert checkout_solution.calculate_cost_for_sku('C', 3) == 60


    def test_checkout(self):
        # Empty string should cost 0
        assert checkout_solution.checkout('') == 0
        
        # Single items
        assert checkout_solution.checkout('A') == 50    # 1A = 50
        assert checkout_solution.checkout('AB') == 80   # 1A(50) + 1B(30) = 80
        
        # Special offers for A (3 for 130)
        assert checkout_solution.checkout('AAA') == 130      # 3A special offer
        assert checkout_solution.checkout('AAAA') == 180     # 3A(130) + 1A(50)
        assert checkout_solution.checkout('AAAAA') == 230    # 3A(130) + 2A(100)
        assert checkout_solution.checkout('AAAAAA') == 260   # 2 × 3A special offers
        
        # Mixed items
        assert checkout_solution.checkout('ABCD') == 115     # 1A(50) + 1B(30) + 1C(20) + 1D(15)
        assert checkout_solution.checkout('ABCDABCD') == 215 # 2A(100) + 2B(45) + 2C(40) + 2D(30)
        assert checkout_solution.checkout('ABCDABCDABCD') == 310 # 3A(130) + 3B(90) + 3C(60) + 3D(45)