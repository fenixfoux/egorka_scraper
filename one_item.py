class Item:
    def __init__(self):
        self.name = ""
        self.price = 0

    def __str__(self):
        return f"{self.name} - {self.price}"