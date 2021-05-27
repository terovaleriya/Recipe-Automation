from parse_ingredient.grammar import Grammar


class IngredQuantity:
    grammar = Grammar('../parse_ingredient/grammar.txt')

    def parse_quantity(self, quantity):
        if quantity is None:
            self.uom = None
            return
        res = IngredQuantity.grammar.parse(quantity)

        
