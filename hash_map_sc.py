# Name: Grace Meyer
# OSU Email: meyerg3@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/05/25
# Description: the separate chaining implementation of a hash map that has buckets which are the indices of the dynamic array
# containing linked lists, the linked lists form when collisions happen to make it so that no value is overwritten, it has
# methods put to add values or key value pairs to the hash map, resize table to fit updating size which is called within put,
# Table_load method is called in put to keep the size capacity ratio at most 1, empty_buckets counts number of empty buckets
# get, contains_key, and remove use a key parameter to return a value or boolean, or to remove a value from the hash map
# get keys and values gives a clear picture of what keys and values are represented in the hash map with one value per key
# find_mode is a function not within the HashMap class but uses the hashmap class by building one based on a given da to
# find the mode of a da


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
         Calcs hash index using key(string), the hash function, and the capacity.
         The variable bucket is the linked list at the given hash index that holds
         the key value pairs that map to the same hash index. If the key exists within the linked list
         the value is updated, if not the key and value are added as a pair, node of the linked list

        :param key: key is a string used to calculate where a given value or key value pair is to be stored
        :param value: value associated with key to be added
        """
        #esnures that the load factor of self._buckets stays at or below 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity*2)

        index = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(index)
        node = bucket.contains(key)

        #if the key already exists assign it the new value, if not, add it to bucket using insert
        if node:
           node.value = value
        else:
            bucket.insert(key, value)
            self._size += 1



    def resize_table(self, new_capacity: int) -> None:
        """
        Is called in put to increase the capacity of the hash map when load factor is >= 1. Creates a new dynamic array
        of empty linked lists, uses put to rehash keys and store key value pairs more evenly based on capacity

        :param new_capacity: new capacity of the hash map given in put as 2*capacity's next prime if not prime
        """
        #requested capacity is invalid
        if new_capacity < 1:
           return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        #save original data and capacity to reference in building new hashmap of new capacity
        old_capacity = self._capacity
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._size = 0
        self._buckets = DynamicArray()

        for i in range(self._capacity):
            self._buckets.append(LinkedList())

        #gets values from original bucket's linked lists and rehashes/stores values
        for i in range(old_capacity):
            bucket = old_buckets.get_at_index(i)
            #available because of linked list iterator
            for node in bucket:
                self.put(node.key, node.value)
















    def table_load(self) -> float:
        """
        calculates the load factor of the hash table n total values/m buckets
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Gives the number of buckets that are empty by using length method for linked list,
        checking if the length is 0

        :return: int, number of empty buckets
        """
        count = 0
        for i in range(self._capacity):
            bucket = self._buckets.get_at_index(i)
            if bucket.length() == 0:
                count += 1
                continue

        return count



    def get(self, key: str) -> object:
        """
        given the key it uses hash function to find which bucket the key would be in,
        uses contains to check if the bucket has a value with that key

        :param key: key to look for in hash map
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets.get_at_index(index)
        node = bucket.contains(key)
        if node:
            return node.value
        else:
            return None


    def contains_key(self, key: str) -> bool:
        """
        similar to get but instead of returning the value it returns boolean value based if key is found
        both use contains from the linked list methods

        :param key: key to look for in hash map

        :return: boolean true if key exists false otherwise
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets.get_at_index(index)
        node = bucket.contains(key)
        if node:
            return True
        else:
            return False


    def remove(self, key: str) -> None:
        """
        removes a value given a key from the hash map uses remove from the linked list class that
        returns boolean value if true is returned decreases size by 1

        :param key: key to look for in hash map
        """
        if self.contains_key(key):
            hash = self._hash_function(key)
            index = hash % self._capacity
            bucket = self._buckets.get_at_index(index)
            removed = bucket.remove(key)
            if removed:
                self._size -= 1









    def get_keys_and_values(self) -> DynamicArray:
        """
        creates dynamic array and appends all key value pairs to the da

        :return: dynamic array with all the key value pairs of the hash map
        """
        new_buckets = DynamicArray()
        for i in range(self._capacity):
            bucket = self._buckets.get_at_index(i)
            for node in bucket:
                new_buckets.append((node.key, node.value))
        return new_buckets

    def clear(self) -> None:
        """
        sets self._buckets to new dynamic array appends empty linked lists resets size to 0
        """
        self._buckets = DynamicArray()
        self._size = 0
        for i in range(self._capacity):
            self._buckets.append(LinkedList())



def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    creates a hashmap from the given dynamic array using the values of the array as keys and the amount of times
    the key/value occurs as the value, then makes a new dynamic array of the keys with values that
    are equal to the max count, found in the process of making the hashmap.

    :param da: dynamic array with objects that will become the keys of the hash map

    :return tuple DynamicArray, int: the da has the mode values used as keys in hash map and max count
    """

    # initializes use of hash map and a max count var
    map = HashMap()
    max_count = 0

    #forms hashmap by adding objs as keys and counting the occurences of the objs within given da
    for i in range (da.length()):
        current_val = da.get_at_index(i)
        count = map.get(current_val)
        if count is None:
            count = 1
            map.put(current_val, count)
        else:
            count += 1
            map.put(current_val, count)

        #stores the highest count of repeats of an obj from original da
        if count> max_count:
            max_count = count

    #creates new dynamic array to store the mode or modes
    new_da = DynamicArray()
    bucket_da = map.get_keys_and_values()
    for i in range(bucket_da.length()):
        key, value = bucket_da.get_at_index(i)
        if value == max_count:
            new_da.append(key)


    return new_da, max_count




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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
