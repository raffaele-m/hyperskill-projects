# Write your code here
class CoffeeMachine:
    def __init__(self, resource):
        self.resource = resource
        self.input_action()

    def input_action(self):
        available_action = {'buy': self.buy, 'fill': self.fill, 'take': self.take, 'remaining': self.display_resource, 'exit': self.exit_program}
        self.input_value = input('Write action (buy, fill, take, remaining, exit):\n')
        try:
            return available_action[self.input_value]()
        except KeyError:
            print('Action not available, try again\n')
            return self.input_action()

    def display_resource(self):
        print(f"""
The coffee machine has:
{self.resource.get('water')} of water
{self.resource.get('milk')} of milk
{self.resource.get('beans')} of coffee beans
{self.resource.get('d_cups')} of disposable cups
{self.resource.get('money')} of money
""")
        return self.input_action()

    def espresso(self):
        """For one espresso, the coffee machine needs
        250 ml of water and 16 g of coffee beans. It costs $4."""
        ingredients = [('water', 250), ('beans', 16)]
        for ingredient in ingredients:
            if self.resource[ingredient[0]] // ingredient[1] < 1:
                print(f'Sorry not enough {ingredient[0]}!\n')
                return self.input_action()
        self.resource['water'] -= 250
        self.resource['beans'] -= 16
        self.resource['money'] += 4
        self.resource['d_cups'] -= 1
        print('have enough resources, making you a coffee!\n')
        return self.input_action()

    def latte(self):
        """For a latte, the coffee machine needs 350 ml of water,
        75 ml of milk, and 20 g of coffee beans. It costs $7."""
        ingredients = [('water', 350), ('milk', 75), ('beans', 20)]
        for ingredient in ingredients:
            if self.resource[ingredient[0]] // ingredient[1] < 1:
                print(f'Sorry not enough {ingredient[0]}!\n')
                return self.input_action()
        self.resource['water'] -= 350
        self.resource['milk'] -= 75
        self.resource['beans'] -= 20
        self.resource['money'] += 7
        self.resource['d_cups'] -= 1
        print('I have enough resources, making you a coffee!\n')
        return self.input_action()

    def cappuccino(self):
        """And for a cappuccino, the coffee machine needs 200 ml of water,
        100 ml of milk, and 12 g of coffee. It costs $6."""
        ingredients = [('water', 200), ('milk', 100), ('beans', 12)]
        for ingredient in ingredients:
            if self.resource[ingredient[0]] // ingredient[1] < 1:
                print(f'Sorry not enough {ingredient[0]}!\n')
                return self.input_action()
        self.resource['water'] -= 200
        self.resource['milk'] -= 100
        self.resource['beans'] -= 12
        self.resource['money'] += 6
        self.resource['d_cups'] -= 1
        print('I have enough resources, making you a coffee!\n')
        return self.input_action()

    def buy(self):
        available_types = {'1': self.espresso,
                           '2': self.latte,
                           '3': self.cappuccino,
                           'back': self.back}
        self.input_type = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n')
        try:
            return available_types[self.input_type]()
        except KeyError:
            print('Not available!\n')
            return self.buy()
    def fill(self):
        water = int(input('Write how many ml of water do you want to add:\n'))
        milk = int(input('Write how many grams of coffee beans do you want to add:\n'))
        coffee = int(input('Write how many grams of coffee beans do you want to add:\n'))
        d_cups = int(input('Write how many disposable cups of coffee do you want to add:\n\n'))
        self.resource['water'] += water
        self.resource['milk'] += milk
        self.resource['beans'] += coffee
        self.resource['d_cups'] += d_cups
        return self.input_action()

    def take(self):
        print(f"I gave you ${self.resource['money']}\n")
        self.resource['money'] = 0
        return self.input_action()

    def back(self):
        return self.input_action()

    @staticmethod
    def exit_program():
        return exit(0)


supplies = {
    'money': 550,
    'water': 400,
    'milk': 540,
    'beans': 120,
    'd_cups': 9
}

CoffeeMachine(supplies)
