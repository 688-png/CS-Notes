# Leetcode problem solution - string
<!-- GFM-TOC -->
* [Leetcode solution - string](#leetcode-solution---string)
    * [1. String rotation includes] (#1-String rotation includes)
    * [2. String circular shift] (#2-String circular shift)
    * [3. Flip of words in string] (#3- Flip of words in string)
    * [4. Whether the characters contained in the two strings are exactly the same] (#4-whether the characters contained in the two strings are exactly the same)
    * [5. Calculate the maximum length of a palindrome string that can be formed by a set of characters] (#5-Calculate the maximum length of a palindrome string that can be formed by a set of characters)
    * [6. String isomorphism](#6-String isomorphism)
    * [7. Number of palindrome substrings] (#7-Number of palindrome substrings)
    * [8. Determine whether an integer is a palindrome] (#8-Determine whether an integer is a palindrome)
    * [9. Count the number of substrings with the same number of consecutive 1s and consecutive 0s in a binary string] (#9-Count the number of substrings with the same number of consecutive 1s and consecutive 0s in a binary string)
<!-- GFM-TOC -->


## 1. String circular shift includes

[The Beauty of Programming 3.1](#)

```html
s1 = AABCD, s2 = CDAA
Return : true
```

Given two strings s1 and s2, it is required to determine whether s2 can be contained by the string obtained by circular shift of s1.

The result of the circular shift of s1 is a substring of s1s1, so you only need to determine whether s2 is a substring of s1s1.

## 2. String circular shift

[The Beauty of Programming 2.17](#)

```html
s = "abcd123" k = 3
Return "123abcd"
```

Rotate the string k bits to the right.

Flip abcd and 123 individually in abcd123 to get dcba321, then flip the entire string to get 123abcd.

## 3. Flip of words in string

[Programmer Code Interview Guide](#)

```html
s = "I am a student"
Return "student a am I"
```

Flip each word, then flip the entire string.

## 4. Whether the characters contained in the two strings are exactly the same

242\. Valid Anagram (Easy)

[Leetcode](https://leetcode.com/problems/valid-anagram/description/) / [Leetcode](https://leetcode-cn.com/problems/valid-anagram/description/)

```html
s = "anagram", t = "nagaram", return true.
s = "rat", t = "car", return false.
```

You can use HashMap to map characters and occurrence times, and then compare whether the number of characters appearing in two strings is the same.

Since the string in this question only contains 26 lowercase characters, you can use an integer array with a length of 26 to count the characters that appear in the string, instead of using HashMap.

```java
public boolean isAnagram(String s, String t) {
    int[] cnts = new int[26];
    for (char c : s.toCharArray()) {
        cnts[c - 'a']++;
    }
    for (char c : t.toCharArray()) {
        cnts[c - 'a']--;
    }
    for (int cnt : cnts) {
        if (cnt != 0) {
            return false;
        }
    }
    return tru
e;
}
```

## 5. Calculate the maximum length of a palindrome string that can be composed of a set of characters

409\. Longest Palindrome (Easy)

[Leetcode](https://leetcode.com/problems/longest-palindrome/description/) / [Leetcode](https://leetcode-cn.com/problems/longest-palindrome/description/)

```html
Input: "abccccdd"
Output: 7
Explanation: One longest palindrome that can be built is "dccaccd", whose length is 7.
```

Use an integer array with a length of 256 to count the number of occurrences of each character. An even number of each character can be used to form a palindrome string.

Because the middle character of the palindrome string can appear alone, if there is a single character, put it in the middle.

```java
public int longestPalindrome(String s) {
    int[] cnts = new int[256];
    for (char c : s.toCharArray()) {
        cnts[c]++;
    }
    int palindrome = 0;
    for (int cnt : cnts) {
        palindrome += (cnt / 2) * 2;
    }
    if (palindrome < s.length()) {
        palindrome++; // Under this condition, there must be a single unused character in s. This character can be placed in the middle of the palindrome.
    }
    return palindrome;
}
```

## 6. String isomorphism

205\. Isomorphic Strings (Easy)

[Leetcode](https://leetcode.com/problems/isomorphic-strings/description/) / [Leetcode](https://leetcode-cn.com/problems/isomorphic-strings/description/)

```html
Given "egg", "add", return true.
Given "foo", "bar", return false.
Given "paper", "title", return true.
```

Record the position where a character last appeared. If the characters in two strings last appeared in the same position, they are isomorphic.

```java
public boolean isIsomorphic(String s, String t) {
    int[] preIndexOfS = new int[256];
    int[] preIndexOfT = new int[256];
    for (int i =
0; i < s.length(); i++) {
        char sc = s.charAt(i), tc = t.charAt(i);
        if (preIndexOfS[sc] != preIndexOfT[tc]) {
            return false;
        }
        preIndexOfS[sc] = i + 1;
        preIndexOfT[tc] = i + 1;
    }
    return true;
}
```

## 7. Number of palindrome substrings

647\. Palindromic Substrings (Medium)

[Leetcode](https://leetcode.com/problems/palindromic-substrings/description/) / [Leetcode](https://leetcode-cn.com/problems/palindromic-substrings/description/)

```html
Input: "aaa"
Output: 6
Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".
```

Starting from a certain bit of the string, try to expand the substring.

```java
private int cnt = 0;

public int countSubstrings(String s) {
    for (int i = 0; i < s.length(); i++) {
        extendSubstrings(s, i, i); // odd length
        extendSubstrings(s, i, i + 1); // even length
    }
    return cnt;
}

private void extendSubstrings(String s, int start, int end) {
    while (start >= 0 && end < s.length() && s.charAt(start) == s.charAt(end)) {
        start--;
        end++;
        cnt++;
    }
}
```

## 8. Determine whether an integer is a palindrome number

9\. Pal
indrome Number (Easy)

[Leetcode](https://leetcode.com/problems/palindrome-number/description/) / [Leetcode](https://leetcode-cn.com/problems/palindrome-number/description/)

It is required that no extra space can be used, so the integer cannot be converted into a string for judgment.

Divide the integer into left and right parts, transpose the right part, and then determine whether the two parts are equal.

```java
public boolean isPalindrome(int x) {
    if (x == 0) {
        return true;
    }
    if (x < 0 || x % 10 == 0) {
        return false;
    }
    int right = 0;
    while (x > right) {
        right = right * 10 + x % 10;
        x /= 10;
    }
    return x == right || x == right / 10;
}
```

## 9. Count the number of substrings with the same number of consecutive 1s and consecutive 0s in a binary string

696\. Count Binary Substrings (Easy)

[Leetcode](https://leetcode.com/problems/count-binary-substrings/description/) / [Leetcode](https://leetcode-cn.com/problems/count-binary-substrings/description/)

```html
Input: "00110011"
Output: 6
Explanation: There are 6 substrings that have equal number of consecutive 1's and 0's: "0011", "01", "1100", "10", "0011", and "01".
```

```java
public int countBinarySubstrings(String s) {
    int preLen = 0, curLen = 1, count = 0;
    for (int i = 1; i < s.length(); i++) {
        if (s.charAt(i) == s.charAt(i - 1)) {
            curLen++;
        } else {
            preLen = curLen;
            curLen = 1;
        }

        if (preLen >= curLen) {
            count++;
        }
    }
    return count;
}
```
