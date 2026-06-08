# Leetcode problem solution - stack and queue
<!-- GFM-TOC -->
* [Leetcode problem solution - stack and queue](#leetcode-problem solution---stack and queue)
    * [1. Use stack to implement queue](#1-Use stack to implement queue)
    * [2. Use queues to implement stacks] (#2-Use queues to implement stacks)
    * [3. Minimum value stack](#3-Minimum value stack)
    * [4. Use stack to implement bracket matching] (#4-Use stack to implement bracket matching)
    * [5. The distance between the element in the array and the next element that is larger than it] (#5-The distance between the element in the array and the next element that is larger than it)
    * [6. Loop the next element in the array that is greater than the current element] (#6- Loop the next element in the array that is greater than the current element)
<!-- GFM-TOC -->


## 1. Use stack to implement queue

232\. Implement Queue using Stacks (Easy)

[Leetcode](https://leetcode.com/problems/implement-queue-using-stacks/description/) / [Leetcode](https://leetcode-cn.com/problems/implement-queue-using-stacks/description/)

The order of the stack is last in first out, and the order of the queue is first in first out. Use two stacks to implement a queue. An element needs to pass through two stacks before it can be dequeued. When passing through the first stack, the order of the elements is reversed, and when passing through the second stack, it is reversed again. This is the first-in, first-out order.

```java
class MyQueue {

    private Stack<Integer> in = new Stack<>();
    private Stack<Integer> out = new Stack<>();

    public void push(int x) {
        in.push(x);
    }

    public int pop() {
        in2out();
        return out.pop();
    }

    public int peek() {
        in2out();
        return out.peek();
    }

    private void in2out() {
        if (out.isEmpty()) {
            while (!in.isEmpty()) {
                out.push(in.pop());
            }
        }
    }

    public boolean empty() {
        return in.isEmpty() && out.isEmpty();
    }
}
```

## 2. Use queue to implement stack

225\. Implement Stack using Queues (Easy)

[Leetcode](https://leetcode.com/problems/implement-stack-using-queues/description/) / [Leetcode](https://leetcode-cn.com/problems/implement-stack-using-queues/description/)

When inserting an element x into the queue, in order to maintain the original last-in-first-out order, x needs to be inserted at the head of the queue. The default insertion order of the queue is the tail of the queue, so after inserting x into the tail of the queue, all elements except x need to be dequeued and re-entered.

```java
class MyStack {

    private Queue<Integer> queue;

    public MyStack() {
        queue = new LinkedList<>();
    }

    public void push(int x) {
        queue.add(x);
        int cnt = queue.size();
        while (cnt-- > 1) {
            queue.add(queue.poll());
        }
    }

    public int pop() {
        return queue.remove();
    }

    public
int top() {
        return queue.peek();
    }

    public boolean empty() {
        return queue.isEmpty();
    }
}
```

## 3. Minimum value stack

155\. Min Stack (Easy)

[Leetcode](https://leetcode.com/problems/min-stack/description/) / [Leetcode](https://leetcode-cn.com/problems/min-stack/description/)

```java
class MinStack {

    private Stack<Integer> dataStack;
    private Stack<Integer> minStack;
    private int min;

    public MinStack() {
        dataStack = new Stack<>();
        minStack = new Stack<>();
        min = Integer.MAX_VALUE;
    }

    public void push(int x) {
        dataStack.add(x);
        min = Math.min(min, x);
        minStack.add(min);
    }

    public void pop() {
        dataStack.pop();
        minStack.pop();
        min = minStack.isEmpty() ? Integer.MAX_VALUE : minStack.peek();
    }

    public int top() {
        return dataStack.peek();
    }

    public int getMin() {
        return minStack.peek();
    }
}
```

For the problem of implementing a minimum queue, you can first implement the queue using a stack, and then convert the problem into a minimum stack. This problem appears in The Beauty of Programming: 3.7.

## 4. Use stack to implement bracket matching

20\. Valid Parentheses (Easy)

[Leetcode](https://leetcode.com/probl
ems/valid-parentheses/description/) / [leetcode](https://leetcode-cn.com/problems/valid-parentheses/description/)

```html
"()[]{}"

Output: true
```

```java
public boolean isValid(String s) {
    Stack<Character> stack = new Stack<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '{' || c == '[') {
            stack.push(c);
        } else {
            if (stack.isEmpty()) {
                return false;
            }
            char cStack = stack.pop();
            boolean b1 = c == ')' && cStack != '(';
            boolean b2 = c == ']' && cStack != '[';
            boolean b3 = c == '}' && cStack != '{';
            if (b1 || b2 || b3) {
                return false;
            }
        }
    }
    return stack.isEmpty();
}
```

## 5. The distance between the element in the array and the next larger element

739\. Daily Temperatures (Medium)

[Leetcode](https://leetcode.com/problems/daily-temperatures/description/) / [Leetcode](https://leetcode-cn.com/problems/daily-temperatures/description/)

```html
Input: [73, 74, 75, 71, 69, 72, 76, 73]
Output: [1, 1, 4, 2, 1, 1, 0, 0]
```

When traversing the array, use the stack to store the numbers in the array. If the number currently traversed is greater than the element on the top of the stack, it means that the next number greater than the element on the top of the stack is the current element.

```java
public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] dist = new int[n];
    Stack<Integer> indexes = new Stack<>();
    for (int curIndex = 0; curIndex < n; curIndex++) {
        while (!indexs.isEmpty() && temperatures[curIndex] > temperatures[indexs.peek()])
{
            int preIndex = indexs.pop();
            dist[preIndex] = curIndex - preIndex;
        }
        indexes.add(curIndex);
    }
    return dist;
}
```

## 6. Loop the next element in the array that is larger than the current element

503\. Next Greater Element II (Medium)

[Leetcode](https://leetcode.com/problems/next-greater-element-ii/description/) / [Leetcode](https://leetcode-cn.com/problems/next-greater-element-ii/description/)

```text
Input: [1,2,1]
Output: [2,-1,2]
Explanation: The first 1's next greater number is 2;
The number 2 can't find next greater number;
The second 1's next greater number needs to search circularly, which is also 2.
```

Unlike 739. Daily Temperatures (Medium), the array is a loop array, and the last requirement is not the distance but the next element.

```java
public int[] nextGreaterElements(int[] nums) {
    int n = nums.length;
    int[] next = new int[n];
    Arrays.fill(next, -1);
    Stack<Integer> pre = new Stack<>();
    for (int i = 0; i < n * 2; i++) {
        int num = nums[i % n];
        while (!pre.isEmpty() && nums[pre.peek()] < num) {
            next[pre.pop()] = num;
        }
        if (i < n){
            pre.push(i);
        }
    }
    return next;
}
```
