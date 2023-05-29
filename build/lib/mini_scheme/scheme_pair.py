from .scheme_repr import get_repr
class EmptyList:
    @classmethod
    def to_list(self):
        return []
    def __repr__(self):
        return '()'
    def __bool__(self):
        return False
class Pair:
    def __init__(self,a,b):
        self.car=a
        self.cdr=b or EmptyList()
    @classmethod
    def from_list(cls,l):
        if not l:
            return EmptyList()
        if len(l)==1:
            return cls(l[0],EmptyList())
        return cls(l[0],cls.from_list(l[1:]))
    def to_list(self):
        try:
            return [self.car]+self.cdr.to_list()
        except AttributeError:
            raise TypeError("this pair is not a list")
    def __repr__(self):
        if hasattr(self.cdr,"to_list"):
            return f'({" ".join(get_repr(i) for i in self.to_list() if type(i)!=EmptyList)})'
        return f'({get_repr(self.car)} . {get_repr(self.cdr)})'
