#Java virtual machine
<!-- GFM-TOC -->
* [Java Virtual Machine](#java-Virtual Machine)
    * [1. Runtime data area](#一runtime data area)
        * [Program Counter](#program counter)
        * [Java virtual machine stack](#java-virtual machine stack)
        * [Local method stack](#local method stack)
        * [Heap](#Heap)
        * [Method area](#method area)
        * [Runtime Constant Pool](#Runtime Constant Pool)
        * [Direct memory](#direct memory)
    * [2. Garbage Collection](#二garbage collection)
        * [Judge whether an object can be recycled](#Judge whether an object can be recycled)
        * [Reference type](#reference type)
        * [Garbage Collection Algorithm](#garbage collection algorithm)
        * [Garbage Collector](#garbage collector)
    * [3. Memory allocation and recycling strategy](#三Memory allocation and recycling strategy)
        * [Minor GC and Full GC](#minor-gc-and-full-gc)
        * [Memory allocation strategy](#memory allocation strategy)
        * [Full GC trigger conditions](#full-gc-trigger conditions)
    * [Four. Class loading mechanism](#Four classes loading mechanism)
        * [Class life cycle](#Class life cycle)
        * [Class loading process](#class loading process)
        * [Class initialization timing](#Class initialization timing)
        * [Class and class loader](#class and class loader)
        * [Class loader classification](#class loader classification)
        * [Parental delegation model](#parental delegationmodel)
        * [Custom class loader implementation](#Custom class loader implementation)
    * [References](#references)
<!-- GFM-TOC -->


Most of the content of this article refers to **Zhou Zhiming's "In-depth Understanding of Java Virtual Machine"**. If you want to study in depth, please read the original book.

## 1. Runtime data area

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5778d113-8e13-4c53-b5bf-80
1e58080b97.png" width="400px"> </div><br>

### Program counter

Record the address of the virtual machine bytecode instruction being executed (null if a native method is being executed).

### Java virtual machine stack

When each Java method is executed, a stack frame is created to store information such as local variable tables, operand stacks, and constant pool references. The process from method invocation to completion of execution corresponds to the process of pushing and popping a stack frame into the Java virtual machine stack.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8442519f-0b4d-48f4-8229-56f984363c69.png" width="400px"> </div><br>

You can specify the Java virtual machine stack memory size of each thread through the -Xss virtual machine parameter. The default is 256K in JDK 1.4, and the default is 1M in JDK 1.5+:

```java
java -Xss2M HackTheJava
```

This area may throw the following exceptions:

- When the stack depth requested by the thread exceeds the maximum value, a StackOverflowError exception will be thrown;
- If sufficient memory cannot be applied for when the stack is dynamically expanded, an OutOfMemoryError exception will be thrown.

### Local method stack

The local method stack is similar to the Java virtual machine stack. The only difference between them is that the local method stack serves local methods.

Native methods are generally written in other languages (C, C++ or assembly language, etc.) and compiled into programs based on the native hardware and operating system. These methods require special treatment.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/66a6899d-c6b0-4a47-8569-9d08f0baf86c.png" width="300px"> </div><br>

### Heap

This is where all objects are allocated memory and is the main area for garbage collection (the "GC heap").

Modern garbage collectors basically use generational collection algorithms. The main idea is to adopt different garbage collection algorithms for different types of objects. The heap can be divided into two pieces:

- Young Generation
-Old Gene
ratio)

The heap does not require contiguous memory, and its memory can be dynamically increased. Failure to increase will throw an OutOfMemoryError exception.

You can specify the heap memory size of a program through the two virtual machine parameters -Xms and -Xmx. The first parameter sets the initial value, and the second parameter sets the maximum value.

```java
java -Xms1M -Xmx2M HackTheJava
```

### Method area

Used to store loaded class information, constants, static variables, code compiled by the just-in-time compiler and other data.

Like the heap, it does not require continuous memory and can be dynamically expanded. If dynamic expansion fails, an OutOfMemoryError exception will be thrown.

The main goal of garbage collection in this area is to recycle the constant pool and uninstall classes, but it is generally difficult to achieve.

The HotSpot virtual machine treats it as a permanent generation for garbage collection. But it is difficult to determine the size of the permanent generation because it is affected by many factors and the size of the permanent generation will change after every Full GC, so OutOfMemoryError exceptions are often thrown. To make it easier to manage the method area, starting with JDK 1.8, the permanent generation is removed and the method area is moved to the metaspace, which is located in local memory instead of virtual machine memory.

The method area is a JVM specification, and the permanent generation and metaspace are both its implementation methods. After JDK 1.8, the original permanent generation data was divided into the heap and metaspace. Metaspace stores metainformation of classes, static variables, constant pools, etc. into the heap.

### Runtime constant pool

The runtime constant pool is part of the method area.

The constant pool (literal and symbolic references generated by the compiler) in the Class file will be placed in this area after the class is loaded.

In addition to constants generated at compile time, dynamic generation is also allowed, such as intern() of the String class.

### Direct memory

The NIO class was newly introduced in JDK 1.4, which can use the Native function library to directly allocate off-heap memory, and then operate through the DirectByteBuffer object in the Java heap as a reference to this memory. This can significantly improve performance in some scenarios because it avoids copying data back and forth between heap memory and off-heap memory.

## 2. Garbage collection

Garbage collection is mainly performed on the heap and method area. The three areas of the program counter, virtual machine stack and local method stack are private to the thread and only exist during the life cycle of the thread. They will disappear after the thread ends, so there is no need to perform garbage collection on these three areas.

### Determine whether an object can be recycled

#### 1. Reference counting algorithm

Add a reference counter to the object. When the object adds a reference, the counter increases by 1. When the reference expires, the counter increases by 1.
Decrement the counter by 1. Objects with a reference count of 0 can be recycled.

In the case of a circular reference between two objects, the reference counter will never be 0, causing them to be unable to be recycled. It is precisely because of the existence of circular references that the Java virtual machine does not use a reference counting algorithm.

```java
public class Test {

    public Object instance = null;

    public static void main(String[] args) {
        Test a = new Test();
        Test b = new Test();
        a.instance = b;
        b.instance = a;
        a = null;
        b = null;
        doSomething();
    }
}
```

In the above code, the object instances referenced by a and b hold object references to each other. Therefore, after we remove the references to the a object and the b object, the two Test objects cannot be recycled because the two objects still have references to each other.

#### 2. Reachability analysis algorithm

Using GC Roots as the starting point for searching, reachable objects are alive, and unreachable objects can be recycled.

The Java virtual machine uses this algorithm to determine whether an object can be recycled. GC Roots generally include the following:

- Objects referenced in the local variable table in the virtual machine stack
- Objects referenced in JNI in the native method stack
- Objects referenced by class static properties in the method area
- Objects referenced by constants in the method area

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/83d909d2-3858-4fe1-8ff4-16471db0b180.png" width="350px"> </div><br>


#### 3. Recycling of method area

Because the method area mainly stores permanent generation objects, and the recycling rate of permanent generation objects is much lower than that of the new generation, recycling in the method area is not cost-effective.

Mainly the recycling of the constant pool and the unloading of classes.

In order to avoid memory overflow, virtual machines need to have class offloading capabilities in scenarios where reflection and dynamic proxies are used extensively.

There are many conditions for uninstalling a class, and the following three conditions need to be met, and if the conditions are met, they may not be uninstalled:

- All instances of this class have been returned
Collect, there is no instance of this class in the heap at this time.
- The ClassLoader that loaded this class has been recycled.
- The Class object corresponding to this class is not referenced anywhere, so the class method cannot be accessed through reflection anywhere.

#### 4. finalize()

C++-like destructor for closing external resources. However, try-finally and other methods can do better, and this method is very expensive to run, has high uncertainty, and cannot guarantee the calling order of each object, so it is best not to use it.

When an object can be recycled, if the finalize() method of the object needs to be executed, it is possible to re-reference the object in this method to achieve self-rescue. Self-rescue can only be performed once. If the recycled object has previously called the finalize() method to save itself, this method will not be called again when it is recycled later.

### Reference type

Whether it is to determine the number of references to an object through a reference counting algorithm or to determine whether an object is reachable through a reachability analysis algorithm, determining whether an object can be recycled is related to references.

Java provides four reference types with different strengths.

#### 1. Strong reference

Objects associated with strong references will not be recycled.

Use new to create a new object to create a strong reference.

```java
Object obj = new Object();
```

#### 2. Soft reference

Objects associated with soft references will only be recycled when there is insufficient memory.

Use the SoftReference class to create soft references.

```java
Object obj = new Object();
SoftReference<Object> sf = new SoftReference<Object>(obj);
obj = null; // Make the object only associated with soft references
```

#### 3. Weak reference

The object associated with a weak reference will definitely be recycled, which means that it can only survive until the next garbage collection occurs.

Use the WeakReference class to create weak references.

```java
Object obj = new Object();
WeakReference<Object> wf = new WeakReference<Object>(obj);
obj = null;
```

#### 4. Virtual reference

Also known as ghost reference or phantom reference, whether an object has a virtual reference will not affect its survival time, and an object cannot be obtained through a virtual reference.

The only purpose of setting a virtual reference to an object is to receive a system notification when the object is recycled.
Use PhantomReference to create phantom references.

```java
Object obj = new Object();
PhantomReference<Object> pf = new PhantomReference<Object>(obj, null);
obj = null;
```

### Garbage collection algorithm

#### 1. Mark - Clear

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/005b481b-502b-4e3f-985d-d043c2b330aa.png" width="400px"> </div><br>

In the marking phase, the program checks whether each object is a live object. If it is a live object, the program puts a mark on the head of the object.

In the clearing phase, the object will be recycled and the flag bit will be cancelled. In addition, it will also be judged whether the recycled block is continuous with the previous free block. If so, the two blocks will be merged. Recycling an object is to treat the object as a block and connect it to a one-way linked list called the "free linked list". When allocating later, you only need to traverse this free linked list to find the block.

When allocating, the program will search the free linked list to find a block with space greater than or equal to the size of the new object. If the block it finds is equal to size, it will directly return the block; if the block it finds is larger than size, it will split the block into two parts of size and (block - size), return a block of size, and return a block of size (block - size) to the free list.

Disadvantages:

- The marking and clearing processes are inefficient;
- A large number of discontinuous memory fragments will be generated, resulting in the inability to allocate memory for large objects.

#### 2. Mark - Organize

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ccd773a5-ad38-4022-895c-7ac318f31437.png" width="400px"> </div><br>

Let all living objects move to one end, and then directly clean up the memory outside the end boundary.

Advantages:

- No memory fragmentation

Disadvantages:

- A large number of objects need to be moved, and the processing efficiency is relatively low.

#### 3. Copy

<div align=
"center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b2b77b9e-958c-4016-8ae5-9c6edd83871e.png" width="400px"> </div><br>

Divide the memory into two blocks of equal size, and only use one block at a time. When this block of memory is used up, copy the surviving objects to the other block, and then clean up the used memory space.

The main drawback is that only half of the memory is used.

Today's commercial virtual machines all use this collection algorithm to recycle the new generation, but it is not divided into two equal-sized blocks, but one larger Eden space and two smaller Survivor spaces. Each time Eden and one of the Survivor spaces are used. During recycling, copy all surviving objects in Eden and Survivor to another Survivor, and finally clean up Eden and the used Survivor.

The default Eden and Survivor size ratio of the HotSpot virtual machine is 8:1, ensuring that the memory utilization reaches 90%. If more than 10% of the objects survive each recycling, then one Survivor is not enough. At this time, you need to rely on the old generation for space allocation guarantee, that is, borrowing the space of the old generation to store objects that cannot be accommodated.

#### 4. Generational collection

Today's commercial virtual machines use a generational collection algorithm, which divides the memory into several blocks according to the object survival cycle, and uses appropriate collection algorithms for different blocks.

The heap is generally divided into the new generation and the old generation.

- New generation use: replication algorithm
- Old generation uses: mark-clear or mark-organize algorithm

### Garbage Collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c625baa0-dde6-449e-93df-c3a67f2f430f.jpg" width=""/> </div><br>

The above are the 7 garbage collectors in the HotSpot virtual machine. The connections indicate that the garbage collectors can be used together.

-Single-threaded and multi-threaded: Single-threaded means that the garbage collector only uses one thread, while multi-threaded uses multiple threads;
- Serial and parallel: Serial means that the garbage collector and the user program are executed alternately, which means that the user program needs to be paused when performing garbage collection; parallel means that the garbage collector and the user program are executed at the same time. Apart from
Except for CMS and G1, other garbage collectors are executed in a serial manner.

#### 1. Serial collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/22fda4ae-4dd5-489d-ab10-9ebfdad22ae0.jpg" width=""/> </div><br>

Serial translates to serial, which means it executes in a serial manner.

It is a single-threaded collector and only uses one thread for garbage collection.

Its advantage is that it is simple and efficient. In a single CPU environment, since there is no overhead of thread interaction, it has the highest single-thread collection efficiency.

It is the default new generation collector in the Client scenario, because the memory in this scenario is generally not very large. The pause time for collecting one to two hundred megabytes of garbage can be controlled within more than a hundred milliseconds. As long as it is not too frequent, this pause time is acceptable.

#### 2. ParNew collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/81538cd5-1bcf-4e31-86e5-e198df1e013b.jpg" width=""/> </div><br>

It is a multi-threaded version of the Serial collector.

It is the default new generation collector in the Server scenario. In addition to performance reasons, it is mainly because apart from the Serial collector, it is the only one that can be used with the CMS collector.

#### 3. Parallel Scavenge Collector

Like ParNew, it is a multi-threaded collector.

The goal of other collectors is to shorten the pause time of user threads during garbage collection as much as possible, while its goal is to achieve a controllable throughput, so it is called a "throughput-first" collector. Throughput here refers to the ratio of the time the CPU spends running user programs to the total time.

The shorter the pause time, the more suitable it is for programs that need to interact with users. Good response speed can improve the user experience. High throughput can efficiently utilize CPU time and complete the program's computing tasks as quickly as possible. It is suitable for tasks that are performed in the background and do not require too much interaction.

Shortening the pause time comes at the expense of throughput and new generation space: the new generation space becomes smaller and garbage collection becomes more frequent, resulting in a decrease in throughput.

The GC adaptive adjustment strategy (GC Ergonomic
s), there is no need to manually specify detailed parameters such as the size of the new generation (-Xmn), the ratio of Eden and Survivor areas, and the age of objects promoted to the old generation. The virtual machine collects performance monitoring information based on the current operating conditions of the system and dynamically adjusts these parameters to provide the most appropriate pause time or maximum throughput.

#### 4. Serial Old collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/08f32fd3-f736-4a67-81ca-295b2a7972f2.jpg" width=""/> </div><br>

It is the old generation version of the Serial collector and is also used by virtual machines in Client scenarios. If used in a Server scenario, it has two major uses:

- Used with the Parallel Scavenge collector in JDK 1.5 and earlier (before Parallel Old).
- As a backup plan for the CMS collector, it is used when Concurrent Mode Failure occurs in concurrent collection.

#### 5. Parallel Old collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/278fe431-af88-4a95-a895-9c3b80117de3.jpg" width=""/> </div><br>

Is the old generation version of the Parallel Scavenge collector.

In situations where throughput is important and CPU resources are sensitive, Parallel Scavenge plus Parallel Old collector can be given priority.

#### 6. CMS Collector

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/62e77997-6957-4b68-8d12-bfd609bb2c68.jpg" width=""/> </div><br>

CMS (Concurrent Mark Sweep), Mark Sweep refers to the mark-sweep algorithm.

It is divided into the following four processes:

- initial
Marking: Just marking objects that GC Roots can directly associate with, it is very fast and requires a pause.
- Concurrent marking: The process of GC Roots Tracing, which takes the longest time in the entire recycling process and does not require pauses.
- Re-marking: In order to correct the mark records of that part of the object that has changed due to the continued operation of the user program during concurrent marking, a pause is required.
- Concurrent cleanup: no pauses required.

During the concurrent marking and concurrent cleaning processes, which are the longest in the entire process, the collector thread can work together with the user thread without pausing.

Has the following disadvantages:

- Low throughput: Low pause time comes at the expense of throughput, resulting in insufficient CPU utilization.
- Unable to handle floating garbage, Concurrent Mode Failure may occur. Floating garbage refers to the garbage generated by the user thread continuing to run during the concurrent cleanup phase. This part of garbage can only be recycled during the next GC. Due to the existence of floating garbage, a portion of memory needs to be reserved, which means that CMS collection cannot wait until the old generation is almost full before recycling like other collectors. If the reserved memory is not enough to store floating garbage, Concurrent Mode Failure will occur, and the virtual machine will temporarily enable Serial Old to replace CMS.
- Space fragmentation caused by the mark-clear algorithm often results in remaining space in the old generation, but it is unable to find a large enough continuous space to allocate the current object, and has to trigger a Full GC in advance.

#### 7. G1 Collector

G1 (Garbage-First), which is a garbage collector for server-side applications, has good performance in multi-CPU and large-memory scenarios. The HotSpot development team has given it the mission of replacing the CMS collector in the future.

The heap is divided into the new generation and the old generation. Other collectors collect the entire new generation or the old generation, while G1 can directly collect the new generation and the old generation together.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/4cf711a8-7ab2-4152-b85c-d5c226733807.png" width="600"/> </div><br>

G1 divides the heap into multiple independent regions (Regions) of equal size, and the new generation and the old generation are no longer physically isolated.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-gu
angzhou.myqcloud.com/9bbddeeb-e939-41f0-8e8e-2b1a0aa7e0a7.png" width="600"/> </div><br>

By introducing the concept of Region, the original entire memory space is divided into multiple small spaces, so that each small space can be garbage collected independently. This partitioning method brings a lot of flexibility, making predictable pause time models possible. By recording the garbage collection time of each Region and the space obtained by recycling (these two values ​​are obtained through past recycling experience), and maintaining a priority list, each time based on the allowed collection time, the Region with the greatest value is recycled first.

Each Region has a Remembered Set, which is used to record the Region where the reference object of the Region object is located. By using Remembered Set, you can avoid a full heap scan when doing reachability analysis.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f99ee771-c56f-47fb-9148-c0036695b5fe.jpg" width=""/> </div><br>

If you do not count the operation of maintaining the Remembered Set, the operation of the G1 collector can be roughly divided into the following steps:

- initial mark
- Concurrent marking
- Final marking: In order to correct the part of the mark record that changes due to the continued operation of the user program during concurrent marking, the virtual machine records the object changes during this period in the thread's Remembered Set Logs. The final marking stage needs to merge the data of the Remembered Set Logs into the Remembered Set. This phase requires the thread to be paused, but can be executed in parallel.
- Screening recycling: First sort the recycling value and cost in each Region, and develop a recycling plan based on the GC pause time expected by the user. This stage can actually be executed concurrently with the user program, but because only a part of the Region is recycled, the time is controllable by the user, and pausing the user thread will greatly improve the collection efficiency.

It has the following characteristics:

- Space integration: Overall, the collector is implemented based on the "mark-sort" algorithm. From a local perspective (between two regions), it is implemented based on the "copy" algorithm, which means that no memory space fragmentation will be generated during operation.
- Predictable pause: allows the user to explicitly specify a pause of length
Within a time frame of M milliseconds, no more than N milliseconds may be spent on the GC.

## 3. Memory allocation and recycling strategy

### Minor GC and Full GC

- Minor GC: Recycle the new generation. Because the survival time of the new generation objects is very short, Minor GC will be executed frequently and the execution speed will generally be faster.

- Full GC: Recycle the old generation and the new generation. Old generation objects have a long survival time, so Full GC is rarely executed and the execution speed will be much slower than Minor GC.

### Memory allocation strategy

#### 1. Objects are allocated in Eden first

In most cases, objects are allocated on the new generation Eden. When Eden space is insufficient, Minor GC is initiated.

#### 2. Large objects enter the old generation directly

Large objects refer to objects that require continuous memory space. The most typical large objects are very long strings and arrays.

Often large objects trigger garbage collection early to obtain enough contiguous space to allocate to large objects.

-XX:PretenureSizeThreshold, objects larger than this value are allocated directly in the old generation to avoid large memory copies between Eden and Survivor.

#### 3. Long-term surviving objects enter the old generation

Define an age counter for the object. If the object is born in Eden and still survives the Minor GC, it will be moved to the Survivor, and its age will be increased by 1 year. When it reaches a certain age, it will be moved to the old generation.

-XX:MaxTenuringThreshold is used to define the age threshold.

#### 4. Dynamic object age determination

The virtual machine does not always require that the age of an object must reach MaxTenuringThreshold before it can be promoted to the old generation. If the sum of the sizes of all objects of the same age in the Survivor is greater than half of the Survivor space, objects whose age is greater than or equal to this age can directly enter the old generation without waiting until the age required in MaxTenuringThreshold.

#### 5. Space allocation guarantee

Before Minor GC occurs, the virtual machine first checks whether the maximum available continuous space in the old generation is greater than the total space of all objects in the new generation. If the condition is true, then Minor GC can be confirmed to be safe.

If not, the virtual machine will check whether the value of HandlePromotionFailure allows guarantee failure. If it is allowed, it will continue to check whether the maximum available continuous space in the old generation is greater than the average size of objects promoted to the old generation. If it is greater, it will try to perform a Minor GC; if it is less, or Han
The value of dlePromotionFailure does not allow risks, so a Full GC will be performed.

### Trigger conditions for Full GC

For Minor GC, the triggering condition is very simple. When the Eden space is full, a Minor GC will be triggered. Full GC is relatively complex and has the following conditions:

#### 1. Call System.gc()

It is only recommended that the virtual machine execute Full GC, but the virtual machine may not actually execute it. It is not recommended to use this method, instead let the virtual machine manage the memory.

#### 2. Insufficient space in the old generation

Common scenarios where there is insufficient space in the old generation include large objects directly entering the old generation as mentioned above, long-term surviving objects entering the old generation, etc.

In order to avoid Full GC caused by the above reasons, you should try not to create overly large objects and arrays. In addition, you can use the -Xmn virtual machine parameter to increase the size of the new generation so that objects can be recycled in the new generation and not enter the old generation. You can also use -XX:MaxTenuringThreshold to increase the age at which an object enters the old generation, allowing the object to survive in the new generation for a longer period of time.

#### 3. Space allocation guarantee failed

Minor GC using the copy algorithm requires the memory space of the old generation for guarantee. If the guarantee fails, a Full GC will be executed. Please refer to Section 5 above for details.

#### 4. Insufficient permanent generation space in JDK 1.7 and earlier

In JDK 1.7 and before, the method area in the HotSpot virtual machine is implemented using the permanent generation, which stores some Class information, constants, static variables and other data.

When there are many classes to be loaded, reflected classes, and methods to be called in the system, the permanent generation may be full, and Full GC will be executed even if CMS GC is not configured. If it still cannot be recycled after Full GC, the virtual machine will throw java.lang.OutOfMemoryError.

To avoid Full GC caused by the above reasons, the methods that can be adopted are to increase the permanent generation space or switch to using CMS GC.

#### 5. Concurrent Mode Failure

During the execution of CMS GC, if there are objects that need to be placed into the old generation, and there is insufficient space in the old generation at this time (it may be that there is too much floating garbage during the GC process, causing a temporary lack of space), a Concurrent Mode Failure error will be reported and Full GC will be triggered.

## 4. Class loading mechanism

Classes are dynamically loaded the first time they are used during runtime, rather than loading all classes at once. Because if you load it all at once, it will take up a lot of memory.
### Class life cycle

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/335fe19c-4a76-45ab-9320-88c90d6a0d7e.png" width="600px"> </div><br>

Includes the following 7 stages:

- **Loading**
- **Verification**
- **Preparation**
- **Resolution**
- **Initialization**
-Using
- Unloading

### Class loading process

It includes five stages: loading, verification, preparation, parsing and initialization.

#### 1. Load

Loading is a phase of class loading, be careful not to confuse it.

The loading process does three things:

- Get the binary byte stream that defines a class by its fully qualified name.
- Convert the static storage structure represented by the byte stream into the runtime storage structure of the method area.
- Generate a Class object representing the class in memory, which serves as the access point for various data of the class in the method area.


The binary byte stream can be obtained in the following ways:

- Reading from ZIP packages becomes the basis for JAR, EAR, and WAR formats.
- Obtained from the network, the most typical application is Applet.
- Runtime calculation generation, such as dynamic proxy technology, in java.lang.reflect.Proxy uses ProxyGenerator.generateProxyClass's binary byte stream for the proxy class.
- Generated from other files, such as the corresponding Class class generated from a JSP file.

#### 2. Verification

Ensure that the information contained in the byte stream of the Class file meets the requirements of the current virtual machine and does not endanger the security of the virtual machine itself.

#### 3. Preparation

Class variables are variables modified by static. In the preparation phase, memory is allocated for class variables and initial values are set. The memory in the method area is used.

Instance variables will not be allocated memory at this stage, they will be allocated in the heap along with the object when the object is instantiated. It should be noted that instantiation is not a process of class loading. Class loading occurs before all instantiation operations, and class loading is only performed once, and instantiation can be performed multiple times.

The initial value is generally 0. For example, the following class variable value is initialized to 0 and
Not 123.

```java
public static int value = 123;
```

If the class variable is a constant, it is initialized to the value defined by the expression instead of 0. For example, the constant value below is initialized to 123 instead of 0.

```java
public static final int value = 123;
```

#### 4. Analysis

The process of replacing a symbolic reference to a constant pool with a direct reference.

The parsing process can start after the initialization phase in some cases, in order to support Java's dynamic binding.

#### 5. Initialization

<div data="modify -->"></div>
The initialization phase actually begins to execute the Java program code defined in the class. The initialization phase is the process in which the virtual machine executes the class constructor &lt;clinit\>() method. In the preparation phase, class variables have been assigned an initial value required by the system, and in the initialization phase, class variables and other resources are initialized according to the subjective plan made by the programmer through the program.

&lt;clinit\>() is generated by the compiler automatically collecting the assignment actions of all class variables in the class and merging the statements in the static statement block. The order of the compiler collection is determined by the order in which the statements appear in the source file. Special note is that a static statement block can only access class variables defined before it, and class variables defined after it can only be assigned values ​​and cannot be accessed. For example the following code:

```java
public class Test {
    static {
        i = 0; // Assigning values to variables can be compiled normally.
        System.out.print(i); // This sentence will cause the compiler to prompt "illegal forward reference"
    }
    static int i = 1;
}
```

Since the &lt;clinit\>() method of the parent class is executed first, it means that the execution of the static statement block defined in the parent class takes precedence over the subclass. For example the following code:

```java
static class Parent {
    public static int A = 1;
    static {
        A = 2;
    }
}

static class Sub extends Parent {
    public static int B = A;
}

public static void main(String[] args) {
     System.
out.println(Sub.B); // 2
}
```

Static statement blocks cannot be used in interfaces, but there are still assignment operations for class variable initialization, so interfaces and classes will generate the &lt;clinit\>() method. But the difference between interfaces and classes is that executing the &lt;clinit\>() method of the interface does not require first executing the &lt;clinit\>() method of the parent interface. The parent interface is initialized only when variables defined in the parent interface are used. In addition, the implementation class of the interface will not execute the &lt;clinit\>() method of the interface during initialization.

The virtual machine ensures that the &lt;clinit\>() method of a class is correctly locked and synchronized in a multi-threaded environment. If multiple threads initialize a class at the same time, only one thread will execute the &lt;clinit\>() method of this class, and other threads will block and wait until the active thread completes the execution of the &lt;clinit\>() method. If there are time-consuming operations in the &lt;clinit\>() method of a class, it may cause multiple threads to be blocked. In the actual process, this blocking is very hidden.

### Class initialization timing

#### 1. Active reference

There is no mandatory restriction on when to load in the virtual machine specification, but the specification strictly stipulates that there are and only the following five situations when a class must be initialized (loading, verification, and preparation will all occur):

- When encountering the four bytecode instructions new, getstatic, putstatic, and invokestatic, if the class has not been initialized, its initialization must be triggered first. The most common scenarios where these four instructions are generated are: when using the new keyword to instantiate an object; when reading or setting static fields of a class (except static fields that are final modified and have the results put into the constant pool at compile time); and when calling static methods of a class.

- When using the method of the java.lang.reflect package to make a reflective call to a class, if the class has not been initialized, its initialization needs to be triggered first.

- When initializing a class, if it is found that its parent class has not been initialized, you need to trigger the initialization of its parent class first.

- When the virtual machine starts, the user needs to specify a main class to be executed (the class containing the main() method), and the virtual machine will initialize the main class first;

- When using the dynamic language support of JDK 1.7, if the final parsing result of a java.lang.invoke.MethodHandle instance is a method handle of REF_getStatic, REF_putStatic, REF_invokeStatic, and the class corresponding to this method handle has not been initialized
Initialization, you need to trigger its initialization first;

#### 2. Passive reference

The behavior in the above 5 scenarios is called actively referencing a class. In addition, all methods of referencing a class will not trigger initialization and are called passive references. Common examples of passive references include:

- Referring to the static fields of the parent class through the subclass will not cause the subclass to be initialized.

```java
System.out.println(SubClass.value); // value field is defined in SuperClass
```

- Referring to a class through an array definition will not trigger the initialization of this class. This process will initialize the array class, which is a subclass automatically generated by the virtual machine and directly inherited from Object, which contains the properties and methods of the array.

```java
SuperClass[] sca = new SuperClass[10];
```

- Constants will be stored in the constant pool of the calling class during the compilation phase. In essence, they do not directly reference the class that defines the constant, so the initialization of the class that defines the constant will not be triggered.

```java
System.out.println(ConstClass.HELLOWORLD);
```

### Classes and class loaders

For two classes to be equal, the classes themselves must be equal and loaded using the same class loader. This is because each class loader has an independent class namespace.

The equality here includes the return result of the equals() method, isAssignableFrom() method, and isInstance() method of the Class object of the class as true, and also includes the use of the instanceof keyword to determine the object ownership relationship as true.

### Class loader classification

From the perspective of the Java virtual machine, there are only two different class loaders:

- Bootstrap ClassLoader, implemented in C++, is part of the virtual machine itself;

- Loaders for all other classes, implemented in Java, independent of the virtual machine, inheriting from the abstract class java.lang.ClassLoader.

From a Java developer's perspective, class loaders can be divided into more granular categories:

- Bootstrap ClassLoader This type of loader is responsible for loading class libraries stored in the &lt;JRE_HOME\>\lib directory, or in the path specified by the -Xbootclasspath parameter, and recognized by the virtual machine (only recognized by the file name, such as rt.jar, class libraries with inconsistent names will not be loaded even if they are placed in the lib directory).
in virtual machine memory. The startup class loader cannot be directly referenced by Java programs. When users write a custom class loader, if they need to delegate the loading request to the startup class loader, they can directly use null instead.

- Extension ClassLoader This class loader is implemented by ExtClassLoader (sun.misc.Launcher$ExtClassLoader). It is responsible for loading all class libraries in <JAVA_HOME\>/lib/ext or the path specified by the java.ext.dir system variable into memory. Developers can directly use the extension class loader.

- Application ClassLoader (Application ClassLoader) This class loader is implemented by AppClassLoader (sun.misc.Launcher$AppClassLoader). Since this class loader is the return value of the getSystemClassLoader() method in ClassLoader, it is generally called the system class loader. It is responsible for loading the class library specified on the user class path (ClassPath). Developers can use this class loader directly. If the application has not customized its own class loader, this is generally the default class loader in the program.

### Parental delegation model

The application uses three class loaders to cooperate with each other to implement class loading. In addition, you can also add your own defined class loader.

The following figure shows the hierarchical relationship between class loaders, called the Parents Delegation Model. This model requires that in addition to the top-level startup class loader, other class loaders must have their own parent class loader. The parent-child relationship here is generally realized through a composition relationship (Composition) rather than an inheritance relationship (Inheritance).

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/0dd2d40a-5b2b-4d45-b176-e75a4cd4bdbf.png" width="500px"> </div><br>

#### 1. Working process

A class loader first forwards the class loading request to the parent class loader and only attempts to load it itself if the parent class loader cannot complete it.

#### 2. Benefits

This allows Java classes to have a hierarchical relationship with priority along with its class loader, thereby unifying the base classes.

For example java.lang
.Object is stored in rt.jar. If you write another java.lang.Object and put it in ClassPath, the program can be compiled and passed. Due to the existence of the parent delegation model, the Object in rt.jar has a higher priority than the Object in ClassPath. This is because the Object in rt.jar uses the startup class loader, while the Object in ClassPath uses the application class loader. The Object in rt.jar has a higher priority, so all Objects in the program are this Object.

#### 3. Implementation

The following is a code snippet of the abstract class java.lang.ClassLoader. The loadClass() method runs as follows: first check whether the class has been loaded, and if not, let the parent class loader load it. A ClassNotFoundException is thrown when the parent class loader fails to load. At this time, try to load it yourself.

```java
public abstract class ClassLoader {
    // The parent class loader for delegation
    private final ClassLoader parent;

    public Class<?> loadClass(String name) throws ClassNotFoundException {
        return loadClass(name, false);
    }

    protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
        synchronized (getClassLoadingLock(name)) {
            // First, check if the class has already been loaded
            Class<?> c = findLoadedClass(name);
            if (c == null) {
                try {
                    if (parent != nul
l) {
                        c = parent.loadClass(name, false);
                    } else {
                        c = findBootstrapClassOrNull(name);
                    }
                } catch (ClassNotFoundException e) {
                    // ClassNotFoundException thrown if class not found
                    // from the non-null parent class loader
                }

                if (c == null) {
                    // If still not found, then invoke findClass in order
                    // to find the class.
                    c = findClass(name);
                }
            }
            if (resolve) {
                resolveClass(c);
            }
            return c;
        }
    }

    protected Class<?> findClass(String name) throws ClassNotFoundException {
        throw new ClassNotFoundException(name);
    }
}
```

### Custom class loader implementation

FileSystemClassLoader in the following code is a custom class loader, inherited from java.lang.ClassLoader, used to load classes on the file system. It first looks up the bytecode file (.class file) of the class on the file system based on the full name of the class, then reads the file content, and finally passes def
ineClass() method to convert these byte codes into instances of the java.lang.Class class.

The loadClass() of java.lang.ClassLoader implements the logic of the parent delegation model. Custom class loaders generally do not rewrite it, but they need to rewrite the findClass() method.

```java
public class FileSystemClassLoader extends ClassLoader {

    private String rootDir;

    public FileSystemClassLoader(String rootDir) {
        this.rootDir = rootDir;
    }

    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] classData = getClassData(name);
        if (classData == null) {
            throw new ClassNotFoundException();
        } else {
            return defineClass(name, classData, 0, classData.length);
        }
    }

    private byte[] getClassData(String className) {
        String path = classNameToPath(className);
        try {
            InputStream ins = new FileInputStream(path);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            int bufferSize = 4096;
            byte[] buffer = new byte[bufferSize];
            int bytesNumRead;
while ((bytesNumRead = ins.read(buffer)) != -1) {
                baos.write(buffer, 0, bytesNumRead);
            }
            return baos.toByteArray();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    private String classNameToPath(String className) {
        return rootDir + File.separatorChar
                + className.replace('.', File.separatorChar) + ".class";
    }
}
```

## 参考资料

- 周志明. 深入理解 Java 虚拟机 [M]. 机械工业出版社, 2011.
- [Chapter 2. The Structure of the Java Virtual Machine](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-2.html#jvms-2.5.4)
- [Jvm memory](https://www.slideshare.net/benewu/jvm-memory)
[Getting Started with the G1 Garbage Collector](http://www.oracle.com/webfolder/technetwork/tutorials/obe/java/G1GettingStarted/index.html)
- [JNI Part1: Java Native Interface Introduction and “Hello World” application](http://electrofriends.com/articles/jni/jni-part1-java-native-interface/)
- [Memory Archite
cture Of JVM(Runtime Data Areas)](https://hackthejava.wordpress.com/2015/01/09/memory-architecture-by-jvmruntime-data-areas/)
- [JVM Run-Time Data Areas](https://www.programcreek.com/2013/04/jvm-run-time-data-areas/)
- [Android on x86: Java Native Interface and the Android Native Development Kit](http://www.drdobbs.com/architecture-and-design/android-on-x86-java-native-interface-and/240166271)
- [In-depth understanding of JVM(2) - GC algorithm and memory allocation strategy](https://crowhawk.github.io/2017/08/10/jvm_2/)
- [In-depth understanding of JVM(3) - 7 types of garbage collectors](https://crowhawk.github.io/2017/08/15/jvm_3/)
- [JVM Internals](http://blog.jamesdbloom.com/JVMInternals.html)
- [Deep dive into Java class loaders](https://www.ibm.com/developerworks/cn/java/j-lo-classloader/index.html#code6)
- [Guide to WeakHashMap in Java](http://www.baeldung.com/java-weakhashmap)
- [Tomcat example source code file (ConcurrentCache.java)](https://alvinalexander.com/java/jwarehouse/apache-tomcat-6.0.16/java/org/apache/el/util/ConcurrentCache.java.shtml)
