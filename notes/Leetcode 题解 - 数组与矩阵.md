# Leetcode problem solutions - arrays and matrices
<!-- GFM-TOC -->
* [Leetcode problem solution - arrays and matrices](#leetcode-problem solution---arrays and matrices)
    * [1. Move 0 in the array to the end] (#1-Move -0- in the array to the end)
    * [2. Change matrix dimensions](#2-Change matrix dimensions)
    * [3. Find the longest consecutive 1 in the array](#3-Find the longest consecutive 1 in the array)
    * [4. Ordered Matrix Search](#4-Ordered Matrix Search)
    * [5. Kth Element of ordered matrix](#5-kth-element of ordered matrix)
    * [6. An array element is between [1, n], one number is replaced with another number, find the duplicate numbers and missing numbers] (#6-An array element is between -[1-n]-, one number is replaced with another number, find the duplicate numbers and missing numbers)
    * [7. Find the repeated numbers in the array, the array value is between [1, n]] (#7-Find the repeated numbers in the array, the array value is between -[1-n]-)
    * [8. The number of adjacent differences in the array] (#8-The number of adjacent differences in the array)
    * [9. Degree of array](#9-Degree of array)
    * [10. Matrix with equal diagonal elements] (#10-Matrix with equal diagonal elements)
    * [11. Nested array](#11-Nested array)
    * [12. Separated array](#12-Separated array)
<!-- GFM-TOC -->


## 1. Move 0 in the array to the end

283\. Move Zeroes (Easy)

[Leetcode](https://leetcode.com/problems/move-zeroes/description/) / [Leetcode](https://leetcode-cn.com/problems/move-zeroes/description/)

```html
For example, given nums = [0, 1, 0, 3, 12], after calling your function, nums should be [1, 3, 12, 0, 0].
```

```java
public void moveZeroes(int[] nums) {
    int idx = 0;
    for (int num : nums) {
        if (num != 0) {
            nums[idx++] = num;
        }
    }
    while (idx < nums.length) {
        nums[idx++] = 0;
    }
}
```

## 2. Change matrix dimensions

566\. Reshape the Matrix (Easy)

[Leetcode](https://leetcode.com/problems/reshape-the-matrix/description/) / [Leetcode](https://leetcode-cn.com/problems/reshape-the-matrix/description/)

```html
Input:
nums =
[[1,2],
 [3,4]]
r = 1, c = 4

Output:
[[1,2,3,4]]

Explanation:
The row-traversing of nums is [1,2,3,4]. The new reshaped matrix is a 1 * 4 matrix, fill it row by row by using the previous list.
```

```java
public int[][] matrixReshape(int[][] nums, int r, int c) {
    int m = nums.length, n = nums[0].length;
    if (m * n != r * c) {
        return nums;
    }
    int[][] reshapedNums = new int[r][c];
    int index = 0;
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            reshapedNums[i][j] = nums[index / n][index % n];
            index++;
        }
    }
    return reshapedNums;
}
```

## 3. Find the longest consecutive 1 in the array

485\. Max Consecutive Ones (Easy)

[Leetcode](https://leetcode.com/problems/max-consecutive-ones/description/) / [Leetcode](https://leetcode-cn.com/problems/max-consecutive-ones/d
escription/)

```java
public int findMaxConsecutiveOnes(int[] nums) {
    int max = 0, cur = 0;
    for (int x : nums) {
        cur = x == 0 ? 0 : cur + 1;
        max = Math.max(max, cur);
    }
    return max;
}
```

## 4. Ordered matrix search

240\. Search a 2D Matrix II (Medium)

[Leetcode](https://leetcode.com/problems/search-a-2d-matrix-ii/description/) / [Leetcode](https://leetcode-cn.com/problems/search-a-2d-matrix-ii/description/)

```html
[
   [1, 5, 9],
   [10, 11, 13],
   [12, 13, 15]
]
```

```java
public boolean searchMatrix(int[][] matrix, int target) {
    if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return false;
    int m = matrix.length, n = matrix[0].length;
    int row = 0, col = n - 1;
    while (row < m && col >= 0) {
        if (target == matrix[row][col]) return true;
        els
e if (target < matrix[row][col]) col--;
        else row++;
    }
    return false;
}
```

## 5. 有序矩阵的 Kth Element

378\. Kth Smallest Element in a Sorted Matrix ((Medium))

[Leetcode](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/) / [力扣](https://leetcode-cn.com/problems/kth-smallest-element-in-a-sorted-matrix/description/)

```html
matrix = [
  [ 1,  5,  9],
  [10, 11, 13],
  [12, 13, 15]
],
k = 8,

return 13.
```

解题参考：[Share my thoughts and Clean Java Code](https://leetcode-cn.com/problems/kth-smallest-element-in-a-sorted-matrix/discuss/85173)

二分查找解法：

```java
public int kthSmallest(int[][] matrix, int k) {
    int m = matrix.length, n = matrix[0].length;
    int lo = matrix[0][0], hi = matrix[m - 1][n - 1];
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int cnt = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n && matrix[i][j] <= mid; j++) {
                cnt++;
            }
        }
        if (cnt < k) lo = mid + 1;
        else hi = mid - 1;
    }
    return lo;
}
```

堆解法：

```java
public int kthSmallest(int[][] matrix, int k) {
    int m = matrix.length, n = matrix[0].length;
    PriorityQueue<Tuple> pq = new PriorityQueue<Tuple>();
    for(int j = 0; j < n; j++) pq.offer(new Tuple(0, j, matrix[0][j]));
    for(int i = 0; i < k - 1; i++) { // 小根堆，去掉 k - 1 个堆顶元素，此时堆顶元素就是第 k 的数
        Tuple t = pq.poll();
        if(t.x == m - 1) continue;
        pq.offer(new Tuple(t.x + 1, t.y, matrix[t.x + 1][t.y]));
    }
    return pq.poll().val;
}

class Tuple implements Comparable<Tuple> {
    int x, y, val;
    public Tuple(int x, int y, int val) {
        this.x = x; this.y = y; this.val = val;
    }

    @Override
    public int compareTo(Tuple that) {
        return this.val - that.val;
    }
}
```

## 6. 一个数组元素在 [1, n] 之间，其中一个数被替换为另一个数，找出重复的数和丢失的数

645\. Set Mismatch (Easy)

[Leetcode](https://leetcode.com/problems/set-mismatch/description/) / [力扣](https://leetcode-cn.com/problems/set-mismatch/description/)

```html
Input: nums = [1,2,2,4]
Output: [2,3]
```

```html
Input: nums = [1,2,2,4]
Output: [2,3]
```

最直接的方法是先对数组进行排序，这种方法时间复
The complexity is O(NlogN). This problem can be solved with O(N) time complexity and O(1) space complexity.

The main idea is to swap the array elements so that the elements on the array are in the correct position.

```java
public int[] findErrorNums(int[] nums) {
    for (int i = 0; i < nums.length; i++) {
        while (nums[i] != i + 1 && nums[nums[i] - 1] != nums[i]) {
            swap(nums, i, nums[i] - 1);
        }
    }
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] != i + 1) {
            return new int[]{nums[i], i + 1};
        }
    }
    return null;
}

private void swap(int[] nums, int i, int j) {
    int tmp = nums[i];
    nums[i] = nums[j];
    nums[j] = tmp;
}
```

## 7. Find the repeated numbers in the array, the array value is between [1, n]

287\. Find the Duplicate Number (Medium)

[Leetcode](https://leetcode.com/problems/find-the-duplicate-number/description/) / [Leetcode](https://leetcode-cn.com/problems/find-the-duplicate-number/description/)

It is required that the array cannot be modified and additional space cannot be used.

Binary search solution:

``
`java
public int findDuplicate(int[] nums) {
     int l = 1 , h = nums . length -- 1 ;
     while ( l <= h ) {
         int mid = l+(h-l)/2;
         int cnt = 0;
         for ( int i = 0 ; i < nums . length ; i ++ ) {
             if ( nums [ i ] <= mid ) cnt ++ ;
         } }
         if ( cnt > mid ) h = mid -- 1 ;
         else l = mid + 1;
     } }
     return l;
} }
```

If you want to build, you can have a snowball fight:

```java
public int findDuplicate(int[] nums) {
    int slow = nums[0], fast = nums[nums[0]];
    while ( slow ! = fast ) {
        slow = nums [ slow ] ;
        fast = nums[nums[fast]];
    } }
    fast = 0;
    while ( slow ! = fast ) {
        slow = nums [ slow ] ;
        fast = nums[fast];
    } }
    return slow ;
} }
```

## 8. Remove snowflakes

667\.Beautiful Arrangement II (Medium)

[Leetcode](https://leetcode.com/problems/beautiful-arrangement-ii/description/) / [January](https://leetcode-cn.com/problems/beautiful-arrangement-ii/description/)

```html
Input: n = 3, k =
Output: [1, 3, 2]
Explanation: The [1, 3, 2] has three different positive integers ranging from 1 to 3, and the [2, 1] has exactly 2 distinct integers: 1 and
```

snowflake: snowflake 1\~n Finally, take a look at the bedroom, a snowflake snowflake and a snowflake for a k.

Give k+1 a fraction of k a fraction of a fraction:1 k+1 2 k 3 k-1 ... k/2 k/2+1.

```java
public int [ ] constructArray ( int n , int k ) {
    int[] ret = new int[n];
    ret [ 0 ] = 1 ;
    for (int i = 1, interval = k; i <= k; i++, interval--) {
        ret [ i ] = i % 2 == 1 ? ret[i - 1] + interval : ret[i - 1] - interval;
    } }
    for ( int i = k + 1 ; i < n ; i ++ ) {
        ret [ i ] = i + 1 ;
    } }
    return ret;
} }
```

## 9. Configuration

697\. Degree of an Array (Easy)

[Leetcode](https://leetcode.com/problems/degree-of-an-array/description/) / [January](https://leetcode-cn.com/problems/degree-of-an-array/description/)

```html
Input: [1,2,2,3,1,4,2]
Output: 6
```

Small-scale firefighting: a snowflake based on a snowflake, a snowflake 3. Make sure you have a snowflake, build a snowflake and a snowflake.

```java
public int findSh
ortestSubArray(int[] nums) {
    Map<Integer, Integer> numsCnt = new HashMap<>();
    Map<Integer, Integer> numsLastIndex = new HashMap<>();
    Map<Integer, Integer> numsFirstIndex = new HashMap<>();
    for ( int i = 0 ; i < nums . length ; i ++ ) {
        int num = nums [ i ] ;
        numsCnt.put(num, numsCnt.getOrDefault(num, 0) + 1);
        numsLastIndex.put(num, i);
        if (!numsFirstIndex.containsKey(num)) {
            numsFirstIndex.put(num, i);
        } }
    } }
    int maxCnt = 0;
    for ( int num : nums ) {
        maxCnt = Math . max ( maxCnt , numsCnt . get ( num ) ) ;
    } }
    int ret = nums.length;
    for ( int i = 0 ; i < nums . length ; i ++ ) {
        int num = nums [ i ] ;
        int cnt = numsCnt . get ( num ) ;
        if ( cnt ! = maxCnt ) continue ;
        right = Math.min(right, numsLastIndex.get(num) - numsFirstIndex.get(num) + 1);
    } }
    return ret ;
} }
```

## 10. Configure the smoothness of the snowflake

766\. Toeplitz Matrix (Easy)

[Leetcode](https://leetcode.com/problems/toeplitz-matrix/description/)

```html
1234
5123
9512

In the above grid, the diagonals are "[9]", "[5, 5]", "[1,
1, 1]", "[2, 2, 2]", "[3, 3]", "[4]", and in each diagonal all elements are the same, so the answer is True.
```

```java
public boolean isToeplitzMatrix(int[][] matrix) {
    for (int i = 0; i < matrix[0].length; i++) {
        if (!check(matrix, matrix[0][i], 0, i)) {
            return false;
        }
    }
    for (int i = 0; i < matrix.length; i++) {
        if (!check(matrix, matrix[i][0], i, 0)) {
            return false;
        }
    }
    return true;
}

private boolean check(int[][] matrix, int expectValue, int row, int col) {
    if (row >= matrix.length || col >= matrix[0].length) {
        return true;
    }
    if (matrix[row][col] != expectValue) {
        return false;
    }
    return check(matrix, expectValue, row + 1, col + 1);
}
```

## 11. 嵌套数组

565\. Array Nesting (Medium)

[Leetcode](https://leetcode.com/problems/array-nesting/description/) / [力扣](https://leetcode-cn.com/problems/array-nesting/description/)

```html
Input: A = [5,4,0,3,1,6,2]
Output: 4
Explanation:
A[0] = 5, A[1] = 4, A[2] = 0, A[3] = 3, A[4] = 1, A[5] = 6, A[6] = 2.

One of the longest S[K]:
S[0] = {A[0], A[5], A[6], A[2]} = {5, 6, 2, 0}
```

题目描述：S[i] 表示一个集合，集合的第一个元素是 A[i]，第二个元素是 A[A[i]]，如此嵌套下去。求最大的 S[i]。

```java
public int arrayNesting(int[] nums) {
    int max = 0;
    for (int i = 0; i < nums.length; i++) {
        int cnt = 0;
        for (int j = i; nums[j] != -1; ) {
            cnt++;
            int t = nums[j];
            nums[j] = -1; // 标记该位置已经被访问
            j = t;

        }
        max = Math.max(max, cnt);
    }
    return max;
}
```

## 12. 分隔数组

769\. Max Chunks To Make Sorted (Medium)

[Leetcode](https://leetcode.com/problems/max-chunks-to-make-sorted/description/) / [力扣](https://leetcode-cn.com/problems/max-chunks-to-make-sorted/description/)

```html
Input: arr = [1,0,2,3,4]
Output: 4
Explanation:
We can split into two chunks, such as [1, 0], [2, 3, 4].
However, splitting into [1, 0], [2], [3], [4] is the highest number of chunks possible.
```

Title description: Separate an array so that the array is ordered after each part is sorted.

```java
public int maxChunksToSorted(int[] arr) {
    if (arr == null) return 0;
    int ret = 0;
    int right = arr[0];
    for (int i = 0; i < arr.length; i++) {
        right = Math.max(right, arr[i]);
        if (right == i) ret++;
    }
    return ret;
}
```
