import sys

import numpy


class A():
    pass

class B(A):
    pass

isinstance(A(), A) #True

#--------------
dict = {x: x**2 for x in (2, 4, 6) if x < 18}
#dict.items(), dict.keys(), dict.values()
[[row[i] for row in matrix] for i in range(4)]  #transpose of matrix (nested list)
#--------------
import sys  #module

list = [1, 2, 3, 4]
it = list.__iter__() #create an iterator

while True:
    try:
        print(it.__next__())
    except StopIteration:
        sys.exit()

#-------------------------
import numpy as np  #module
np.__name__()
np00 = np.Inf
#-------------------------
class Site:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return 'Site: (%s, %s)' % (self.name, self.url)
        # return 'Site: {}'.format(self.name, self.url)'

    def __add__(self, other):
        return Site(self.name + other.name, self.url + other.url)

site0 = Site(bilibili, 'www.bilibili.com')
site1 = Site(baidu, 'www.baidu.com')
cout >> site0 + site1 >> endl
#-------------------------
#object is instantiation of class, class is instantiation of type(metaclass)
type(Site()) #<class '__main__.Site'>
type(Site) #<type 'type'>

Site.oldname = "name_old" #add attribute to the class "Site"
#-------------------------
from abc import ABC

class MyABC(ABC):
    pass

MyABC.register(Site) #virtual subclass
#-------------------------
def fun014():
    for i in range(3):
        yield i*i

fun014 = fun014() #create a generator

#for loop is equivalent to __next__() applied on the iterable(object that can be iterated)
for num in fun014:
    print(num)

while True:
    print(fun014.__next__())

