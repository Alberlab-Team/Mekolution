# Developed by 0N17
from math import *
from typing import *


class Vector2():
    def __init__(self, value : Tuple[float, float]) -> None:
        self.x = value[0]
        self.y = value[1]

    class get_with:

        def coordinates(x, y):
            return Vector2((x,y))

        def polar(angle : float, norm : float):
            x = cos(angle * pi/180)*norm
            y = sin(angle * pi/180)*norm
            return Vector2((x,y))

        def V3(vector3 : 'Vector3'):
            x = vector3.x
            y = vector3.y
            return Vector2((x,y))


        def VN(self, vectorN : 'VectorN'):
            x, y = vectorN.set_N(2, True, False).value
            return Vector2((x,y))

    def V0() -> 'Vector2' :
        return Vector2((0, 0))

    def tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


    def __add__(self, other : 'Vector2') :

        return Vector2((self.x + other.x, self.y + other.y))

    def __sub__(self, other : 'Vector2') :

        return Vector2((self.x - other.x, self.y - other.y))

    def __neg__(self):

        return Vector2.V0() - self

    def __mul__(self, other : float) :

        return Vector2((self.x * other, self.y * other))

    def __truediv__(self, other : float) :

        return Vector2((self.x / other, self.y / other))

    def __floordiv__(self, other : float) :

        return Vector2((self.x // other, self.y // other))

    def __eq__(self, other : 'Vector2') -> bool:

        return self.tuple() == other.tuple()

    def norm(self) -> float:
        return sqrt((self.x ** 2) + (self.y ** 2))

    def into(self, V1 : 'Vector2', V2 : 'Vector2') -> bool:
        x = (V1.x < self.x < V2.x) or (V2.x < self.x < V1.x)
        y = (V1.y < self.y < V2.y) or (V2.y < self.y < V1.y)
        return x and y

    def dist(V1 : 'Vector2', V2 : 'Vector2'):
        return (V1 - V2).norm()

    def smallest(self):
        return min(self.tuple())

    def bigest(self):
        return max(self.tuple())
    
    def get_vectorN(self)-> 'VectorN':
        return VectorN([self.x, self.y])
    
class Vector3():
    def __init__(self, value : Tuple[float, float, float]) -> None:
        self.x = value[0]
        self.y = value[1]
        self.z = value[2]

    class get_with:

        def coordinates(x, y, z):
            return Vector3((x,y,z))

        def polar(angle_xy : float, angle_z, norm : float):
            x = cos(angle_xy * pi/180) * cos(angle_z * pi/180) *norm
            y = sin(angle_xy * pi/180) * cos(angle_z * pi/180) *norm
            z = sin(angle_z * pi/180) * norm
            return Vector3((x,y,z))

        def V2(vector2 : 'Vector2', z=0):
            x = vector2.x
            y = vector2.y
            return Vector3((x,y,z))

        def VN(vectorN : 'VectorN'):
            x, y, z = vectorN.set_N(3, True, False).value
            return Vector2((x,y,z))

    def V0() -> 'Vector3' :
        return Vector3((0, 0, 0))

    def tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)


    def __add__(self, other : 'Vector3') :

        return Vector3((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other : 'Vector2') :

        return Vector3((self.x - other.x, self.y - other.y, self.z - other.z))

    def __neg__(self):

        return Vector3.V0() - self

    def __mul__(self, other : float) :

        return Vector3((self.x * other, self.y * other, self.z * other))

    def __truediv__(self, other : float) :

        return Vector3((self.x / other, self.y / other, self.z / other))

    def __floordiv__(self, other : float) :

        return Vector3((self.x // other, self.y // other, self.z // other))

    def __eq__(self, other : 'Vector3') -> bool:

        return self.tuple() == other.tuple()

    def norm(self) -> float:
        return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

    def into(self, V1 : 'Vector3', V2 : 'Vector3') -> bool:
        x = (V1.x < self.x < V2.x) or (V2.x < self.x < V1.x)
        y = (V1.y < self.y < V2.y) or (V2.y < self.y < V1.y)
        z = (V1.z < self.z < V2.z) or (V2.z < self.z < V1.z)
        return x and y and z

    def dist(V1 : 'Vector3', V2 : 'Vector3'):
        return (V1 - V2).norm()

    def smallest(self):
        return min(self.tuple())

    def bigest(self):
        return max(self.tuple())
    
    def get_vectorN(self)-> 'VectorN':
        return VectorN([self.x, self.y, self.z])

class VectorN():
    def __init__(self, value : List[float]) -> None:
        self.value = [*value]
    
    class get_with:
        def coordinates(*values : float):
            return VectorN(values)

        def polar(angles : List[float], norm : float = 1):
            value = [norm]
            for i in range(len(angles)):
                for j in range(len(value)):
                    value[j] *= cos(angles[i] * pi/180)
                value.append(sin(angles[i] * pi/180)*norm)
            return VectorN(value)

        def polars(norm : float = 1, *angles : float):
            return VectorN.get_with.polar(angles, norm)

    def get_size(self):
        return len(self.value)

    def V0(N) -> 'VectorN' :
        coordinates = []
        for i in range(N):
            coordinates.append(0)
        return VectorN(coordinates)

    def get_list(self) -> List[float]:
        return [*self.value]
    
    def set_N(self, N, cut : bool = False, on_this : bool = False):
        Missing = N - self.value.__len__()
        if Missing < 0:
            if not cut :
                print('Vector resized must have as many or less coordinates as the expected new Vector. Cut vector has been returned')
            if on_this:
                self.value = self.value[:N]
            else:
                return VectorN(self.value[:N])
        else:
            if on_this:
                for i in range(N):
                    self.value.append(0)
            else:
                value = [*self.value]
                for i in range(Missing):
                    value.append(0)
                return VectorN(value)
            

    def __add__(self, other : 'VectorN') :
        len_self = self.value.__len__()
        len_other = other.value.__len__()
        if len_self < len_other:
            return other + self
        else:
            returned = VectorN([])
            for i in range(len_other):
                returned.value.append(self.value[i] + other.value[i])
            returned.value.extend(self.value[len_other:])
            return returned

    def __sub__(self, other : 'Vector2') :
        len_self = self.value.__len__()
        len_other = other.value.__len__()
        if len_self < len_other:
            return - other + self
        else:
            returned = VectorN([])
            for i in range(len_other):
                returned.value.append(self.value[i] - other.value[i])
            returned.value.extend(self.value[len_other:])
            return returned

    def __neg__(self):

        return VectorN.V0(self.value.__len__()) - self

    def __mul__(self, other : float) :
        returned = []
        for i in range(self.value.__len__()):
            returned.append(self.value[i] * other)
        return VectorN(returned)

    def __truediv__(self, other : float) :
        returned = []
        for i in range(self.value.__len__()):
            returned.append(self.value[i] / other)
        return VectorN(returned)

    def __floordiv__(self, other : float) :
        returned = []
        for i in range(self.value.__len__()):
            returned.append(self.value[i] // other)
        return VectorN(returned)

    def __eq__(self, other : 'VectorN') -> bool:
        return self.value == other.value

    def norm(self) -> float:
        returned = 0
        for coordinate in self.value:
            returned += coordinate ** 2
        returned = sqrt(returned)
        return returned

    def into(self, V1 : 'VectorN', V2 : 'VectorN') -> bool:
        max_len = max([len(self.value),len(V1.value),len(V2.value)])
        self2 = self.set_N(max_len)
        v1 = V1.set_N(max_len)
        v2 = V2.set_N(max_len)
        for i in range(max_len):
            if not ((v1.value[i] < self2.value[i] < v2.value[i]) or (v2.value[i] < self2.value[i] < v1.value[i])):
                return False
        return True

    def dist(V1 : 'VectorN', V2 : 'VectorN'):
        return (V1 - V2).norm()

    def smallest(self):
        return min(self.value)

    def bigest(self):
        return max(self.value)


def parse(Vector : Union[Vector2, Vector3, VectorN], type_ : Type):
    Base_type = type(Vector)

    if type_ == Vector2:
        if Base_type in [Vector2, Vector3]:
            return Vector2([Vector.x, Vector.y])
        elif Base_type == VectorN:
            return Vector2(Vector.set_N(2, True, False).value)
        
    elif type_ == Vector3:
        if Base_type in [Vector2, Vector3]:
            try:
                z = Vector.z
            except:
                z = 0
            return Vector3([Vector.x, Vector.y, z])
        elif Base_type == VectorN:
            return Vector3(Vector.set_N(3, True, False).value)

    elif type_ == VectorN:
        if Base_type == Vector2:
            return VectorN([Vector.x, Vector.y])
        elif Base_type == Vector3:
            return VectorN([Vector.x, Vector.y, Vector.z])
        elif Base_type == VectorN:
            return VectorN(Vector.value)