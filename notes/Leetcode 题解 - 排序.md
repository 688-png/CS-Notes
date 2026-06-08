# Leetcode problem solution - sorting
<!-- GFM-TOC -->
* [Leetcode problem solution - sorting] (#leetcode-problem solution---sorting)
    * [Quick Select](#quick select)
    * [Heap](#Heap)
        * [1. Kth Element](#1-kth-element)
    * [Bucket Sort](#Bucket Sort)
        * [1. The k elements with the most frequency](#1-the k-elements with the most frequency)
        * [2. Sort strings according to the number of occurrences of characters] (#2-Sort strings according to the number of occurrences of characters)
    * [DutchFlagQuestion](#DutchFlagQuestion)
        * [1. Sort by color](#1-Sort by color)
<!-- GFM-TOC -->


## Quick selection

Used to solve the **Kth Element** problem, which is the problem of the Kth element.

This can be achieved using quicksort's partition(). The array needs to be scrambled first, otherwise the worst-case time complexity is O(N<sup>2</sup>).

## Heap

Used to solve the **TopK Elements** problem, which is the problem of K minimum elements. Use the min heap to implement the TopK problem, and the min heap uses the big top heap. The top element of the big top heap is the largest element of the current heap. Implementation process: Continuously insert new elements into the big top heap. When the number of elements in the heap is greater than k, remove the top element from the heap, which is the largest element in the current heap. The remaining elements are the smallest K elements among the currently added elements. The time complexity of inserting and removing the top element of the heap is log<sub>2</sub>N.

The heap can also be used to solve the Kth Element problem. After obtaining the minimum heap of size K, because a large top heap is used to implement it, the top element of the heap is the Kth largest element.

Quick selection can also solve the TopK Elements problem, because after finding the Kth Element, the array is traversed again, and all elements less than or equal to the Kth Element are TopK Elements.

It can be seen that both quick selection and heap sort can solve the Kth Element and TopK Elements problems.

### 1. Kth Element

215\. Kth Largest Element in an Array (Medium)

[Leetcode](https://leetcode.com/problems/kth-largest-element-in-an-array/description/) / [Leetcode](https://leetcode-cn.com/problems/kth-largest-element-in-an-array/description/)

```text
Input: [3,2,1,5,6,4] and k = 2
Output: 5
```

Problem description: Find the k-th element from the bottom.

**Sort**: Time complexity O(NlogN), space complexity O(1)

```java
public int findKthLargest(int[] nums, int k) {
    Arrays.sort(nums);
    return nums[nums.length - k];
}
```

**Heap**: time complexity O(NlogK), space complexity O(K).

```java
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> pq = new PriorityQueue<>(); // Small top heap
    for (int val : nums) {
        pq.add(val);
        if (pq.size() > k) // Maintain the size of the heap as K
            pq.poll();
    }
    return pq.peek();
}
```

**Quick Select
ion**: Time complexity O(N), space complexity O(1)

```java
public int findKthLargest(int[] nums, int k) {
    k = nums.length - k;
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int j = partition(nums, l, h);
        if (j == k) {
            break;
        } else if (j < k) {
            l = j + 1;
        } else {
            h = j - 1;
        }
    }
    return nums[k];
}

private int partition(int[] a, int l, int h) {
    int i = l, j = h + 1;
    while (true) {
        while (a[++i] < a[l] && i < h) ;
        while (a[--j] > a[l] && j > l) ;
        if (i >= j) {
            break;
        }
        swap(a, i, j);
    }
    swap(a, l, j);
    return j;
}

private void swap(int[] a, int i, int j) {
    int t = a[i];
    a[i] = a[j];
    a[j] = t;
}
```

## Bucket sort

### 1. The k elements with the most frequency

347\. Top K Frequent Elements (Medium)

[Leetcode](https://leetcode.com/problems/top-k-frequent-elements/description/) / [Leetcode](https://leetcode-cn.com/problems/top-k-frequent-elements/description/)

```html
Given [1,1,1,2,2,3] and k = 2, return [1,2].
```

Set up several buckets, each bucket stores numbers that appear with the same frequency. The subscript of the bucket indicates the frequency of occurrence of the number, that is, the frequency of occurrence of the number stored in the i-th bucket is i.

After putting all the numbers into the bucket, traverse the bucket from back to front. The k numbers obtained first are the k numbers that appear most frequently.

```java
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> frequencyForNum = new HashMap<>();
    for (int num : nums) {
        frequencyForNum.put(n
um, frequencyForNum.getOrDefault(num, 0) + 1);
    }
    List<Integer>[] buckets = new ArrayList[nums.length + 1];
    for (int key : frequencyForNum.keySet()) {
        int frequency = frequencyForNum.get(key);
        if (buckets[frequency] == null) {
            buckets[frequency] = new ArrayList<>();
        }
        buckets[frequency].add(key);
    }
    List<Integer> topK = new ArrayList<>();
    for (int i = buckets.length - 1; i >= 0 && topK.size() < k; i--) {
        if (buckets[i] == null) {
            continue;
        }
        if (buckets[i].size() <= (k - topK.size())) {
            topK.addAll(buckets[i]);
        } else {
            topK.addAll(buckets[i].subList(0, k - topK.size()));
        }
    }
    int[] res = new int[k];
    for (int i = 0; i < k; i++) {
        res[i] = topK.get(i);
    }
    return res;
}
```

### 2. 按照字符出现次数对字符串排序

451\. Sort Characters By Frequency (Medium)

[Leetcode](https://leetcode.com/problems/sort-characters-by-frequency/description/) / [力扣](https://leetcode-cn.com/problems/sort-characters-by-frequency/description/)

```html
Input:
"tree"

Output:
"eert"

Explanation:
'e' appears twice while 'r' and 't' both appear once.
So 'e' must appear before both 'r' and 't'. Therefore "eetr" is also a valid answer.
```

```java
public S
tring frequencySort(String s) {
    Map<Character, Integer> frequencyForNum = new HashMap<>();
    for (char c : s.toCharArray())
        frequencyForNum.put(c, frequencyForNum.getOrDefault(c, 0) + 1);

    List<Character>[] frequencyBucket = new ArrayList[s.length() + 1];
    for (char c : frequencyForNum.keySet()) {
        int f = frequencyForNum.get(c);
        if (frequencyBucket[f] == null) {
            frequencyBucket[f] = new ArrayList<>();
        }
        frequencyBucket[f].add(c);
    }
    StringBuilder str = new StringBuilder();
    for (int i = frequencyBucket.length - 1; i >= 0; i--) {
        if (frequencyBucket[i] == null) {
            continue;
        }
        for (char c : frequencyBucket[i]) {
            for (int j = 0; j < i; j++) {
                str.append(c);
            }
        }
    }
    return str.toString();
}
```

## Dutch flag question

The Dutch flag contains three colors: red, white and blue.

There are three colors of balls, and the goal of the algorithm is to correctly arrange these three balls in color order. It is actually a variant of three-way split quick sort. In three-way split quick sort, each split divides the array into three intervals: less than the cut element, equal to the cut element, and greater than the cut element. This algorithm divides the array into three intervals: equal to red, equal to white, and equal to blue.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7a3215ec-6fb7-4935-8b0d-cb408208f7cb.png"/> </div><br>


### 1. Sort by color

75\. Sort Colors (Medium)

[Leetcode](https://leetcode.com/problems/sort-colors/description/) / [Leetcode](https://leetcode-cn.com/problems/sort-colors/description/)

```html
Input: [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]
```

Problem description: There are only three colors 0/1/2.

```java
public void sortColors(int[] nums) {
    int zero = -1, one = 0, two = nums.length;
    while (one < two) {
        if (nums[one] == 0) {
            swap(nums, ++zero, one++);
        } else if (nums[one] == 2) {
            swap(nums, --two, one);
        } else {
++one;
        }
    }
}

private void swap(int[] nums, int i, int j) {
    int t = nums[i];
    nums[i] = nums[j];
    nums[j] = t;
}
```
