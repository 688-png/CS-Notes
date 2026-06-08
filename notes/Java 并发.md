# Java concurrency
<!-- GFM-TOC -->
* [Java Concurrency](#java-concurrency)
    * [1. Use thread](#1 use thread)
        * [Implement Runnable interface](#implement-runnable-interface)
        * [Implement Callable interface](#implement-callable-interface)
        * [Inherit Thread class](#Inherit-thread-class)
        * [Implement interface VS inherit Thread](#implement interface-vs-inherit-thread)
    * [2. Basic Threading Mechanism](#2Basic Threading Mechanism)
        * [Executor](#executor)
        * [Daemon](#daemon)
        * [sleep()](#sleep)
        * [yield()](#yield)
    * [三、INTERRUPTION](#三INTERRUPTION)
        * [InterruptedException](#interruptedexception)
        * [interrupted()](#interrupted)
        * [Interrupt operation of Executor](Interrupt operation of #executor-)
    * [Four. Mutually exclusive synchronization](#four mutually exclusive synchronization)
        * [synchronized](#synchronized)
        * [ReentrantLock](#reentrantlock)
        * [Compare](#Compare)
        * [Use Choice](#Use Choice)
    * [5. Collaboration between threads] (#5. Collaboration between threads)
        * [join()](#join)
        * [wait() notify() notifyAll()](#wait-notify-notifyall)
        * [await() signal() signalAll()](#await-signal-signalall)
    * [6. Thread status](#6thread status)
        * [New (NEW)](#newnew)
        * [RUNABLE](#runable)
        * [BLOCKED](#blocked)
        * [Waiting indefinitely (WAITING)](#waiting indefinitely)
        * [Timed waiting (TIMED_WAITING)](#timed_waiting)
        * [TERMINATED](#死terminated)
    * [七、J.U.C - AQS](#七juc---aqs)
        * [CountDownLatch](#countdownlatch)
        * [CyclicBarrier](#cyclicbarrier)
        * [Semaphore](#semaphore)
    * [八、J.U.C - Other components](#八juc---Other components)
        * [FutureTask](#futuretask)
        * [BlockingQueue](#blockingqueue)
        * [ForkJoin](#forkjoin)
    * [Nine, Thread Unsafe Examples](#九Thread Unsafe Examples)
    * [10. Java memory model] (#十java-memory model)
        * [Main Memory and Working Memory](#Main Memory and Working Memory)
        * [Inter-memory interaction](#Inter-memory interaction)
        * [Three major characteristics of memory model](#三 major characteristics of memory model)
        * [Principle of occurrence first](#Principle of occurrence first)
    * [Eleven, Thread Safety](#ElevenThreadSafety)
        * [Immutable](#immutable)
        * [Mutually exclusive synchronization](#mutually exclusive synchronization)
        * [Non-blocking synchronization](#non-blocking synchronization)
        * [No synchronization plan](#No synchronization plan)
    * [Twelve, Lock Optimization](#十二 LockOptimization)
        * [Spin Lock](#spinlock)
        * [Lock Elimination](#LOCK Elimination)
        * [Lock Coarse](#LOCK COARSE)
        * [Lightweight Lock](# lightweight lock)
        * [bias lock](#bias lock)
    * [Thirteen, good practices in multi-thread development] (#十三 Good practices in multi-thread development)
    * [Refe
rences](#references)
<!-- GFM-TOC -->



## 1. Use threads

There are three ways to use threads:

- Implement Runnable interface;
- Implement the Callable interface;
- Inherited from Thread class.

A class that implements the Runnable and Callable interfaces can only be regarded as a task that can be run in a thread, not a thread in the true sense, so it needs to be called through Thread in the end. It can be understood that tasks are executed through thread driving.

### Implement Runnable interface

The run() method in the interface needs to be implemented.

```java
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        // ...
    }
}
```

Create another Thread instance using the Runnable instance, and then call the start() method of the Thread instance to start the thread.

```java
public static void main(String[] args) {
    MyRunnable instance = new MyRunnable();
    Thread thread = new Thread(instance);
    thread.start();
}
```

### Implement the Callable interface

Compared with Runnable, Callable can have a return value, and the return value is encapsulated by FutureTask.

```java
public class MyCallable implements Callable<Integer> {
    public Integer call() {
        return 123;
    }
}
```

```java
public static void main(String[] args) throws ExecutionException, InterruptedException {
    MyCallable mc = new MyCallable();
    FutureTask<Integer> ft = new FutureTask<>(mc);
    Thread thread = new Thread(ft);
    thread.start();
    System.out.println(ft.get());
}
```

### Inherit Thread class

It is also necessary to implement the run() method, because the Thread class also implements the Runable interface.

When the start() method is called to start a thread, the virtual machine puts the thread into the ready queue waiting to be scheduled. When a thread is scheduled, the run() method of the thread will be executed.

```java
public class MyThread extends Thread {
    public void run() {
        // ...
    }
}
```

```java
public static void main(String[] args) {
    MyThread mt = new MyThread();
    mt.start();
}
```

### Implementing interface VS inheriting Thread

Implementing an interface is better because:

- Java does not support multiple inheritance, so if you inherit the Thread class, you cannot inherit other classes, but you can implement multiple interfaces;
- The class may only need to be executable, and inheriting the entire Thread class is too expensive.

## 2. Basic thread mechanism

### Executor

Executors manage the execution of multiple asynchronous tasks without requiring the programmer to explicitly manage thread lifecycles. Asynchronous here means that the execution of multiple tasks does not interfere with each other and does not require synchronous operations.

There are three main types of Executors:

- CachedThreadPool: A task creates a thread;
- FixedThreadPool: All tasks can only use fixed-size threads;
- SingleThreadExecutor: Equivalent to FixedThreadPool of size 1.

```j
ava
public static void main(String[] args) {
    ExecutorService executorService = Executors.newCachedThreadPool();
    for (int i = 0; i < 5; i++) {
        executorService.execute(new MyRunnable());
    }
    executorService.shutdown();
}
```

### Daemon

Daemon threads are threads that provide services in the background when the program is running and are not an integral part of the program.

When all non-daemon threads end, the program terminates and all daemon threads are killed.

main() belongs to the non-daemon thread.

A thread can be set as a daemon thread using the setDaemon() method before the thread is started.

```java
public static void main(String[] args) {
    Thread thread = new Thread(new MyRunnable());
    thread.setDaemon(true);
}
```

### sleep()

The Thread.sleep(millisec) method sleeps the currently executing thread. The unit of millisec is milliseconds.

sleep() may throw InterruptedException because exceptions cannot be propagated across threads back into main() and therefore must be handled locally. Other exceptions thrown in the thread also need to be handled locally.

```java
public void run() {
    try {
        Thread.sleep(3000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}
```

### yield()

The call to the static method Thread.yield() declares that the current thread has completed the most important part of its life cycle and can be switched to other threads for execution. This method is only a suggestion to the thread scheduler, and only a suggestion that other threads with the same priority can run.

```java
public void run() {
    Thread.yield();
}
```

## 3. Interruption

A thread will automatically end after it is executed. If an exception occurs during operation, it will also end early.

### InterruptedException

Interrupt a thread by calling its interrupt(). If the thread is blocked, waiting for a limited time, or waiting indefinitely, an InterruptedException will be thrown, thus ending the thread early. However, I/O blocking and synchronized lock blocking cannot be interrupted.

For the following code, start a thread in main() and then interrupt it. Since the Thread.sleep() method is called in the thread, an InterruptedException will be thrown, thus ending the thread early and not executing subsequent statements.

```java
public class InterruptExample {

    private static class MyThread1 extends Thread {
        @Override
        public void run() {
            try {
                Thread.sleep(2000);
                System.out.println("Thread run");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
```

```java
public static void main(String[] args) throws InterruptedException {
    Thread thread1 = new MyThread1();
    thread1.start();
    thread1.interrupt();
    System.out.println("Main run");
}
```

```html
Main run
java.lang.InterruptedException: sleep interrupted
    at java.lang.Thread.sleep(Native Met
hod)
    at InterruptExample.lambda$main$0(InterruptExample.java:5)
    at InterruptExample$$Lambda$1/713338599.run(Unknown Source)
    at java.lang.Thread.run(Thread.java:745)
```

### interrupted()

If a thread's run() method executes an infinite loop and does not perform operations such as sleep() that will throw InterruptedException, then calling the thread's interrupt() method cannot cause the thread to end early.

But calling int
The errupt() method will set the interrupt flag of the thread, and calling the interrupted() method will return true. Therefore, you can use the interrupted() method in the loop body to determine whether the thread is in an interrupted state, thereby ending the thread early.

```java
public class InterruptExample {

    private static class MyThread2 extends Thread {
        @Override
        public void run() {
            while (!interrupted()) {
                // ..
            }
            System.out.println("Thread end");
        }
    }
}
```

```java
public static void main(String[] args) throws InterruptedException {
    Thread thread2 = new MyThread2();
    thread2.start();
    thread2.interrupt();
}
```

```html
Thread end
```

### Interrupt operation of Executor

Calling the shutdown() method of Executor will wait for all threads to finish executing before shutting down. However, if the shutdownNow() method is called, it is equivalent to calling the interrupt() method of each thread.

The following uses Lambda to create a thread, which is equivalent to creating an anonymous internal thread.

```java
public static void main(String[] args) {
    ExecutorService executorService = Executors.newCachedThreadPool();
    executorService.execute(() -> {
        try {
            Thread.sleep(2000);
            System.out.println("Thread run");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    });
    executorService.shutdownNow();
    System.out.println("Main run");
}
```

```html
Main run
java.lang.InterruptedException: sleep interrupted
    at java.lang.Thread.sleep(Native Method)
    at ExecutorInterruptExample.lambda$main$0(ExecutorInterruptExample.java:9)
    at ExecutorInterruptExample$$Lambda$1/1160460865.run(Unknown Source)
    at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
    at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
    at java.lang.Thread.run(Thread.java:745)
```

If you only want to interrupt one thread in the Executor, you can submit a thread by using the submit() method, which will return a Future\<?\> object, and you can interrupt the thread by calling the object's cancel(true) method.

```java
Future<?> future = executorService.submit(() -> {
    // ..
});
future.cancel(true);
```

## 4. Mutually exclusive synchronization

Java provides two lock mechanisms to control mutually exclusive access to shared resources by multiple threads. The first is synchronized implemented by the JV
M, and the other is ReentrantLock implemented by the JDK.

### synchronized

**1. Synchronize a code block**

```java
public void func() {
    synchronized (this) {
        // ...
    }
}
```

It only works on the same object, if synchronized code blocks are called on two objects, no synchronization will occur.

For the following code, two threads are executed using ExecutorService. Since the synchronization code block of the same object is called, the two threads will be synchronized. When one thread enters the synchronization statement block, the other thread must wait.

```java
public class SynchronizedExample {

    public void func1() {
        synchronized (this) {
            for (int i = 0; i < 10; i++) {
                System.out.print(i + " ");
            }
        }
    }
}
```

```java
public static void main(String[] args) {
    SynchronizedExample e1 = new SynchronizedExample();
    ExecutorService executorService = Executors.newCachedThreadPool();
    executorService.execute(() -> e1.func1());
    executorService.execute(() -> e1.func1());
}
```

```html
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9
```

For the following code, the two threads call the synchronization code block of different objects, so the two threads do not need to be synchronized. It can be seen from the output that the two threads are executed cross-cuttingly.

```java
public static void main(String[] args) {
    SynchronizedExample e1 = new SynchronizedExample();
    SynchronizedExample e2 = new SynchronizedExample();
    ExecutorService executorService = E
xecutors.newCachedThreadPool();
    executorService.execute(() -> e1.func1());
    executorService.execute(() -> e2.func1());
}
```

```html
0 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9
```


**2. Synchronize a method**

```java
public synchronized void func () {
    // ...
}
```

It acts on the same object as the synchronized code block.

**3. Synchronize a class**

```java
public void func() {
    synchronized (SynchronizedExample.class) {
        // ...
    }
}
```

Acts on the entire class, that is to say, two threads calling this synchronization statement on different objects of the same class will also be synchronized.

```java
public class SynchronizedExample {

    public void func2() {
        synchronized (SynchronizedExample.class) {
            for (int i = 0; i < 10; i++) {
                System.out.print(i + " ");
            }
        }
    }
}
```

```java
public static void main(String[] args) {
    SynchronizedExample e1 = new SynchronizedExample();
    SynchronizedExample e2 = new SynchronizedExample();
    ExecutorService executorService = Executors.newCachedThreadPool();
    executorService.execute(() -> e1.func2());
    executorService.execute(() -> e2.func2());
}
```

```html
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9
```

**4. Synchronize a static method**

```java
public synchronized static void fun() {
    // ...
}
```

Applies to the entire class.

### ReentrantLock

ReentrantLock is a lock
in the java.util.concurrent (J.U.C) package.

```java
public class LockExample {

    private Lock lock = new ReentrantLock();

    public void func() {
        lock.lock();
        try {
            for (int i = 0; i < 10; i++) {
                System.out.print(i + " ");
            }
        } finally {
            lock.unlock(); // Ensure the lock is released to avoid deadlock.
        }
    }
}
```

```java
public static void main(String[] args) {
    LockExample lockExample = new LockExample();
    ExecutorService executorService = Executors.newCachedThreadPool();
    executorService.execute(() -> lockExample.func());
    executorService.execute(() -> lockExample.func());
}
```

```html
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9
```


### Compare

**1. Implementation of lock**

synchronized is implemented by JVM, while ReentrantLock is implemented by JDK.

**2. Performance**

The new version of Java has made many optimizations to synchronized, such as spin locks, etc. Synchronized is roughly the same as ReentrantLock.

**3. Waiting can be interrupted**

When the thread holding the lock does not release the lock for a long time, the waiting thread can choose to give up waiting and deal with other things instead.

ReentrantLock can be interrupted, but synchronized cannot.

**4. Fair lock**

Fair lock means that when multiple threads are waiting for the same lock, they must obtain the lock in sequence according to the time order of applying for the lock.

Locks in synchronized are unfair, and ReentrantLock is also unfair by default, but it can also be fair.

**5. The lock is bound to multiple conditions**

A ReentrantLock can bind multiple Condition objects at the same time.

### Use select

Unless you need to use the advanced features of ReentrantLock, use synchronized in preference. This is because synchronized is a lock mechanism implemented by the JVM. The JVM natively supports it, but ReentrantLock is not supported by all JDK versions. And using synchronized, you don’t have to worry about deadlock problems caused by not releasing the lock, because the JVM will ensure that the lock is released.

## 5. Cooperation between threads

When multiple threads can work together to solve a problem, if some parts must be completed before other parts, then the threads need to be coordinated.

### join()

Calling the join() method of another thread in a thread will suspend the current thread instead of busy waiting until the target thread ends.

For the following code, although thread b starts first, because the join() method of thread a is called in thread b, thread b will wait for thread a to end before continuing execution, so in the end it is guaranteed that the output of thread a precedes the output of thread b.

```java
public class JoinExample {

    private class A extends Thread {
        @Override
        public void run() {
            System.out.println("A");
        }
    }

    private class B extends Thread {

        private A a;
B
(A a) {
            this.a = a;
        }

        @Override
        public void run() {
            try {
                a.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("B");
        }
    }

    public void test() {
        A a = new A();
        B b = new B(a);
        b.start();
        a.start();
    }
}
```

```java
public static void main(String[] args) {
    JoinExample example = new JoinExample();
    example.test();
}
```

```
A
B
```

### wait() notify() notifyAll()

Calling wait() causes the thread to wait for a certain condition to be met. The thread will be suspended while waiting. When other threads run and the condition is met, other threads will call notify() or notifyAll() to wake up the suspended thread.

They are all part of Object, not Thread.

It can only be used in synchronized methods or synchronized control blocks, otherwise IllegalMonitorStateException will be thrown at runtime.

While suspended using wait(), the thread releases the lock. This is because if the lock is not released, other threads cannot enter the object's synchronization method or synchronization control block, and then cannot execute notify() or notifyAll() to wake up the suspended thread, causing a deadlock.

```java
public class WaitNotifyExample {

    public synchronized void before() {
        System.out.println("before");
        notifyAll();
    }

    public synchronized void after() {
        try {
            wait();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("after");
    }
}
```

```java
public static void main(String[] args) {
    ExecutorService executorService = Executors.newCachedThreadPool();
    WaitNotifyExample example = new WaitNotifyExample();
    executorService.execute(() -> example.after());
    executorService.execute(() -> example.before());
}
```

```html
before
after
```

**The difference between wait() and sleep()**

- wait() is a method of Object, and sleep() is a static method of Thread;
- wait() will release the lock, sleep() will not.

### await() signal() signalAll()

The java.util.concurrent class library provides the Condition class to achieve coordination between threads. You can call the await() method on the Condition to make the thread wait, and other threads call the signal() or signalAll() method to wake up the waiting thread.

Compared with the waiting method of wait(), await() can specify the waiting conditions, so it is more flexible.

Use Lock to obtain a Condition object.

```java
public class AwaitSignalExample {

    private Lock lock = new ReentrantLock();
    private Condition condition = lock.newCondition();

    public void before() {
        lock.lock();
        try {
            System.out.println("before");
            condition.signalAll();
        } finally {
            lock.unlock();
        }
    }

    public void after() {
lock.lock();
        try {
            condition.await();
            System.out.println("after");
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
}
```

```java
public static void main(String[] args) {
    ExecutorService executorService = Executors.newCachedThreadPool();
    AwaitSignalExample example = new AwaitSignalExample();
    executorService.execute(() -> example.after());
    executorService.execute(() -> example.before());
}
```

```html
before
after
```

## 6. Thread status

A thread can only be in one state, and the thread state here specifically refers to the thread state of the Java virtual machine and cannot reflect the state of the thread under a specific operating system.

### NEW

It has not been started since it was created.

### RUNABLE

Running in a Java virtual machine. But at the operating system level, it may be in a running state, or it may be waiting for resource scheduling (such as processor resources). After resource scheduling is completed, it will enter operation.
state. Therefore, runnability in this state means that it can be run. Whether it can run or not depends on the resource scheduling of the underlying operating system.

### BLOCKED

Requesting to obtain the monitor lock to enter the synchronized function or code block, but other threads have already occupied the monitor lock, so it is in a blocking state. To end this state and enter RUNABLE requires other threads to release the monitor lock.

### Waiting indefinitely (WAITING)

Wait for other threads to wake up explicitly.

The difference between blocking and waiting is that blocking is passive, waiting to acquire the monitor lock. Waiting is active and is entered by calling methods such as Object.wait().

| Entry method | Exit method |
| --- | --- |
| Object.wait() method without setting Timeout parameter | Object.notify() / Object.notifyAll() |
| The Thread.join() method without setting the Timeout parameter | The called thread has completed execution |
| LockSupport.park() method | LockSupport.unpark(Thread) |

### Time limit waiting (TIMED_WAITING)

There is no need to wait for other threads to wake up explicitly, it will be automatically woken up by the system after a certain period of time.

| Entry method | Exit method |
| --- | --- |
| Thread.sleep() method | Time ends |
| Object.wait() method with Timeout parameter set | Time ends / Object.notify() / Object.notifyAll() |
| Thread.join() method with Timeout parameter set | Time ends/The called thread completes execution |
| LockSupport.parkNanos() method | LockSupport.unpark(Thread) |
| LockSupport.parkUntil() method | LockSupport.unpark(Thread) |

When calling the Thread.sleep() method to put a thread into a time-limited waiting state, it is often described as "putting a thread to sleep". When calling the Object.wait() method to cause a thread to wait for a limited time or wait indefinitely, it is often des
cribed as "suspending a thread". Sleep and suspend are used to describe behavior, while blocking and waiting are used to describe state.

### TERMINATED

It can be that the thread ends itself after completing the task, or it ends due to an exception.

[Java SE 9 Enum Thread.State](https://docs.oracle.com/javase/9/docs/api/java/lang/Thread.State.html)

## 7. J.U.C - AQS

java.util.concurrent (J.U.C) greatly improves concurrency performance, and AQS is considered the core of J.U.C.

### CountDownLatch

Used to control one or more threads waiting for multiple threads.

A counter cnt is maintained. Each time the countDown() method is called, the counter value will be decremented by 1. When it is reduced to 0, those threads waiting due to calling the await() method will be awakened.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ba078291-791e-4378-b6d1-ece76c2f0b14.png" width="300px"> </div><br>

```java
public class CountdownLatchExample {

    public static void main(String[] args) throws InterruptedException {
        final int totalThread = 10;
        CountDownLatch countDownLatch = new CountDownLatch(totalThread);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalThread; i++) {
            executorService.execute(() -> {
                System.out.print("run..");
                countDownLatch.countDown();
            });
        }
        countDownLatch.await();
        System.out.println("end");
        executorService.shutdown();
    }
}
```

```html
run..run..run..run..run..run..run..run..run..run..end
```

### CyclicBarrier

Used to control multiple threads to wait for each other. Only when multiple threads arrive, these threads will continue to execute.

Similar to CountdownLatch, it is implemented by maintaining counters. After the thread executes the await() method, the counter will be decremented by 1 and waits until the counter reaches 0. All threads that are waiting by calling the await() method can continue to execute.

One difference between CyclicBarrier and CountdownLatch is that the counter of CyclicBarrier can be used cyclically by calling the reset() method, so it is called a cycle barrier.

CyclicBarrier has two constructors, where parties indicates the initial value of the counter, and barrierAction is executed once when all threads reach the barrier.

```java
public CyclicBarrier(int parties, Runnable barrierAction) {
    if (parties <= 0) throw new IllegalArgumentException();
    this.parties = parties;
    this.count = parties;
    this.barrierCommand = barrierAction;
}

public CyclicBarrier(int parties) {
    this(parties, null);
}
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f71af66b-0d54-4399-a44b-f47b58321984.png" width="300px"> </div><br>

``
`java
public class CyclicBarrierExample {

    public static void main(String[] args) {
        final int totalThread = 10;
CyclicBarrier cyclicBarrier = new CyclicBarrier(totalThread);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalThread; i++) {
            executorService.execute(() -> {
                System.out.print("before..");
                try {
                    cyclicBarrier.await();
                } catch (InterruptedException | BrokenBarrierException e) {
                    e.printStackTrace();
                }
                System.out.print("after..");
            });
        }
        executorService.shutdown();
    }
}
```

```html
before..before..before..before..before..before..before..before..before..before..after..after..after..after..after..after..after..after..after..after..
```

### Semaphore

Semaphore is similar to a semaphore in the operating system and can control the number of threads accessing mutually exclusive resources.

The following code simulates concurrent requests to a service that can only be accessed by 3 clients at a time, for a total of 10 requests.

```java
public class SemaphoreExample {

    public static void main(String[] args) {
        final int clientCount = 3;
        final int totalRequestCount = 10;
        Semaphore semaphore = new Semaphore(clientCount);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalRequestCount; i++) {
            executorService.execute(()->{
                try {
                    semaphore.acquire();
                    System.out.print(semaphore.availablePermits() + " ");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    semaphore.release();
                }
            });
        }
        executorService.shutdown();
    }
}
```

```html
2 1 2 2 2 2 2 1 2 2
```

## 8. J.U.C - Other components

### FutureTask

When introducing Callable, we knew that it can have a return value, and the return value is encapsulated by Future\<V\>. FutureTask implements the RunnableFuture interface, which inherits from Runnable and Future\<V\> interfaces, which allows FutureTask to be executed as a task and return a value.

```java
public class FutureTask<V> implements RunnableFuture<V>
```

```java
public interface RunnableFuture<V> extends Runnable, Future<V>
```

FutureTask can be used to asynchronously obtain execution results or cancel execution tasks. When a computing task takes a long time to execute, you can use FutureTask to encapsulate the task, and the main thread will get the results after completing its own task.

```java
public class FutureTaskExample {

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureTask<Integer> futureTask = new FutureTask<Integer>(new Callable<Integer>() {
            @Override
            public Integer call() throws Exception {
                int result = 0;
                for (int i = 0; i <
100; i++) {
                    Thread.sleep(10);
                    result += i;
                }
                return result;
            }
        });

        Thread computeThread = new Thread(futureTask);
        computeThread.start();

        Thread otherThread = new Thread(() -> {
            System.out.println("other task is running...");
            try {
                Threa
d.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        otherThread.start();
        System.out.println(futureTask.get());
    }
}
```

```html
other tasks are running...
4950
```

### BlockingQueue

The java.util.concurrent.BlockingQueue interface has the following blocking queue implementations:

- **FIFO Queue**: LinkedBlockingQueue, ArrayBlockingQueue (fixed length)
- **Priority Queue**: PriorityBlockingQueue

Blocking take() and put() methods are provided: if the queue is empty, take() will block until there is content in the queue; if the queue is full, put() will block until there is a free space in the queue.

**Use BlockingQueue to implement the producer-consumer problem**

```java
public class ProducerConsumer {

    private static BlockingQueue<String> queue = new ArrayBlockingQueue<>(5);

    private static class Producer extends Thread {
        @Override
        public void run() {
            try {
                queue.put("product");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.print("produce..");
        }
    }

    private static class Consumer extends Thread {

        @Override
        public void run() {
            try {
                String product = queue.take();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.print("consume..");
        }
    }
}
```

```java
public static void main(String[] args) {
    for (int i = 0; i < 2; i++) {
        Producer producer = new Producer();
        producer.start();
    }
    for (int i = 0; i < 5; i++) {
        Consumer consumer = new Consumer();
        consumer.start();
    }
    for (int i = 0; i < 3; i++) {
        Producer producer = new Producer();
        producer.start();
    }
}
```

```html
produce..produce..consume..consume..produce..consume..produce..consume..produce..consume..
```

### ForkJoin

It is mainly used in parallel computing. The principle is similar to MapReduce. It splits large computing tasks into multiple small tasks for parallel computing.

```java
public class ForkJoinExample extends RecursiveTask<Integer> {

    private final int threshold = 5;
    private int first;
    private int last;

    public ForkJoinExample(int first, int last) {
        this.first = first;
        this.last = last;
    }

    @Override
    protected Integer compute() {
        int result = 0;
        if (last - first <= threshold) {
            // If the task is smal
l enough, calculate it directly
            for (int i = first; i <= last; i++) {
                result += i;
            }
        } else {
            // Split into small tasks
            int middle = first + (last - first) / 2;
            ForkJoinExample leftTask = new ForkJoinExample(first, middle);
            ForkJoinExample rightTask = new ForkJoinExample(middle + 1, last);
            leftTask.fork();
            rightTask.fork();
            result = leftTask.join() + rightTask.join();
        }
        return result;
    }
}
```

```java
public static void main(String[] args) throws ExecutionException, InterruptedException {
    ForkJoinExample example = new ForkJoinExample(1, 10000);
    ForkJoinPool forkJoinPool = new ForkJoinPool();
    Future result = forkJoinP
ool.submit(example);
    System.out.println(result.get());
}
```

ForkJoin is started using ForkJoinPool, which is a special thread pool. The number of threads depends on the number of CPU cores.

```java
public class ForkJoinPool extends AbstractExecutorService
```

ForkJoinPool implements a work-stealing algorithm to improve CPU utilization. Each thread maintains a double-ended queue to store tasks that need to be executed. The work-stealing algorithm allows an idle thread to steal a task from another thread's deque for execution. The stolen task must be the latest task to avoid competition with the thread to which the queue belongs. For example, in the figure below, Thread2 takes out the latest Task1 task from Thread1's queue, and Thread1 will take out Task2 to execute, thus avoiding competition. But if there is only one task in the queue, competition will still occur.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e42f188f-f4a9-4e6f-88fc-45f4682072fb.png" width="300px"> </div><br>

## 9. Thread unsafe example

If multiple threads access the same shared data without taking synchronization operations, the results of the operations will be inconsistent.

The following code demonstrates that 1000 threads perform an increment operation on cnt at the same time. After the operation is completed, its value may be less than 1000.

```java
public class ThreadUnsafeExample {

    private int cnt = 0;

    public void add() {
        cnt++;
    }

    public int get() {
        return cnt;
    }
}
```

```java
public static void main(String[] args) throws InterruptedException {
    final int threadSize = 1000;
    ThreadUnsafeExample example = new ThreadUnsafeExample();
    final CountDownLatch countDownLatch = new CountDownLatch(threadSize);
    ExecutorService executorService = Executors.newCachedThreadPool();
    for (int i = 0; i < threadSize; i++) {
        executorService.execute(() -> {
            example.add();
            countDownLatch.countDown();
        });
    }
    countDownLatch.await();
    executorService.shutdown();
    System.out.println(example.get());
}
```

```html
997
```

## 10. Java memory model

The Java memory
model attempts to shield memory access differences among various hardware and operating systems, so that Java programs can achieve consistent memory access effects on various platforms.

### Main memory and working memory

The read and write speed of registers on the processor is several orders of magnitude faster than that of memory. In order to solve this speed contradiction, a cache is added between them.

Adding cache brings a new problem: cache consistency. If multiple caches share the same main memory area, the data in the multiple caches may be inconsistent, and some protocols are needed to solve this problem.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/942ca0d2-9d5c-45a4-89cb-5fd89b61913f.png" width="600px"> </div><br>

All variables are stored in main memory, and each thread also has its own working memory. The working memory is stored in a cache or register, and holds a copy of the main memory copy of the variables used by the thread.

Threads can only directly operate variables in working memory, and the transfer of variable values ​​between different threads needs to be completed through main memory.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/15851555-5abc-497d-ad34-efed10f43a6b.png" width="600px"> </div><br>

### Interaction between memories

The Java memory model defines 8 operations to complete the interaction between main memory and working memory.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8b7ebbad-9604-4375-84e3-f412099d170c.png" width="450px"> </div><br>

- read: transfer the value of a variable from main memory to working memory
- load: Executed after read, put the value obtained by read into a copy of the variable in the working memory
- use: Pass the value of a variable in the working memory to the execution engine
- assign: assign a value received from the execution engine to a variable in the working memory
- store: transfer the value of a variable in the working memory to the main memory
- write: executed after store, put the value obtained by store into the variable in main memory
- lock: variables acting on main memory
- unlock

### Three major features of the memory model

#### 1. Atomicity

The Java memory model ensures that read, load, use, assign, store, write, lock and unlock operations are atomic. For example, if an assign operation is performed on an int type variable, this operation is atomic. However, the Java memory model allows the virtual machine to divide the read and write operations of 64-bit data (long, double) that are not modified by volatile into two 32-bit operations, that is, the load, store, read and write operations do not need to be atomic.

There is a misunderstanding that atomic types such as int will not cause thread safety issues in a multi-threaded environment. In the previous thread-unsafe sample code, cnt is an int type variable. After 1000 threads in
crement it, the value obtained is 997 instead of 1000.

For the convenience of discussion, the interaction operations between memories are simplified into three: load, assign, and store.

The figure below demonstrates that two threads operate cnt at the same time. The series of operations of load, assign, and store are not atomic as a whole.
, then after T1 modifies cnt and the modified value has not been written to the main memory, T2 can still read the old value. It can be seen that although these two threads performed two auto-increment operations, the value of cnt in the main memory ended up being 1 instead of 2. Therefore, the atomicity of read and write operations of the int type only means that the individual operations of load, assign, and store are atomic.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2797a609-68db-4d7b-8701-41ac9a34b14f.jpg" width="300px"> </div><br>

AtomicInteger can guarantee the atomicity of modifications by multiple threads.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/dd563037-fcaa-4bd8-83b6-b39d93a12c77.jpg" width="300px"> </div><br>

After rewriting the previous thread-unsafe code using AtomicInteger, we got the following thread-safe implementation:

```java
public class AtomicExample {
    private AtomicInteger cnt = new AtomicInteger();

    public void add() {
        cnt.incrementAndGet();
    }

    public int get() {
        return cnt.get();
    }
}
```

```java
public static void main(String[] args) throws InterruptedException {
    final int threadSize = 1000;
    AtomicExample example = new AtomicExample(); // Only modify this statement
    final CountDownLatch countDownLatch = new CountDownLatch(threadSize);
    ExecutorService executorService = Executors.newCachedThreadPool();
    for (int i = 0; i < threadSize; i++) {
        executorService.execute(() -> {
            example.add();
            countDownLatch.countDown();
        });
    }
    countDownLatch.await();
    executorService.shutdown();
    System.out.println(example.get());
}
```

```html
1000
```

In addition to using atomic classes, you can also use synchronized mutex locks to ensure the atomicity of operations. Its corresponding inter-memory interaction operations are: lock and unlock, and the corresponding bytecode instructions in virtual machine implementation are monitorenter and monitorexit.

```java
public class AtomicSynchronizedExample {
    private int cnt = 0;

    public synchronized void add() {
        cnt++;
    }

    public synchronized int get() {
        return cnt;
    }
}
```

```java
public static void main(String[] args) throws InterruptedException {
    final int threadSize = 1000;
    AtomicSynchronizedExample example = new AtomicSynchronizedExample();
    final CountDownLatch countDownLatch = new CountDownLatch(threadSize);
    ExecutorService executorService = Executors.newCachedThreadPool();
    for (int i = 0; i < thre
adSize; i++) {
        executorService.execute(() -> {
            example.add();
            countDownLatch.countDown();
        });
    }
    countDownLatch.await();
    executorService.shutdown();
    System.out.println(example.get());
}
```

```html
1000
```

#### 2. Visibility

Visibility means that when one thread modifies the value of a shared variable, other threads can immediately learn about the modification. The Java memory model achieves visibility by synchronizing the new value back to main memory after the variable is modified, and refreshing the variable value from main memory before the variable is read.

There are three main ways to achieve visibility:

- volatile
- synchronized, before performing an unlock operation on a variable, the variable value must be synchronized back to the main memory.
- final. Once the field modified by the final keyword is initialized in the constructor and no this escape occurs (other threads access the half-initialized object through this reference), then other threads can see the value of the final field.

Using volatile to modify the cnt variable in the previous thread-unsafe example cannot solve the thread-unsafe problem, because volatile does not guarantee the atomicity of the operation.

#### 3. Orderliness

Orderliness means: observed within this thread, all operations are ordered. When one thread observes another thread, all operations are out of order. The disorder is due to instruction reordering. In the Java memory model, the compiler and processor are allowed to reorder instructions. The reordering process will not affect the execution of single-threaded programs, but will affect the correctness of multi-threaded concurrent execution.

The volatile keyword prohibits instruction reordering by adding a memory barrier, that is, subsequent instructions cannot be placed before the memory barrier during reordering.

Orderliness can also be ensured through synchronized, which ensures that only one thread executes synchronization code at each moment, which is equivalent to letting threads execute synchronization code sequentially.

### Principle of occurrence first

As mentioned above, volatile and synchronized can be used to ensure orderliness. In addition, the JVM also stipulates the principle of occurrence first, allowing one operation to precede another without control.
The operation is complete.

#### 1. Single thread principle

> Single Thread rule

Within a thread, operations at the front of the program occur before operations at the back.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/874b3ff7-7c5c-4e7a-b8ab-a82a3e038d20.png" width="180px"> </div><br>

#### 2. Monitor locking rules

> Monitor Lock Rule

An unlock operation occurs before a subsequent lock operation on the same lock.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8996a537-7c4a-4ec8-a3b7-7ef1798eae26.png" width="350px"> </div><br>

#### 3.
Volatile variable rules

> Volatile Variable Rule

A write operation to a volatile variable occurs before a subsequent read operation to the variable.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/942f33c9-8ad9-4987-836f-007de4c21de0.png" width="400px"> </div><br>

#### 4. Thread startup rules

> Thread Start Rule

The Thread object's start() method call precedes every action that occurs on this thread.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6270c216-7ec0-4db7-94de-0003bce37cd2.png" width="380px"> </div><br>

#### 5. Thread joining rules

> Thread Join Rule

The end of the Thread object occurs before the join() method returns.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/233f8d89-31d7-413f-9c02-042f19c46ba1.png" width="400px"> </div><br>

#### 6. Thread interruption rules

> Thread Interruption Rule

The call to the thread's interrupt() method first occurs when the code of the interrupted thread detects the occurrence of an interrupt event. You can use the interrupted() method to detect whether an interrupt occurs.

#### 7. Object termination rules

> Finalizer Rule

The completion of initialization of an object (the end of constructor execution) occurs first at the beginning of its finalize() method.

#### 8. Transitivity

> Transitivity

If operation A happens before operation B, and operation B happens before operation C, then operation A happens before operation C.

## 11. Thread safety

Multiple threads can exhibit correct behavior no matter how they access a class, and no synchronization is required in the main calling code.

Thread safety has the following implementation methods:

### Immutable

Immutable objects must be thread-safe and do not need to take any thread-safety measures. As long as an immutable object is constructed correctly, you will never see it in an inconsistent state across multiple threads. In a multi-threaded environment, objects should be made immutable as much as possible to ensure thread safety.

Immutable types:

- Basic data type modified by final keyword
-String
- enumeration type
- Some subclasses of Number, such as numeric packaging types such as Long and Double, and large data types such as BigInteger and BigDecimal. But the atomic classes AtomicInteger and AtomicLong, both Number, are mutable.

For collection types, you can use the Collections.unmodifiableXXX() method to obtain an immutable collection.

```java
public class ImmutableExample {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();
        Map<String, Integer> unmodifiableMap = Collections.unmodifiableMap(map);
        unmodifiableMap.put("a", 1);
    }
}
```

```html
Exception in thread "main" java.lang.UnsupportedOperationException
    at java.util.Collections$UnmodifiableMap.put(Collections.java:1457)
    at ImmutableExample.main(ImmutableExample.java:9)
```

Col
lections.unmodifiableXXX() first copies the original collection, and any method that needs to modify the collection will directly throw an exception.

```java
public V put(K key, V value) {
    throw new UnsupportedOperationException();
}
```

### Mutually exclusive synchronization

synchronized and ReentrantLock.

### Non-blocking synchronization

The main problem of mutually exclusive synchronization is the performance problem caused by thread blocking and waking up, so this kind of synchronization is also called blocking synchronization.

Mutually exclusive synchronization is a pessimistic concurrency strategy. It is always believed that as long as correct synchronization measures are not taken, problems will definitely occur. Regardless of whether there is competition for shared data, it must perform operations such as locking (discussed here is a conceptual model, in fact the virtual machine optimizes a large part of unnecessary locking), user mode core mode conversion, maintaining lock counters and checking whether there are blocked threads that need to be awakened.

With the development of hardware instruction sets, we can use an optimistic concurrency strategy based on conflict detection: perform the operation first, and if no other threads compete for shared data, the operation is successful, otherwise compensation measures are taken (continuously retry until successful). Many implementations of this optimistic concurrency strategy do not require threads to be blocked, so this synchronization operation is called non-blocking synchronization.

#### 1.CAS

Optimistic locking requires the two steps of operation and conflict detection to be atomic. Mutex synchronization can no longer be used to ensure this, and it can only be accomplished by hardware. The most typical atomic operation supported by hardware is: Compare-and-Swap (CAS). The CAS instruction requires 3 operands, namely memory address V, old
Expected value A and new value B. When the operation is performed, the value of V is updated to B only if the value of V is equal to A.

#### 2. AtomicInteger

The method of the integer atomic class AtomicInteger in the J.U.C package calls the CAS operation of the Unsafe class.

The following code uses AtomicInteger to perform an increment operation.

```java
private AtomicInteger cnt = new AtomicInteger();

public void add() {
    cnt.incrementAndGet();
}
```

The following code is the source code of incrementAndGet(), which calls Unsafe's getAndAddInt().

```java
public final int incrementAndGet() {
    return unsafe.getAndAddInt(this, valueOffset, 1) + 1;
}
```

The following code is the source code of getAndAddInt(). var1 indicates the object memory address, var2 indicates the offset of the field relative to the object memory address, and var4 indicates the value that needs to be added for the operation, which is 1 here. Get the old expected value through getIntVolatile(var1, var2), and perform CAS comparison by calling compareAndSwapInt()
. If the value in the memory address of this field is equal to var5, then update the variable with the memory address var1+var2 to var5+var4.

You can see that getAndAddInt() is performed in a loop. If a conflict occurs, it is constantly retried.

```java
public final int getAndAddInt(Object var1, long var2, int var4) {
    int var5;
    do {
        var5 = this.getIntVolatile(var1, var2);
    } while(!this.compareAndSwapInt(var1, var2, var5, var5 + var4));

    return var5;
}
```

#### 3. ABA

If a variable is first read with value A, its value is changed to B, and then changed back to A, then the CAS operation will mistakenly think that it has never been changed.

The J.U.C package provides a marked atomic reference class AtomicStampedReference to solve this problem, which can ensure the correctness of CAS by controlling the version of the variable value. In most cases, ABA problems will not affect the correctness of program concurrency. If you need to solve ABA problems, switching to traditional mutually exclusive synchronization may be more efficient than atomic classes.

### No synchronization solution

To ensure thread safety, synchronization is not necessarily necessary. If a method does not involve sharing data, then it naturally does not require any synchronization measures to ensure correctness.

#### 1. Stack closure

When multiple threads access local variables of the same method, thread safety problems will not occur because local variables are stored in the virtual machine stack and are thread-private.

```java
public class StackClosedExample {
    public void add100() {
        int cnt = 0;
        for (int i = 0; i < 100; i++) {
            cnt++;
        }
        System.out.println(cnt);
    }
}
```

```java
public static void main(String[] args) {
    StackClosedExample example = new StackClosedExample();
    ExecutorService executorService = Executors.newCachedThreadPool();
    executorService.execute(() -> example.add100());
    executorService.execute(() -> example.add100());
    executorService.shutdown();
}
```

```html
100
100
```

#### 2. Thread Local Storage

If the data required in a piece of code must be shared with other code, then see if the code that shares the data can be guaranteed to execute in the same thread. If it can be guaranteed, we can limit the visible range of shared data to the same thread. In this way, we can ensure that there is no data contention problem between threads without synchronization.

Applications that meet this characteristic are not uncommon. Most architectural patterns that use consumption queues (such as the "producer-consumer" pattern) will try to consume the product in one thread. One of the most important application examples is the "Thread-per-Request" processing method in the classic Web interaction model. The widespread application of this processing method allows many Web server-side applications to use thread local storage to solve thread safety issues.

Thread local storage f
unctionality can be implemented using the java.lang.ThreadLocal class.

For the following code, threadLocal is set to 1 in thread1 and threadLocal is set to 2 in thread2. After a while, thread1 reads threadLocal and it is still 1, which is not affected by thread2.

```java
public class ThreadLocalExample {
    public static void main(String[] args) {
        ThreadLocal threadLocal = new ThreadLocal();
        Thread thread1 = new Thread(() -> {
            threadLocal.set(1);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println(threadLocal.get());
            threadLocal.remove();
        });
        Thread thread2 = new Thread(() -> {
            threadLocal.set(2);
            threadLocal.remove();
        });
        thread1.start();
        thread2.start();
    }
}
```

```html
1
```
In order to understand ThreadLocal, first look at the following code:

```java
public class ThreadLocalExample1 {
    public static void main(String[] args) {
        ThreadLocal threadLocal1 = new ThreadLocal();
        ThreadLocal threadLocal2 = new ThreadLocal();
        Thread thread1 = new Thread(() -> {
            threadLocal1.set(1);
            threadLocal2.set(1);
        });
        Thread thread2 = new Thread(() -> {
            threadLocal1.set(2);
            threadLocal2.set(2);
        });
        thread1.start();
        thread2.start();
    }
}
```

The corresponding underlying structure diagram is:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6782674c-1bfe-4879-af39-e9d722a95d39.png" width="500px"> </div><br>

Every Thread has a ThreadLocal.ThreadLocalMap object.

```java
/* ThreadLocal values pertaining to this thread. This map is maintained
 * by the ThreadLocal class. */
ThreadLocal.ThreadLocalMap threadLocals = null;
```

When calling a ThreadLocal's set(T value) method, first obtain the ThreadLocalMap object of the current thread, and then insert the ThreadLocal-\>value key-value pair into the Map.

```java
public void set(T value) {
    Thread t = Thread.currentThread();
    ThreadLocalMap map = getMap(t);
    if (map != null)
        map.set(this, value);
    else
        createMap(t, value);
}
```

The get() method is similar.

```java
public T get() {
    Thread t = Thread.currentThread();
    ThreadLocalMap map = getMap(t);
    if (map != null) {
        ThreadLocalMap.Entry e = map.getEntry(this);
        if (e != null) {
            @SuppressWarnings("unchecked")
            T result = (T)e.value;
            return result;
        }
    }
    return setInitialValue();
}
```

ThreadLocal is not theoretically designed to solve multi-thread concurrency problems because there is no multi-thread competition at all.

In some scenarios (especially when using thread pools), ThreadLocal may have memory leaks due to the underlying data structure of ThreadLocal.ThreadLo
calMap. You should manually call remove() after each use of ThreadLocal as much as possible to avoid ThreadLocal's classic memory leaks or even the risk of causing confusion in your own business.

#### 3. Reentrant Code

This kind of code is also called pure code. It can interrupt the code at any time during its execution and switch to executing another piece of code (including recursively calling itself). After control is returned, the original program will not cause any errors.

Reentrant code has some common characteristics, such as not relying on data stored on the heap and public system resources, all state variables used are passed in as parameters, and non-reentrant methods are not called.

## 12. Lock optimization

The lock optimization here mainly refers to the JVM's optimization of synchronized.

### Spin lock

Mutually exclusive synchronization into the blocking state is very expensive and should be avoided as much as possible. In many applications, shared data is locked for only a short period of time. The idea of ​​a spin lock is to allow a thread to perform a busy loop (spin) for a period of time when requesting a shared data lock. If the lock can be obtained during this period, it can avoid entering the blocking state.

Although the spin lock can avoid entering the blocking state and reduce overhead, it requires a busy loop operation to occupy CPU time. It is only suitable for scenarios where the lock state of shared data is very short.

Adaptive spin locks were introduced in JDK 1.6. Adaptive means that the number of spins is no longer fixed, but is determined by the previous number of spins on the same lock and the status of the lock owner.

### Lock elimination

Lock elimination refers to the elimination of locks on shared data that are detected to be unlikely to have competition.

Lock elimination is mainly supported through escape analysis. If the shared data on the heap cannot escape and be accessed by other threads, then they can be treated as private data, and their locks can be eliminated.

For some code that does not appear to be locked, in fact, many locks are implicitly added. For example, the following string concatenation code implicitly adds a lock:

```java
public static String concatString(String s1, String s2, String s3) {
    return s1 + s2 + s3;
}
```

String is an immutable class, and the compiler will automatically optimize the concatenation of String. Prior to JDK 1.5, this was converted to consecutive append() operations on StringBuffer objects:

```java
public static String concatString(String s1, String s2, String s3) {
    StringBuffer sb = new StringBuffer();
    sb.append(s1);
    sb.append(s2);
    sb.append(s3);
    return sb.toString();
}
```

There is a synchronized block in every append() method. The virtual machine observes the variable sb and quickly discovers that its dynamic scope is restricted to the concatString() method. That is, any reference to sb never escapes outside the concatString() m
ethod and is inaccessible to other threads, so it can be eliminated.

##
# Lock coarsening

If a series of consecutive operations repeatedly lock and unlock the same object, frequent locking operations will cause performance loss.

The consecutive append() methods in the example code in the previous section fall into this category. If the virtual machine detects that the same object is locked by such a series of fragmented operations, it will expand (coarsen) the locking range to the outside of the entire operation sequence. The sample code in the previous section is extended from before the first append() operation to after the last append() operation, so that it only needs to be locked once.

### Lightweight lock

JDK 1.6 introduced biased locks and lightweight locks, allowing locks to have four states: unlocked, biased, lightweight locked, and inflated.

The following is the memory layout of the HotSpot virtual machine object header. This data is called Mark Word. The tag bits correspond to five states, which are given in the state table on the right. In addition to the marked for gc state, the other four states have been introduced previously.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/bb6a49be-00f2-4f27-a0ce-4ed764bc605c.png" width="500"/> </div><br>

The left side of the figure below is the virtual machine stack of a thread. There is a part of the area called Lock Record, which is created during the lightweight lock operation process and is used to store the Mark Word of the lock object. On the right is a lock object, which contains Mark Word and other information.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/051e436c-0e46-4c59-8f67-52d89d656182.png" width="500"/> </div><br>

Compared with traditional heavyweight locks, lightweight locks use CAS operations to avoid the overhead of heavyweight locks using mutexes. For most locks, there is no competition during the entire synchronization cycle, so there is no need to use mutexes for synchronization. You can first use CAS operations for synchronization. If CAS fails, use mutexes for synchronization instead.

When trying to acquire a lock object, if the lock object is marked 0 01, it means that the lock object is in the unlocked state. At this time, the virtual machine creates a Lock Record in the virtual machine stack of the current thread, and then uses the CAS operation to update the object's Mark Word to the Lock Record pointer. If the CAS operation succeeds, the thread acquires the lock on the object, and the object's Mark Word lock tag changes to 00, indicating that the object is in a lightweight lock state.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/baaa681f-7c52-4198-a5ae-303b9386cf47.png" width="400"/> </div><br>

If the CAS operation fails, the virtual machine will first check whether the object's Mark Word points to the virtual machine stack of th
e current thread. If so, it means that the current thread already owns the lock object, and then it can directly enter the synchronization block to continue execution. Otherwise, it means that the lock object has been preempted by other threads. If more than two threads compete for the same lock, the lightweight lock is no longer effective and needs to be expanded into a heavyweight lock.

### Bias lock

The idea of biased locking is to favor the first thread to acquire the lock object. This thread no longer needs to perform synchronization operations when acquiring the lock, and even CAS operations are no longer needed.

When the lock object is acquired by the thread for the first time, it enters the biased state and is marked as 1 01. At the same time, use the CAS operation to record the thread ID into Mark Word. If the CAS operation is successful, this thread does not need to perform any synchronization operations every time it enters the synchronization block related to this lock.

When another thread tries to acquire this lock object, the bias state ends. At this time, the bias (Revoke Bias) is revoked and returned to the unlocked state or lightweight lock state.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/390c913b-5f31-444f-bbdb-2b88b688e7ce.jpg" width="600"/> </div><br>

## 13. Good practices for multi-threaded development

- Give the thread a meaningful name to make it easier to find bugs.

- Reduce synchronization scope, thereby reducing lock contention. For example, for synchronized, you should try to use synchronized blocks instead of synchronized methods.

- Use synchronization tools more and use wait() and notify() less. First of all, synchronization classes such as CountDownLatch, CyclicBarrier, Semaphore and Exchanger simplify coding operations, while it is difficult to implement complex control flows with wait() and notify(); secondly, these synchronization classes are written and maintained by the best companies, and will continue to be optimized and improved in subsequent JDKs.

- Use BlockingQueue to implement the producer-consumer problem.

- Use more concurrent collections and less use of synchronized collections. For example, you should use ConcurrentHashMap instead of Hashtable.

- Use local variables and immutable classes to ensure thread safety.

- Use a thread pool instead of directly creating threads. This is because creating threads is expensive. Thread pools can effectively utilize limited threads to start tasks.

## References

- BruceEckel. Java Programming Thoughts: 4th Edition [M]. Machinery Industry Press, 2007.
- Zhou Zhiming. In-depth understanding of Java virtual machine [M]. Machinery Industry Press, 2011.
- [Threads and Locks](https://docs.oracle.com/javase/specs/jvms/se6/html/Threads.doc.html)
- [Thread Communication](http://ifeve.com/thread-signaling/#missed_signal)
- [Top 50 Java thread interview questions](http://www.importnew.com/12773.html)
- [BlockingQueue
](http://tutorials.jenkov.com/java-util-concurrent/blockingqueue.html)
- [thread state java](https://stackoverflow.com/questions/11265289/thread-state-java)
- [CSC 456 Spring 2012/ch7 MN](http://wiki.expertiza.ncsu.edu/index.php/CSC_456_Spring_2012/ch7_MN)
- [Java - Understanding Happens-before relationship](https://www.logicbig.co
m/tutorials/core-java-tutorial/java-multi-threading/happens-before.html)
- [6장 Thread Synchronization](https://www.slideshare.net/novathinker/6-thread-synchronization)
- [How is Java's ThreadLocal implemented under the hood?](https://stackoverflow.com/questions/1202444/how-is-javas-threadlocal-implemented-under-the-hood/15653015)
- [Concurrent](https://sites.google.com/site/webdevelopart/21-compile/06-java/javase/concurrent?tmpl=%2Fsystem%2Fapp%2Ftemplates%2Fprint%2F&showPrintDialog=1)
- [JAVA FORK JOIN EXAMPLE](http://www.javacreed.com/java-fork-join-example/ "Java Fork Join Example")
- [聊聊并发（八）——Fork/Join 框架介绍](http://ifeve.com/talk-concurrency-forkjoin/)
- [Eliminating SynchronizationRelated Atomic Operations with Biased Locking and Bulk Rebiasing](http://www.oracle.com/technetwork/java/javase/tech/biasedlocking-oopsla2006-preso-150106.pdf)
