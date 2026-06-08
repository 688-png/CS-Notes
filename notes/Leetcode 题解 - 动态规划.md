# Leetcode problem solution - dynamic programming
<!-- GFM-TOC -->
* [Leetcode problem solution - dynamic programming] (#leetcode-problem solution---dynamic programming)
    * [Fibonacci Sequence](#Fibonacci Sequence)
        * [1. Climb the stairs](#1-Climb the stairs)
        * [2. Robbery](#2-Robbery)
        * [3. Robbers robbed in the Ring Block] (#3-Robbers robbed the Ring Street)
        * [4. Letters are misarranged](#4-Letter is misarranged)
        * [5. Cow production](#5-Cow production)
    * [Matrix Path](#Matrix Path)
        * [1. Minimum path sum of matrix](#1-Minimum path sum of matrix)
        * [2. The total number of paths in the matrix] (#2-The total number of paths in the matrix)
    * [array interval](#array interval)
        * [1. Array range sum] (#1-array range sum)
        * [2. The number of medium difference increasing sub-intervals in the array] (#2-The number of medium difference increasing sub-intervals in the array)
    * [split integer](#split integer)
        * [1. Maximum product of divided integers] (#1-Maximum product of divided integers)
        * [2. Divide integers by squares](#2-Divide integers by squares)
        * [3. Divide integers to form alphabetic strings](#3-Split integers to form alphabetic strings)
    * [Longest Increasing Subsequence](#Longest Increasing Subsequence)
        * [1. Longest increasing subsequence](#1-Longest increasing subsequence)
        * [2. The longest chain that can be formed by a set of integer pairs] (#2-The longest chain that can be formed by a set of integer pairs)
        * [3. Longest wobble subsequence](#3-Longest wobble subsequence)
    * [Longest common subsequence](#longest common subsequence)
        * [1. Longest common subsequence](#1-Longest common subsequence)
    * [0-1 Backpack](#0-1-Backpack)
        * [1. Divide the array into two parts equal to sum](#1-Divide the array into two parts equal to sum)
        * [2. Change the sign of a group of numbers so that their sum is a given number] (#2-Change the sign of a group of numbers so that their sum is a given number)
        * [3. 01 characters make up the most string] (#3-01-characters make up the most string)
        * [4. Minimum number of coins for change] (#4-Minimum number of coins for change)
        * [5. Coin number combination for change] (#5-Coin number combination for change)
        * [6. String split by word list] (#6-String split by word list)
        * [7. Combination sum](#7-combination sum)
    *[StockTrading](#stocktrade)
        * [1. Stock transactions that require a cooling-off period] (#1-Stock transactions that require a cooling-off period)
        *[2. Stock transactions requiring transaction fees](#2-Stock transactions requiring transaction fees)
        * [3. Stock trades can only be made twice] (#3- Stock trades can only be made twice)
        * [4. Only k stock transactions can be performed](#4-Only k stock transactions can be performed)
    * [String Edit](#String Edit)
* [1. Delete the characters of the two strings to make them equal] (#1-Delete the characters of the two strings to make them equal)
        * [2. Edit distance](#2-Edit distance)
        * [3. Copy and paste characters](#3-Copy and paste characters)
<!-- GFM-TOC -->


Both recursive and dynamic programming split the original problem into multiple sub-problems and then solve them. The most essential difference between them is that dynamic programming saves the solutions to the sub-problems and avoids repeated calculations.

## Fibonacci Sequence

### 1. Climb the stairs

70\. Climbing Stairs (Easy)

[Leetcode](https://leetcode.com/problems/climbing-stairs/description/) / [Leetcode](https://leetcode-cn.com/problems/climbing-stairs/description/)

Question description: There are N steps of stairs. You can go up one or two steps at a time. Find how many ways to go up the stairs.

Define an array dp to store the number of ways to go up the stairs (for the convenience of discussion, the array subscript starts from 1), dp[i] represents the number of ways to go to the i-th staircase.

The i-th staircase can be reached by taking one more step from the i-1 and i-2 stairs. The number of ways to reach the i-th staircase is the sum of the number of ways to reach the i-1 and i-2 stairs.

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i]=dp[i-1]+dp[i-2]" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/14fe1e71-8518-458f-a220-116003061a83.png" width="200px"> </div><br>

Considering that dp[i] is only related to dp[i - 1] and dp[i - 2], only two variables can be used to store dp[i - 1] and dp[i - 2], so that the original O(N) space complexity is optimized to O(1) complexity.

```java
public int climbStairs(int n) {
    if (n <= 2) {
        return n;
    }
    int pre2 = 1, pre1 = 2;
    for (int i = 2; i < n; i++) {
        int cur = pre1 + pre2;
        pre2 = pre1;
        pre1 = cur;
    }
    return pre1;
}
```

### 2. Robbery

198\. House Robber (Easy)

[Leetcode](https://leetcode.com/problems/house-robber/description/) / [Leetcode](https://leetcode-cn.com/problems/house-robber/description/)

Problem description: Rob a row of households, but cannot rob neighboring households. Find the maximum amount of robbery.

Define the dp array to store the maximum amount of robbery, where dp[i] represents the maximum amount of robbery when the i-th household is robbed.

Since neighboring households cannot be robbed, if the i-1th household is robbed, then the i-th household cannot be robbed again, so

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i]=max(dp[i-2]+nums[i],dp[i-1])" class="mathjax-pic"/></div> <br>-->

<div align="cent
er"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2de794ca-aa7b-48f3-a556-a0e2708cb976.jpg" width="350px"> </div><br>

```java
public int rob(int[] nums) {
    int pre2 = 0, pre1 = 0;
    f
or (int i = 0; i < nums.length; i++) {
        int cur = Math.max(pre2 + nums[i], pre1);
        pre2 = pre1;
        pre1 = cur;
    }
    return pre1;
}
```

### 3. Robbers robbed in the ring district

213\. House Robber II (Medium)

[Leetcode](https://leetcode.com/problems/house-robber-ii/description/) / [Leetcode](https://leetcode-cn.com/problems/house-robber-ii/description/)

```java
public int rob(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }
    int n = nums.length;
    if (n == 1) {
        return nums[0];
    }
    return Math.max(rob(nums, 0, n - 2), rob(nums, 1, n - 1));
}

private int rob(int[] nums, int first, int last) {
    int pre2 = 0, pre1 = 0;
    for (int i = first; i <= last; i++) {
        int cur = Math.max(pre1, pre2 + nums[i]);
        pre2 = pre1;
        pre1 = cur;
    }
    return pre1;
}
```

### 4. Letters are misarranged

Problem description: There are N letters and envelopes. They are scrambled. Find the number of wrong ways to pack the letters.

Define an array dp to store the number of error modes, dp[i] represents the number of error modes for the first i letters and envelopes. Suppose the i-th letter is put into the j-th envelope, and the j-th letter is put into the k-th envelope. Depending on whether i and k are equal, there are two situations:

- i==k, after exchanging i and j's letters, their letters and envelopes are in the correct position, but the remaining i-2 letters have dp[i-2] wrong ways of packing them. Since j has i-1 values, there are (i-1)\*dp[i-2] wrong ways to load the message.
- i != k, after exchanging the letters of i and j, the i-th letter and envelope are in the correct position, and the remaining i-1 letters have dp[i-1] wrong ways of packaging. Since j has i-1 values, there are (i-1)\*dp[i-1] wrong ways to load the message.

To sum up, the number of wrong ways to load letters is:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i]=(i-1)*dp[i-2]+(i-1)*dp[i-1]" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/da1f96b9-fd4d-44ca-8925-fb14c5733388.png" width="350px"> </div><br>

### 5. Cow production

[Programmer Code Interview Guide-P181](#)

Description of the problem: Assume that mature cows on the farm will give birth to one heifer every year and they will never die. There is 1 heifer in the first year and from the second year onwards the cows start giving birth to heifers. Each heifer is mature enough to give birth to another heifer after 3 years. Given an integer N, find the number of cattle N years from now.

The number of mature cattle in year i is:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i]=dp[i-1]+dp[i-3]" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/879814ee-48b5-4bcb-86f5-dcc400cb81ad.png" width="250px"> </div><br>

## Matrix path

### 1. Minimum path sum of matrix

64\. Minimum Path Sum (Medium)

[Leetcode](https://leetcode.com/problems/minimum-path-sum/description/) / [Leetcode](https://leetcode-cn.com/problems/minimum-path-sum/description/)

```html
[[1,3,1],
 [1,5,1],
 [4,2,1]]
Given the above grid map, return 7. Because the path 1→3→1→1→1 minimizes the sum.
```

Question description: Find the minimum path sum from the upper left corner to the lower right corner of the matrix, and can only move to the right and downward each time.

```java
public int minPathSum(int[][] grid) {
    if (grid.length == 0 || grid[0].length == 0) {
        return 0;
    }
    int m = grid.length, n = grid[0].length;
    int[] dp = new int[n];
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (j == 0) {
                dp[j] = dp[j]; // You can only walk to this position from the top
            } else if (i == 0) {
                dp[j] = dp[j - 1]; // You can only go to this location from the left
            } else {
dp[j] = Math.min(dp[j - 1], dp[j]);
            }
            dp[j] += grid[i][j];
        }
    }
    return dp[n - 1];
}
```

### 2. Total number of paths in the matrix

62\. Unique Paths (Medium)

[Leetcode](
https://leetcode.com/problems/unique-paths/description/) / [Leetcode](https://leetcode-cn.com/problems/unique-paths/description/)

Title description: Count the total number of paths from the upper left corner to the lower right corner of the matrix. Each time you can only move to the right or down.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/dc82f0f3-c1d4-4ac8-90ac-d5b32a9bd75a.jpg" width=""> </div><br>

```java
public int uniquePaths(int m, int n) {
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[j] = dp[j] + dp[j - 1];
        }
    }
    return dp[n - 1];
}
```

It can also be solved directly using mathematical formulas. This is a combination problem. The total number of movements of the robot is S=m+n-2, and the number of downward movements is D=m-1. Then the problem can be seen as taking the number of combinations of D positions from S. The solution to this problem is C(S, D).

```java
public int uniquePaths(int m, int n) {
    int S = m + n - 2; // Total number of moves
    int D = m - 1; // Number of downward moves
    long ret = 1;
    for (int i = 1; i <= D; i++) {
        ret = ret * (S - D + i) / i;
    }
    return (int) ret;
}
```

## Array range

### 1. Array range sum

303\. Range Sum Query - Immutable (Easy)

[Leetcode](https://leetcode.com/problems/range-sum-query-immutable/description/) / [Leetcode](https://leetcode-cn.com/problems/range-sum-query-immutable/description/)

```html
Given nums = [-2, 0, 3, -5, 2, -1]

sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3
```

Finding the sum of the interval i \~ j can be converted into sum[j + 1] - sum[i], where sum[i] is the sum of 0 \~ i - 1.

```java
class NumArray {

    private int[] sums;

    public NumArray(int[] nums) {
        sums = new int[nums.length + 1];
        for (int i = 1; i <= nums.length; i++) {
            sums[i] = sums[i - 1] + nums[i - 1];
        }
    }

    public int sumRange(int i, int j) {
        return sums[j + 1] - sums[i];
    }
}
```

### 2. The number of increasing subintervals in the array

413\. Arithmetic Slices (Medium)

[Leetcode](https://leetcode.com/problems/arithmetic-slices/description/) / [Leetcode](https://leetcode-cn.com/problems/arithmetic-slices/description/)

```html
A = [0, 1, 2, 3, 4]

return: 6, for 3 arithmetic slices in A:

[0, 1, 2],
[1, 2, 3],
[0, 1, 2, 3],
[0, 1, 2, 3, 4],
[1, 2, 3, 4],
[2, 3, 4]
```

dp[i] represents the number of arithmetic increasing subintervals ending with A[i].

When A[i] - A[i-1] == A[i-1] - A[i-2], then [A[i-2], A[i-1], A[i]] forms an arithmetic increasing subinterval. Moreover, adding an A[i] after the increasing sub-interval ending with A[i-1] can also form a new increasing sub-interval.

```html
dp[2] = 1
    [0, 1, 2]
dp[3] = dp[2] + 1 = 2
    [0, 1, 2, 3], // Add a 3 after [0, 1, 2]
    [1, 2, 3] // New increasing subrange
dp[4] = dp[3] + 1 = 3
    [0
, 1, 2, 3, 4], // add 4 after [0, 1, 2, 3]
    [1, 2, 3, 4], // add 4 after [1, 2, 3]
    [2, 3, 4] // New increasing subrange
```

In summary, when A[i] - A[i-1] == A[i-1] - A[i-2], dp[i] = dp[i-1] + 1.

Because the increasing subrange does not necessarily end with the last element and can end with any element, the accumulated result of the dp array needs to be returned.

```java
public int numberOfArithmeticSlices(int[] A) {
    if (A == null || A.length == 0) {
        return 0;
    }
    int n = A.length;
    int[] dp = new int[n];
    for (int i = 2; i < n; i++) {
        if (A[i] - A[i - 1] == A[i - 1] - A[i - 2]) {
dp[i] = dp[i - 1] + 1;
        }
    }
    int total = 0;
    for (int cnt : dp) {
        total += cnt;
    }
    return total;
}
```

## Split integers

### 1. Maximum product of divided integers

343\. Integer Break (Medim)

[Leetcode](https://leetcode.com/problems/integer-break/description/) / [Leetcode](https://leetcode-cn.com/problems/integer-break/description/)

Question description: For example, given n = 2, return 1 (2 = 1 + 1); given n = 10, return 36 (10 = 3 + 3 + 4).

```java
public int integerBreak(int n) {
    int[] dp = new int[n + 1];
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        for (int j = 1; j <= i - 1; j++) {
            dp[i] = Math.max(dp[i], Math.max(j * dp[i - j], j * (i - j)));
        }
    }
    return dp[n];
}
```

### 2. Divide integers by squares

279\. Perfect Squares(Medium)

[Leetcode](https://leetcode.com/problems/perfect-squares/description/) / [Leetcode](https://leetcode-cn.com/problems/perfect-squares/description/)

Question description: For example, given n = 12, return 3 because 12 = 4 + 4 + 4; given n = 13, return 2 because 13 = 4 + 9.

```java
public int numSquares(int n) {
    List<Integer> squareList = generateSquareList(n);
    int[] dp = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        int min = Integer.MAX_VALUE;
        for (int square : squareList) {
            if (square > i) {
                break;
            }
            min = Math.min(min, dp[i - square] + 1);
        }
        dp[i] = min;
    }
    return dp[n];
}

private List<Integer> generateSquareList(int n) {
    List<Integer> squareList = new ArrayList<>();
    int diff = 3;
    int square = 1;
    while (square <= n) {
        squareList.add(square);
        square += diff;
        diff += 2;
    }
    return squareList;
}
```

### 3. Split integers to form alphabetic strings

91\. Decode Ways (Medium)

[Leetcode](https://leetcode.com/problems/decode-ways/description/) / [Leetcode](https://leetcode-cn.com/problems/decode-ways/description/)

Title description: Given encoded message "12", it could be decoded as "AB" (1 2) or "L" (12).

```java
public int numDecodings(String s) {
    if (s == null || s.length() == 0) {
        return 0;
    }
    int n = s.length();
    int[] dp = new int[n + 1];
    dp[0] = 1;
    dp[1] = s.charAt(0) == '0' ? 0 : 1;
    for (int i = 2; i <= n; i++) {
        in
t one = Integer.valueOf(s.substring(i - 1, i));
        if (one != 0) {
            dp[i] += dp[i - 1];
        }
        if (s.charAt(i - 2) == '0') {
            continue;
        }
        int two = Integer.valueOf(s.substring(i - 2, i));
        if (two <= 26) {
            dp[i] += dp[i - 2];
        }
    }
    return dp[n];
}
```

## Longest increasing subsequence

Given a sequence {S<sub>1</sub>, S<sub>2</sub>,...,S<sub>n</sub>}, take out a number of numbers to form a new sequence {S<sub>i1</sub>, S<sub>i2</sub>,..., S<sub>im</sub>}, where i1, i2...im keep increasing, that is, the numbers in the new sequence still maintain the order of the original sequence, and the new sequence is called a part of the original sequence. **Subsequence**.

If in a subsequence, when the subscript ix > iy, S<sub>ix</sub> > S<sub>iy</sub>, the subsequence is called an **increasing subsequence** of the original sequence.

Define an array dp to store the length of the longest increasing subsequence, dp[n] represents the length of the longest increasing subsequence of the sequence ending with S<sub>n</sub>. For an increasing subsequence {S<sub>i1</sub>, S<sub>i2</sub>,...,S<sub>im</sub>}, if im < n and S<sub>im
</sub> < S<sub>n</sub>, at this time {S<sub>i1</sub>, S<sub>i2</sub>,..., S<sub>im</sub>, S<sub>n</sub>} is an increasing subsequence, and the length of the increasing subsequence increases by 1. Among the increasing subsequences that meet the above conditions, the longest increasing subsequence is what we are looking for. Add S<sub>n</sub> to the longest increasing subsequence to form the longest increasing subsequence ending with S<sub>n</sub>. Therefore dp[n] = max{ dp[i]+1 | S<sub>i</sub> < S<sub>n</sub> && i < n} .

Because it may not be possible to find an increasing subsequence that meets the conditions when calculating dp[n]. At this time, {S<sub>n</sub>} constitutes an increasing subsequence. The previous solution equation needs to be modified to make dp[n] minimum 1, that is:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[n]=max\{1,dp[i]+1|S_i<S_n\&\&i<n\}" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ee994da4-0fc7-443d-ac56-c08caf00a204.jpg" width="350px"> </div><br>

For a sequence of length N, the longest increasing subsequence does not necessarily end with S<sub>N</sub>. Therefore, dp[N] is not the length of the longest increasing subsequence of the sequence. The desired result is to traverse the dp array to find the maximum value. max{ dp[i] | 1 <= i <= N} is what is required.

### 1. Longest increasing subsequence

300\. Longest Increasing Subsequence (Medium)

[Leetcode](https://leetcode.com/problems/longest-increasing-subsequence/description/) / [Leetcode](https://leetcode-cn.com/problems/longest-increasing-subsequence/description/)

```java
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
for (int i = 0; i < n; i++) {
        int max = 1;
        for (int j = 0; j < i; j++) {
            if (nums[i] > nums[j]) {
                max = Math.max(max, dp[j] + 1);
            }
        }
        dp[i] = max;
    }
    return Arrays.stream(dp).max().orElse(0);
}
```

Using Stream to find the maximum value will cause the running time to be too long. It can be changed to the following form:

```java
int ret = 0;
for (int i = 0; i < n; i++) {
    ret = Math.max(ret, dp[i]);
}
return ret;
```

The time complexity of the above solution is O(N<sup>2</sup>). Binary search can be used to reduce the time complexity to O(NlogN).

Define a tails array, where tails[i] stores the last element of the longest increasing subsequence of length i + 1. For an element x,

- If it is greater than all the values in the tails array, then add it to the end of tails, indicating that the length of the longest increasing subsequence is increased by 1;
- If tails[i-1] \< x \<= tails[i], then update tails[i] = x.

For example, for the array [4,3,6,5], there is:

```html
tailslennum
[] 0 4
[4] 1 3
[3] 1 6
[3,6] 2 5
[3,5] 2 null
```

It can be seen that the tails array remains ordered, so a binary search can be used to find the position of S<sub>i</sub> in the tails array.

```java
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] tails = new int[n];
    int len = 0;
    for (int num : nums) {
        int index = binarySearch(tails, len, num);
        tails[index] = num;
        if (index == len) {
            len++;
        }
    }
    return len;
}

private int binarySearch(int[] tails, int len, int key) {
    int l = 0, h = len;
    while (l < h) {
        int mid = l + (h - l) / 2;
        if (tails[mid] == key) {
            return mid;
        } else if (tails[mid] > key) {
            h = mid;
        } else {
            l = mid + 1;
        }
    }
    return l;
}
```

### 2. The longest chain that can be formed by a set of integer pairs

646\. Maximum Length of Pair Chain (Medium)

[Leetcode](https://leetcode.com/problems/maximum-length-of-pair-chain/description/) / [Leetcode](https://leetcode-cn.com/problems/maximum-length-of-pair-chain/description/)

```html
Input: [[1,2], [2,3], [3,4]]
Output: 2
Explanation: The longest chain is [1,2] -> [3,4]
```

Title description: Yes
For (a, b) and (c, d), if b \< c, they can form a chain.

```java
public int findLongestChain(int[][] pairs) {
    if (pairs == null || pairs.length == 0) {
        return 0;
    }
    Arrays.sort(pairs, (a, b) -> (a[0] - b[0]));
    int n = pairs.length;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (pairs[j][1] < pairs[i][0]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
    }
    return Arrays.stream(dp).max().orElse(0);
}
```

### 3. The longest wobble subsequence

376\. Wiggle Subsequence (Medium)

[Leetcode](https://leetcode.com/proble
ms/wiggle-subsequence/description/) / [Leetcode](https://leetcode-cn.com/problems/wiggle-subsequence/description/)

```html
Input: [1,7,4,9,2,5]
Output: 6
The entire sequence is a wiggle sequence.

Input: [1,17,5,10,13,15,10,5,16,8]
Output: 7
There are several subsequences that achieve this length. One is [1,17,10,13,10,16,8].

Input: [1,2,3,4,5,6,7,8,9]
Output: 2
```

Requirement: Solve using O(N) time complexity.

```java
public int wiggleMaxLength(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }
    int up = 1, down = 1;
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] > nums[i - 1]) {
            up = down + 1;
        } else if (nums[i] < nums[i - 1]) {
            down = up + 1;
        }
    }
    return Math.max(up, down);
}
```

## Longest common subsequence

For two subsequences S1 and S2, find their longest common subsequence.

Define a two-dimensional array dp to store the length of the longest common subsequence, where dp[i][j] represents the length of the longest common subsequence of the first i characters of S1 and the first j characters of S2. Considering whether the values of S1<sub>i</sub> and S2<sub>j</sub> are equal, there are two situations:

- When S1<sub>i</sub>==S2<sub>j</sub>, then the value S1<sub>i</sub> can be added to the longest common subsequence of the first i-1 characters of S1 and the first j-1 characters of S2, and the length of the longest common subsequence is increased by 1, that is, dp[i][j] = dp[i-1][j-1] + 1.
- When S1<sub>i</sub> != S2<sub>j</sub>, the longest common subsequence at this time is the longest common subsequence of the first i-1 characters of S1 and the first j characters of S2, or the longest common subsequence of the first i characters of S1 and the first j-1 characters of S2, whichever is the largest, that is, dp[i][j] = max{ dp[i-1][j], dp[i][j-1]}.

To sum up, the state transition equation of the longest common subsequence is:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i][j]=\left\{\begin{array}{rcl}dp[i- 1][j-1]&&{S1_i==S2_j}\\max(dp[i-1][j],dp[i][j-1])&&{S1_i<>S2_j}\end{array}\right." class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ecd89a22-c075-4716-8423-e0ba89230e9a.jpg" width="450px"> </div><br>

For a sequence S<sub>1</sub> of length N and a sequence S<sub>2</sub> of length M, dp[N][M] is the length of the longest common subsequence of sequence S<sub>1</sub> and sequence S<sub>2</sub>.

Compared with the longest increasing subsequence, the longest common subsequence has the following differences:

- For two sequences, find their longest common subsequence.
- In the longest increasing subsequence, dp[i] represents the length of the longest increasing subsequence ending with S<sub>i</sub>, and the subsequence must contain S<sub>i</sub>; in the longest common subsequence, dp[i][j] represents the length of the longest common subs
equence between the first i characters in S1 and the first j characters in S2, which does not necessarily include S1<sub>i</sub> and S2<sub>j</sub>.
- When finding the final solution, dp[N][M] in the longest common subsequence is the final solution, while dp[N] in the longest increasing subsequence is not the final solution, because the longest increasing subsequence ending with S<sub>N</sub> is not necessarily the longest increasing subsequence of the entire sequence. It is necessary to traverse the dp array to find the largest one.

### 1. Longest common subsequence

1143\. Longest Common Subsequence

[Leetcode](https://leetcode.com/problems/longest-common-subsequence/) / [Leetcode](https://leetcode-cn.com/problems/longest-common-subsequence/)

```java
    public int longestCommonSubsequence(String text1,
String text2) {
        int n1 = text1.length(), n2 = text2.length();
        int[][] dp = new int[n1 + 1][n2 + 1];
        for (int i = 1; i <= n1; i++) {
            for (int j = 1; j <= n2; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[n1][n2];
    }
```

## 0-1 Backpack

There is a knapsack with a capacity of N. Use this knapsack to pack items of maximum value. These items have two attributes: volume w and value v.

Define a two-dimensional array dp to store the maximum value, where dp[i][j] represents the maximum value that can be achieved when the volume of the first i items does not exceed j. Assume that the volume of the i-th item is w and its value is v. Depending on whether the i-th item is added to the backpack, the discussion can be divided into two situations:

- The i-th item is not added to the backpack, and the maximum value of the first i items whose total volume does not exceed j is the maximum value of the first i-1 items whose total volume does not exceed j, dp[i][j] = dp[i-1][j].
- The i-th item is added to the backpack, dp[i][j] = dp[i-1][j-w] + v.

The i-th item may or may not be added, depending on which case the maximum value is greater. Therefore, the state transition equation of the 0-1 knapsack is:

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[i][j]=max(dp[i-1][j],dp[i-1][j-w]+v)" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8cb2be66-3d47-41ba-b55b-319fc68940d4.png" width="400px"> </div><br>

```java
// W is the total volume of the backpack
// N is the number of items
//The weights array stores the weight of N items
// The values array stores the value of N items
public int knapsack(int W, int N, int[] weights, int[] values) {
    int[][] dp = new int[N + 1][W + 1];
    for (int i = 1; i <= N; i++) {
        int w = weights[i - 1], v = values[i - 1];
        for (int j = 1; j <=
W; j++) {
            if (j >= w) {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i - 1][j - w] + v);
            } else {
                dp[i][j] = dp[i - 1][j];
            }
        }
    }
    return dp[N][W];
}
```

**Space Optimization**

The 0-1 backpack can be optimized during program implementation. Observing the state transition equation, we can know that the state of the first i items is only related to the state of the first i-1 items, so dp can be defined as a one-dimensional array, where dp[j] can represent either dp[i-1][j] or dp[i][j]. At this time,

<!--<div align="center"><img src="https://latex.codecogs.com/gif.latex?dp[j]=max(dp[j],dp[j-w]+v)" class="mathjax-pic"/></div> <br>-->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/9ae89f16-7905-4a6f-88a2-874b4cac91f4.jpg" width="300px"> </div><br>

Because dp[j-w] represents dp[i-1][j-w], dp[i][j-w] cannot be found first to prevent dp[i-1][j-w] from being overwritten. That is to say, dp[i][j] must be calculated first and then dp[i][j-w]. When the program is implemented, it needs to be solved in reverse order.

```java
public int knapsack(int W, int N, int[] weights, int[] values) {
    int[] dp = new int[W + 1];
    for (int i = 1; i <= N; i++) {
        int w = weights[i - 1], v = values[i - 1];
        for (int j = W; j >= 1; j--) {
            if (j >= w) {
                dp[j] = Math.max(dp[j], dp[j - w] + v);
            }
        }
    }
    return dp[W];
}
```

**Explanation that greedy algorithm cannot be used**

The 0-1 knapsack problem cannot be solved using a greedy algorithm, which means that the optimal solution cannot be achieved by adding the most cost-effective items first. This is because this method may cause a waste of backpack space and thus cannot achieve the optimal solution. Consider the following items and a backpack with a capacity of 5. If you add item 0 first and then item 1, you can only store a value of 16, wasting space of size 2. The optimal way is to store Item 1 and Item 2, with a value of 22.

| id | w | v | v/w |
| --- | --- | --- | --- |
| 0 | 1 | 6 | 6 |
| 1 | 2 | 10 | 5 |
| 2 | 3 | 12 | 4 |

**Variant**

- Complete backpack: unlimited number of items

-Multiple backpacks: the number of items is limited

- Multi-dimensional cost backpack: items not only have weight, but also volume, taking into account both limitations

- Others: items are mutually constrained or dependent on each other

### 1. Divide the array into sum
two parts of waiting

416\. Partition Equal Subset Sum (Medium)

[Leetcode](https://leetcode.com/problems/partition-equal-subset-sum/description/) / [Leetcode](https://leetcode-cn.com/problems/partition-equal-subset-sum/description/)

```html
Input: [1, 5, 11, 5]

Output: true

Explanation: The array can be partitioned as [1, 5, 5] and [11].
```

It can be viewed as a 0-1 knapsack problem with a knapsack size of sum/2.

```java
public boolean canPartition(int[] nums) {
    int s
um = computeArraySum(nums);
    if (sum % 2 != 0) {
        return false;
    }
    int W = sum / 2;
    boolean[] dp = new boolean[W + 1];
    dp[0] = true;
    for (int num : nums) { // 0-1 An item in the backpack can only be used once
        for (int i = W; i >= num; i--) { // From back to front, calculate dp[i] first and then dp[i-num]
            dp[i] = dp[i] || dp[i - num];
        }
    }
    return dp[W];
}

private int computeArraySum(int[] nums) {
    int sum = 0;
    for (int num : nums) {
        sum += num;
    }
    return sum;
}
```

### 2. Change the sign of a group of numbers so that their sum is a given number

494\. Target Sum (Medium)

[Leetcode](https://leetcode.com/problems/target-sum/description/) / [Leetcode](https://leetcode-cn.com/problems/target-sum/description/)

```html
Input: nums is [1, 1, 1, 1, 1], S is 3.
Output: 5
Explanation:

-1+1+1+1+1 = 3
+1-1+1+1+1 = 3
+1+1-1+1+1 = 3
+1+1+1-1+1 = 3
+1+1+1+1-1 = 3

There are 5 ways to assign symbols to make the sum of nums be target 3.
```

This problem can be converted into a Subset Sum problem and solved using the 0-1 knapsack method.

This set of numbers can be regarded as two parts, P and N, where P uses a positive sign and N uses a negative sign. There is the following derivation:

```html
                  sum(P) - sum(N) = target
sum(P) + sum(N) + sum(P) - sum(N) = target + sum(P) + sum(N)
                       2 * sum(P) = target + sum(nums)
```

Therefore, as long as we find a subset such that they all have positive signs and the sum is equal to (target + sum(nums))/2, we prove that a solution exists.

```java
public int findTargetSumWays(int[] nums, int S) {
    int sum = computeArraySum(nums);
    if (sum < S || (sum + S) % 2 == 1) {
        return 0;
    }
    int W = (sum + S) / 2;
    int[] dp = new int[W + 1];
    dp[0] = 1;
    for (int num : nums) {
        for (int i = W; i >= num; i--) {
            dp[i] = dp[i] + dp[i - num];
        }
    }
    return dp[W];
}

private int computeArraySum(int[] nums) {
    int sum = 0;
    for (int num : nums) {
        sum += num;
    }
    return sum;
}
```

DFS solution:

```java
public int findTargetSumWays(int[] nums, int S) {
    return findTargetSumWays(nums, 0, S);
}

private int findTargetSumWays(int[] nums, int start, int S) {
    if (start == nums.length) {
        return S == 0 ? 1 : 0;
    }
    return findTargetSumWays(nums, start + 1, S + nums[start])
            + findTargetSumWays(nums, start + 1, S - nums[start]);
}
```

### 3. 01 characters form the most string

474\. Ones and Zeroes (Medium)

[Leetcode](https://leetcode.com/problems/ones-and-zeroes/description/) / [Leetcode](https://leetcode-cn.com/problems/ones-and-zeroes/description/)

```html
Input: Array = {"10", "0001", "111001", "1", "0"}, m = 5, n = 3
Output: 4

Explanation: There are totally 4 strings can be formed by the using of 5 0s and 3 1s, which are "10","0001","1","0"
```

This is a multidimensional cost 0-1 knapsack problem with two
knapsack sizes, the number of 0s and the number of 1s.

```java
p
ublic int findMaxForm(String[] strs, int m, int n) {
    if (strs == null || strs.length == 0) {
        return 0;
    }
    int[][] dp = new int[m + 1][n + 1];
    for (String s : strs) { // Each string can only be used once
        int ones = 0, zeros = 0;
        for (char c : s.toCharArray()) {
            if (c == '0') {
                zeros++;
            } else {
                ones++;
            }
        }
        for (int i = m; i >= zeros; i--) {
            for (int j = n; j >= ones; j--) {
                dp[i][j] = Math.max(dp[i][j], dp[i - zeros][j - ones] + 1);
            }
        }
    }
    return dp[m][n];
}
```

### 4. Minimum number of coins required for change

322\. Coin Change (Medium)

[Leetcode](https://leetcode.com/problems/coin-change/description/) / [Leetcode](https://leetcode-cn.com/problems/coin-change/description/)

```html
Example 1:
coins = [1, 2, 5], amount = 11
return 3 (11 = 5 + 5 + 1)

Example 2:
coins = [2], amount = 3
return -1.
```

Description of the problem: Given some coins of denominations, it is required to use these coins to form the amount of money of a given denomination in such a way that the number of coins is minimized. Coins can be reused.

- Item: Coin
- Item size: denomination
- Item value: quantity

Because coins can be reused, this is a complete knapsack problem. The complete knapsack only requires changing the reverse order traversal of the dp array of the 0-1 knapsack into a forward order traversal.

```java
public int coinChange(int[] coins, int amount) {
    if (amount == 0 || coins == null) return 0;
    int[] dp = new int[amount + 1];
    for (int coin : coins) {
        for (int i = coin; i <= amount; i++) { //Change reverse order traversal to forward order traversal
            if (i == coin) {
                dp[i] = 1;
            } else if (dp[i] == 0 && dp[i - coin] != 0) {
                dp[i] = dp[i - coin] + 1;

            } else if (dp[i - coin] != 0) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    return dp[amount] == 0 ? -1 : dp[amount];
}
```

### 5. Coin number combination for change

518\. Coin Change 2 (Medium)

[Leetcode](https://leetcode.com/problems/coin-change-2/description/) / [Leetcode](https://leetcode-cn.com/problems/coin-change-2/description/)

```text-html-basic
Input: amount = 5, coins = [1, 2, 5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1
```

Complete knapsack problem, use dp to record the number of combinations that can achieve the goal.

```java
public int change(int amount, int[] coins) {
    if (coins == null) {
        return 0;
    }
    int[] dp = new int[amount + 1];
    dp[0] = 1;
    for (int coin : coins) {
        for (int i = coin; i <= amount; i++) {
            dp[i] += dp[i - coin];
        }
    }
    return dp[amount];
}
```

### 6. Split the string by word list
139\. Word Break (Medium)

[Leetcode](https://leetcode.com/problems/word-break/description/) / [Leetcode](https://leetcode-cn.com/problems/word-break/description/)

```html
s = "leetcode",
dict = ["leet", "code"].
Return true because "leetcode" can be segmented as "leet code".
```

There is no limit to the number of times a word in dict can be used, so this is a complete knapsack problem.

This problem involves the order of use of words in the dictionary, which means that items must be put into the backpack in a certain order. For example, the following dict is not enough to form the string "leetcode":

```html
["lee", "tc", "cod"]
```

When solving the sequential complete knapsack problem, the iteration of items should be placed in the innermost layer, and the iteration of the backpack should be placed in the outer layer. Only in this way can items be put into the backpack in a certain order.

```java
public boolean wordBreak(String s, List<String> wordDict) {
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;
    for (int i = 1; i
<= n; i++) {
        for (String word : wordDict) { // Iteration of items should be placed at the innermost level
            int len = word.length();
            if (len <= i && word.equals(s.substring(i - len, i))) {
                dp[i] = dp[i] || dp[i - len];
            }
        }
    }
    return dp[n];
}
```

### 7. Combination sum

377\. Combination Sum IV (Medium)

[Leetcode](https://leetcode.com/problems/combination-sum-iv/description/) / [Leetcode](https://leetcode-cn.com/problems/combination-sum-iv/description/)

```html
nums = [1, 2, 3]
target=4

The possible combination ways are:
(1, 1, 1, 1)
(1, 1, 2)
(1, 2, 1)
(1, 3)
(2, 1, 1)
(2, 2)
(3, 1)

Note that different sequences are counted as different combinations.

Therefore the output is 7.
```

Complete backpack involving sequence.

```java
public int combinationSum4(int[] nums, int target) {
    if (nums == null || nums.length == 0) {
        return 0;
    }
    int[] maximum = new int[target + 1];
    maximum[0] = 1;
    Arrays.sort(nums);
    for (int i = 1; i <= target; i++) {
        for (int j = 0; j < nums.length && nums[j] <= i; j++) {
            maximum[i] += maximum[i - nums[j]];
        }
    }
    return maximum[target];
}
```

## Stock Trading

### 1. Stock transactions requiring a cooling-off period

309\. Best Time to Buy and Sell Stock with Cooldown(Medium)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/) / [Leetcode](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/)

Title description: There is a one-day cooling-off period after the transaction.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ffd96b99-8009-487c-8e98-11c9d44ef14f.png" width="300px"> </div><br>

```java
public int maxProfit(int[] prices) {
    if (prices == null || prices.length == 0) {
        return 0;
}
    int N = prices.length;
    int[] buy = new int[N];
    int[] s1 = new int[N];
    int[] sell = new int[N];
    int[] s2 = new int[N];
    s1[0] = buy[0] = -prices[0];
    sell[0] = s2[0] = 0;
    for (int i = 1; i < N; i++) {
        buy[i] = s2[i - 1] - prices[i];
        s1[i] = Math.max(buy[i - 1], s1[i - 1]);
        sell[i] = Math.max(buy[i - 1], s1[i - 1]) + prices[i];
        s2[i] = Math.max(s2[i - 1], sell[i - 1]);
    }
    return Math.max(sell[N - 1], s2[N - 1]);
}
```

### 2. Stock transactions requiring transaction fees

714\. Best Time to Buy and Sell Stock with Transaction Fee (Medium)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/description/) / [Leetcode](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/description/)

```html
Input: prices = [1, 3, 2, 8, 4, 9], fee = 2
Output: 8
Explanation: The maximum profit can be achieved by:
Buying at prices[0] = 1
Selling at prices[3] = 8
Buying at prices[4] = 4
Selling at prices[5] = 9
The total profit is ((8 - 1) - 2) + ((9 - 4) - 2) = 8.
```

Title description: Every time you make a transaction, you have to pay a certain fee.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1e2c588c-72b7-445e-aacb-d55dc8a88c29.png" width="300px"> </div><br>

```java
public int maxPr
ofit(int[] prices, int fee) {
    int N = prices.length;
    int[] buy = new int[N];
    int[] s1 = new int[N];
    int[] sell = new int[N];
    int[] s2 = new int[N];
    s1[0] = buy[0] = -prices[0];
    sell[0] = s2[0] = 0;
    for (int i = 1; i < N; i++) {
        buy[i] = Math.max(sell[i - 1], s2[i - 1]) - prices[i];
        s1[i] = Math.max(buy[i - 1], s1[i - 1]);
        sell[i] = Math.max(buy[i - 1], s1[i - 1]) - fee + prices[i];
        s2[i] = Math.max(s2[i - 1], sell[i - 1]);
    }
    return Math.max(sell[N - 1], s2[N - 1]);
}
```


### 3. 只能进行两次的股票交易

123\. Best Time to Buy and Sell Stock III (Hard)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/description/) / [力扣](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iii/description/)

```java
public int maxProfit(int[] prices) {
    int firstBuy = Integer.MIN_VALUE, firstSell = 0;
    int secondBuy = Integer.MIN_VALUE, secondSell = 0;
    for (int curPrice : prices) {
        if (firstBuy < -curPrice) {
            firstBuy = -curPrice;
        }
        if (firstSell < firstBuy + curPrice) {
            firstSell = firstBuy + curPrice;
        }
        if (secondBuy < firstSell - curPrice) {
            secondBuy = firstSell - curPrice;
        }
        if (secondSell < secondBuy + curPrice) {
            secondSell = secondBuy + curPrice;
        }
    }
    return secondSell;
}
```

### 4. 只能进行 k 次的股票交易

188\. Best Time to Buy and Sell Stock IV (Hard)

[Leetcode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/description/) / [力扣](https://leetcode-cn.com/problems/b
est-time-to-buy-and-sell-stock-iv/description/)

```java
public int maxProfit(int k, int[] prices) {
    int n = prices.length;
    if (k >= n / 2) { // In this case, the problem degenerates into an ordinary stock trading problem
        int maxProfit = 0;
        for (int i = 1; i < n; i++) {
            if (prices[i] > prices[i - 1]) {
                maxProfit += prices[i] - prices[i - 1];
            }
        }
        return maxProfit;
    }
    int[][] maxProfit = new int[k + 1][n];
    for (int i = 1; i <= k; i++) {
        int localMax = maxProfit[i - 1][0] - prices[0];
        for (int j = 1; j < n; j++) {
            maxProfit[i][j] = Math.max(maxProfit[i][j - 1], prices[j] + localMax);
            localMax = Math.max(localMax, maxProfit[i - 1][j] - prices[j]);
        }
    }
    return maxProfit[k][n - 1];
}
```

## String editing

### 1. Delete characters from two strings to make them equal

583\. Delete Operation for Two Strings (Medium)

[Leetcode](https://leetcode.com/problems/delete-operation-for-two-strings/description/) / [Leetcode](https://leetcode-cn.com/problems/delete-operation-for-two-strings/description/)

```html
Input: "sea", "eat"
Output: 2
Explanation: You need one step to make "sea" to "ea" and another step to make "eat" to "ea".
```

It can be converted into the problem of finding the longest common subsequence of two strings.

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i
++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i][j - 1], dp[i - 1][j]);
            }
        }
    }
    return m + n - 2 * dp[m][n];
}
```

### 2. Edit distance

72\. Edit Distance (Hard)

[Leetcode](https://leetcode.com/problems/edit-distance/description/) / [Leetcode](https://leetcode-cn.com/problems/edit-distance/description/)

```html
Example 1:

Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')
Example 2:

Input: word1 = "intention", word2 = "execution"
Output: 5
Explanation:
intention -> intention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
extension -> execution (replace 'n' with 'c')
execution -> execution (insert 'u')
```

Title description: Modify a string into another string so that the number of modifications is minimized. A modification operation includes: inserting a character, deleting a character, and replacing a character.

```java
public int minDistance(String word1, String word2) {
    if (word1 == null || word2 == null) {
        return 0;
    }
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++) {
        dp[i][0] = i;
    }
    for (int i = 1; i <= n; i++) {
        dp[0][i] = i;
    }
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word
1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = Math.min(dp[i - 1][j - 1], Math.min(dp[i][j - 1], dp[i - 1][j])) + 1;
            }
        }
    }
    return dp[m][n];
}
```

### 3. Copy and paste characters

650\. 2 Keys Keyboard (Medium)

[Leetcode](https://leetcode.com/problems/2-keys-keyboard/description/) / [Leetcode](https://leetcode-cn.com/problems/2-keys-keyboard/description/)

Question description: There is only one character A at the beginning. How many operations are needed to get n characters A. Each operation can copy or paste all the current characters.

```
Input: 3
Output: 3
Explanation:
Initially, we have one character 'A'.
In step 1, we use Copy All operation.
In step 2, we use Paste operation to get 'AA'.
In step 3, we use Paste operation to get 'AAA'.
```

```java
public int minSteps(int n) {
    if (n == 1) return 0;
    for (int i = 2; i <= Math.sqrt(n); i++) {
        if (n % i == 0) return i + minSteps(n / i);
    }
    return n;
}
```

```java
public int minSteps(int n) {
    int[] dp = new int[n + 1];
    int h = (int) Math.sqrt(n);
    for (int i = 2; i <= n; i++) {
        dp[i] = i;
        for (int j = 2; j <= h; j++) {
            if (i % j == 0) {
                dp[i] = dp[j] + dp[i/j];
                break;
            }
        }
    }
    return dp[n];
}
```
