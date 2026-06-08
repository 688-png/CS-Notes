# Leetcode problem solution - double pointer
<!-- GFM-TOC -->
* [Leetcode solution - double pointers](#leetcode-solution---double pointers)
    * [1. Two Sum of ordered array](#1-Two-sum of ordered array)
    * [2. Sum of squares of two numbers](#2-Sum of squares of two numbers)
    * [3. Reverse vowel characters in string](#3-Reverse vowel characters in string)
    * [4. Palindrome string](#4-Palindrome string)
    * [5. Merge two ordered arrays](#5-Merge two ordered arrays)
    * [6. Determine whether there is a ring in the linked list] (#6-Judge whether there is a ring in the linked list)
    * [7. Longest subsequence](#7-Longest subsequence)
<!-- GFM-TOC -->


Double pointers are mainly used to traverse arrays. The two pointers point to different elements to complete the task together.

## 1. Two Sum of ordered array

167\. Two Sum II - Input array is sorted (Easy)

[Leetcode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/) / [Leetcode](https://leetcode-cn.com/problems/two-sum-ii-input-array-is-sorted/description/)

```html
Input: numbers={2, 7, 11, 15}, target=9
Output: index1=1, index2=2
```

Problem description: Find two numbers in an ordered array so that their sum is target.

Use double pointers, one pointer points to the element with the smaller value and one pointer points to the element with the larger value. Pointers to smaller elements are traversed from beginning to end, and pointers to larger elements are traversed from tail to beginning.

- If the sum of the two pointers pointing to elements sum == target, then the required result is obtained;
- If sum \> target, move the larger element to make sum smaller;
- If sum \< target, move the smaller element so that sum becomes larger.

The elements in the array are traversed at most once, and the time complexity is O(N). Only two extra variables are used and the space complexity is O(1).

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/437cb54c-5970-4ba9-b2ef-2541f7d6c81e.gif" width="200px"> </div><br>

```java
public int[] twoSum(int[] numbers, int target) {
    if (numbers == null) return null;
    int i = 0, j = numbers.length - 1;
    while (i < j) {
        int sum = numbers[i] + numbers[j];
        if (sum == target) {
            return new int[]{i + 1, j + 1};
        } else if (sum < target) {
            i++;
        } else {
            j--;
        }
    }
    return null;
}
```

## 2. Sum of squares of two numbers

633\. Sum of Square Numbers (Easy)

[Leetcode](https://leetcode.com/problems/sum-of-square-numbers/description/) / [Leetcode](https://leetcode-cn.com/problems/sum-of-square-numbers/description/)

```html
Input: 5
Output: True
Explanation: 1 * 1 + 2 * 2 = 5
```

Problem description: Determine whether a non-negative integer is the sum of the squares of two integers.

It can be seen as searching for two numbers in an ordered array whose elements are 0\~target, so that the sum of the squares of th
e two numbers is target. If it can be found, it returns true, indicating that target is the sum of the squares of two integers.

This question is similar to 167\. Two Sum II - Input array is sorted, with only one obvious difference: one is the sum as target, and the other is the sum of squares as target. In this question, you can also use double pointers to get two numbers so that the sum of their squares is target.

The key to this question is the initialization of the right pointer to implement pruning, thereby reducing the time complexity. Let the right pointer be x and the left pointer be fixed at 0. In order to make the value of 0<sup>2</sup> + x<sup>2</sup> as close as possible to the target, we can take x as sqrt(target).

Because 0\~sqrt(target) only needs to be traversed once at most, the time complexity is O(sqrt(target)). And because only two additional variables are used, the space complexity is O(1).

```java
 public boolean judgeSquareSum(int target) {
     if (target < 0) return false;
     int i = 0, j = (int) Math.sqrt(target);
     while (i <= j) {
         int powSum = i * i + j * j;
         if (powSum == target) {
             return true;
         } else if (powSum > target) {
             j--;
         } else {
             i++;
         }
     }
     return false;
 }
```

## 3. Reverse vowel characters in a string

345\. Reverse Vowels of a String (Easy)

[Leetcode](https://leetcode.com/problems/reverse-vowels-of-a-string/description/) / [Leetcode](https://leetcode-cn.com/problems/reverse-vowels-of-a-string/description/)

```html
Given s = "leetcode", return "leotcede".
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a7cb8423-895d-4975-8ef8-
662a0029c772.png" width="400px"> </div><br>

Use double pointers, one pointer traverses from beginning to end, and one pointer traverses from end to beginning. When both pointers traverse to a vowel character, the two vowel characters are exchanged.

In order to quickly determine whether a character is a vowel character, we add all vowel characters to the set HashSet, thereby performing the operation with O(1) time complexity.

- Time complexity is O(N): only need to traverse all elements once
- Space complexity O(1): only two extra variables need to be used

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ef25ff7c-0f63-420d-8b30-eafbea35d11.gif" width="400px"> </div><br>

```java
private final static HashSet<Character> vowels = new HashSet<>(
        Arrays.asList('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'));

public String reverseVowels(String s) {
    if (s == null) return null;
    int i = 0, j = s.length() - 1;
    char[] result = new char[s.length()];
    while (i <= j) {
        char ci = s.charAt(i);
        char cj = s.charAt(j);
        if (!vowels.contains(ci)) {
            result[i++] = ci;
        } else if (!vowels.contains(cj)) {
            result[j--] = cj;
        } else {
result[i++] = cj;
            result[j--] = ci;
        }
    }
    return new String(result);
}
```

## 4. Palindrome string

680\. Valid Palindrome II (Easy)

[Leetcode](https://leetcode.com/problems/valid-palindrome-ii/description/) / [Leetcode](https://leetcode-cn.com/problems/valid-palindrome-ii/description/)

```html
Input: "abca"
Output: True
Explanation: You could delete the character 'c'.
```

Title description: You can delete a character to determine whether it can form a palindrome string.

The so-called palindrome string refers to a string with left-right symmetry. For example, "abcba" is a palindrome string.

Using double pointers, you can easily determine whether a string is a palindrome string: let one pointer traverse from left to right, and one pointer traverse from right to left. The two pointers move one position at the same time, and each time it is judged whether the characters pointed to by the two pointers are the same. If they are the same, the string is a palindrome string with left-right symmetry.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/fcc941ec-134b-4dcd-bc86-1702fd305300.gif" width="250px"> </div><br>

The key to this question is to deal with deleting a character. When using double pointers to traverse a string, if the characters pointed to by the two pointers are not equal, we try to delete a character and then determine whether the deleted string is a palindrome string.

When judging whether it is a palindrome string, we do not need to judge the entire string, because the characters to the left of the left pointer and to the right of the right pointer have been judged to be symmetrical before, so we only need to judge the middle substring.

When trying to delete a character, we can delete the character pointed to by the left pointer or the character pointed by the right pointer.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/db5f30a7-8bfa-4ecc-ab5d-747c77818964.gif" width="300px"> </div><br>

```java
public boolean validPalindrome(String s) {
    for (int i = 0, j = s.length() - 1; i < j; i++, j--) {
        if (s.charAt(i) != s.charAt(j)) {
            return isPalindrome(s, i, j - 1) || isPalindrome(s, i + 1, j);
        }
    }
    return true;
}

private boolean isPalindrome(String s, int i, int j) {
    while (i < j) {
        if (s.charAt(i++) != s.charAt(j--)) {
            return false;
        }
    }
    return true;
}
```

## 5. Merge two ordered arrays

88\. Merge Sorted Array (Easy)

[Leetcode](https://leetcode.com/problems/merge-sorted-array/description/) / [Leetcode](https://leetcode-cn.com/problems/merge-sorted-array/description/)

```html
Input:
nums1 = [1,2,3,0,0,0], m = 3
nums2 = [2,5,6], n = 3

Output: [1,2,2,3,5,6]
```

Problem description: Store the merged results in the first array.

It is necessary to traverse from the end, otherwise the value obtained by merging on nums1 will overwrite the v
alues that have not been merged and compared.

```java
public void merge(int[] nums1, int m, int[] nums2, int n) {
    int index1 = m - 1, index2 = n - 1;
    int indexMerge = m + n - 1;
    while (index2 >= 0) {
        if (
index1 < 0) {
            nums1[indexMerge--] = nums2[index2--];
        } else if (index2 < 0) {
            nums1[indexMerge--] = nums1[index1--];
        } else if (nums1[index1] > nums2[index2]) {
            nums1[indexMerge--] = nums1[index1--];
        } else {
            nums1[indexMerge--] = nums2[index2--];
        }
    }
}
```

## 6. Determine whether there is a cycle in the linked list

141\. Linked List Cycle (Easy)

[Leetcode](https://leetcode.com/problems/linked-list-cycle/description/) / [Leetcode](https://leetcode-cn.com/problems/linked-list-cycle/description/)

Using dual pointers, one pointer moves one node at a time, and one pointer moves two nodes at a time. If there is a cycle, the two pointers will definitely meet.

```java
public boolean hasCycle(ListNode head) {
    if (head == null) {
        return false;
    }
    ListNode l1 = head, l2 = head.next;
    while (l1 != null && l2 != null && l2.next != null) {
        if (l1 == l2) {
            return true;
        }
        l1 = l1.next;
        l2 = l2.next.next;
    }
    return false;
}
```

## 7. Longest subsequence

524\. Longest Word in Dictionary through Deleting (Medium)

[Leetcode](https://leetcode.com/problems/longest-word-in-dictionary-through-deleting/description/) / [Leetcode](https://leetcode-cn.com/problems/longest-word-in-dictionary-through-deleting/description/)

```
Input:
s = "abpcplea", d = ["ale","apple","monkey","plea"]

Output:
"apple"
```

Problem description: Delete some characters in s so that it forms a string in the string list d, and find the longest string that can be formed. If there are multiple results of the same length, return the lexicographically smallest string.

By deleting a character in the string s, the string t can be obtained. It can be considered that t is a subsequence of s. We can use double pointers to determine whether a string is a subsequence of another string.

```java
public String findLongestWord(String s, List<String> d) {
    String longestWord = "";
    for (String target : d) {
        int l1 = longestWord.length(), l2 = target.length();
        if (l1 > l2 || (l1 == l2 && longestWord.compareTo(target) < 0)) {
            continue;
        }
        if (isSubstr(s, target)) {
            longestWord = target;
        }
    }
    return longestWord;
}

private boolean isSubstr(String s, String target) {
    int i = 0, j = 0;
    while (i < s.length() && j < target.length()) {
        if (s.charAt(i) == target.charAt(j)) {
            j++;
        }
        i++;
    }
    return j == target.length();
}
```
