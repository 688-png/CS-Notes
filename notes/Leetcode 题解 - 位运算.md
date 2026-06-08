# Leetcode problem solution - bit operations
<!-- GFM-TOC -->
* [Leetcode problem solution-bit operation](#leetcode-problem solution---bit operation)
    * [0. Principle](#0-Principle)
    * [1. Count how many bits are different in the binary representation of two numbers] (#1-Count how many bits are different in the binary representation of two numbers)
    * [2. The only non-duplicate element in the array] (#2-The only non-duplicate element in the array)
    * [3. Find the missing number in the array] (#3-Find the missing number in the array)
    * [4. Two non-duplicate elements in the array] (#4-Two non-duplicate elements in the array)
    * [5. Flip the bits of a number] (#5-flip the bits of a number)
    * [6. Exchange two integers without extra variables] (#6-Exchange two integers without extra variables)
    * [7. Determine whether a number is 2 to the nth power] (#7-Judge whether a number is -2- to the n-th power)
    * [8. Determine whether a number is 4 to the nth power] (#8--Judge whether a number is -4- to the n-th power)
    * [9. Determine whether the bit-level representation of a number will not appear consecutive 0 and 1] (#9-Judge whether the bit-level representation of a number will not appear consecutive -0- and -1)
    * [10. Find the complement of a number](#10-Find the complement of a number)
    * [11. Implement the addition of integers](#11-Realize the addition of integers)
    * [12. Maximum product of string array](#12-Maximum product of string array)
    * [13. Count the number of 1's in the binary representation of each number from 0 \~ n] (#13-Count the number of -1- in the binary representation of each number from -0-\~-n-)
<!-- GFM-TOC -->


## 0. Principle

**Basic Principle**

0s represents a string of 0s, and 1s represents a string of 1s.

```
x ^ 0s = x x & 0s = 0 x | 0s = x
x ^ 1s = ~x x & 1s = x x | 1s = 1s
x ^ x = 0 x & x = x x | x = x
```

Using the characteristics of x ^ 1s = \~x, you can flip the bit-level representation of a number; using the characteristics of x ^ x = 0, you can remove two repeated numbers from three numbers, leaving only the other number.

```
1^1^2 = 2
```

Using the characteristics of x & 0s = 0 and x & 1s = x, mask operations can be implemented. A number num is bitwise ANDed with mask: 00111100, retaining only the bits in num that correspond to the 1 part of mask.

```
01011011&
00111100
--------
00011000
```

Using the characteristics of x | 0s = x and x | 1s = 1s, the value setting operation can be realized. A number num is bitwise ORed with mask: 00111100, setting all bits in num corresponding to the 1 part of mask to 1.

```
01011011 |
00111100
--------
01111111
```

**Bitwise AND Operation Skills**

n&(n-1) removes the lowest bit, 1, from the bit-level representation of n. For example, for the binary representation of 01011011, subtract 1 to get 01011010, and the two numbers are summed to get 01011010.

```
01011011&
01011010
--------
01011010
```

n&(-n) gets the lowest bit 1 i
n the bit-level representation of n. -n gets the complement of n plus 1, that is -n=\~n+1. For example, for the binary representation of 10110100, -n gives 01001100, and ANDing gives 00000100.

```
10110100&
01001100
--------
00000100
```

n-(n&(-n)) can remove the lowest bit 1 in the bit-level representation of n, which has the same effect as n&(n-1).

**Shift operation**

\\>\\> n is an arithmetic right shift, which is equivalent to dividing by 2n, for example -7 \\>\\> 2 = -2.

```
11111111111111111111111111111001 >> 2
--------
11111111111111111111111111111110
```

\\>\\>\\> n is an unsigned right shift, and 0 will be added to the left. For example -7 \\>\\>\\> 2 = 1073741822.

```
11111111111111111111111111111001 >>> 2
--------
00111111111111111111111111111111
```

\<\< n is an arithmetic left shift, which is equivalent to multiplying by 2n. -7 \<\< 2 = -28.

```
11111111111111111111111111111001 << 2
--------
11111111111111111111111111100100
```

**mask calculation**

To get 111111111, just invert 0, \~0.

To get a mask with only the i-th bit being 1, just move 1 to the left by i-1 bits, 1\<\<(i-1). For example, 1\<\<4 results in a mask with only the 5th bit being 1: 00010000.

To get a mask with bits 1 to i equal to 1, (1\<\<i)-1 is sufficient, for example, (1\<\<4)-1 = 00010000-1 = 00001111.

To get a mask with 0 bits from 1 to i, just invert the mask with 1 bits from 1 to i, that is, \~((1\<\<i)-1).

**Bit operations in Java**

```html
static int Integer.bitCount(); // Count the number of 1's
static int Integer.highestOneBit(); // Get the highest bit
static String toBinaryString(int i); // Convert to binary representation of string
```

## 1. Count how many bits are different in the binary representation of two numbers

461. Hamming Distance (Easy)

[Leetcode](https://leetcode.com/problems/hamming-distance/) / [Leetcode](https://leetcode-cn.com/problems/hamming-distance/)

```html
Input: x = 1, y = 4

Output: 2

Explanation:
1 (0 0 0 1)
4 (0 1 0 0)
       ↑ ↑

The above arrows point to positions where the corresponding bits are different.
```

Perform an XOR operation on two numbers. The bit level indicating the difference is 1. Just count how many 1's there are.

```java
public int hammingDistance(int x, int y) {
    int z = x ^ y;
int cnt = 0;
    while(z != 0) {
        if ((z & 1) == 1) cnt++;
        z = z >> 1;
    }
    return cnt;
}
```

Use z&(z-1) to remove the lowest z-level representation.

```java
public int hammingDistance(int x, int y) {
    int z = x ^ y;
    int cnt = 0;
    while (z != 0) {
        z &= (z - 1);
        cnt++;
    }
    return cnt;
}
```

You can use Integer.bitcount() to count the number of 1's.

```java
public int hammingDistance(int x, int y) {
    return Integer.bitCount(x ^ y);
}
```

## 2. The only unique element in the array

136\.Single Number (Easy)

[Leetcode](https://leetcode.com/problems/single-number/description/) / [Leetcode](https://leetcode-cn.com/problems/single-number/description/)

```h
tml
Input: [4,1,2,1,2]
Output: 4
```

The result of the XOR of two identical numbers is 0. Perform the XOR operation on all numbers, and the final result is the number that appears alone.

```java
public int singleNumber(int[] nums) {
    int ret = 0;
    for (int n : nums) ret = ret ^ n;
    return ret;
}
```

## 3. Find the missing number in the array

268\. Missing Number (Easy)

[Leetcode](https://leetcode.com/problems/missing-number/description/) / [Leetcode](https://leetcode-cn.com/problems/missing-number/description/)

```html
Input: [3,0,1]
Output: 2
```

Problem description: The array elements are between 0-n, but one number is missing. You are required to find the missing number.

```java
public int missingNumber(int[] nums) {
    int ret = 0;
    for (int i = 0; i < nums.length; i++) {
        ret = ret ^ i ^ nums[i];
    }
    return ret ^ nums.length;
}
```

## 4. Two non-repeating elements in the array

260\. Single Number III (Medium)

[Leetcode](https://leetcode.com/problems/single-number-iii/description/) / [Leetcode](https://leetcode-cn.com/problems/single-number-iii/description/)

Two unequal elements must have one bit difference in bit-level representation.

The result obtained by XORing all elements of an array is the result of XORing two elements without duplicates.

diff &= -diff gets the rightmost bit of diff that is not 0, that is, the rightmost bit of the bit-level representation of two elements that are not duplicated. This bit can be used to distinguish the two elements.

```java
public int[] singleNumber(int[] nums) {
    int diff = 0;
    for (int num : nums) diff ^= num;
    diff &= -diff; // get the rightmost digit
    int[] ret = new int[2];
    for (int num : nums) {
        if ((num & diff) == 0) ret[0] ^= num;
        else ret[1] ^= num;
    }
    return ret;
}
```

## 5. Flip the bits of a number

190\. Reverse Bits (Easy)

[Leetcode](https://leetcode.com/problems/reverse-bits/description/) / [Leetcode](https://leetcode-cn.com/problems/reverse-bits/description/)

```java
public int reverseBits(int n) {
    int ret = 0;
    for (int i = 0; i < 32; i++) {
        ret <<= 1;
        ret |= (n & 1);
        n >>>= 1;
    }
    return ret;
}
```

If this function needs to be called many times, you can split the int into 4 bytes, then cache the corresponding bits of the byte, flip them, and finally splice them together.

```java
private static Map<Byte, Integer> cache = new HashMap<>();

public int reverseBits(int n) {
    int ret = 0;
    for (int i = 0; i < 4; i++) {
        ret <<= 8;
        ret |= reverseByte((byte) (n & 0b11111111));
        n>>= 8;
    }
    return ret;
}

private int reverseByte(byte b) {
    if (cache.containsKey(b)) return cache.get(b);
    int ret = 0;
    byte t = b;
    for (int i = 0; i < 8; i++) {
        ret <<= 1;
        ret |= t & 1;
        t >>= 1;
    }
    cache.put(b, ret);
    return ret;
}
```

## 6. Swap two integers without extra variables

[Programmer Code Interview Guid
e: P317](#)

```java
a = a ^ b;
b = a ^ b;
a = a ^ b;
```

## 7. Determine whether a number is 2 raised to the nth power
231\. Power of Two (Easy)

[Leetcode](https://leetcode.com/problems/power-of-two/description/) / [Leetcode](https://leetcode-cn.com/problems/power-of-two/description/)

Binary representation has only one 1 present.

```java
public boolean isPowerOfTwo(int n) {
    return n > 0 && Integer.bitCount(n) == 1;
}
```

Using the property 1000 & 0111 == 0, we get the following solution:

```java
public boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

## 8. Determine whether a number is 4 raised to the nth power

342\. Power of Four (Easy)

[Leetcode](https://leetcode.com/problems/power-of-four/) / [Leetcode](https://leetcode-cn.com/problems/power-of-four/)

This number has exactly one odd bit in binary representation, such as 16 (10000).

```java
public boolean isPowerOfFour(int num) {
    return num > 0 && (num & (num - 1)) == 0 && (num & 0b01010101010101010101010101010101) != 0;
}
```

Regular expressions can also be used for matching.

```java
public boolean isPowerOfFour(int num) {
    return Integer.toString(num, 4).matches("10*");
}
```

## 9. Determine whether the bit-level representation of a number does not contain consecutive 0s and 1s.

693\. Binary Number with Alternating Bits (Easy)

[Leetcode](https://leetcode.com/problems/binary-number-with-alternating-bits/description/) / [Leetcode](https://leetcode-cn.com/problems/binary-number-with-alternating-bits/description/)

```html
Input: 10
Output: True
Explanation:
The binary representation of 10 is: 1010.

Input: 11
Output: False
Explanation:
The binary representation of 11 is: 1011.
```

For a bit-level representation of a number like 1010, shifting it to the right by 1 bit yields 101. Each bit of these two numbers is different, so the result of XOR is 1111.

```java
public boolean hasAlternatingBits(int n) {
    int a = (n ^ (n >> 1));
    return (a & (a + 1)) == 0;
}
```

## 10. Find the complement of a number

476\. Number Complement (Easy)

[Leetcode](https://leetcode.com/problems/number-complement/description/) / [Leetcode](https://leetcode-cn.com/problems/number-complement/description/)

```html
Input: 5
Output: 2
Explanation: The binary representation of 5 is 101 (no leading zero bits), and its complement is 010. So you need to output 2.
```

Problem description: The first 0 part in the binary representation is not considered.

For 00000101, requiring one's complement XORs it with 00000111. Then the problem is transformed into finding the mask 00000111.

```java
public int findComplement(int num) {
    if (num == 0) return 1;
    int mask = 1 << 30;
    while ((num & mask) == 0) mask >>= 1;
    mask = (mask << 1) - 1;
    return num ^ mask;
}
```

You can use Java's Integer.highestOneBit() method to get the number containing the first 1.

```java
public int findComplement(int num) {
    if (num == 0) return 1;
    int mask = Integer.highest
OneBit(num);
    mask = (mask << 1) - 1;
    return num ^ mask;
}
```

To expand a number like 10000000 to 11111111, you can use the following method:

```html
mask |= mask >> 1 11000000
mask |= mask >> 2 11110000
mask |= mask >> 4 11111111
```

```java
public int findComplement(int num) {
    int mask = num;
    mask |= mask >> 1;
    mask |= mask >> 2;
    mask |= mask >> 4;
    mask |= mask >> 8;
    mask |= mask >> 16;
    return (mask ^ num);
}
```

## 11. Implement integer addition

371\. Sum of Two Integers (Easy)

[Leetcode](https://leetcode.com/problems/sum-of-two-integers/description/) / [Leetcode](https://leetcode-cn.com/problems/sum-of-two-integers/description/)

a ^ b represents the sum of two numbers without considering carry. (a & b) \<\< 1 is carry.

The reason why the recursion will terminate is that (a & b) \<\< 1 will have one more rightmost
0, then continue the recursion, the rightmost 0 in the carry will slowly increase, and finally the carry will become 0, and the recursion terminates.

```java
public int getSum(int a, int b) {
    return b == 0 ? a : getSum((a ^ b), (a & b) << 1);
}
```

## 12. Maximum product of string arrays

318\. Maximum Product of Word Lengths (Medium)

[Leetcode](https://leetcode.com/problems/maximum-product-of-word-lengths/description/) / [Leetcode](https://leetcode-cn.com/problems/maximum-product-of-word-lengths/description/)

```html
Given ["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]
Return 16
The two words can be "abcw", "xtfn".
```

Title description: The strings in the string array only contain lowercase characters. To find the maximum product of the lengths of two strings in a string array, it is required that the two strings cannot contain the same characters.

The main problem of this question is to determine whether two strings contain the same characters. Since the strings only contain lowercase characters, with a total of 26 bits, a 32-bit integer can be used to store whether each character appears.

```java
public int maxProduct(String[] words) {
    int n = words.length;
    int[] val = new int[n];
    for (int i = 0; i < n; i++) {
        for (char c : words[i].toCharArray()) {
            val[i] |= 1 << (c - 'a');
        }
    }
    int ret = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if ((val[i] & val[j]) == 0) {
                ret = Math.max(ret, words[i].length() * words[j].length());
            }
        }
    }
    return ret;
}
```

## 13. Count the number of 1’s in the binary representation of each number from 0 \~ n

338\. Counting Bits (Medium)

[Leetcode](https://leetcode.com/problems/counting-bits/description/) / [Leetcode](https://leetcode-cn.com/problems/counting-bits/description/)

For the number 6(110), it can be seen as 4(100) plus 2(10), so dp[i] = dp[i&(i-1)] + 1;

```java
public int[] countBits(int num) {
    int[] ret = new int[num + 1];
    for(int i = 1; i <= num; i++){
        ret[i] = ret[i&(i-1)] + 1;
    }
return ret;
}
```
