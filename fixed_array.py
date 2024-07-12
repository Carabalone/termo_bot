class FixedArray:
    def __init__(self, size: int):
        self.size = size
        self.array = [None for n in range(self.size)]

    def push(self, obj):
        for i in range(self.size):
            if (self.array[i] == None):
                self.array[i] = obj
                return
        
        previous = self.array[0]
        save = None
        for i in range(self.size):
            save = self.array[i]
            self.array[i] = previous
            previous = save


        self.array[0] = obj

    def push_list(self, lst):
        for i in range(min(len(lst), self.size)):
            self.push(lst[i])

    def __getitem__(self, index):
        if 0 <= index < self.size:
            return self.array[index]
        else:
            raise IndexError("Index out of range")

    def __str__(self):
        return str(self.array)
            

if __name__ == "__main__":
    fixed_array = FixedArray(5)
    print(fixed_array)
    fixed_array.push_list([1, 2, 3, 4, 5])
    print(fixed_array)  # Output: [1, 2, 3, 4, 5]
    fixed_array.push(6)
    print(fixed_array[0])  # Output: 6
    print(fixed_array[1])  # Output: 1
    print(fixed_array)  # Output: [6, 1, 2, 3, 4]
    fixed_array.push(7)
    print(fixed_array)  # Output: [6, 1, 2, 3, 4]
    fixed_array.push(7)
    print(fixed_array)  # Output: [6, 1, 2, 3, 4]
    fixed_array.push(7)
    print(fixed_array)  # Output: [6, 1, 2, 3, 4]
    try:
        print(fixed_array[5])  # Raises IndexError
    except IndexError:
        print("Index out of range")
    try:
        print(fixed_array[10])  # Raises IndexError
    except IndexError:
        print("Index out of range")
    try:
        print(fixed_array[-1])  # Raises IndexError
    except IndexError:
        print("Index out of range")
    try:
        print(fixed_array[-10])  # Raises IndexError
    except IndexError:
        print("Index out of range")
