from typing import Any


class Term: 
    def __eq__(self, __value: object) -> bool:
        pass
    
    def __str__(self) -> str:
        pass
    
    def __call__(self, that):
        return Apply(self, that).reduction()
    
    def FV(self):
        pass
    
    def substitute(self):
        pass
    
    def reduction(self):
        pass


class Atom(Term):
    name: str

    def __init__(self, name="") -> None:
        self.name = name
        
    def __eq__(self, __value: object) -> bool:
        return self is __value
    
    def __str__(self) -> str:
        return self.name
    
    def __rshift__(self, that):
        return Map(self, that).reduction()
    
    def FV(self):
        return set(self)
        
    def substitute(self, var, subs):
        if self == var:
            return subs
        else:
            return self
        
    def reduction(self):
        return self
        
    
class Map(Term):
    bind: Atom
    body: Term

    def __init__(self, lhs: Atom, rhs: Term) -> None:
        self.bind = Atom(lhs.name)
        self.body = rhs.substitute(lhs, self.bind)
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Map) and \
            self.body == other.body.substitute(other.bind, self.bind)
        
        
    def __str__(self) -> str:
        return str("(") + str(u"\u03bb") + self.bind.__str__() + str(".") + self.body.__str__() + str(")")

    def __call__(self, rhs: Term) -> Any:
        return Apply(self, rhs).reduction()

    def FV(self):
        return self.body.FV() - set(self.bind)
    
    def substitute(self, var, subs):
        if var == self.bind:
            raise ValueError("Bounded variable leakage.")
        else:
            return Map(self.bind, self.body.substitute(var, subs))
        
    def reduction(self):
        if isinstance(self.body, Apply) and\
            self.body.rhs == self.bind and self.bind not in self.body.lhs.FV():
            return self.body.lhs.reduction()
        else:
            return Map(self.bind, self.body.reduction())
    

class Apply(Term):
    lhs: Term
    rhs: Term

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs
        
    def __eq__(self, other) -> bool:
        return isinstance(other, Apply) and \
            other.lhs == self.lhs and other.rhs == self.rhs
            
    def __str__(self):
        if isinstance(self.lhs, Atom):
            return str(self.lhs) + str(self.rhs)
        
        return str(self.lhs) + str("(") + str(self.rhs) + str(")")
        
    def FV(self):
        return set.union(self.lhs.FV(), self.rhs.FV())
        
    def substitute(self, var, subs):
        return Apply(self.lhs.substitute(var, subs), 
                     self.rhs.substitute(var, subs))
        
    def reduction(self):
        lhs_ = self.lhs.reduction()
        if isinstance(lhs_, Map):
            return lhs_.body.substitute(lhs_.bind, self.rhs).reduction()
        else:
            return Apply(lhs_, self.rhs.reduction())



# Test
if __name__ == '__main__':
    x = Atom("x")
    y = Atom("y")
    z = Atom("z")


    K = x >> (y >> x)
    print("K: ", K)

    S = (x >> (y >> (z >> ( (x(z))(y(z)) ))))
    print("S: ", S)
    
    
    I = (S(K))(K)
    print("Id: ", I)
    
    print(K(z))
    print(K(I))