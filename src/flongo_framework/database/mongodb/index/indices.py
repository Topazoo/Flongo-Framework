
from ....database.mongodb.index.base import MongoDB_Index

class MongoDB_Indices:
    ''' Client to store a collection of MongoDB index information '''

    def __init__(self, *indices:MongoDB_Index):
        self._index = 0
        self._indices:list[MongoDB_Index]= list(indices)


    def add_index(self, index:MongoDB_Index):
        ''' Add an index to be stored '''
        
        self._indices.append(index)


    def __iter__(self):
        # Return the iterator object (in this case, self)
        return self


    def __next__(self) -> MongoDB_Index:
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
    
    
    def __len__(self):
        return len(self._indices)