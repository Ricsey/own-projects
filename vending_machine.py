from dataclasses import dataclass


@dataclass
class ItemLine:
    name: str
    price: float
    quantity: int

    def empty(self):
        return self.quantity <= 0

class Stock:

    def __init__(self, items: dict[str, ItemLine]):
        self.items = items

    def get_item_line(self, code: str) -> ItemLine:
        return self.items[code]

    def valid_code(self, code: str) -> bool:
        return code in self.items.keys()

class CoinBox:

    def __init__(self, money: int) -> None:
        self.money = money

    def can_pay_change(self, change: int) -> bool:
        return change <= self.money

    def decrease(self, pay_amount: int) -> None:
        self.money -= pay_amount
            

class VendingMachine:

    def __init__(self, stock: Stock, coin_box: CoinBox) -> None:
        self.stock = stock
        self.coin_box = coin_box
    
    def pay(self, item_price: int) -> int:
        sum_coins = 0
        while sum_coins < item_price:
            try:
                sum_coins += int(input(f'Missing {item_price - sum_coins}. The price is {item_price} '))
            except ValueError:
                print('Invalid coin!')
        return sum_coins

    def buy(self, code: str) -> None:
        if not self.stock.valid_code(code):
            print(f'Invalid code: {code}')
            return

        item_line = self.stock.get_item_line(code)

        if item_line.empty():
            print(f'{item_line.name} is empty!')
            return

        total_payed = self.pay(item_line.price)
        change = total_payed - item_line.price

        if not self.coin_box.can_pay_change(change):
            print('Cannot pay change')
            return

        
        self.coin_box.decrease(change)
        print(f'Change is {change}')
        item_line.quantity -= 1
        print(f'You bought {item_line.name} for {item_line.price}')

def main():
    items = {
        'a1' : ItemLine(name='Coca cola', 
                        price=500,
                        quantity=2),
        'a2' : ItemLine(name='Pepsi', 
                        price=1000,
                        quantity=1),                    
    }
    
    vending_machine = VendingMachine(stock=Stock(items), coin_box=CoinBox(money=100))
    while (running := True):
        code = input('Write the code of the desired item: ')
        if code.lower() == 'x':
            break
        vending_machine.buy(code)

if __name__ == '__main__':
    main()
