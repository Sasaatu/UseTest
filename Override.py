
'''class parent:
    parent_name = 'parent'

    def parent_func(self):
        print('Parent method', end=' ')
        print(self.parent_name)

class child(parent):
    child_name = 'child'

    def child_func(self):
        print('Child method', end=' ')
        print(self.child_name)


Inst1 = child()
print(Inst1.parent_name)
Inst1.parent_func()'''



class MyBase:
    coeff = 2

    def __init__(self, x):
        self.x = x

    def mult(self):
        return self.coeff * self.x


class MyDevlop(MyBase):
    coeff = 3

    # Reconfigure constructor
    def __init__(self, x, y):
        # call base function
        super().__init__(x) 
        self.y = y

    # (7)新しいメソッドを追加
    def mult2(self):
        return self.coeff * self.x * self.y


Inst2 = MyBase(10)
print('Base mult: {}' .format(Inst2.mult())) 

Inst3 = MyDevlop(10, 20)
print('Devlopped mult: {}' .format(Inst3.mult()))
print('Devlopped mult2: {}' .format(Inst3.mult2()))

