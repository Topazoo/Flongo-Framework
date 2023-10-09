
from src.database.mongodb.index.base import Index

class Indices:
    ''' Client to store a collection of MongoDB index information '''

    def __init__(self, indices:list[Index]):
        self._index = 0
        self._indices:list[Index]= indices


    def add_index(self, index:Index):
        ''' Add an index to be stored '''
        
        self._indices.append(index)


    def __iter__(self):
        # Return the iterator object (in this case, self)
        return self


    def __next__(self) -> Index:
        # Implement the __next__ method for iteration
        if self._index < len(self._indices):
            result = self._indices[self._index]
            self._index += 1
            return result
        # Reset the index for future iterations
        self._index = 0
        # Raise StopIteration to signal the end of the iteration
        raise StopIteration
    

    def __str__(self):
        return str(self._indices)