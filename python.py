##########################
### Python type annotations are part of Python syntax
### First version with Python 3 in 2008
### First spec of type annotations 2006 - PEP 3107 – Function Annotations



#########################
### Python has syntax for annotation but no type checker
### Type checkers are separated programs like MyPy,PyRight, Pylance(MS) - integrated with VS Code language server
### All types annotations are totally valid Python, runtime ignores them
### No compilation happens, no type annotations removal happens

### First version of annotated Python was compiled to Python language MyPy (2012)


from abc import abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable, Dict, Generic, List, Literal, NamedTuple, Optional, Protocol, Set, Tuple, TypeVar, TypedDict, Union










### Simple/Atomic types
def simple_types():
    a: str = "I am str"
    b: bool = True
    c: int = 12
    d: float = 1.2

    # Lists
    strs: List[str] = ['a','b']
    nums: List[int] = [1,2,3]

    ## x[y] - index syntax was allowed for everything in Python, also for a class










def dicts_maps_tuples():
    dic_nums: Dict[int, float] = {1: 1.2, 2: 2.2}
    dic_strs: Dict[str, str] = {'a': 'a', 'b': 'b'}

    class User:
        pass

    user_orders: Dict[User, List[int]] = {User(): [1,2,3], User(): [2,3,4]} # key are unique by identity

    # Sets
    set_nums: Set[str] = {'Dry', 'Dry'}












### Records/Structs/NamedTuple (AND)
def records():

    # Tuple
    point: Tuple[int, int] = 1,2

    # using NamedTuple
    class User(NamedTuple):
        name: str
        last_name: str

    guido = User(name="Guido", last_name="Python")

    # using dataclass = mutable NamedTuple
    @dataclass
    class UserDC:
        name: str
        last_name: str

    batman = UserDC(name='Bruce', last_name="Wayne")

    # using typeddict
    class UserMarvel(TypedDict):
        name: str
        last_name: str
    
    spider = UserMarvel(name='Peter', last_name='Parker')









#### Union (OR)
def union():
    union: Union[str, int] = 1
    union = 'aa' # ok
    union = 1.2 # error
    union = True # ok 🤔

    # compose unions
    unions: List[Union[float, int]] = [1, 1.2, 2.3]
    dict_union: Dict[Union[int, str], str] = {
        1: 'a',
        'key': 'b'
    }

    # new union syntax (Python 3.10) PEP 604 
    union_new: str | int = 'a'
    union_new = 1




### Intersection (AND)
def intersection():
    class A(TypedDict):
        a: str
    class B(TypedDict):
        b: str
    class C(A, B):
        ...
    
    c: C = {'a':'a','b':'b'}











### Optional/Nullable
def optional():
    x: int | None = 1
    x = None

    y: Optional[int] = 1
    y = None












### Any and Gradual types
def any():
    x: Any = 'a'
    x = 'b'
    x = 1









### Type aliases

# by design we cannot declare that in function scope
Grade = int
Name = str
DateBirth = date
def aliases():
    class Student(NamedTuple):
        name: Name
        last_name: Name
        birth: DateBirth

    School = Dict[Student, List[Grade]]

    batman = Student(name='Bruce', last_name='Wayne', birth=date(2000,10,10))
    joker = Student(name="Jack", last_name="Napier", birth=date(2000,10,10))
    school = School()
    school[batman] = [1,3,5]
    school[joker] = [5,5,5]









### Function types annotations
Comparator = Callable[[int, int], bool] # by design we cannot declare that in function scope
def functions():
    def compare(comparator: Comparator):
        def call(x: int, y: int):
            return comparator(x,y)
        return call

    is_bigger = compare(lambda x,y: x > y)
    is_bigger(1, 2) # False
    is_bigger(4,3) # True










### Type inference
def type_inference():
    def who_am_i(x: str):
        return x

    def who_am_i_second(x: str, y: int):
        return x + y # strong types WOW!

    def who_am_i_third(x: Dict[str, str], prefix: str):
        return {k:int(f'{prefix}{v}')for (k,v) in x.items()}

    def who_am_i_fourth(x: Dict[str, int], key: str):
        return x.get(key)


    def who_am_i_fifth():
        return {
            'a': 1,
            'b': True
        }

    def who_am_i_sixth(x: str | List[str]):
        if isinstance(x, List):
            return ''.join(x)
        else:
            return x










### Literal types
TeamMember = Literal['Batman'] | Literal['Robin']
def literals():
    bat: Literal['Batman'] = 'Batman'
    bat = 'Joker'

    bat_team_member: TeamMember = 'Robin'
    bat_team_member = 'Joker'

    def want_literal(x: TeamMember):
        match x:
            case 'Batman':
                return 'This city needs me'
            case 'Robin':
                return 'Holy...'
            case _:
                return 'Runtime allows the Joker'

        
    want_literal('Joker') # error
    return want_literal(bat_team_member)














### Generics
def generics():
    T = TypeVar('T', str, int)
    def append(x: T, y: T) -> T:
        return x + y

    x = append('a', 'a') # str
    y = append(1, 2) # int
    err = append(1, 'a') # error

    Key = TypeVar('Key')
    Val = TypeVar('Val')
    def val(dict: Dict[Key, Val], k: Key) -> Val:
        return dict[k]

    val1 = val({'a': 1}, 'a') # int
    val2 = val({'a':'b'}, 'a') # str
    val3 = val({'a':1}, 'b')













### User-defined generic
def custom_generics():

    IN = TypeVar('IN')
    OUT = TypeVar('OUT')
    class Mappable(Generic[IN]):
        @abstractmethod
        def map(self, f: Callable[[IN], OUT]) -> 'Mappable[OUT]': ...

    class Arr(Mappable[IN]):
        def __init__(self, list: List[IN]):
            self.list=list

        def map(self, f: Callable[[IN], OUT]) -> 'Arr[OUT]': 
            return Arr[OUT](list=[f(x) for x in self.list])


    x = Arr([1,2,3,4])
    y = x.map(lambda n: n+1)
    z = y.map(str)














### Type Guards
def type_guards():
    from typing_extensions import TypeGuard
    def is_str_list(val: List[Any]) -> TypeGuard[List[str]]:
        return all(isinstance(x, str) for x in val)

    def get_list_from_third_party(list: List[Any]):
        if is_str_list(list):
            return list
        else:
            raise ValueError('Not a str list')
        
    xs = get_list_from_third_party(['a','b'])

    @dataclass
    class Power:
        name: str
        level: int

    @dataclass
    class SuperHero:
        name: str
        powers: List[Power]
    
    @dataclass
    class Villain:
        name: str
        powers: List[Power]

    def is_superhero(x: object) -> TypeGuard[SuperHero]:
        if isinstance(x, SuperHero):
            return True
        else:
            return False

    superman = SuperHero(
        name="Superman",
        powers=[Power('flying',10)]
    )
    lex = Villain(
        name="Lex Luthor",
        powers=[Power('brain', 10)]
    )
    if is_superhero(lex):
        print(f'Yes, {lex.name} is a superhero')
    else:
        print(f'No, {lex.name} is not a superhero')












### Structural/Nominal types
def structural_nominal():

    @dataclass
    class SuperHero:
        name: str
    
    @dataclass
    class Villain():
        name: str

    # nominal
    x = SuperHero(name="Clark Kent")
    xx: Villain = x # error no Villain is not SuperHero

    """
    Nominal typing means that two variables are type-compatible if and only if their declarations name the same type.
    """

    # structural

    class Duck(Protocol):
        name: str

    def wants_a_duck(s: Duck):
        return s.name

    superman = SuperHero(
        name="Superman",
    )
    lex = Villain(
        name="Lex Luthor",
    )

    duck: Duck = lex # works

    wants_a_duck(superman) # works
    wants_a_duck(lex) # works

    """
        Duck typing
        If it looks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck.
    """

    # trying to simulate TS structural behavior on objects
    # TypeDict compare by structure
    class X(TypedDict):
        x: str

    class Y(TypedDict):
        x: str
        y: str

    def wants_x(x: X):
        return x.get('x')
    
    y: Y = {'x': 'x', 'y': 'y'}
    wants_x(y) # works













### Type transformations

"""
No type transformations (or no I know about)
"""

### Comparison

"""
👉 Gradual typing
👉 Included in base language syntax
👉 No compilation
👉 Nominal types support - default
👉 Limited but supported structural types support by protocols
👉 Heavily uses class syntax
👉 No type transformation functionalities
👉 Type syntax mostly as - what we can make in Python to still be Python - so tradeoffs like TypeVar

"""
"""
Does Python have his TypeScript? 
No, as type system syntax and types were included into Python
No, as static type checking is not a part of Python

Python with its build in syntax and already created type checkers is comparable with TypeScript 
Python transformed into kinda TypeScript
"""
