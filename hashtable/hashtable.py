

class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        if capacity <= MIN_CAPACITY:
            capacity = 8
        self.myTable = [None] * capacity
        self.capacity = capacity
        self.full = 0

    def __repr__(self):
        print()
        for item in self.myTable:
            if item:
                newItem = item
                str_ = ""
                while newItem:
                    print(f"({newItem.key}: {newItem.value})")
                    newItem = newItem.next
            else:
                print("empty")
        return ""

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.full / self.get_num_slots()
        # divide the full slots by capacity (which is 8)

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """
        FNV_offset_basis= 14695981039346656037
        FNV_prime = 1099511628211

        hash = FNV_offset_basis
        for character in key:
            hash*=FNV_prime
            hash = ord(character)
        return hash


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
    #    hash = 5381
    #    for character in key:
    #        hash = ((hash << 5) + hash) + ord(character)
    #     return hash


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.fnv1(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        hash_index = self.hash_index(key)
        item = HashTableEntry(key,value)
        newItem = self.myTable[hash_index]

        if newItem:
            while newItem.next and newItem.key != key:
                newItem = newItem.next
            if newItem.key == key:
                newItem.value = value
            else:
                newItem.next = item
                self.full += 1
        else:
            self.myTable[hash_index] = item
            self.full += 1


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        hash_index = self.hash_index(key)
        newItem = self.myTable[hash_index]

        if newItem:
            if newItem.key == key:
                self.myTable[hash_index] = newItem.next
                self.full -=1
            else:
                prev = newItem
                newItem = newItem.next

                while newItem:
                    if newItem.key == key:
                        prev.next = newItem.next
                        self.full -=1
                        break
                    prev = newItem
                    newItem = newItem.next

            if newItem:
                return newItem
        print("Warning, key not found.")


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        hash_index = self.hash_index(key)
        if self.myTable[hash_index]:
            newItem = self.myTable[hash_index]
            while newItem:
                if newItem.key == key:
                    return newItem.value
                newItem = newItem.next

    def newTable(self, new_capacity):
            self.capacity = new_capacity
            self.myTable = [None] * new_capacity
            self.full = 0

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        oldTable = self.myTable
        self.newTable(new_capacity)
        for oldList in oldTable:
            if oldList:
                while oldList:
                    self.put(oldList.key, oldList.value)
                    oldList = oldList.next





if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))


    print("")
