class Person:
    def __init__(self, name):
        self.name = name

    def test(self, a):
        print(a)
        print(self.name)

    def execute(self, *args):
        return getattr(self, self.name)(args)


class Person2:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def test(self, a):
        print(a)

    def process(self, pname, *args):
        return getattr(self, pname)(args)


person2 = Person2('test', 12)
person2.process('test')