import dataclasses
import random
from dataclasses import dataclass #Really important module and decorater!!!!!!!!
from abc import ABC
from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T') #Means any type
#A = TypeVar('A', str, bytes) #must be string or bytes

class Distribution(ABC, Generic[T]): #Generic can equip abstract/concrete class with type: T
    @abstractmethod
    def sample(self) -> T:
        pass

    DistributionOrnot = True

@dataclass(frozen = True) #Immutability -> can work in dict {key: value}
class Die(Distribution[int]):
    sides: int #help to typecheck

    def sample(self) -> int:
        return random.randint(1, self.sides)

#print(Die(6))
#print(isinstance(Die(6), Die)) #True
#print(Die(10) + Die(11))
#print(Die(6) == Die(6))

d6 = Die(sides = 6)
#d6.sides = 10
d1 = dataclasses.replace(d6, sides = 10)
print(d1)
print(d1.DistributionOrnot)

import statistics
def expected_value(d: Distribution[int], n: int = 100) -> float: #typecheck/type annotation here!
    return statistics.mean(d.sample() for _ in range(n))

print(expected_value(Die(6)))