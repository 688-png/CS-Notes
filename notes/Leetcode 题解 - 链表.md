# Leetcode problem solution - linked list
<!-- GFM-TOC -->
* [Leetcode problem solution - linked list](#leetcode-problem solution---linked list)
    * [1. Find the intersection point of two linked lists] (#1-Find the intersection point of two linked lists)
    * [2. Linked list reversal](#2-Linked list reversal)
    * [3. Merge two ordered linked lists] (#3-Merge two ordered linked lists)
    * [4. Delete duplicate nodes from ordered linked list] (#4-Delete duplicate nodes from ordered linked list)
    * [5. Delete the nth node from the bottom of the linked list] (#5-Delete the nth node from the bottom of the linked list)
    * [6. Exchange adjacent nodes in the linked list] (#6-Exchange adjacent nodes in the linked list)
    * [7. Linked list sum](#7-Linked list sum)
    * [8. Palindrome linked list](#8-Palindrome linked list)
    * [9. Separated linked list](#9-Separated linked list)
    * [10. Linked list elements are aggregated by odd and even] (#10-Linked list elements are aggregated by odd and even)
<!-- GFM-TOC -->


A linked list is either an empty node or has a value and a pointer to the next linked list, so many linked list problems can be solved using recursion.

## 1. Find the intersection point of two linked lists

160\. Intersection of Two Linked Lists (Easy)

[Leetcode](https://leetcode.com/problems/intersection-of-two-linked-lists/description/) / [Leetcode](https://leetcode-cn.com/problems/intersection-of-two-linked-lists/description/)

For example, in the following example, two linked lists A and B intersect at c1:

```html
A: a1 → a2
                    ↘
                      c1 → c2 → c3
                    ↗
B: b1 → b2 → b3
```

However, the following intersection will not occur, because each node has only one next pointer, and therefore can only have one successor node. In the following example, node c has two successor nodes.

```html
A: a1 → a2 d1 → d2
                    ↘ ↗
                      c
                    ↗ ↘
B: b1 → b2 → b3 e1 → e2
```



The required time complexity is O(N) and the space complexity is O(1). Returns null if no intersection exists.

Suppose the length of A is a + c, and the length of B is b + c, where c is the length of the common part of the tail, it can be seen that a + c + b = b + c + a.

When the pointer accessing linked list A accesses the tail of linked list, let it access linked list B starting from the head of linked list B; similarly, when the pointer accessing linked list B accesses the tail of linked list, let it start accessing linked list A starting from the head of linked list A. In this way, the pointers accessing the two linked lists A and B can be controlled to access the intersection point at the same time.

If there is no intersection, then a + b = b + a, l1 and l2 in the following implementation code will be null at the same time, thus exiting the loop.

```java
public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
    ListNode l1 = headA, l2 = headB;
    w
hile (l1 != l2) {
        l1 = (l1 == null) ? headB : l1.next;
        l2 = (l2 == null) ? headA : l2.next;
    }
    return l1;
}
```

If it is just to determine whether there is an intersection, then it is another problem, that is, the problem of [The Beauty of Programming 3.6](). There are two solutions:

- Connect the end of the first linked list to the beginning of the second linked list to see if there is a cycle in the second linked list;
- Or directly compare whether the last nodes of the two linked lists are the same.

## 2. Reverse linked list

206\. Reverse Linked List (Easy)

[Leetcode](https://leetcode.com/problems/reverse-linked-list/description/) / [Leetcode](https://leetcode-cn.com/problems/reverse-linked-list/description/)

recursion

```java
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) {
        return head;
    }
    ListNode next = head.next;
    ListNode newHead = reverseList(next);
    next.next = head;
    head.next = null;
    return newHead;
}
```

Head insertion method

```java
public ListNode reverseList(ListNode head) {
    ListNode newHead = new ListNode(-1);
    while (head != null) {
        ListNode next = head.next;
        head.next = newHead.next;
        newHead.next = head;
        head = next;
    }
    return newHead.next;
}
```

## 3. Merge two ordered linked lists

21\. Merge Two Sorted Lists (Easy)

[Leetcode](https://leetcode.com/problems/merge-two-sorted-lists/description/) / [Leetcode](https://leetcode-cn.com/problems/merge-two-sorted-lists/description/)

```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    if (l1 == null) return l2;
    if (l2 == null) return l1;
    if (l1.val < l2.val) {
        l1.next = mergeTwoLists(l1.next, l2);
        return l1;
    } else {
        l2.next = mergeTwoLists(l1, l2.next);
return l2;
    }
}
```

##  4. 从有序链表中删除重复节点

83\. Remove Duplicates from Sorted List (Easy)

[Leetcode](https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/) / [力扣](https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list/description/)

```html
Given 1->1->2, return 1->2.
Given 1->1->2->3->3, return 1->2->3.
```

```java
public ListNode deleteDuplicates(ListNode head) {
    if (head == null || head.next == null) return head;
    head.next = deleteDuplicates(head.next);
    return head.val == head.next.val ? head.next : head;
}
```

##  5. 删除链表的倒数第 n 个节点

19\. Remove Nth Node From End of List (Medium)

[Leetcode](https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/) / [力扣](https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list/description/)

```html
Given linked list: 1->2->3->4->5, and n = 2.
After removing the second node from the end, the linked list becomes 1->2->3->5.
```

```java
public ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode fast = head;
    while (n-- > 0) {
        fast = fast.next;
    }
    if (fast == null) return head.next;
    List
Node slow = head;
    while (fast.next != null) {
        fast = fast.next;
        slow = slow.next;
    }
    slow.next = slow.next.next;
    return head;
}
```

## 6. Exchange adjacent nodes in the linked list

24\. Swap Nodes in Pairs (Medium)

[Leetcode](https://leetcode.com/problems/swap-nodes-in-pairs/description/) / [Leetcode](https://leetcode-cn.com/problems/swap-nodes-in-pairs/description/)

```html
Given 1->2->3->4, you should return the list as 2->1->4->3.
```

Question requirements: The val value of the node cannot be modified, O(1) space complexity.

```java
public ListNode swapPairs(ListNode head) {
    ListNode node = new ListNode(-1);
    node.next = head;
    ListNode pre = node;
    while (pre.next != null && pre.next.next != null) {
        ListNode l1 = pre.next, l2 = pre.next.next;
        ListNode next = l2.next;
        l1.next = next;
        l2.next = l1;
        pre.next = l2;

        pre = l1;
    }
    return node.next;
}
```

## 7. Linked list sum

445\. Add Two Numbers II (Medium)

[Leetcode](https://leetcode.com/problems/add-two-numbers-ii/description/) / [Leetcode](https://leetcode-cn.com/problems/add-two-numbers-ii/description/)

```html
Input: (7 -> 2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 8 -> 0 -> 7
```

Question requirement: The original linked list cannot be modified.

```java
public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
    Stack<Integer> l1Stack = buildStack(l1);
    Stack<Integer> l2Stack = buildStack(l2);
    ListNode head = new ListNode(-1);
    int carry = 0;
    while (!l1Stack.isEmpty() || !l2Stack.isEmpty() || carry != 0) {
        int x = l1Stack.isEmpty() ? 0 : l1Stack.pop();
        int y = l2Stack.isEmpty() ? 0 : l2Stack.pop();
        int sum = x + y + carry;
        ListNode node = new ListNode(sum % 10);
        node.next = head.next;
        head.next = node;
        carry = sum / 10;
    }
    return head.next;
}

private Stack<Integer> buildStack(ListNode l) {
    Stack<Integer> stack = new Stack<>();
while (l != null) {
        stack.push(l.val);
        l = l.next;
    }
    return stack;
}
```

## 8. Palindrome linked list

234\. Palindrome Linked List (Easy)

[Leetcode](https://leetcode.com/problems/palindrome-linked-list/description/) / [Leetcode](https://leetcode-cn.com/problems/palindrome-linked-list/description/)

Question requirement: Solve it with a space complexity of O(1).

Cut it in half, turn the second half over and compare the two halves to see if they are equal.

```java
public boolean isPalindrome(ListNode head) {
    if (head == null || head.next == null) return true;
    ListNode slow = head, fast = head.next;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    if (fast != null) slow = slow.next; // Even node, let slow point to the next node
    cut(head, slow); // Cut into two linked lists
    return isEqual(head, reverse(slow));
}

private void cut(ListNode head, ListNode cutNode) {
    while (head.next != cutNode) {
        head = head.next;
    }
    head.next = null;
}

private ListNode reverse(ListNode head) {
    ListNode newHead = null;
    while (
head != null) {
        ListNode nextNode = head.next;
        head.next = newHead;
        newHead = head;
        head = nextNode;
    }
    return newHead;
}

private boolean isEqual(ListNode l1, ListNode l2) {
    while (l1 != null && l2 != null) {
        if (l1.val != l2.val) return false;
        l1 = l1.next;
        l2 = l2.next;
    }
    return true;
}
```

## 9. Separate linked list

725\. Split Linked List in Parts(Medium)

[Leetcode](https://leetcode.com/problems/split-linked-list-in-parts/description/) / [Leetcode](https://leetcode-cn.com/problems/split-linked-list-in-parts/description/)

```html
Input:
root = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], k = 3
Output: [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]
Explanation:
The input has been split into consecutive parts with size difference at most 1, and earlier parts are a larger size than the later parts.
```

Title description: Divide the linked list into k parts. The length of each part should be as equal as possible, and the length of the front part should be greater than or equal to the length of the back part.

```java
public ListNode[] splitListToParts(ListNode root, int k) {
    int N = 0;
    ListNode cur = root;
    while (cur != null) {
        N++;
        cur = cur.next;
    }
    int mod = N % k;
    int size = N / k;
    ListNode[] ret = new ListNode[k];
    cur = root;
    for (int i = 0; cur != null && i < k; i++) {
        ret[i] = cur;
        int curSize = size + (mod-- > 0 ? 1 : 0);
        for (int j = 0; j < curSize - 1; j++) {
            cur = cur.next;
        }
        ListNode next = cur.next;
        cur.next = null;
        cur = next;
    }
    return ret;
}
```

## 10. Linked list elements are gathered according to odd and even numbers

328\. Odd Even Linked List (Medium)

[Leetcode](https://leetcode.com/problems/odd-even-linked-list/description/) / [Leetcode](https://leetcode-cn.com/problems/odd-even-linked-list/description/)

```html
Example:
Given 1->2->3->4->5->NULL,
return 1->3->5->2->4->NULL.
```

```java
public ListNode oddEvenList(ListNode head) {
    if (head == null) {
        return head;
    }
    ListNode odd = head, even = head.next, evenHead = even;
    while (even != null && even.next != null) {
odd.next = odd.next.next;
        odd = odd.next;
        even.next = even.next.next;
        even = even.next;
    }
    odd.next = evenHead;
    return head;
}
```
