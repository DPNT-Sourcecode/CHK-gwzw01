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
        assert checkout_solution.checkout('') == 0
        assert checkout_solution.checkout('A') == 50
        assert checkout_solution.checkout('AB') == 80
        assert checkout_solution.checkout('AAA') == 130
        assert checkout_solution.checkout('AAAA') == 180
        assert checkout_solution.checkout('AAAAA') == 230
        assert checkout_solution.checkout('AAAAAA') == 260