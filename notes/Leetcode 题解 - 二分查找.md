# Leetcode problem solution - binary search
<!-- GFM-TOC -->
* [Leetcode problem solution - binary search](#leetcode-problem solution---binary search)
    * [1. Find the square root](#1-Find the square root)
    * [2. The smallest element that is greater than the given element] (#2-The smallest element that is greater than the given element)
    * [3. Single Element of ordered array](#3-single-element of ordered array)
    * [4. First wrong version](#4-First wrong version)
    * [5. Minimum number of rotated array](#5-Minimum number of rotated array)
    * [6. Search interval](#6-Search interval)
<!-- GFM-TOC -->


**Normal implementation**

```text
Input: [1,2,3,4,5]
key: 3
return the index : 2
```

```java
public int binarySearch(int[] nums, int key) {
    int l = 0, h = nums.length - 1;
    while (l <= h) {
        int m = l + (h - l) / 2;
        if (nums[m] == key) {
            return m;
        } else if (nums[m] > key) {
            h = m - 1;
        } else {
            l = m + 1;
        }
    }
    return -1;
}
```

**Time Complexity**

Binary search is also called halving search, which can halve the search interval every time. The algorithm time complexity of this halving feature is O(logN).

**m calculation**

There are two ways to calculate the median m:

- m = (l + h) / 2
- m = l + (h - l) / 2

l + h may cause addition overflow, which means that the result of addition is larger than the range that the integer can represent. But l and h are both positive numbers, so h - l does not have an additive overflow problem. Therefore, it is better to use the second calculation method.

**Return value of unsuccessful search**

If the key is still not found when the loop exits, it means that the search failed. There can be two return values:

- -1: An error code indicates that the key was not found.
- l: Insert key into the correct position in nums

**Variant**

Binary search can have many variants. When implementing variants, attention should be paid to the judgment of boundary values. For example, the implementation of finding the leftmost position of key in an array with repeated elements is as follows:

```java
public int binarySearch(int[] nums, int key) {
    int l = 0, h = nums.length;
    while (l < h) {
        int m = l + (h - l) / 2;
        if (nums[m] >= key) {
            h = m;
        } else {
            l = m + 1;
        }
    }
    return l;
}
```

This implementation differs from the normal implementation in the following ways:

- The assignment expression of h is h = m
- The loop condition is l \< h
- Finally returns l instead of -1

In the case of nums[m] \>= key, it can be deduced that the leftmost key is located in the [l, m] interval, which is a closed interval. The assignment expression for h is h = m, since position m is also a possible solution.

When the assignment expression of h is h = m, if the loop condition is l \<= h, then the loop cannot exit, so the loop condition can only be l \< h. The following demonst
rates the situation where the loop cannot exit when the loop condition is l \<= h:

```text
nums = {0, 1, 2}, key = 1
l m h
0 1 2 nums[m] >= key
0 0 1 nums[m] < key
1 1 1 nums[m] >= key
1 1 1 nums[m] >= key
...
```

When the loop body exits, it does not mean that the key is not found, so the final returned result should not be -1. In order to verify whether it has been found, it is necessary to determine whether the value at the return position and the key are equal on the calling side.

## 1. Find the square root

69\. Sqrt(x) (Easy)

[Leetcode](https://leetcode.com/problems/sqrtx/description/) / [Leetcode](https://leetcode-cn.com/problems/sqrtx/description/)

```html
Input: 4
Output: 2

Input: 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since we want to return an integer, the decimal part will be truncated.
```

The square root sqrt of a number x must be between 0 \~ x, and satisfy sqrt == x / sqrt. You can use binary search to find sqrt between 0 \~ x.

For x = 8, its square root is 2.82842..., which should return 2 instead of 3. When the loop condition is l \<= h and the loop exits, h is always 1 less than l, that is, h = 2, l = 3, so the final return value should be h instead of l.

```java
public int mySqrt(int x) {
    if (x <= 1) {
        return x;
    }
    int l = 1, h = x;
    while (l <= h) {
        int mid = l + (h - l) / 2;
        int sqrt = x / mid;
        if (sqrt == mid) {
            return mid;
        } else if (mid > sqrt) {
            h = mid - 1;
        } else {
            l = mid + 1;
        }
    }
    return h;
}
```

## 2. The smallest element greater than the given element

744\. Find Smallest Letter Greater Than Target (Easy)

[Leetcode](https://leetcode.com/problems/find-smallest-letter-greater-than-target/description/) / [Leetcode](https://leetcode-cn.com/problems/find-smallest-lett
er-greater-than-target/description/)

```html
Input:
letters = ["c", "f", "j"]
target = "d"
Output: "f"

Input:
letters = ["c", "f", "j"]
target = "k"
Output: "c"
```

Question description: Given an ordered character array letters and a character target, it is required to find the smallest character in letters that is greater than target. If it is not found, return the first character.

```java
public char nextGreatestLetter(char[] letters, char target) {
    int n = letters.length;
    int l = 0, h = n - 1;
    while (l <= h) {
        int m = l + (h - l) / 2;
        if (letters[m] <= target) {
            l = m + 1;
        } else {
            h = m - 1;
        }
    }
    return l < n ? letters[l] : letters[0];
}
```

## 3. Single Element of ordered array

540\. Single Element in a Sorted Array (Medium)

[Leetcode](https://leetcode.com/problems/single-element-in-a-sorted-array/description/) / [Leetcode](https://leetcode-cn.com/problems/single-element-in-a-sorted-array/description/)

```html
Input: [1, 1, 2, 3, 3, 4, 4, 8, 8]
Output: 2
```

Question description: In an ordered array, only one number does
not appear twice. Find this number.

It requires O(logN) time complexity to solve, so it cannot be solved by traversing the array and performing an XOR operation. The time complexity of doing so is O(N).

Let index be the position of the Single Element in the array. After index, the state of the pairs originally existing in the array is changed. If m is an even number, and m + 1 \< index, then nums[m] == nums[m + 1]; m + 1 \>= index, then nums[m] != nums[m + 1].

From the above rules, we can know that if nums[m] == nums[m + 1], then the array position where index is located is [m + 2, h], then let l = m + 2; if nums[m] != nums[m + 1], then the array position where index is located is [l, m], and then let h = m.

Because the assignment expression of h is h = m, the loop condition can only use the form l \< h.

```java
public int singleNonDuplicate(int[] nums) {
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int m = l + (h - l) / 2;
        if (m % 2 == 1) {
            m--; // Ensure that l/h/m are all in even numbers, so that the search interval size is always an odd number
        }
        if (nums[m] == nums[m + 1]) {
            l = m + 2;
        } else {
            h = m;
        }
    }
    return nums[l];
}
```

## 4. The first wrong version

278\. First Bad Version (Easy)

[Leetcode](https://leetcode.com/problems/first-bad-version/description/) / [Leetcode](https://leetcode-cn.com/problems/first-bad-version/description/)

Problem description: Given an element n, it represents [1, 2, ..., n] versions. An incorrect version starts to appear at the x-th position, causing all subsequent versions to be incorrect. You can call isBadVersion(int x) to know if a version is wrong, asking to find the first wrong version.

If the mth version is wrong, it means that the first wrong version is between [l, m], let h = m; otherwise, the first wrong version is between [m + 1, h], let l = m + 1.

Because the assignment expression of h is h = m, the loop condition is l \< h.

```java
public int firstBadVersion(int n) {
    int l = 1, h = n;
    while (l < h) {
        int mid = l + (h - l) / 2;
        if (isBadVersion(mid)) {
            h = mid;
        } else {
            l = mid + 1;
        }
    }
    return l;
}
```

## 5. Minimum number of rotated array

153\. Find Minimum in Rotated Sorted Array (Medium)

[Leetcode](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/) / [Leetcode](https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array/description/)

```html
Input: [3,4,5,1,2],
Output: 1
```

```java
public int findMin(int[] nums) {
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int m = l + (h - l) / 2;
        if (nums[m] <= nums[h]) {
            h = m;
        } else {
            l = m + 1;
        }
    }
    return nums[l];
}
```

## 6. Find the interval

34\. Find First and Last Positi
on of Element in Sorted Array

[Leetcode](https://leetcode.com/problems/find-fir
st-and-last-position-of-element-in-sorted-array/) / [Leetcode](https://leetcode-cn.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

```html
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]
```

Problem description: Given an ordered array nums and a target target, it is required to find the first and last position of target in nums.

You can use binary search to find the first position and the last position, but the search method is different and you need to implement two binary searches. We will convert the search for the last position of target into the search for the first position of target+1, and then move forward one position. In this way we only need to implement a binary search code.

```java
public int[] searchRange(int[] nums, int target) {
    int first = findFirst(nums, target);
    int last = findFirst(nums, target + 1) - 1;
    if (first == nums.length || nums[first] != target) {
        return new int[]{-1, -1};
    } else {
        return new int[]{first, Math.max(first, last)};
    }
}

private int findFirst(int[] nums, int target) {
    int l = 0, h = nums.length; // Note the initial value of h
    while (l < h) {
        int m = l + (h - l) / 2;
        if (nums[m] >= target) {
            h = m;
        } else {
            l = m + 1;
        }
    }
    return l;
}
```

In the binary search code that finds the first position, it is important to note that the value of h is nums.length, not nums.length - 1. Let’s look at the following example first:

```
nums = [2,2], target = 2
```

If the value of h is nums.length - 1, then last = findFirst(nums, target + 1) - 1 = 1 - 1 = 0. This is because findLeft will only return values ​​in the range [0, nums.length - 1]. For findFirst([2,2], 3), we want to return the position where 3 is inserted into nums, which is one position after the last position of the array, that is, nums.length. So we need to set the value of h to nums.length, so that the range returned by findFirst is larger and can cover the situation where target is greater than the last element of nums.
