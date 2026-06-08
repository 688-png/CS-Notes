# Leetcode Problem Solutions - Mathematics
<!-- GFM-TOC -->
* [Leetcode Problem Solution - Mathematics](#leetcode-Problem Solution---Mathematics)
    * [Prime number decomposition](#prime number decomposition)
    * [divisible](#divisible)
    * [Greatest common divisor least common multiple](#greatest common divisor least common multiple)
        * [1. Generate prime number sequence](#1-Generate prime number sequence)
        * [2. Greatest common divisor](#2-Greatest common divisor)
        * [3. Use bitwise operations and subtraction to find the greatest common divisor] (#3-Use bitwise operations and subtraction to find the greatest common divisor)
    * [Hex conversion](#Hex conversion)
        * [1. 7-base](#1-7-base)
        * [2.16-base](#2-16-base)
        * [3. 26-base](#3-26-base)
    * [factorial](#factorial)
        * [1. Count the number of 0s in the tail of the factorial] (#1-Count the number of 0s in the tail of the factorial)
    * [String addition and subtraction](#String addition and subtraction)
        * [1. Binary addition](#1-Binary addition)
        * [2. String addition](#2-String addition)
    * [EncounterProblem](#EncounterProblem)
        * [1. Change array elements to make all array elements equal] (#1-Change array elements to make all array elements equal)
    *[majority voting question](#majority voting question)
        * [1. Elements that appear more than n / 2 in the array] (#1-elements that appear more than -n--2- in the array)
    * [Other](#OTHER)
        * [1. Square number](#1-square number)
        * [2. 3 to the nth power] (#2-3- to the n-th power)
        * [3. Product array](#3-Product array)
        * [4. Find the three numbers with the largest product in the array] (#4-Find the three numbers with the largest product in the array)
<!-- GFM-TOC -->


## Prime number decomposition

Every number can be decomposed into the product of prime numbers, for example 84 = 2<sup>2</sup> \* 3<sup>1</sup> \* 5<sup>0</sup> \* 7<sup>1</sup> \* 11<sup>0</sup> \* 13<sup>0</sup> \* 17<sup>0</sup> \* …

## Divisible

Let x = 2<sup>m0</sup> \* 3<sup>m1</sup> \* 5<sup>m2</sup> \* 7<sup>m3</sup> \* 11<sup>m4</sup> \* …

Let y = 2<sup>n0</sup> \* 3<sup>n1</sup> \* 5<sup>n2</sup> \* 7<sup>n3</sup> \* 11<sup>n4</sup> \* …

If x divides y (y mod x == 0), then mi \<= ni for all i.

## Greatest common divisor least common multiple

The greatest common divisor of x and y is: gcd(x,y) = 2<sup>min(m0,n0)</sup> \* 3<sup>min(m1,n1)</sup> \* 5<sup>min(m2,n2)</sup> \* ...

The least common multiple of x and y is: lcm(x,y) = 2<sup>max(m0,n0)</sup> \* 3<sup>max(m1,n1)</sup> \* 5<sup>max(m2,n2)</sup> \* ...

### 1. Generate a sequence of prime numbers

204\. Count Primes (Easy)

[Leetcode](https://leetcode.com/problems/count-primes/description/) / [Leetcode](https://leetcode-cn.com/problems/count-primes/description/)

The Sieve of Eratosthenes eliminates numbers that are divisible by a prime number every time it finds one.

```java
public int
countPrimes(int n) {
    boolean[] notPrimes = new boolean[n + 1];
    int count = 0;
    for (int i = 2; i < n; i++) {
        if (notPrimes[i]) {
            continue;
        }
        count++;
        // Start with i * i, because if k < i, then k * i has been removed before
        for (long j = (long) (i) * i; j < n; j += i) {
            notPrimes[(int) j] = true;
        }
    }
    return count;
}
```

### 2. Greatest common divisor

```java
int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}
```

The least common multiple is the product of two numbers divided by their greatest common divisor.

```java
int lcm(int a, int b) {
    return a * b / gcd(a, b);
}
```

### 3. Use bit operations and subtraction to find the greatest common divisor

[The beauty of programming: 2.7](#)

For the greatest common divisor f(a, b) of a and b, we have:

- If a and b are both even numbers, f(a, b) = 2\*f(a/2, b/2);
- If a is even and b is odd, f(a, b) = f(a/2, b);
- If b is even and a is odd, f(a, b) = f(a, b/2);
- If a and b are both odd, f(a, b) = f(b, a-b);

Both multiplication by 2 and division by 2 can be converted into shift operations.

```java
public int gcd(int a, int b) {
    if (a < b) {
        return gcd(b, a);
    }
    if (b == 0) {
        return a;
    }
    boolean isAEven = isEven(a), isBEven = isEven(b);
    if (isAEven && isBEven) {
        return 2 * gcd(a >> 1, b >> 1);
    } else if (isAEven && !isBEven) {
        return gcd(a >> 1, b);
    } else if (!isAEven && isBEven) {
        return gcd(a, b >> 1);
    } else {
        return gcd(b, a - b);
    }
}
```

## Base conversion

###
1. 7 base

504\. Base 7 (Easy)

[Leetcode](https://leetcode.com/problems/base-7/description/) / [Leetcode](https://leetcode-cn.com/problems/base-7/description/)

```java
public String convertToBase7(int num) {
    if (num == 0) {
        return "0";
    }
    StringBuilder sb = new StringBuilder();
    boolean isNegative = num < 0;
    if (isNegative) {
        num = -num;
    }
    while (num > 0) {
        sb.append(num % 7);
        num /= 7;
    }
    String ret = sb.reverse().toString();
    return isNegative ? "-" + ret : ret;
}
```

In Java, static String toString(int num, int radix) can convert an integer into a string represented by radix.

```java
public String convertToBase7(int num) {
    return Integer.toString(num, 7);
}
```

### 2. Hexadecimal

405\. Convert a Number to Hexadecimal (Easy)

[Leetcode](https://leetcode.com/problems/convert-a-number-to-hexadecimal/description/) / [Leetcode](https://leetcode-cn.com/problems/convert-a-number-to-hexadecimal/description/)

```html
Input:
26

Output:
"1a"

Input:
-1

Output:
"ffffffff"
```

Negative numbers use their complement form.

```java
public String toHex(int num) {
    char[] map = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
    if (num == 0) return "0";
    StringBuilder sb = new StringBuilder();
    while (num != 0) {
        sb.append(
map[num & 0b1111]);
        num >>>= 4; // Because the two's complement form is considered, the sign bit cannot have a special meaning. You need to use unsigned right shift and fill in 0 on the left
    }
    return sb.reverse().toString();
}
```

### 3. Hexadecimal

168\. Excel Sheet Column Title (Easy)

[Leetcode](https://leetcode.com/problems/excel-sheet-column-title/description/) / [Leetcode](https://leetcode-cn.com/problems/excel-sheet-column-title/description/)

```html
1->A
2->B
3->C
...
26->Z
27->AA
28 -> AB
```

Because the calculation starts at 1, not 0, you need to perform a -1 operation on n.

```java
public String convertToTitle(int n) {
    if (n == 0) {
        return "";
    }
    n--;
    return convertToTitle(n / 26) + (char) (n % 26 + 'A');
}
```

## Factorial

### 1. Count how many 0’s there are in the tail of the factorial

172\. Factorial Trailing Zeroes (Easy)

[Leetcode](https://leetcode.com/problems/factorial-trailing-zeroes/description/) / [Leetcode](https://leetcode-cn.com/problems/factorial-trailing-zeroes/description/)

The 0 at the end is derived from 2 * 5. The number of 2 is obviously more than the number of 5, so just count how many 5 there are.

For a number N, the number of 5s it contains is: N/5 + N/5<sup>2</sup> + N/5<sup>3</sup> + ..., where N/5 means that multiples of 5 in numbers not greater than N contribute one 5, and N/5<sup>2</sup> means that multiples of 5<sup>2</sup> in numbers not greater than N contribute another 5....

```java
public int trailingZeroes(int n) {
    return n == 0 ? 0 : n / 5 + trailingZeroes(n / 5);
}
```

If you count the position of the lowest 1 in the binary representation of N!, you only need to count how many 2s there are. This question comes from [The Beauty of Programming: 2.2](#). Just like solving how many 5's there are, the number of 2's is N/2 + N/2<sup>2</sup> + N/2<sup>3</sup> + ...

## String addition and subtraction

### 1. Binary addition

67\. Add Binary (Easy)

[Leetcode](https://leetcode.com/problems/add-binary/description/) / [Leetcode](https://leetcode-cn.com/problems/add-binary/description/)

```html
a = "11"
b = "1"
Return "100".
```

```java
public String addBinary(String a, String b) {
    int i = a.length() - 1, j = b.length() - 1, carry = 0;
    StringBuilder str = new StringBuilder();
    while (carry == 1 || i >= 0 || j >= 0) {
if (i >= 0 && a.charAt(i--) == '1') {
            carry++;
        }
        if (j >= 0 && b.charAt(j--) == '1') {
            carry++;
        }
        str.append(carry % 2);
        carry /= 2;
    }
    return str.reverse().toString();
}
```

### 2. String addition

415\. Add Strings (Easy)

[Leetcode](https://leetcode.com/problems/add-strings/description/) / [Leetcode](https://leetcode-cn.com/problems/add-strings/description/)

The value of a string is a non-negative integer.

```java
public String addStrings(String num1, String num2) {
    StringBuilder str = new StringBuilder();
    int carry = 0, i = num1.length() - 1, j =
num2.length() - 1;
    while (carry == 1 || i >= 0 || j >= 0) {
        int x = i < 0 ? 0 : num1.charAt(i--) - '0';
        int y = j < 0 ? 0 : num2.charAt(j--) - '0';
        str.append((x + y + carry) % 10);
        carry = (x + y + carry) / 10;
    }
    return str.reverse().toString();
}
```

## Encounter problem

### 1. Change the array elements to make all array elements equal

462\. Minimum Moves to Equal Array Elements II (Medium)

[Leetcode](https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii/description/) / [Leetcode](https://leetcode-cn.com/problems/minimum-moves-to-equal-array-elements-ii/description/)

```html
Input:
[1,2,3]

Output:
2

Explanation:
Only two moves are needed (remember each move increments or decrements one element):

[1,2,3] => [2,2,3] => [2,2,2]
```

Each time you can add one or subtract one to an array element, find the minimum number of changes.

This is a typical encounter problem. The way to move the smallest distance is to move all elements to the median. The reasons are as follows:

Let m be the median. a and b are two elements on either side of m, and b \> a. To make a and b equal, they need to move a total of times b - a, which is equal to (b - m) + (m - a), which is the number of moves to move the two numbers to the median.

Assuming that the length of the array is N, you can find N/2 combinations of a and b so that they both move to the position of m.

**Solution 1**

Sort first, time complexity: O(NlogN)

```java
public int minMoves2(int[] nums) {
    Arrays.sort(nums);
    int move = 0;
    int l = 0, h = nums.length - 1;
    while (l <= h) {
        move += nums[h] - nums[l];
        l++;
        h--;
    }
    return move;
}
```

**Solution 2**

Find the median using quick selection, time complexity O(N)

```java
public int minMoves2(int[] nums) {
    int move = 0;
    int median = findKthSmallest(nums, nums.length / 2);
    for (int num : nums) {
        move += Math.abs(num - median);
    }
    return move;
}

private int findKthSmallest(int[] nums, int k) {
    int l = 0, h = nums.length - 1;
    while (l < h) {
        int j = partition(nums, l, h);
        if (j == k) {
            break;
        }
        if (j < k) {
            l = j + 1;
        } else {
            h = j - 1;
        }
    }
    return nums[k];
}

private int partition(int[] nums, int l, int h) {
    int i = l, j = h + 1;
    while (true) {
        while (nums[++i] < nums[l] && i < h) ;
        while (nums[--j] > nums[l] && j > l) ;
        if (i >= j) {
            break;
        }
        swap(nums, i, j);
    }
    swap(nums, l, j);
    return j;
}

private void swap(int[] nums, int i, int j) {
    int tmp = nums[i];
    nums[i] = nums[j];
    nums[j] = tmp;
}
```

## Majority voting question

### 1. Elements that appear more than n / 2 times in the array

169\. Majority Element (Easy)

[Leetcode](https://leetcode.com/problems/majority-element/description/) / [Leetcode](https://leetcode-cn.com/
problems
/majority-element/description/)

First sort the array, the number in the middle must appear more than n / 2.

```java
public int majorityElement(int[] nums) {
    Arrays.sort(nums);
    return nums[nums.length / 2];
}
```

You can use the Boyer-Moore Majority Vote Algorithm to solve this problem, making the time complexity O(N). The algorithm can be understood this way: use cnt to count the number of occurrences of an element. When the traversed elements are not equal to the counted elements, let cnt--. If i elements are found earlier and cnt == 0, it means that the first i elements do not have a majority, or there is a majority, but the number of occurrences is less than i / 2, because if there are more than i / 2, cnt will definitely not be 0. At this time, among the remaining n - i elements, the number of majorities is still more than (n - i) / 2, so continuing to search can find the majority.

```java
public int majorityElement(int[] nums) {
    int cnt = 0, majority = nums[0];
    for (int num : nums) {
        majority = (cnt == 0) ? num : majority;
        cnt = (majority == num) ? cnt + 1 : cnt - 1;
    }
    return majority;
}
```

## Others

### 1. Square number

367\. Valid Perfect Square (Easy)

[Leetcode](https://leetcode.com/problems/valid-perfect-square/description/) / [Leetcode](https://leetcode-cn.com/problems/valid-perfect-square/description/)

```html
Input: 16
Returns: True
```

Square sequence: 1,4,9,16,..

Interval: 3,5,7,...

The interval is an arithmetic sequence. Using this feature, you can get a sequence of squares starting from 1.

```java
public boolean isPerfectSquare(int num) {
    int subNum = 1;
    while (num > 0) {
        num -= subNum;
        subNum += 2;
    }
    return num == 0;
}
```

### 2. 3 to the nth power

326\. Power of Three (Easy)

[Leetcode](https://leetcode.com/problems/power-of-three/description/) / [Leetcode](https://leetcode-cn.com/problems/power-of-three/description/)

```java
public boolean isPowerOfThree(int n) {
    return n > 0 && (1162261467 % n == 0);
}
```

### 3. Product array

238\. Product of Array Except Self (Medium)

[Leetcode](https://leetcode.com/problems/product-of-array-except-self/description/) / [Leetcode](https://leetcode-cn.com/problems/product-of-array-except-self/description/)

```html
For example, given [1,2,3,4], return [24,12,8,6].
```

Given an array, create a new array where each element of the new array is the product of all elements in the original array except the element at that position.

The required time complexity is O(N), and division cannot be used.

```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] products = new int[n];
    Arrays.fill(products, 1);
    int left = 1;
    for (int i = 1; i < n; i++) {
        left *= nums[i - 1];
        products[i] *= left;
    }
    int right = 1;
    for (int i = n - 2; i >= 0; i--) {
        right *= nums[i + 1];
        products[i] *= right;
    }
    return products;
}
```

###
4. Find the three numbers with the largest product in the array

628\. Maximum Product of Three Numbers (Easy)

[Leetcode](https://leetcode.com/problems/maximum-product-of-three-numbers/description/) / [Leetcode](https://leetcode-cn.com/problems/maximum-product-of-three-numbers/description/)

```html
Input: [1,2,3,4]
Output: 24
```

```java
public int maximumProduct(int[] nums) {
    int max1 = Integer.MIN_VALUE, max2 = Integer.MIN_VALUE, max3 = Integer.MIN_VALUE, min1 = Integer.MAX_VALUE, min2 = Integer.MAX_VALUE;
    for (int n : nums) {
        if (n > max1) {
            max3 = max2;
            max2 = max1;
            max1 = n;
        } else if (n > max2) {
            max3 = max2;
            max2 = n;
        } else if (n > max3) {
            max3 = n;
        }

        i
f (n < min1) {
            min2 = min1;
            min1 = n;
        } else if (n < min2) {
            min2 = n;
        }
    }
    return Math.max(max1*max2*max3, max1*min1*min2);
}
```
