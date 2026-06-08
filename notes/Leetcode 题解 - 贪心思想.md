# Leetcode problem solution - greedy thinking
<!-- GFM-TOC -->
* [Leetcode problem solution-greedy thinking](#leetcode-problem solution---greedy thinking)
    * [1. Distribute cookies](#1-Distribute cookies)
    * [2. Number of non-overlapping intervals] (#2-Number of non-overlapping intervals)
    * [3. Throw darts to puncture the balloon](#3-Throw darts to puncture the balloon)
    * [4. Reorganize the queue based on height and serial number] (#4-Reorganize the queue based on height and serial number)
    * [5. The biggest profit from buying and selling stocks](#5-The biggest profit from buying and selling stocks)
    * [6. The maximum profit from buying and selling stocks II](#6-The maximum profit from buying and selling stocks-ii)
    * [7. Plant flowers](#7-Plant flowers)
    * [8. Determine whether it is a subsequence] (#8-Judge whether it is a subsequence)
    * [9. Modify a number to become a non-decreasing array] (#9-Modify a number to become a non-decreasing array)
    * [10. Maximum sum of subarrays] (#10-Maximum sum of subarrays)
    * [11. Separate strings so that characters of the same type appear together] (#11-Separate strings so characters of the same type appear together)
<!-- GFM-TOC -->


It is guaranteed that each operation is locally optimal and the final result is globally optimal.

## 1. Distribute cookies

455\. Assign Cookies (Easy)

[Leetcode](https://leetcode.com/problems/assign-cookies/description/) / [Leetcode](https://leetcode-cn.com/problems/assign-cookies/description/)

```html
Input: grid[1,3], size[1,2,4]
Output: 2
```

Title description: Each child has a satisfaction grid, and each cookie has a size. Only when the size of the cookie is greater than or equal to a child's satisfaction, the child will be satisfied. Find the maximum number of children that can be satisfied.

1. The biscuits given to one child should be as small as possible and satisfy the child, so that the larger biscuits can be given to the more satisfied child.
2. Because the child with the smallest degree of satisfaction is the easiest to be satisfied, the child with the smallest degree of satisfaction is satisfied first.

In the above solution, we only choose an allocation method that seems to be the current optimal every time we allocate cookies, but there is no guarantee that this local optimal allocation method will eventually obtain the global optimal solution. We assume that the global optimal solution can be obtained and prove it by proof by contradiction, that is, we assume that there is an optimal strategy that is better than the greedy strategy we use. If there is no such optimal strategy, it means that the greedy strategy is the optimal strategy, and the solution obtained is the global optimal solution.

Proof: Suppose that in a certain selection, the greedy strategy chooses to allocate the m-th cookie to the child with the smallest current satisfaction, and the m-th cookie is the smallest cookie that can satisfy the child. Suppose t
here is an optimal policy that assigns the n-th cookie to the child, and m \< n. We can find that after this round of allocation, one of the remaining cookies after the greedy strategy allocation must be larger than the optimal strategy. Therefore, in subsequent allocations, the greedy strategy will definitely satisfy more children. In other words, there is no strategy better than the greedy strategy, that is, the greedy strategy is the optimal strategy.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e69537d2-a016-4676-b169-9ea17eeb9037.gif" width="430px"> </div><br>

```java
public int findContentChildren(int[] grid, int[] size) {
    if (grid == null || size == null) return 0;
    Arrays.sort(grid);
    Arrays.sort(size);
    int gi = 0, si = 0;
    while (gi < grid.length && si < size.length) {
        if (grid[gi] <= size[si]) {
            gi++;
        }
        si++;
    }
    return gi;
}
```

## 2. Number of non-overlapping intervals

435\. Non-overlapping Intervals (Medium)

[Leetcode](https://leetcode.com/problems/non-overlapping-intervals/description/) / [Leetcode](https://leetcode-cn.com/problems/non-overlapping-intervals/description/)

```html
Input: [ [1,2], [1,2], [1,2] ]

Output: 2

Explanation: You need to remove two [1,2] to make the rest of intervals non-overlapping.
```

```html
Input: [ [1,2], [2,3] ]

Output: 0

Explanation: You don't need to remove any of the intervals since they're already non-overlapping.
```

Problem description: Calculate the number of intervals that need to be removed to make a set of intervals non-overlapping.

First calculate the maximum number of non-overlapping intervals that can be formed, and then subtract the number of non-overlapping intervals from the total number of intervals.

In each choice, the end of the interval is the most important. The smaller the end of the selected interval, the greater the space left for the subsequent intervals, and the greater the number of intervals that can be selected later.

Sort by the end of the interval, each time selecting the interval with the smallest end and no overlap with the previous interval.

```java
public int eraseOverlapIntervals(int[][] intervals) {
    if (intervals. length == 0) {
        return 0;
    }
    Arrays.sort(intervals, Comparator.comparingInt(o -> o[1]));
    int cnt = 1;
    int end = intervals[0][1];
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] < end) {
            continue;
        }
        end = intervals[i][1];
        cnt++;
    }
    return intervals.length - cnt;
}
```

Using lambda expressions to create a Comparator will cause the algorithm to run too long. If you focus on running time, you can modify it to create a Comparator statement normally:

```java
Arrays.sort(intervals, new Comp
arator<int[]>() {
     @Override
     public int compare(int[] o1, int[] o2) {
         return (o1[1] < o2[1]) ? -1 : ((o1[1] == o2[1]) ? 0 : 1);
     }
});
```
Avoid using `return o1[1] - o2[1];` when implementing the compare() function to prevent overflow.

## 3. Throw darts to pop balloons

452\. Minimum Number of Arrows to Burst Balloons (Medium)

[Leetcode](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/description/) / [Leetcode](https://leetcode-cn.com/problems/minimum-number-of-arrows-to-burst-balloons/description/)

```
Input:
[[10,16], [2,8], [1,6], [7,12]]

Output:
2
```

Description of the problem: Balloons are placed on a horizontal axis and can overlap. The darts are thrown vertically towards the axis, causing all the balloons on the path to be punctured. Find the minimum number of dart throws so that all balloons are punctured.

It also calculates the number of non-overlapping intervals, but the difference from Non-overlapping Intervals is that [1, 2] and [2, 3] are considered overlapping intervals in this question.

```java
public int findMinArrowShots(int[][] points) {
    if (points. length == 0) {
        return 0;
    }
    Arrays.sort(points, Comparator.comparingInt(o -> o[1]));
    int cnt = 1, end = points[0][1];
    for (int i = 1; i < points.length; i++) {
        if (points[i][0] <= end) {
            continue;
        }
        cnt++;
        end = points[i][1];
    }
    return cnt;
}
```

## 4. Reorganize the queue according to height and serial number

406\. Queue Reconstruction by Height(Medium)

[Leetcode](https://leetcode.com/problems/queue-reconstruction-by-height/description/) / [Leetcode](https://leetcode-cn.com/problems/queue-reconstruction-by-height/description/)

```html
Input:
[[7,0], [4,4], [7,1], [5,0], [6,1], [5,2]]

Output:
[[5,0], [7,0], [5,2], [6,1], [4,4], [7,1]]
```

Problem description: A student is described by two components (h, k), h represents height, and k represents that there are k students in front who are taller than him or as tall as him.

In order to prevent the insertion operation from affecting subsequent operations, taller students should perform the insertion operation first, otherwise the k-th position originally correctly inserted by smaller students may become the k+1-th position.

The height h is in descending order, the number k is in ascending order, and then a student is inserted into the k-th position of the queue.

```java
public int[][] reconstructQueue(int[][] people) {
    if (people == null || people.length == 0 || people[0].length == 0) {
        return new int[0][0];
    }
    Arrays.sort(people, (a, b) -> (a[0] == b[0] ? a[1] - b[1] : b[0] - a[0]));
    List<int[]> queue = new ArrayList<>();
    for (int[] p : people) {
        queue.add(p[1], p);
    }
    return queue.toArray(new int[queue.size()][]);
}
```

## 5. The biggest profit from buying and selling stocks

121\. Best Time to Buy and Sell Stock (Easy)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/) / [Leetcode](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/description/)

Question des
cription: A stock transaction includes buying and selling. Only one transaction is performed to find the maximum profit.

Just record the previous minimum price, use this minimum price as the buying price, and then use the current price as the selling price to see if the current profit is the maximum profit.

```java
public int maxProfit(int[] prices) {
    int n = prices.length;
    if (n == 0) return 0;
    int soFarMin = prices[0];
    int max = 0;
    for (int i = 1; i < n; i++) {
        if (soFarMin > prices[i]) soFarMin = prices[i];
        else max = Math.max(max, prices[i] - soFarMin);
    }
    return max;
}
```


## 6. Maximum returns from buying and selling stocks II

122\. Best Time to Buy and Sell Stock II (Easy)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/) / [Leetcode](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-ii/description/)

Description of the topic: Multiple transactions can be carried out. Multiple transactions cannot be crossed. Multiple transactions can be carried out.

For [a, b, c, d], if there is a \<= b \<= c \<=
d , then the maximum benefit is d - a. And d - a = (d - c) + (c - b) + (b - a) , so when a prices[i] is accessed and prices[i] - prices[i-1] \> 0, then prices[i] - prices[i-1] are added to the income.

```java
public int maxProfit(int[] prices) {
    int profit = 0;
    for (int i = 1; i < prices.length; i++) {
        if (prices[i] > prices[i - 1]) {
            profit += (prices[i] - prices[i - 1]);
        }
    }
    return profit;
}
```


## 7. Plant flowers

605\. Can Place Flowers (Easy)

[Leetcode](https://leetcode.com/problems/can-place-flowers/description/) / [Leetcode](https://leetcode-cn.com/problems/can-place-flowers/description/)

```html
Input: flowerbed = [1,0,0,0,1], n = 1
Output: True
```

Title description: 1 in the flowerbed array indicates that flowers have been planted. There needs to be at least one unit of separation between flowers. Find out whether n flowers can be planted.

```java
public boolean canPlaceFlowers(int[] flowerbed, int n) {
    int len = flowerbed.length;
    int cnt = 0;
    for (int i = 0; i < len && cnt < n; i++) {
        if (flowerbed[i] == 1) {
            continue;
        }
        int pre = i == 0 ? 0 : flowerbed[i - 1];
        int next = i == len - 1 ? 0 : flowerbed[i + 1];
        if (pre == 0 && next == 0) {
            cnt++;
            flowerbed[i] = 1;
        }
    }
    return cnt >= n;
}
```

## 8. Determine whether it is a subsequence

392\. Is Subsequence (Medium)

[Leetcode](https://leetcode.com/problems/is-subsequence/description/) / [Leetcode](https://leetcode-cn.com/problems/is-subsequence/description/)

```html
s = "abc", t = "ahbgdc"
Return true.
```

```java
public boolean isSubsequence(String s, String t) {
    int index = -1;
    for (char c : s.toCharArray()) {
        index = t.indexOf(c, index + 1);
        if (index == -1) {
            return false;
        }
    }
return true;
}
```

## 9. Modify a number into a non-decreasing array

665\. Non-decreasing Array (Easy)

[Leetcode](https://leetcode.com/problems/non-decreasing-array/description/) / [Leetcode](https://leetcode-cn.com/problems/non-decreasing-array/description/)

```html
Input: [4,2,3]
Output: True
Explanation: You could modify the first 4 to 1 to get a non-decreasing array.
```

Problem description: Determine whether an array can become a non-decreasing array by modifying only one number.

When nums[i] \< nums[i - 1] appears, what needs to be considered is which number in the array should be modified so that this modification can make the array before i a non-decreasing array and **does not affect subsequent operations**. Priority is given to setting nums[i - 1] = nums[i], because if nums[i] = nums[i - 1] is modified, then the number nums[i] will become larger, and may be larger than nums[i + 1], thus affecting subsequent operations. Another special case is nums[i] \< nums[i - 2]. Modifying nums[i - 1] = nums[i] cannot make the array a non-decreasing array. You can only modify nums[i] = nums[i - 1].

```java
public boolean checkPossibility(int[] nums) {
    int cnt = 0;
    for (int i = 1; i < nums.length && cnt < 2; i++) {
        if (nums[i] >= nums[i - 1]) {
            continue;
        }
        cnt++;
        if (i - 2 >= 0 && nums[i - 2] > nums[i]) {
            nums[i] = nums[i - 1];
        } else {
            nums[i - 1] = nums[i];
        }
    }
    return cnt <= 1;
}
```



## 10. Maximum sum of subarrays

53\. Maximum Subarray (Easy)

[Leetcode](https://leetcode.com/problems/maximum-subarray/description/) / [Leetcode](https://leetcode-cn.com/problems/maximum-subarray/description/)

```html
For example, given the array [-2,1,-3,4,-1,2,1,-5,4],
the contiguous subarray [4,-1,2,1] has
the largest sum = 6.
```

```java
public int maxSubArray(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }
    int preSum = nums[0];
    int maxSum = preSum;
    for (int i = 1; i < nums.length; i++) {
        preSum = preSum > 0 ? preSum + nums[i] : nums[i];
        maxSum = Math.max(maxSum, preSum);
    }
    return maxSum;
}
```

## 11. 分隔字符串使同种字符出现在一起

763\. Partition Labels (Medium)

[Leetcode](https://leetcode.com/problems/partition-labels/description/) / [力扣](https://leetcode-cn.com/problems/partition-labels/description/)

```html
Input: S = "ababcbacadefegdehijhklij"
Output: [9,7,8]
Explanation:
The partition is "ababcbaca", "defegde", "hijhklij".
This is a partition so that each letter appears in at most one part.
A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits S into less parts.
```

```java
public List<Integer> partitionLabels(String S) {
    int[] lastIndexsOfChar = new int[26];
    for (int i = 0; i < S.length(); i++) {
        lastIndexsOfChar[char2Index(S.charAt(i))] = i;
    }
    List<Integer> partitions = new ArrayList<>();
    int firstIndex = 0;
    while (firstIndex < S
.length()) {
        int lastIndex = firstIndex;
        for (int i = firstIndex; i < S.length() && i <= lastIndex; i++) {
            int index = lastIndexsOfChar[char2Index(S.charAt(i))];
            if (index > lastIndex) {
                lastIndex = index;
            }
        }
        partitions.add(lastIndex - firstIndex + 1);
        firstIndex = lastIndex + 1;
    }
    return partitions;
}

private int char2Index(char c) {
    return c - 'a';
}
```
