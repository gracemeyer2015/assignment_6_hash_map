# Name: Grace Meyer
# OSU Email: meyerg3@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/05/25
# Description: creates a hash map using a dynamic array that accepts HashEntry instances/Objects at its given indices
#with data members self._bucket holding the data entered. This implementation does not rely on the linked list class as
#with open adddressing we use some form of probing to find the next valid index of entry, in this case quadratic probing is used
# the put method attempts to add a HashEntry object to the dynamic array, put calls resize_table which creates a new table of
# the given argument passed to resize as suggested capacity, resize also calls put when building the new dynamic array of
# new capacity, table load gives the load factor to be monitored within put, empty_buckets gives the number of blank
#slots in the array, get returns the value given a key passed as argument, contains_key returns a boolean value that gives
#whether that key is already in the hashmap, remove uses a key to search for pair to remove, get_keys_and_values returns
# a dynamic array with all the key value pairs found in the hashmap at the given time, clear resets the self._buckets to
# an empty dynamic array/emptied hashmap clearing original contents of self._buckets, finally I have iter and next within
#the hashmap class that make the hashmap iterable

from unittest import skipIf

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Uses open addressing to add a key value pair or to update the given key's value
        if it already is found in the hash map

        :param key: key to add and to hash
        :param value: value to add as a pair with given key
        """
        #for open addressing load factor is to be at most 0.5 cause no Linked list
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)
        initial_index = hash % self._capacity

        j = 0
        # j starts at 0 j = 0 represents first attempt to find right index with quadratic probing
        while j < self._capacity:
            index = (initial_index + j ** 2) % self._capacity
            initial_val = self._buckets.get_at_index(index)

            # if the given index does not already hold a hashEntry instance the new instance is added
            if initial_val is None or initial_val.is_tombstone:
                self._buckets.set_at_index(index, HashEntry(key, value))
                self._size += 1
                return

            # if the key is found the value is overwritten for the given key
            if initial_val.key == key:
                self._buckets.set_at_index(index, HashEntry(key, value))
                return

            #moves to next probing attempt if conditions arent met
            j += 1

        return


    def resize_table(self, new_capacity: int) -> None:
        """
        called within put to ensure the size to capacity ration remains at 0.50 and lower, creates a new
        DA and rehashes keys given the new usually larger capacity

        :param new_capacity: new capacity request
        """
        #capacity request is invalid
        if new_capacity < self._size or new_capacity < 1:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)


        #save old values and reset
        old_buckets = self._buckets
        old_capacity = self._capacity

        self._capacity = new_capacity
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

        #uses put to rehash and insert new values or key value pairs in the correct spot
        for i in range(old_capacity):
            index_val = old_buckets.get_at_index(i)
            if index_val is not None and not index_val.is_tombstone:
                self.put(index_val.key, index_val.value)





    def table_load(self) -> float:
        """
        calculates the load factor size over capacity of the hash map
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        goes through dynamic array seeing if values are none returns count of empty buckets

        :return: count of empty buckets
        """
        count = 0
        for i in range(self._capacity):
            if self._buckets.get_at_index(i) is None:
                count += 1
        return count

    def get(self, key: str) -> object:
        """
        finds the value of a key value pair based on the key argument given uses quadratic probing to find
        where the key could be if it is not the first initial value

        :param key: key to look for in hash map

        :return: value of a key value pair given the key as parameter
        """
        hash = self._hash_function(key)
        initial_index = hash % self._capacity

        #same quadratic probing method used as is in put
        j = 0
        while j < self._capacity:
            index = (initial_index + j ** 2) % self._capacity
            index_val = self._buckets.get_at_index(index)

            if index_val is None:
                return None
            if index_val.key == key and not index_val.is_tombstone:
                return index_val.value

            j+=1

        return None






    def contains_key(self, key: str) -> bool:
        """
        hashes key to find index to start probing searching at max the entire capacity of the array which
        will only be at most half full returns true if key is found in hash map

        :param key: key to look for in hash map

        :return: True if key is found in hash map, false if not found
        """
        hash = self._hash_function(key)
        initial_index = hash % self._capacity

        j = 0
        while j < self._capacity:
            index = (initial_index + j ** 2) % self._capacity
            index_val = self._buckets.get_at_index(index)

            if index_val is None:
                return False
            if index_val.key == key and not index_val.is_tombstone:
                return True

            j+=1

        return False


    def remove(self, key: str) -> None:
        """
        Removes a value from the hash map by setting the index to be a tombstone if the key argument is found within
        the hash map

        :param key: key to remove from hash map/ to find index to set to tombstone is true
        """

        hash = self._hash_function(key)
        initial_index = hash % self._capacity

        for j in range(self._capacity):
            index = (initial_index + j ** 2) % self._capacity
            initial_val = self._buckets.get_at_index(index)
            if initial_val is None:
                return
            if initial_val.key == key and not initial_val.is_tombstone:
                initial_val.is_tombstone = True
                self._size -= 1
                return



    def get_keys_and_values(self) -> DynamicArray:
        """
        Collects the key value pairs of the hash map by going through indices of capacity checking if
        there is a key and value there if there is it is added to the dynamic array that is returned
        at the end

        :return DynamicArray: containing key and value pairs of the hash map
        """
        val_array = DynamicArray()
        for i in range(self._capacity):
            index_val = self._buckets.get_at_index(i)
            if index_val is not None and not index_val.is_tombstone:
                val_array.append((index_val.key, index_val.value))

        return val_array

    def clear(self) -> None:
        """
        Sets the data storage data member self._buckets to a new DA adds the value none for each capacity slot
        """
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(None)

        self._size = 0


    def __iter__(self):
        """
        Initializes HashMap class as its own iterator, sets an index starting at 0 to allow for the
        use of iterators as for loops
        """
        self._index = 0
        return self

    def __next__(self):
        """
        calls to next return the next valid hash entry of the given instance of the hash map
        it is made to skip over none and tombstone slots and return all valid entries
        stopIteration is raised when there are no longer any valid entries
        """
        while self._index < self._capacity:
            initial_val = self._buckets.get_at_index(self._index)
            self._index += 1
            if initial_val is not None and not initial_val.is_tombstone:
                return initial_val
        raise StopIteration



# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
