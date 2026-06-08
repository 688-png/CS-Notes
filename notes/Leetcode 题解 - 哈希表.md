# Leetcode problem solution - Hash table
<!-- GFM-TOC -->
* [Leetcode solution - hash table](#leetcode-solution---hash table)
    * [1. The sum of two numbers in the array is a given value] (#1-The sum of two numbers in the array is a given value)
    * [2. Determine whether the array contains duplicate elements] (#2-Determine whether the array contains duplicate elements)
    * [3. The longest harmonious sequence](#3-The longest harmonious sequence)
    * [4. Longest continuous sequence](#4-Longest continuous sequence)
<!-- GFM-TOC -->


Hash tables store data using O(N) space complexity and solve problems in O(1) time complexity.

- **HashSet** in Java is used to store a set and can find whether an element is in the set. If the elements are finite and the range is not large, a Boolean array can be used to store whether an element exists. For example, for elements with only lowercase characters, a Boolean array with a length of 26 can be used to store a character set, reducing the space complexity to O(1).

 **HashMap** in Java is mainly used for mapping relationships to connect two elements. HashMap can also be used to count elements, where the key is the element and the value is the count. Similar to HashSet, if the elements are finite and the range is not large, you can use an integer array for statistics. When compressing or otherwise transforming a content, HashMap can be used to connect the original content and the converted content. For example, in a system that simplifies urls [Leetcdoe : 535. Encode and Decode TinyURL (Medium)

[Leetcode](https://leetcode.com/problems/encode-and-decode-tinyurl/description/), use HashMap to store the mapping from the simplified url to the original url, so that not only the simplified url can be displayed, but also the original url can be obtained based on the simplified url to locate the correct resource.) / [Leetcode-cn.com/problems/encode-and-decode-tinyurl/description/), you can use HashMap to store the mapping from the simplified url to the original url, so that you can not only display the simplified url, but also get the original url based on the simplified url to locate the correct resource.)


## 1. The sum of two numbers in the array is a given value

1\.Two Sum (Easy)

[Leetcode](https://leetcode.com/problems/two-sum/description/) / [Leetcode](https://leetcode-cn.com/problems/two-sum/description/)

You can sort the array first, and then use the double pointer method or binary search method. The time complexity of doing this is O(NlogN) and the space complexity is O(1).

Use HashMap to store the mapping between array elements and indexes. When accessing nums[i], determine whether target - nums[i] exists in the HashMap. If it exists, the index where target - nums[i] is located and i are the two numbers you are looking for. The time complexity of this method is O(N) and the space complexity is O(N), using space in exchange for time.

```java
public int[] twoSum(int[] nums, int target) {
    HashMa
p<Integer, Integer> indexForNum = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        if (indexForNum.containsKey(target - nums[i])) {
            return new int[]{indexForNum.get(target - nums[i]), i};
        } else {
            indexForNum.put(nums[i], i);
        }
    }
    return null;
}
```

## 2. Determine whether the array contains duplicate elements

217\. Contains Duplicate (Easy)

[Leetcode](https://leetcode.com/problems/contains-duplicate/description/) / [Leetcode](https://leetcode-cn.com/problems/contains-duplicate/description/)

```java
public boolean containsDuplicate(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int num : nums) {
        set.add(num);
    }
    return set.size() < nums.length;
}
```

## 3. The longest harmonious sequence

594\. Longest Harmonious Subsequence (Easy)

[Leetcode](https://leetcode.com/problems/longest-harmonious-subsequence/description/) / [Leetcode](https://leetcode-cn.com/problems/longest-harmonious-subsequence/description/)

```html
Input: [1,3,2,2,5,2,3,7]
Output: 5
Explanation: The longest harmonious subsequence is [3,2,2,2,3].
```

The difference between the largest number and the smallest number in a harmonious sequence is exactly 1. It should be noted that the elements of the sequence are not necessarily consecutive elements of the array.

```java
public int findLHS(int[] nums) {
    Map<Integer, Integer> countForNum = new HashMap<>();
    for (int num : nums) {
        countForNum.put(num, countForNum.getOrDefault(num, 0) + 1);
    }
    int longest = 0;
    for (int num : countForNum.keySet()) {
        if (countForNum.containsKey(num + 1)) {
            longest = Math.max(longest, countForNum.get(num + 1) + countForNum.get(num));
        }
    }
    return longest;
}
```

## 4.
New snowflakes

128\. Longest Consecutive Sequence (Hard)

[Leetcode](https://leetcode.com/problems/longest-consecutive-sequence/description/)

```html
Given [ 100 , 4 , 200 , 1 , 3 , 2 ] ,
The longest consecutive element sequence is [1, 2, 3, 4]. Return its length:
```

Check out the O(N) National Park Service.

```java
public int longestConsecutive(int[] nums) {
    Map<Integer, Integer> countForNum = new HashMap<>();
    for ( int num : nums ) {
        countForNum . put ( num , 1 ) ;
    } }
    for ( int num : nums ) {
        forward ( countForNum , num ) ;
    } }
    return maxCount ( countForNum ) ;
} }

private int forward(Map<Integer, Integer> countForNum, int num) {
    if ( ! countForNum . containsKey ( num )) {
        return 0 ;
    } }
    int cnt = countForNum . get ( num ) ;
    if ( cnt > 1 ) {
        return cnt ;
    } }
    cnt = forward ( countForNum , num + 1 ) + 1 ;
    countForNum . put ( num , cnt ) ;
    return cnt ;
} }

private int maxCount(Map<Integer, Integer> countForNum) {
    int max = 0 ;
    for ( int num : countForNum . keySet ()) {
        max = Math . max ( max , countForNum . get ( num ) ) ;
    } }
    return max ;
} }
```
