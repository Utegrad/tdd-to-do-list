class Critter:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def _to_str(self):
        return f"{self.type} : {self.name}"

    def __repr__(self):
        return f"Critter() {self._to_str()}"

    def __str__(self):
        return f"{self.type} - {self.name}"

if __name__ == '__main__':
    items = (
        Critter('mammal', 'cat'),
        Critter('mammal', 'dog'),
        Critter('reptile', 'lizard'),
        Critter('mammal', 'horse'),
        Critter('amphibian', 'frog'),
    )
    value = 'mammal'

    # call any() on iterable of all items where item.attr == value
    # iterable of all items where item.attr == value
    # list comprehension
    mammals = [i for i in items if i.type == value]

    print(mammals)