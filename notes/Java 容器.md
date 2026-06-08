# Java container
<!-- GFM-TOC -->
* [Java Container](#java-container)
    * [1. Overview](#一OVERVIEW)
        * [Collection](#collection)
        * [Map](#map)
    * [2. Design Patterns in Containers](#2 Design Patterns in Containers)
        * [Iterator mode](#Iterator mode)
        * [Adapter Mode](#Adapter Mode)
    * [3. Source code analysis](#三Source code analysis)
        * [ArrayList](#arraylist)
        * [Vector](#vector)
        * [CopyOnWriteArrayList](#copyonwritearraylist)
        * [LinkedList](#linkedlist)
        * [HashMap](#hashmap)
        * [ConcurrentHashMap](#concurrenthashmap)
        * [LinkedHashMap](#linkedhashmap)
        * [WeakHashMap](#weakhashmap)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Overview

Containers mainly include Collection and Map. Collection stores a collection of objects, while Map stores a mapping table of key-value pairs (two objects).

### Collection

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208220948084.png"/> </div><br>

#### 1. Set

- TreeSet: Based on red-black tree implementation, it supports ordered operations, such as searching for elements based on a range. However, the search efficiency is not as good as that of HashSet. The time complexity of HashSet search is O(1), while that of TreeSet is O(logN).

- HashSet: Based on hash table implementation, supports fast search, but does not support ordered operations. And the insertion order information of the elements is lost, which means that the result obtained by using Iterator to traverse the HashSet is uncertain.

- LinkedHashSet: It has the search efficiency of HashSet, and internally uses a doubly linked list to maintain the insertion order of elements.

#### 2. List

- ArrayList: Based on dynamic array implementation, supports random access.

- Vector: Similar to ArrayList, but it is thread-safe.

- LinkedList: Based on a doubly linked list, it can only be accessed sequentially, but elements can be quickly inserted and deleted in the middle of the linked list. Not only that, LinkedList can also be used as a stack, queue and deque.

#### 3. Queue

- LinkedList: You can use it to implement a two-way queue.

- PriorityQueue: Based on the heap structure, you can use it to implement priority queues.

### Map

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20201101234335837.png"/> </div><br>

- TreeMap: implemented based on red-black trees.

- HashMap: implemented based on hash table.

- HashTable: Similar to HashMap, but it is thread-safe, which means that multiple threads writing to HashTable at the same time will not cause data inconsistency. It is a legacy class and should not be used. Instead, use ConcurrentHashMap to support thread safety. ConcurrentHashMap will be more efficient because ConcurrentHashMap introduces segmentation locks.

- LinkedHashMap: Use a doubly linked list to maintain the order of elements in insert
ion order or least recently used (LRU) order.


## 2. Design patterns in containers

### Iterator pattern

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208225301973.png"/> </div><br>

Collection inherits the Iterable interface, and its iterator() method can generate an Iterator object through which the elements in the Collection can be iterated.

Starting from JDK 1.5, you can use the foreach method to traverse aggregate objects that implement the Iterable interface.

```java
List<String> list = new ArrayList<>();
list.add("a");
list.add("b");
for (String item : list) {
    System.out.println(item);
}
```

### Adapter mode

java.util.Arrays#asList() can convert array type to List type.

```java
@SafeVarargs
public static <T> List<T> asList(T... a)
```

It should be noted that the parameters of asList() are generic variable-length parameters. Basic type arrays cannot be used as parameters, and only corresponding packaging type arrays can be used.

```java
Integer[] arr = {1, 2, 3};
List list = Arrays.asList(arr);
```

asList() can also be called using:

```java
List list = Arrays.asList(1, 2, 3);
```

## 3. Source code analysis

Unless otherwise stated, the following source code analysis is based on JDK 1.8.

In IDEA, double shift to call up Search EveryWhere, search for source code files, and then read the source code.

### ArrayList


#### 1. Overview

Because ArrayList is implemented based on arrays, it supports fast random access. The RandomAccess interface indicates that the class supports fast random access.

```java
public class ArrayList<E> extends AbstractList<E>
        implements List<E>, RandomAccess, Cloneable, java.io.Serializable
```

The default size of the array is 10.

```java
private static final int DEFAULT_CAPACITY = 10;
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/imag
e-20191208232221265.png"/> </div><br>

#### 2. Expansion

When adding elements, use the ensureCapacityInternal() method to ensure that the capacity is sufficient. If it is not enough, you need to use the grow() method to expand the capacity. The size of the new capacity is `oldCapacity + (oldCapacity >> 1)`, that is, oldCapacity+oldCapacity/2. Among them, oldCapacity >> 1 needs to be rounded, so the new capacity is about 1.5 times the old capacity. (If oldCapacity is an even number, it is 1.5 times, and if it is an odd number, it is 1.5 times-0.5)

The expansion operation requires calling `Arrays.copyOf()` to copy the entire original array to the new array. This operation is very expensive, so it is best to specify the approximate capacity when creating the ArrayList object to reduce the number of expansion operations.

```java
public boolean add(E e) {
    ensureCapacityInternal(size + 1); // Increments modCount!!
    elementData[size++] = e;
    return true;
}

private void ensureCapacityInternal(int minCapacity) {
    if (elementData == DEFAULTCAPACITY_EMP
TY_ELEMENTDATA) {
        minCapacity = Math.max(DEFAULT_CAPACITY, minCapacity);
    }
    ensureExplicitCapacity(minCapacity);
}

private void ensureExplicitCapacity(int minCapacity) {
    modCount++;
    // overflow-conscious code
    if (minCapacity - elementData.length > 0)
        grow(minCapacity);
}

private void grow(int minCapacity) {
    // overflow-conscious code
    int oldCapacity = elementData.length;
    int newCapacity = oldCapacity + (oldCapacity >> 1);
    if (newCapacity - minCapacity < 0)
        newCapacity = minCapacity;
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        newCapacity = hugeCapacity(minCapacity);
    // minCapacity is usually close to size, so this is a win:
    elementData = Arrays.copyOf(elementData, newCapacity);
}
```

#### 3. Delete elements

You need to call System.arraycopy() to copy all the elements after index+1 to the index position. The time complexity of this operation is O(N). You can see that the cost of deleting elements from ArrayList is very high.

```java
public E remove(int index) {
    rangeCheck(index);
    modCount++;
    E oldValue = elementData(index);
    int numMoved = size - index - 1;
    if (numMoved > 0)
        System.arraycopy(elementData, index+1, elementData, index, numMoved);
    elementData[--size] = null; // clear to let GC do its work
    return oldValue;
}
```

#### 4. Serialization

ArrayList is implemented based on arrays and has dynamic expansion characteristics. Therefore, the arrays storing elements may not all be used, so there is no need to serialize them all.

The array elementData that holds the elements is modified with transient, which declares that the array will not be serialized by default.

```java
transient Object[] elementData; // non-private to simplify nested class access
```

ArrayList implements writeObject() and readObject() to control the serialization of only the portion of the array filled with elements.

```java
private void readObject(java.io.ObjectInputStream s)
    throws java.io.IOException, ClassNotFoundException {
    elementData = EMPTY_ELEMENTDATA;

    // Read in size, and any hidden stuff
    s.defaultReadObject();

    // Read in capacity
    s.readInt(); // ignored

    if (size > 0) {
        // be like clone(), allocate array based upon size not capacity
        ensureCapacityInternal(size);

        Object[] a = elementData;
        // Read in all elements in the proper order.
        for (int i=0; i<size; i++) {
            a[i] = s.readObject();
        }
    }
}
```

```java
private void writeObject(java.io.ObjectOutputStream s)
    throws java.io.IOException{
    // Write out element count, and any hidden stuff
    int expectedModCount = modCount;
    s.defaultWriteObject();

    // Write out size as capacity for behavioral compatibility w
ith clone()
    s.writeInt(size);

    // Write out all elements in the proper order.
    for (int i=0; i<size; i++) {
        s.writeObject(elementData[i]);
    }

    if (modCount != expecte
dModCount) {
        throw new ConcurrentModificationException();
    }
}
```

When serializing, you need to use writeObject() of ObjectOutputStream to convert the object into a byte stream and output it. When the writeObject() method exists in the incoming object, it will reflect and call writeObject() of the object to achieve serialization. Deserialization uses the readObject() method of ObjectInputStream, and the principle is similar.

```java
ArrayList list = new ArrayList();
ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(file));
oos.writeObject(list);
```

#### 5. Fail-Fast

modCount is used to record the number of times the ArrayList structure has changed. Structural changes refer to all operations that add or delete at least one element, or adjust the size of the internal array. Merely setting the value of an element does not count as a structural change.

When performing operations such as serialization or iteration, you need to compare whether modCount has changed before and after the operation. If it changes, you need to throw a ConcurrentModificationException. For code, refer to the writeObject() method in the previous section of serialization.


### Vector

#### 1. Synchronization

Its implementation is similar to ArrayList, but uses synchronized for synchronization.

```java
public synchronized boolean add(E e) {
    modCount++;
    ensureCapacityHelper(elementCount + 1);
    elementData[elementCount++] = e;
    return true;
}

public synchronized E get(int index) {
    if (index >= elementCount)
        throw new ArrayIndexOutOfBoundsException(index);

    return elementData(index);
}
```

#### 2. Expansion

The constructor of Vector can pass in the capacityIncrement parameter, which is used to increase the capacity by capacityIncrement when expanding. If the value of this parameter is less than or equal to 0, the capacity will be doubled each time during expansion.

```java
public Vector(int initialCapacity, int capacityIncrement) {
    super();
    if (initialCapacity < 0)
        throw new IllegalArgumentException("Illegal Capacity: "+
                                           initialCapacity);
    this.elementData = new Object[initialCapacity];
    this.capacityIncrement = capacityIncrement;
}
```

```java
private void grow(int minCapacity) {
    // overflow-conscious code
    int oldCapacity = elementData.length;
    int newCapacity = oldCapacity + ((capacityIncrement > 0) ?
                                     capacityIncrement : oldCapacity);
    if (newCapacity - minCapacity < 0)
        newCapacity = minCapacity;
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        newCapacity = hugeCapacity(minCapacity);
    elementData = Arrays.copyOf(elementData, newCapacity);
}
```

When calling the constructor without capacityIncrement, the capacityIncrement value is set to 0, which means that by default the capacity of Vector will be doubled each time it is expanded.

```java
public Vector(int initialCapacity) {
this(initialCapacity, 0);
}

public Vector() {
    this(10);
}
```

#### 3. Comparison with ArrayList

- Vector is synchronized, so the overhead is greater than ArrayList and the access speed is slower. It is better to use ArrayList instead of Vector because synchronization operations are completely controlled by the programmer himself;
- Vector requires 2 times its size each time it is expanded (the growing capacity can also be set through the constructor), while ArrayList requests 1.5 times.

#### 4. Alternatives

You can use `Collections.synchronizedList();` to get a thread-safe ArrayList.

```java
List<String> list = new ArrayList<>();
List<String> synList = Collections.synchronizedList(list);
```

You can also use the CopyOnWriteArrayList class under the concurrent package.

```java
List<String> list = new CopyOnWriteArrayList<>();
```

### CopyOnWriteArrayList

#### 1. Separation of reading and writing

The writing operation is performed on a copied array, and the reading operation is still performed on the original array. Reading and writing are separated and do not affect each other.

Write operations need to be locked to prevent loss of written data due to concurrent writes.

After the write operation is completed, the original array needs to point to the new copied array.

```
java
public boolean add(E e) {
    final ReentrantLock lock = this.lock;
    lock.lock();
    try {
        Object[] elements = getArray();
        int len = elements.length;
        Object[] newElements = Arrays.copyOf(elements, len + 1);
        newElements[len] = e;
        setArray(newElements);
        return true;
    } finally {
        lock.unlock();
    }
}

final void setArray(Object[] a) {
    array = a;
}
```

```java
@SuppressWarnings("unchecked")
private E get(Object[] a, int index) {
    return (E) a[index];
}
```

#### 2. Applicable scenarios

CopyOnWriteArrayList allows reading operations at the same time as writing operations, which greatly improves the performance of reading operations, so it is very suitable for application scenarios with more reading and less writing.

But CopyOnWriteArrayList has its flaws:

- Memory usage: When writing, a new array needs to be copied, causing the memory usage to be about twice the original size;
- Data inconsistency: The read operation cannot read real-time data because some of the write operation data has not yet been synchronized to the reading group.

Therefore, CopyOnWriteArrayList is not suitable for memory-sensitive and real-time requirements scenarios.

### LinkedList

#### 1. Overview

Implemented based on doubly linked list, using Node to store linked list node information.

```java
private static class Node<E> {
    E item;
    Node<E> next;
    Node<E> prev;
}
```

Each linked list stores first and last pointers:

```java
transient Node<E> first;
transient Node<E> last;
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208233940066.png"/> </
div><br>

#### 2. Comparison with ArrayList

ArrayList is implemented based on dynamic arrays, and LinkedList is implemented based on doubly linked lists. The difference between ArrayList and LinkedList can be attributed to the difference between arrays and linked lists:

- Arrays support random access, but insertion and deletion are very expensive and require moving a large number of elements;
- Linked lists do not support random access, but insertion and deletion only require changing the pointer.

### HashMap

For ease of understanding, the following source code analysis is based on JDK 1.7.

#### 1. Storage structure

Internally contains an array table of Entry type. Entry stores key-value pairs. It contains four fields. From the next field we can see that Entry is a linked list. That is, each position in the array is regarded as a bucket, and each bucket stores a linked list. HashMap uses the zipper method to resolve conflicts. Entries with the same hash value and hash bucket modulo operation result are stored in the same linked list.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208234948205.png"/> </div><br>

```java
transient Entry[] table;
```

```java
static class Entry<K,V> implements Map.Entry<K,V> {
    final K key;
    V value;
    Entry<K,V> next;
    int hash;

    Entry(int h, K k, V v, Entry<K,V> n) {
        value = v;
        next = n;
        key = k;
        hash = h;
    }

    public final K getKey() {
        return key;
    }

    public final V getValue() {
        return value;
    }

    public final V setValue(V newValue) {
        V oldValue = value;
        value = newValue;
        return oldValue;
    }

    public final boolean equals(Object o) {
        if (!(o instanceof Map.Entry))
            return false;
        Map.Entry e = (Map.Entry)o;
        Object k1 = getKey();
        Object k2 = e.getKey();
        if (k1 == k2 || (k1 != null && k1.equals(k2))) {
            Object v1 = getValue();
            Object v2 = e.getValue();
            if (v1 == v2 || (v1 != null && v1.equals(v2)))
                return true;
        }
        return false;
    }

    public final int hashCode() {
        return Objects.hashCode(getKey()) ^ Objects.hashCode(getValue());
    }

    public final String toString() {
        return getKey() + "=" + getValue();
    }
}
```

#### 2. How the zipper method works

```java
HashMap<String, String> map = new HashMap<>();
map.put("K1", "V1");
map.put("K2", "V2");
map.put("K3", "V3");
```

- new
Create a HashMap, the default size is 16;
- Insert the &lt;K1,V1\> key-value pair, first calculate the hashCode of K1 to 115, and use the division-leaving-remainder method to obtain the bucket subscript 115%16=3.
- Insert the &lt;K2,V2\> key-value pair, first calculate the hashCode of K2 to 118, and use the division-leaving-remainder method to obtain the bucket subscript 118%16=6.
- Insert the &lt;K3,V3\> key-value pair, first calculat
e the hashCode of K3 to 118, use the division-remainder method to get the bucket subscript 118%16=6, and insert it in front of &lt;K2,V2\>.

It should be noted that the insertion into the linked list is performed by head insertion. For example, the above &lt;K3,V3\> is not inserted after &lt;K2,V2\>, but at the head of the linked list.

The search needs to be divided into two steps:

- Calculate the bucket where the key-value pair is located;
- When searching sequentially on a linked list, the time complexity is obviously proportional to the length of the linked list.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208235258643.png"/> </div><br>

#### 3. put operation

```java
public V put(K key, V value) {
    if (table == EMPTY_TABLE) {
        inflateTable(threshold);
    }
    // Keys that are null are handled separately.
    if (key == null)
        return putForNullKey(value);
    int hash = hash(key);
    // Determine the bucket index
    int i = indexFor(hash, table.length);
    // First find out whether there is already a key-value pair with key key. If it exists, update the value of this key-value pair to value.
    for (Entry<K,V> e = table[i]; e != null; e = e.next) {
        Object k;
        if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
            V oldValue = e.value;
            e.value = value;
            e.recordAccess(this);
            return oldValue;
        }
    }

    modCount++;
    //Insert new key-value pair
    addEntry(hash, key, value, i);
    return null;
}
```

HashMap allows inserting key-value pairs with null keys. However, because the hashCode() method of null cannot be called, the bucket index of the key-value pair cannot be determined, and it can only be stored by forcibly specifying a bucket index. HashMap uses the 0th bucket to store key-value pairs with null keys.

```java
private V putForNullKey(V value) {
    for (Entry<K,V> e = table[0]; e != null; e = e.next) {
        if (e.key == null) {
            V oldValue = e.value;
            e.value = value;
            e.recordAccess(this);
            return oldValue;
        }
    }
    modCount++;
    addEntry(0, null, value, 0);
    return null;
}
```

Use the head insertion method of the linked list, that is, the new key-value pair is inserted at the head of the linked list, not the tail of the linked list.

```java
void addEntry(int hash, K key, V value, int bucketIndex) {
    if ((size >= threshold) && (null != table[bucketIndex])) {
        resize(2 * table.length);
        hash = (null != key) ? hash(key) : 0;
        bucketIndex = indexFor(hash, table.length);
    }

    createEntry(hash, key, value, bucketIndex);
}

void createEntry(int hash, K key, V value, int bucketIndex) {
    Entry<K,V> e = table[bucketIndex];
    // Head interpolation method, the head of the linked list points to the new key-value pair
    table[bucketIndex] = new Entry<>(hash, key, value, e);
    size++
;
}
```

```java
Entry(int h, K k, V v, Entry<K,V> n) {
    value = v;
    next = n;
    key = k;
    hash = h;
}
```

#### 4. Determine the bucket index

Many operations require first determining the bucket index where a key-value pair is located.

```java
int hash = hash(key);
int i = indexFor(hash, table.length);
```

**4.1 Calculate hash value**

```java
final int hash(Object k) {
    int h = hashSeed;
    if (0 != h && k instanceof String) {
        return sun.misc.Hashing.stringHash32((String) k);
    }

    h ^= k.hashCode();

    // This function ensures that hashCodes that differ only by
    // constant multiples at each bit position have a bounded
    // number of collisions (approximately 8 at default load factor).
    h ^= (h >>> 20) ^ (h >>> 12);
    return h ^ (h >>> 7) ^ (h >>> 4);
}
```

```java
public final int hashCode() {
return Objects.hashCode(key) ^ Objects.hashCode(value);
}
```

**4.2 Modulo**

Let x = 1\<\<4, that is, x is the fourth power of 2, which has the following properties:

```
x: 00010000
x-1: 00001111
```

Let a number y do an AND operation with x-1, and the 4th and above digits represented by y can be removed:

```
y : 10110010
x-1: 00001111
y&(x-1) : 00000010
```

This property is the same as y modulo x:

```
y : 10110010
x: 00010000
y%x: 00000010
```

We know that the cost of bit operations is much smaller than the modulo operation, so using bit operations when performing this kind of calculation can bring higher performance.

The last step to determine the bucket index is to take the hash value of the key modulo the number of buckets: hash%capacity. If the capacity can be guaranteed to be 2 to the nth power, then this operation can be converted into a bit operation.

```java
static int indexFor(int h, int length) {
    return h & (length-1);
}
```

#### 5. Capacity expansion - basic principles

Suppose the table length of HashMap is M, and the number of key-value pairs that need to be stored is N. If the hash function meets the requirements of uniformity, then the length of each linked list is approximately N/M, so the search complexity is O(N/M).

In order to reduce the search cost, N/M should be made as small as possible, so M needs to be as large as possible, which means that the table should be as large as possible. HashMap uses dynamic expansion to adjust the M value according to the current N value, so that both space efficiency and time efficiency can be guaranteed.

The parameters related to expansion mainly include: capacity, size, threshold and load_factor.

| Parameters | Meaning |
| :--: | :-- |
| capacity | The capacity size of the table, the default is 16. It should be noted that capacity must be guaranteed to be 2 to the nth power. |
| size | Number of key-value pairs. |
| threshold | The critical value of size. When size is greater than or equal to threshold, expansion operation must be performed. |
| loadFactor | Load factor, the proportion that the table can use, threshold = (int)(capacity*
loadFactor). |

```java
static final int DEFAULT_INITIAL_CAPACITY = 16;

static final int MAXIMUM_CAPACITY = 1 << 30;

static final float DEFAULT_LOAD_FACTOR = 0.75f;

transient Entry[] table;

transient int size;

int threshold;

final float loadFactor;

transient int modCount;
```

As can be seen from the code for adding elements below, when expansion is required, the capacity is doubled.

```java
void addEntry(int hash, K key, V value, int bucketIndex) {
    Entry<K,V> e = table[bucketIndex];
    table[bucketIndex] = new Entry<>(hash, key, value, e);
    if (size++ >= threshold)
        resize(2 * table.length);
}
```

Expansion is implemented using resize(). It should be noted that the expansion operation also requires reinserting all key-value pairs of oldTable into newTable, so this step is very time-consuming.

```java
void resize(int newCapacity) {
    Entry[] oldTable = table;
    int oldCapacity = oldTable.length;
    if (oldCapacity == MAXIMUM_CAPACITY) {
        threshold = Integer.MAX_VALUE;
        return;
    }
    Entry[] newTable = new Entry[newCapacity];
    transfer(newTable);
    table = newTable;
    threshold = (int)(newCapacity * loadFactor);
}

void transfer(Entry[] newTable) {
    Entry[] src = table;
    int newCapacity = newTable.length;
    for (int j = 0; j < src.length; j++) {
        Entry<K,V> e = src[j];
        if (e != null) {
            src[j] = null;
            do {
                Entry<K,V> next = e.next;
                int i = indexFor(e.hash, newCapacity);
                e.next = newTable[i];
                newTable[i] = e;
                e = next;
            } while (e != null);
        }
    }
}
```

#### 6. Capacity expansion-recalculate bucket index

When expanding, the key-value pairs need to be recalculated into bucket subscripts and placed in the corresponding buckets. As mentioned earlier, HashMap uses hash%capacity to determine the bucket index. The feature of HashMap capacity being 2 to the nth power can greatly reduce the complexity of recalculating bucket subscripts.

Assume that the original array length capacity is 16, and the new capacity after expansion is 32:

```html
capacity: 00010000
new capacity: 00100000
```

For a Key, its hash value is at bit 5:

- is 0, then hash%00010000 = hash%00100000, and the bucket position is the same as before;
- is 1, hash%00010000 = hash%00100000 + 16, and the bucket position is the original position + 16.

#### 7. Calculate array capacity

The HashMap constructor allows users to pass in a capacity that is not 2 to the nth power, because it can automatically convert the incoming capacity to 2
nth power.

First consider how to find the mask of a number. For 10010000, its mask is 11111111, which can be obtained using the following method:

```
mask |= mask >> 1 11011000
mask |= mask >> 2 11111110
mask |= mask >> 4 11111111
```

mask+1 is the smallest 2 raised to the nth power greater than the original number.

```
num 10010000
mask+1 100000000
```

T
he following is the code in HashMap to calculate the capacity of an array:

```java
static final int tableSizeFor(int cap) {
    int n = cap - 1;
    n |= n >>> 1;
    n |= n >>> 2;
    n |= n >>> 4;
    n |= n >>> 8;
    n |= n >>> 16;
    return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
}
```

#### 8. Convert linked list to red-black tree

Starting from JDK 1.8, when the length of the linked list stored in a bucket is greater than or equal to 8, the linked list will be converted into a red-black tree.

#### 9. Comparison with Hashtable

- Hashtable uses synchronized for synchronization.
- HashMap can insert Entries with null keys.
- HashMap iterators are fail-fast iterators.
- HashMap does not guarantee that the order of elements in the Map remains unchanged over time.

### ConcurrentHashMap

#### 1. Storage structure

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191209001038024.png"/> </div><br>

```java
static final class HashEntry<K,V> {
    final int hash;
    final K key;
    volatile V value;
    volatile HashEntry<K,V> next;
}
```

ConcurrentHashMap and HashMap are similar in implementation. The main difference is that ConcurrentHashMap uses segment locks (Segment). Each segment lock maintains several buckets (HashEntry). Multiple threads can access buckets on different segment locks at the same time, thus making the concurrency higher (the concurrency is the number of Segments).

Segment inherits from ReentrantLock.

```java
static final class Segment<K,V> extends ReentrantLock implements Serializable {

    private static final long serialVersionUID = 2249069246763182397L;

    static final int MAX_SCAN_RETRIES =
        Runtime.getRuntime().availableProcessors() > 1 ? 64 : 1;

    transient volatile HashEntry<K,V>[] table;

    transient int count;

    transient int modCount;

    transient int threshold;

    final float loadFactor;
}
```

```java
final Segment<K,V>[] segments;
```

The default concurrency level is 16, which means 16 Segments are created by default.

```java
static final int DEFAULT_CONCURRENCY_LEVEL = 16;
```

#### 2. size operation

Each Segment maintains a count variable to count the number of key-value pairs in the Segment.

```java
/**
 * The number of elements. Accessed only either within locks
 * or among other volatile reads that maintain visibility.
 */
transient int count;
```

When performing the size operation, you need to traverse all Segments and then accumulate the count.

ConcurrentHashMap first tries not to lock when performing the size operation. If the results obtained by two consecutive non-locking operations are consistent, the result can be considered correct.

The number of attempts is defined using RETRIES_BEFORE_LOCK, which has a value of 2. The initial value of retries is -1, so the number of attempts is 3.

If the number of attempts exceeds 3, each Segment needs to be locked.

```java

/**
 * Number of unsynchroniz
ed retries in size and containsValue
 * methods before resorting to locking. This is used to avoid
 * unbounded retries if tables undergo continuous modification
 * which would make it impossible to obtain an accurate result.
 */
static final int RETRIES_BEFORE_LOCK = 2;

public int size() {
    // Try a few times to get accurate count. On failure due to
    // continuous async changes in table, resort to locking.
    final Segment<K,V>[] segments = this.segments;
    int size;
    boolean overflow; // true if size overflows 32 bits
    long sum; // sum of modCounts
    long last = 0L; // previous sum
    int retries = -1; // first iteration isn't retry
    try {
        for (;;) {
            // If the number of attempts is exceeded, then for each S
element lock
            if (retries++ == RETRIES_BEFORE_LOCK) {
                for (int j = 0; j < segments.length; ++j)
                    ensureSegment(j).lock(); // force creation
            }
            sum = 0L;
            size = 0;
            overflow = false;
            for (int j = 0; j < segments.length; ++j) {
                Segment<K,V> seg = segmentAt(segments, j);
                if (seg != null) {
                    sum += seg.modCount;
                    int c = seg.count;
                    if (c < 0 || (size += c) < 0)
                        overflow = true;
                }
            }
            // If the results obtained twice in a row are consistent, the result is considered correct.
            if (sum == last)
                break;
            last = sum;
        }
    } finally {
        if (retries > RETRIES_BEFORE_LOCK) {
            for (int j = 0; j < segments.length; ++j)
                segmentAt(segments, j).unlock();
        }
    }
    return overflow ? Integer.MAX_VALUE : size;
}
```

#### 3. Changes in JDK 1.8

JDK 1.7 uses the segment lock mechanism to implement concurrent update operations. The core class is Segment, which inherits from the reentrant lock ReentrantLock. The degree of concurrency is equal to the number of Segments.

JDK 1.8 uses CAS operations to support higher concurrency, and uses the built-in lock synchronized when the CAS operation fails.

And the implementation of JDK 1.8 will also convert to a red-black tree when the linked list is too long.

### LinkedHashMap

#### Storage structure

Inherited from HashMap, it has the same fast search features as HashMap.

```java
public class LinkedHashMap<K,V> extends HashMap<K,V> implements Map<K,V>
```

A doubly linked list is maintained internally to maintain the insertion order or LRU order.

```java
/**
 * The head (eldest) of the doubly linked list.
 */
transient LinkedHashMap.Entry<K,V> head;

/**
 * The tail (youngest) of the doubly linked list.
 */
transient LinkedHashMap.Entry<K,V> tail;
```

accessOrder determines the order, and the default is false. At this time, the insertion order is maintained.

```java
final boolean accessOrder;
```

The most important thing about LinkedHa
shMap is the following functions for maintaining order, which are called in put, get, etc. methods.

```java
void afterNodeAccess(Node<K,V> p) { }
void afterNodeInsertion(boolean evict) { }
```

#### afterNodeAccess()

When a node is accessed, if accessOrder is true, the node will be moved to the end of the linked list. That is to say, after specifying the LRU order, each time a node is accessed, the node will be moved to the end of the linked list to ensure that the end of the linked list is the most recently visited node, and the head of the linked list is the most recent and longest unused node.

```java
void afterNodeAccess(Node<K,V> e) { // move node to last
    LinkedHashMap.Entry<K,V> last;
    if (accessOrder && (last = tail) != e) {
        LinkedHashMap.Entry<K,V> p =
            (LinkedHashMap.Entry<K,V>)e, b = p.before, a = p.after;
        p.after = null;
        if(b==null)
            head = a;
        else
            b.after = a;
        if (a != null)
            a.before = b;
        else
            last = b;
        if (last == null)
            head = p;
        else {
            p.before = last;
            last.after = p;
        }
        tail = p;
        ++modCount;
    }
}
```

#### afterNodeInsertion()

Executed after operations such as put, when the removeEldestEntry() method returns true, the latest node, which is the first node of the linked list, will be removed.

evict is false only when building the Map, here it is true.

```java
void afterNodeInsertion(boolean evict) { // possibly remove eldest
    LinkedHashMap.Entry<K,V> first;
    if (evict && (first = head) != null && removeEldestEntry(first)) {
        K key = first.key;
        removeNode(hash(key), key, null, false, true);
    }
}
```

removeEldestEn
try() defaults to false. If you need to make it true, you need to inherit LinkedHashMap and override the implementation of this method. This is particularly useful in implementing LRU cache. By removing the most recently unused node, it ensures that the cache space is sufficient and the cached data is hot data.

```java
protected boolean removeEldestEntry(Map.Entry<K,V> eldest) {
    return false;
}
```

#### LRU cache

The following is an LRU cache implemented using LinkedHashMap:

- Set the maximum cache space MAX_ENTRIES to 3;
- Use the constructor of LinkedHashMap to set accessOrder to true to enable LRU order;
- Override the implementation of the removeEldestEntry() method, and when there are more nodes than MAX_ENTRIES, the most recently unused data will be removed.

```java
class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private static final int MAX_ENTRIES = 3;

    protected boolean removeEldestEntry(Map.Entry eldest) {
        return size() > MAX_ENTRIES;
    }

    LRUCache() {
        super(MAX_ENTRIES, 0.75f, true);
    }
}
```

```java
public static void main(String[] args) {
    LRUCache<Integer, String> cache = new LRUCache<>();
    cache.put(1, "a");
    cache.put(2, "b");
    cache.
put(3, "c");
    cache.get(1);
    cache.put(4, "d");
    System.out.println(cache.keySet());
}
```

```html
[3, 1, 4]
```

### WeakHashMap

#### Storage structure

The Entry of WeakHashMap inherits from WeakReference, and the object associated with WeakReference will be recycled during the next garbage collection.

WeakHashMap is mainly used to implement caching. By using WeakHashMap to reference the cache object, the JVM will recycle this part of the cache.

```java
private static class Entry<K,V> extends WeakReference<Object> implements Map.Entry<K,V>
```

#### ConcurrentCache

ConcurrentCache in Tomcat uses WeakHashMap to implement the caching function.

ConcurrentCache uses generational caching:

- Put frequently used objects into eden, which is implemented using ConcurrentHashMap, so there is no need to worry about being recycled (Garden of Eden);
- Put rarely used objects into longterm, which is implemented using WeakHashMap. These old objects will be recycled by the garbage collector.
- When the get() method is called, it will be obtained from the eden area first. If it is not found, it will be obtained from the longterm. When the object is obtained from the longterm, the object will be put into eden to ensure that frequently visited nodes are not easily recycled.
- When the put() method is called, if the size of eden exceeds size, then all objects in eden are put into longterm, and the virtual machine is used to recycle some of the objects that are not frequently used.

```java
public final class ConcurrentCache<K, V> {

    private final int size;

    private final Map<K, V> eden;

    private final Map<K, V> longterm;

    public ConcurrentCache(int size) {
        this.size = size;
        this.eden = new ConcurrentHashMap<>(size);
        this.longterm = new WeakHashMap<>(size);
    }

    public V get(K k) {
        V v = this.eden.get(k);
        if (v == null) {
            v = this.longterm.get(k);
            if (v != null)
                this.eden.put(k, v);
        }
        return v;
    }

    public void put(K k, V v) {
        if (this.eden.size() >= size) {
            this.longterm.putAll(this.eden);
            this.eden.clear();
        }
        this.eden.put(k, v);
    }
}
```


## References

- Eckel B. Java Programming Thoughts [M]. Machinery Industry Press, 2002.
- [Java Collection Framework](https://www.w3resource.com/java-tutorial/java-collections.php)
- [Iterator Pattern](https://openhome.cc/Gossip/DesignPattern/IteratorPattern.htm)
- [Java 8 series: Re-understanding HashMap](https://tech.meituan.com/java_hashmap.html)
- [What is difference between HashMap and Hashtable in Java?](http://javarevisited.blogspot.hk/2010/10/difference-between-hashmap-and.html)
- [Java Collection HashMap](http://www.zhangchangle.com/2018/02/07/Java%E9%9B%86%E5%90%88%E4%B9%8BHashMap/)
- [The principle of ConcurrentHashMap analysis](http:
//www.programering.com/a/MDO3QDNwATM.html)
- [Explore the high concurrency implementation mecha
nism of ConcurrentHashMap](https://www.ibm.com/developerworks/cn/java/java-lo-concurrenthashmap/)
- [HashMap related interview questions and answers](https://www.jianshu.com/p/75adf47958a7)
- [Java Collection Details (2): Defects of asList](http://wiki.jikexueyuan.com/project/java-enhancement/java-thirtysix.html)
- [Java Collection Framework – The LinkedList Class](http://javaconceptoftheday.com/java-collection-framework-linkedlist-class/)
