# Name: Richard Silva
# OSU Email: silvari@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 12/3/2021
# Description: Implementation of a hash map using linked lists and dynamic arrays


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears contents of hash map, does not change capacity
        """
        # Starts a new DynamicArray and repopulates the dynamic array with empty linked list objects, then
        # sets the size to 0
        self.buckets = DynamicArray()
        for i in range(self.capacity):
            self.buckets.append(LinkedList())
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns value associated with given key. If key is not found, function returns None
        """
        # Gets appropriate index, then gets the correct bucket
        hash = self.hash_function(key)
        index = hash % self.capacity
        bucket = self.buckets[index]

        # Uses bucket contains method, if the return value is None, the key was not found so None is returned.
        # Otherwise, the return value is the node that contains the key so the value in that node is returned.
        node = bucket.contains(key)
        if node is None:
            return None
        else:
            return node.value

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in hash map. If key already exists, value replaces existing value. Otherwise,
        the key/value pair is added to the hashmap
        """
        # Gets hash and gets the index by taking the modulo of the total array size so the hash is within array bounds
        hash = self.hash_function(key)
        index = hash % self.capacity

        # Determines if key is in bucket
        bucket = self.buckets[index]
        node = bucket.contains(key)

        # If the key is not in the bucket, the key/value pair is inserted at the beginning of the linked list
        # and the size is updated
        if node is None:
            bucket.insert(key, value)
            self.size += 1

        # If the key is found, the value is updated. Size remains the same
        else:
            node.value = value

    def remove(self, key: str) -> None:
        """
        Removes key and associated value from hash map. Does nothing if the key does not exist
        """
        # Gets hash and gets the index by taking the modulo of the total array size so the hash is within array bounds
        hash = self.hash_function(key)
        index = hash % self.capacity

        # Uses index to locate bucket, then uses the linked list method to remove node with key in the linked list
        bucket = self.buckets[index]
        result = bucket.remove(key)

        # If key was located, reduces size as necessary. Otherwise, method does nothing
        if result is True:
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is in the hash map, returns False if the function fails to find the key
        """
        # Gets hash and index through modulo of total capacity
        hash = self.hash_function(key)
        index = hash % self.capacity

        # Uses linked list's method of contains to check if a node containing the key is in the bucket
        bucket = self.buckets[index]
        node = bucket.contains(key)

        # Contains method returns None if key is not found, returns the node containing the key otherwise
        if node is None:
            return False
        else:
            return True

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        empty_count = 0

        # Iterates through dynamic array and checks each linked list's length. If the length is 0, the bucket
        # is empty and is added to empty_count
        for i in range(self.capacity):
            bucket = self.buckets[i]
            if bucket.length() == 0:
                empty_count += 1
        return empty_count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        # Table load is number of elements stored divided by number of buckets
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of hash table, all elements currently in hash map are rehashed. If new capacity is below 1,
        this function does nothing
        """
        # Ends function immediately if entered capacity is below 1
        if new_capacity < 1:
            return

        # Creates a new dynamic array and fills the array with empty linked lists
        new_arr = DynamicArray()
        for i in range(new_capacity):
            new_arr.append(LinkedList())

        # Iterates through the old dynamic array and reruns the hash with the new capacity, then places each
        # key/value pair in the appropriate location in the new array
        for j in range(self.capacity):
            bucket = self.buckets[j]
            if bucket.length() != 0:
                for node in bucket:
                    hash = self.hash_function(node.key)
                    index = hash % new_capacity
                    new_bucket = new_arr[index]
                    new_bucket.insert(node.key, node.value)

        # Updates members with new dynamic array and capacity once these values are no longer needed
        self.buckets = new_arr
        self.capacity = new_capacity

    def get_keys(self) -> DynamicArray:
        """
        Returns a dynamic array with all keys stored in the hash map
        """
        key_arr = DynamicArray()

        # Iterates through array of buckets and loops over linked list if not empty, then appends the node's key
        # to the array we will return
        for i in range(self.capacity):
            bucket = self.buckets[i]
            if bucket.length() != 0:
                for node in bucket:
                    key_arr.append(node.key)
        return key_arr


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
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
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
