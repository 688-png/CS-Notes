# Java Basics
<!-- GFM-TOC -->
* [Java Basics](#java-Basics)
    * [1. Data type](#一data type)
        * [Basic type](#Basic type)
        * [Packaging type](#Packaging type)
        * [cache pool](#cache pool)
    * [二、String](#二string)
        * [Overview](#overview)
        * [Benefits of Immutability](#Benefits of Immutability)
        * [String, StringBuffer and StringBuilder](#string-stringbuffer-and-stringbuilder)
        * [String Pool](#string-pool)
        * [new String("abc")](#new-stringabc)
    * [三、Operation](#三operative)
        * [Parameter transfer](#Parameter transfer)
        * [float and double](#float-and-double)
        * [Implicit type conversion](#implicit type conversion)
        * [switch](#switch)
    * [四、Keywords](#四Keywords)
        * [final](#final)
        * [static](#static)
    * [5. Object universal method](#五object-general method)
        * [Overview](#overview)
        * [equals()](#equals)
        * [hashCode()](#hashcode)
        * [toString()](#tostring)
        * [clone()](#clone)
    *[6.Inheritance](#六 inheritance)
        * [Access Permissions](#Access Permissions)
        * [Abstract Classes and Interfaces](#Abstract Classes and Interfaces)
        * [super](#super)
        * [Rewrite and Overload](#Rewrite and Overload)
    * [Seven, reflection](#七 Reflection)
    * [Eight, abnormality](#八 abnormal)
    * [Nine, generic](#九generic)
    * [十、Note](#十Note)
    * [Eleven, characteristics](#Eleven characteristics)
        * [New features in each version of Java](#java-New features in each version)
        * [The difference between Java and C++](#java-and-c-difference)
        * [JRE or JDK](#jre-or-jdk)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Data type

### Basic types

- byte/8
- char/16
- short/16
-int/32
- float/32
- long/64
-double/64
- boolean/\~

boolean has only two values: true and false. It can be stored in 1 bit, but the specific size is not clearly defined. The JVM will convert boolean type data to int at compile time, using 1 to represent true and 0 to represent false. JVM supports boolean arrays, but it is implemented by reading and writing byte arrays.

- [Primitive Data Types](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html)
- [The Java® Virtual Machine Specification](https://docs.oracle.com/javase/specs/jvms/se8/jvms8.pdf)

### Packaging type

Basic types have corresponding packaging types, and the assignment between basic types and their corresponding packaging types is completed using automatic boxing and unboxing.

```java
Integer x = 2; // Boxing calls Integer.valueOf(2)
int y = x; // Unboxing called X.intValue()
```

- [Autoboxing and Unboxing](https://docs.oracle.com/javase/tutorial/java/data/autoboxing.html)

### Cache pool

The difference between new Integer(123) and Integer.valueOf(123) is:

- new Integer(123) will create a new object every time;
- Integer.valueOf(123) will use the object in the cache pool, and multiple calls will get a re
ference to the same object.

```java
Integer x = new Integer(123);
Integer y = new Integer(123);
System.out.println(x == y); // false
Integer z = Integer.valueOf(123);
Integer k = Integer.valueOf(123);
System.out.println(z == k); // true
```

The implementation of the valueOf() method is relatively simple, that is, first determine whether the value is in the cache pool, and if so, directly return the contents of the cache pool.

```java
public static Integer valueOf(int i) {
    if (i >= IntegerCache.low && i <= IntegerCache.high)
        return IntegerCache.cache[i + (-IntegerCache.low)];
    return new Integer(i);
}
```

In Java 8, the Integer cache pool size defaults to -128\~127.

```java
static final int low = -128;
static final int high;
static final Integer cache[];

static {
    // high value may be configured by property
    int h = 127;
    String integerCacheHighPropValue =
        sun.misc.VM.getSavedProperty("java.lang.Integer.IntegerCache.high");
    if (integerCacheHighPropValue != null) {
        try {
            int i = parseInt(integerCacheHighPropValue);
            i = Math.max(i, 127);
            //Maximum array size
e is Integer.MAX_VALUE
            h = Math.min(i, Integer.MAX_VALUE - (-low) -1);
        } catch(NumberFormatException nfe) {
            // If the property cannot be parsed into an int, ignore it.
        }
    }
    high = h;

    cache = new Integer[(high - low) + 1];
    int j = low;
    for(int k = 0; k < cache.length; k++)
        cache[k] = new Integer(j++);

    // range [-128, 127] must be interned (JLS7 5.1.7)
    assertIntegerCache.high >= 127;
}
```

The compiler will call the valueOf() method during the autoboxing process, so multiple Integer instances with the same value and values within the cache pool range are created using autoboxing, and they will reference the same object.

```java
Integer m = 123;
Integer n = 123;
System.out.println(m == n); // true
```

The buffer pools corresponding to the basic types are as follows:

- boolean values true and false
- all byte values
- short values between -128 and 127
- int values between -128 and 127
- char in the range \u0000 to \u007F

When using the wrapper types corresponding to these basic types, if the value range is within the buffer pool range, you can directly use the objects in the buffer pool.

Among all the numerical buffer pools in jdk 1.8, the Integer buffer pool IntegerCache is very special. The lower bound of this buffer pool is - 128, and the upper bound is 127 by default. However, this upper bound is adjustable. When starting the jvm, specify the size of this buffer pool through -XX:AutoBoxCacheMax=&lt;size&gt;. This option will set a name when the JVM is initialized. java.lang.IntegerCache.high system property, and then when IntegerCache is initialized, the system property will be read to determine the upper bound.

[StackOverflow: Differences between new Integer(123), Integer.valueOf(123) and just 123
](https://stackoverflow.com/qu
estions/9030817/differences-between-new-integer123-integer-valueof123-and-just-123)

## 2. String

### Overview

String is declared final, so it is not inheritable. (Wrapper classes such as Integer cannot be inherited either)

In Java 8, String internally uses char array to store data.

```java
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence {
    /** The value is used for character storage. */
    private final char value[];
}
```

After Java 9, the implementation of the String class uses a byte array to store strings, and uses `coder` to identify which encoding is used.

```java
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence {
    /** The value is used for character storage. */
    private final byte[] value;

    /** The identifier of the encoding used to encode the bytes in {@code value}. */
    private final byte coder;
}
```

The value array is declared final, which means that after the value array is initialized, it cannot reference other arrays. And there is no internal method of String to change the value array, so String can be guaranteed to be immutable.

### Benefits of immutability

**1. Can cache hash values**

Because the hash value of String is often used, for example, String is used as the key of HashMap. The immutable feature makes the hash value immutable, so it only needs to be calculated once.

**2. Need for String Pool**

If a String object has been created, a reference will be obtained from the String Pool. Using String Pool is only possible if String is immutable.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191210004132894.png"/> </div><br>

**3. Security**

String is often used as a parameter, and String immutability ensures that the parameters are immutable. For example, if String is variable as a network connection parameter, then during the network connection process, String is changed, and the party that changes String thinks that it is connected to another host, but the actual situation may not be the case.

**4. Thread safety**

String immutability is inherently thread-safe and can be safely used across multiple threads.

[Program Creek: Why String is immutable in Java?](https://www.programcreek.com/2013/04/why-string-is-immutable-in-java/)

### String, StringBuffer and StringBuilder

**1. Variability**

- String immutable
- StringBuffer and StringBuilder are mutable

**2. Thread safety**

- String is immutable and therefore thread-safe
- StringBuilder is not thread-safe
- StringBuffer is thread-safe and uses synchronized internally for synchronization.

[StackOverflow: String, Str
ingBuffer, and StringBuilder](https://stackoverflow.com/questions/2971315/string-stringbuffer-and-stringbuilder)

### String Pool

The String Constant Pool stores all string literals (literal strings), which are determined at compile time. Not only that, you can also use String's intern() m
ethod to add strings to the String Pool during runtime.

When a string calls the intern() method, if there is already a string in the String Pool that is equal to the string value (use the equals() method to determine), then a reference to the string in the String Pool will be returned; otherwise, a new string will be added to the String Pool and a reference to the new string will be returned.

In the following example, s1 and s2 use new String() to create two new strings, while s3 and s4 obtain the same string reference through the s1.intern() and s2.intern() methods. intern() first puts "aaa" into the String Pool and then returns the string reference, so s3 and s4 refer to the same string.

```java
String s1 = new String("aaa");
String s2 = new String("aaa");
System.out.println(s1 == s2); // false
String s3 = s1.intern();
String s4 = s2.intern();
System.out.println(s3 == s4); // true
```

If you create a string in the form of a literal like "bbb", the string will be automatically put into the String Pool.

```java
String s5 = "bbb";
String s6 = "bbb";
System.out.println(s5 == s6); // true
```

Before Java 7, String Pool was placed in the runtime constant pool, which belonged to the permanent generation. In Java 7, String Pool was moved to the heap. This is because the permanent generation has limited space, which can cause OutOfMemoryError errors in scenarios where strings are used extensively.

- [StackOverflow : What is String interning?](https://stackoverflow.com/questions/10578984/what-is-string-interning)
- [In-depth analysis String#intern](https://tech.meituan.com/in_depth_understanding_string_intern.html)

### new String("abc")

A total of two string objects will be created using this method (provided there is no "abc" string object in the String Pool).

- "abc" is a string literal, so a string object will be created in the String Pool during compilation, pointing to this "abc" string literal;
- Using new will create a string object in the heap.

Create a test class that uses this method to create string objects in its main method.

```java
public class NewStringTest {
    public static void main(String[] args) {
        String s = new String("abc");
    }
}
```

Decompile using javap -verbose and get the following:

```java
// ...
Constant pool:
// ...
   #2 = Class #18 // java/lang/String
   #3 = String #19 // abc
// ...
  #18 = Utf8 java/lang/String
  #19 = Utf8 abc
// ...

  public static void main(java.lang.String[]);
    descriptor: ([Ljava/lang/String;)V
    flags: ACC_PUBLIC, ACC_STATIC
    Code:
      stack=3, locals=2, args_size=1
         0: new #2 // class java/lang/String
         3: dup
         4: ldc #3 // String abc
         6: invokespecial #4 // Method java/lang/String."<init>":(Ljava/lang/String;)V
         9: astore_1
// ...
```

In Constant Pool, #19 stores the string literal "abc", and #3 is the string object of String Pool, which points to the string literal #19. In the main method, line 0: uses new #2 to create a
string object in the heap, and uses ldc #3 to pass the string object in the String Pool as a parameter to the String constructor.

The following is the source code of the String constructor. You can see that when a string object is used as a constructor parameter of another string object, the contents of the value array will not be completely copied, but will point to the same value array.

```java
public String(String original) {
    this.value = original.value;
    this.hash = original.hash;
}
```

## 3. Operation

### Parameter passing

Java parameters are passed into methods by value, not by reference.

In the following code, dog of Dog dog is a pointer, which stores the address of the object. When passing a parameter into a method, you are essentially passing the address of the object into the formal parameter by value.

```java
public class Dog {

    String name;

    Dog(String name) {
        this.name = name;
    }

    String getName() {
        return this.name;
    }

    void set
Name(String name) {
        this.name = name;
    }

    String getObjectAddress() {
        return super.toString();
    }
}
```

Changing the field value of the object in the method will change the field value of the original object because it refers to the same object.

```java
class PassByValueExample {
    public static void main(String[] args) {
        Dog dog = new Dog("A");
        func(dog);
        System.out.println(dog.getName()); // B
    }

    private static void func(Dog dog) {
        dog.setName("B");
    }
}
```

But if the pointer refers to other objects in the method, then the two pointers inside the method and outside the method point to different objects. Changing the content of the object pointed by one pointer has no effect on the object pointed by the other pointer.

```java
public class PassByValueExample {
    public static void main(String[] args) {
        Dog dog = new Dog("A");
        System.out.println(dog.getObjectAddress()); // Dog@4554617c
        func(dog);
        System.out.println(dog.getObjectAddress()); // Dog@4554617c
        System.out.println(dog.getName()); // A
    }

    private static void func(Dog dog) {
        System.out.println(dog.getObjectAddress()); // Dog@4554617c
        dog = new Dog("B");
        System.out.println(dog.getObjectAddress()); // Dog@74a14482
        System.out.println(dog.getName()); // B
    }
}
```

[StackOverflow: Is Java “pass-by-reference” or “pass-by-value”?](https://stackoverflow.com/questions/40480/is-java-pass-by-reference-or-pass-by-value)

### float and double

Java cannot perform downcasting implicitly because this would result in loss of precision.

1.1 literal is of double type, and 1.1 cannot be directly assigned to a float variable because this is a downward conversion.

```java
// float f = 1.1;
```

1.1f literals are of type float.

```java
float f = 1.1f;
```

### Implicit type conversion

Because literal 1 is of type int, which is more precise than type short, t
ype int cannot be implicitly downcast to type short.

```java
short s1 = 1;
// s1 = s1 + 1;
```

But using the += or ++ operator performs an implicit type conversion.

```java
s1 += 1;
s1++;
```

The above statement is equivalent to downward transformation of the calculation result of s1 + 1:

```java
s1 = (short) (s1 + 1);
```

[StackOverflow : Why don't Java's +=, -=, *=, /= compound assignment operators require casting?](https://stackoverflow.com/questions/8710619/why-dont-javas-compound-assignment-operators-require-casting)

### switch

Starting from Java 7, String objects can be used in switch conditional statements.

```java
String s = "a";
switch (s) {
    case "a":
        System.out.println("aaa");
        break;
    case "b":
        System.out.println("bbb");
        break;
}
```

Switch does not support long, float, and double because the original intention of switch is to judge the equality of types with only a few values. If the value is too complex, it is more appropriate to use if.

```java
// long x = 111;
// switch (x) { // Incompatible types. Found: 'long', required: 'char, byte, short, int, Character, Byte, Short, Integer, String, or an enum'
// case 111:
// System.out.println(111);
// break;
// case 222:
// System.out.println(222);
// break;
// }
```

[StackOverflow: Why can't your switch statement data type be long, Java?](https://stackoverflow.com/questions/2676210/why-cant-your-switch-statement-data-type-be-long-java)


## 4. Keywords

### final

**1. Data**

Declare data as constants, which can be compile-time constants or constants that cannot be changed after being initialized at runtime.

- For basic types, final makes the value unchanged;
- For reference types, final makes the reference immutable, so it cannot reference other objects, but the referenced object itself can be modified.

```java
final int x = 1;
// x = 2; // cannot assign value to final variable 'x'
final A y = new A();
y.a = 1;
```

**2
.Method**

Declared methods cannot be overridden by subclasses.

Private methods are implicitly designated as final. If the method defined in the subclass has the same signature as a private method in the base class, then the subclass method does not override the base class method, but defines a new method in the subclass.

**3. Class**

Declared classes are not allowed to be inherited.

### static

**1. Static variables**

- Static variable: Also known as a class variable, which means that this variable belongs to the class. All instances of the class share the static variable and can access it directly through the class name. Static variables only have one copy in memory.
- Instance variable: Every time an instance is created, an instance variable is generated, which lives and dies with the instance.

```java
public class A {

    private int x; // instance variable
    private static int y; // static variable

    public static void main(String[] args) {
        // int x = A.x; // Non-static field 'x' cannot be refere
nced from a static context
        A a = new A();
        int x = a.x;
        int y = A.y;
    }
}
```

**2. Static method**

Static methods exist when the class is loaded and do not depend on any instance. So the static method must have an implementation, which means it cannot be an abstract method.

```java
public abstract class A {
    public static void func1(){
    }
    // public abstract static void func2(); // Illegal combination of modifiers: 'abstract' and 'static'
}
```

You can only access static fields and static methods of the class you belong to. The this and super keywords cannot be included in the method because these two keywords are associated with specific objects.

```java
public class A {

    private static int x;
    private int y;

    public static void func1(){
        int a = x;
        // int b = y; // Non-static field 'y' cannot be referenced from a static context
        // int b = this.y; // 'A.this' cannot be referenced from a static context
    }
}
```

**3. Static statement block**

Static statement blocks are run once when the class is initialized.

```java
public class A {
    static {
        System.out.println("123");
    }

    public static void main(String[] args) {
        A a1 = new A();
        A a2 = new A();
    }
}
```

```html
123
```

**4. Static inner class**

Non-static inner classes depend on instances of outer classes, which means that you need to create an instance of the outer class before you can use this instance to create a non-static inner class. Static inner classes are not required.

```java
public class OuterClass {

    class InnerClass {
    }

    static class StaticInnerClass {
    }

    public static void main(String[] args) {
        // InnerClass innerClass = new InnerClass(); // 'OuterClass.this' cannot be referenced from a static context
        OuterClass outerClass = new OuterClass();
        InnerClass innerClass = outerClass.new InnerClass();
        StaticInnerClass staticInnerClass = new StaticInnerClass();
    }
}
```

Static inner classes cannot access non-static variables and methods of outer classes.

**5. Static guide package**

There is no need to specify ClassName when using static variables and methods, thus simplifying the code, but the readability is greatly reduced.

```java
import static com.xxx.ClassName.*
```

**6. Initialization sequence**

Static variables and static statement blocks take precedence over instance variables and ordinary statement blocks. The initialization order of static variables and static statement blocks depends on their order in the code.

```java
public static String staticField = "static variable";
```

```java
static {
    System.out.println("static statement block");
}
```

```java
public String field = "instance variable";
```

```java
{
    System.out.println("Ordinary statement block");
}
```

The last step is the initialization of the constructor.

```java
public InitialOrderTest() {
    System.out.println("constructor");
}
```

In the case of inheritance, the initialization sequence is:

- Parent class (static variables, static statement blocks)
- Subclasses (static variables, static statement blocks)
- Parent class (instance variables, ordinary statement blocks)
- Parent class (constructor)
- Subclasses (instance variables, ordinary statement blocks)
- Subclass (constructor)

## 5. Object general methods

### Overview

```java

public native int hashCode()

public boolean equals(Object obj)

protected native Object clone() throws CloneNotSupportedException

public String toString()

public final native Class<?> getClass()

protected void finalize() throws Throwable {}

public final native void notify()

public final native void notifyAll()

public final native void wait(long timeout) throws In
interruptedException

public final void wait(long timeout, int nanos) throws InterruptedException

public final void wait() throws InterruptedException
```

### equals()

**1. Equivalence relationship**

For two objects to have an equivalence relationship, the following five conditions need to be met:

Ⅰ Reflexivity

```java
x.equals(x); // true
```

Ⅱ Symmetry

```java
x.equals(y) == y.equals(x); // true
```

Ⅲ Transitivity

```java
if (x.equals(y) && y.equals(z))
    x.equals(z); // true;
```

Ⅳ Consistency

The result of calling equals() method multiple times remains unchanged

```java
x.equals(y) == x.equals(y); // true
```

Ⅴ Comparison with null

Calling x.equals(null) on any object x that is not null returns false

```java
x.equals(null); // false;
```

**2. Equivalence and equality**

- For basic types, == determines whether two values are equal. Basic types do not have an equals() method.
- For reference types, == determines whether two variables refer to the same object, while equals() determines whether the referenced objects are equivalent.

```java
Integer x = new Integer(1);
Integer y = new Integer(1);
System.out.println(x.equals(y)); // true
System.out.println(x == y); // false
```

**3. Implementation**

- Check whether it is a reference to the same object, if so, return true directly;
- Check whether they are of the same type, if not, return false directly;
- Transform the Object object;
- Determine whether each key field is equal.

```java
public class EqualExample {

    private int x;
    private int y;
    private int z;

    public EqualExample(int x, int y, int z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        EqualExample that = (EqualExample) o;

        if (x != that.x) return false;
        if (y != that.y) return false;
        return z == that.z;
    }
}
```

### hashCode()

hashCode() returns a hash value, while equals() is used to determine whether two objects are equivalent. Two objects that are equivalent must have the same hash value, but two objects with t
he same hash value are not necessarily equivalent. This is because the hash value calculation is random, and two objects with different values ​​​​may calculate the same hash value.

The hashCode() method should always be overridden when overriding the equals() method to ensure that the hash values ​​of two equivalent objects are also equal.

Collection classes such as HashSet and HashMap use the hashCode() method to calculate the location where an object should be stored. Therefore, to add an object to these collection classes, the corresponding class needs to implement the hashCode() method.

In the code below, two new equivalent objects are created and added to the HashSet. We want to treat the two objects as the same and only add one object to the collection. However, EqualExample does not implement the hashCode() method, so the hash values ​​of the two objects are different, ultimately causing two equivalent objects to be added to the collection.

```java
EqualExample e1 = new EqualExample(1, 1, 1);
EqualExample e2 = new EqualExample(1, 1, 1);
System.out.println(e1.equals(e2)); // true
HashSet<EqualExample> set = new HashSet<>();
set.add(e1);
set.add(e2);
System.out.println(set.size()); // 2
```

An ideal hash function should have uniformity, that is, unequal objects should be evenly distributed over all possible hash values. This requires the hash function to take the values ​​of all fields into account. Each field can be regarded as a certain bit in R base, and then formed into an R base integer.

R is generally set to 31 because it is an odd prime number. If it is an even number, information will be lost when multiplication overflow occurs, because multiplying by 2 is equivalent to shifting one bit to the left and the leftmost bit is lost. And multiplying a number by 31 can be converted into a shift and subtraction: `31*x == (x<<5)-x`, and the compiler will automatically perform this optimization.

```java
@Override
public int hashCode() {
    int result = 17;
    result = 31 * result + x;
    result = 31 * result + y;
    result = 31 * result + z;
    return result;
}
```

### toString()

By default, the form ToStringExample@4554617c is returned, where the value after @ is the unsigned hexadecimal representation of the hash code.

```java
public class ToStringExample {

    private int number;

    public ToStringExample(int number) {
        this.number = number;
    }
}
```

```java
ToStringExample example = new ToStringExample(123);
System.out.println(example.toString());
```

```html
ToStringExample@4554617c
```

### clone()

**1. cloneable**

clone() is a protected method of Object. It is not public. If a class does not explicitly override clone(), other classes
You cannot directly call the clone() method of this class instance.

```java
public class CloneExample {
    private int a;
    private int b;
}
```

```java
CloneExample e1 = new CloneExample();
// CloneExample e2 = e1.clone(); // 'clone()' has protected access in 'java.lan
g.Object'
```

Overriding clone() results in the following implementation:

```java
public class CloneExample {
    private int a;
    private int b;

    @Override
    public CloneExample clone() throws CloneNotSupportedException {
        return (CloneExample)super.clone();
    }
}
```

```java
CloneExample e1 = new CloneExample();
try {
    CloneExample e2 = e1.clone();
} catch (CloneNotSupportedException e) {
    e.printStackTrace();
}
```

```html
java.lang.CloneNotSupportedException: CloneExample
```

The above throws CloneNotSupportedException because CloneExample does not implement the Cloneable interface.

It should be noted that the clone() method is not a method of the Cloneable interface, but a protected method of Object. The Cloneable interface only stipulates that if a class does not implement the Cloneable interface and calls the clone() method, a CloneNotSupportedException will be thrown.

```java
public class CloneExample implements Cloneable {
    private int a;
    private int b;

    @Override
    public Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}
```

**2. Shallow copy**

The reference types of the copied object and the original object refer to the same object.

```java
public class ShallowCloneExample implements Cloneable {

    private int[] arr;

    public ShallowCloneExample() {
        arr = new int[10];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = i;
        }
    }

    public void set(int index, int value) {
        arr[index] = value;
    }

    public int get(int index) {
        return arr[index];
    }

    @Override
    protected ShallowCloneExample clone() throws CloneNotSupportedException {
        return (ShallowCloneExample) super.clone();
    }
}
```

```java
ShallowCloneExample e1 = new ShallowCloneExample();
ShallowCloneExample e2 = null;
try {
    e2 = e1.clone();
} catch (CloneNotSupportedException e) {
    e.printStackTrace();
}
e1.set(2, 222);
System.out.println(e2.get(2)); // 222
```

**3. Deep copy**

The reference types of the copied object and the original object refer to different objects.

```java
public class DeepCloneExample implements Cloneable {

    private int[] arr;

    public DeepCloneExample() {
        arr = new int[10];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = i;
        }
    }

    public void set(int index, int value) {
        arr[index] = value;
    }

    public int get(int index) {
        return arr[index];
    }

    @Override
    protected DeepCloneExample clone() throws CloneNotSupportedException {
        DeepCloneExample result = (DeepCloneExample) super.clone();
        result.arr = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            result.arr[i] = arr[i];
        }
        return result;
    }
}
```

```java
DeepCloneExample e1 = new DeepCloneExample();
DeepCloneExample e2 = null;
try {
    e2 = e1.clone();
} catch (CloneNotSupportedException e) {
e.printStackTrace();
}
e1.set(2, 222);
System.out.println(e2.get(2)); // 2
```

**4. Alternatives to clone()**

Using the clone() method to copy an object is complex and risky. It will throw
An exception occurs and type conversion is required. The Effective Java book says that it is best not to use clone(). You can use the copy constructor or copy factory to copy an object.

```java
public class CloneConstructorExample {

    private int[] arr;

    public CloneConstructorExample() {
        arr = new int[10];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = i;
        }
    }

    public CloneConstructorExample(CloneConstructorExample original) {
        arr = new int[original.arr.length];
        for (int i = 0; i < original.arr.length; i++) {
            arr[i] = original.arr[i];
        }
    }

    public void set(int index, int value) {
        arr[index] = value;
    }

    public int get(int index) {
        return arr[index];
    }
}
```

```java
CloneConstructorExample e1 = new CloneConstructorExample();
CloneConstructorExample e2 = new CloneConstructorExample(e1);
e1.set(2, 222);
System.out.println(e2.get(2)); // 2
```

## 6. Inheritance

### Access permissions

There are three access modifiers in Java: private, protected and public. If no access modifier is added, it means that the package level is visible.

Access modifiers can be added to classes or members (fields and methods) within a class.

- A class is visible means that other classes can use this class to create instance objects.
- A member is visible means that other classes can access the member using instance objects of this class;

Protected is used to modify members, indicating that the member is visible to subclasses in the inheritance system, but this access modifier has no meaning for the class.

A well-designed module hides all implementation details, clearly isolating its API from its implementation. Modules communicate with each other only through their APIs, and one module does not need to know the inner workings of other modules. This concept is called information hiding or encapsulation. Therefore, access permissions should be as much as possible to prevent each class or member from being accessed by the outside world.

If a subclass method overrides a parent class method, the access level of the method in the subclass is not allowed to be lower than the access level of the parent class. This is to ensure that wherever a parent class instance can be used, a subclass instance can be used instead, that is, to ensure that the Liskov substitution principle is met.

Fields must not be public, because if you do so, you lose control of the modification behavior of this field, and the client can modify it at will. For example, in the following example, AccessExample has the id public field. If at some point, we want to use int to store the id field, then all client code needs to be modified.

```java
public class AccessExample {
    public String
id;
}
```

You can use public getter and setter methods to replace public fields, so you can control the modification behavior of the fields.

```java
public class AccessExample {

    private int id;

    public String getId() {
        return id + "";
    }

    public void setId(String id) {
        this.id = Integer.valueOf(id);
    }
}
```

But there are exceptions. If it is a package-level private class or a private nested class, then directly exposing the members will not have a particularly big impact.

```java
public class AccessWithInnerClassExample {

    private class InnerClass {
        int x;
    }

    private InnerClass innerClass;

    public AccessWithInnerClassExample() {
        innerClass = new InnerClass();
    }

    public int getValue() {
        return innerClass.x; // direct access
    }
}
```

### Abstract classes and interfaces

**1. Abstract class**

Both abstract classes and abstract methods are declared using the abstract keyword. If a class contains abstract methods, the class must be declared abstract.

The biggest difference between abstract classes and ordinary classes is that abstract classes cannot be instantiated and can only be inherited.

```java
public abstract class AbstractClassExample {

    protected int x;
    private int y;

    public abstract void func1();

    public void func2() {
        System.out.println("func2");
    }
}
```

```java
public class AbstractExtendClassExample extends AbstractClassExample {
    @Override
    public void func1() {
        System.out.println("func1");
    }
}
```

```java
// AbstractClassExample ac1 = new AbstractClassExample(); // 'AbstractClassExample' is abstract; cannot be instantiated
AbstractClassExample ac2 = new AbstractExtendClassExample();
ac2.func1();
```

**2. Interface**

An interface is an extension of an abstract class. Before Java 8, it could be regarded as a completely abstract class, which means that it cannot have any method implementation.

Starting from Java 8, interfaces can also have default method implementations. This is because the maintenance cost of interfaces that do not support default methods is too high. Before Java 8, if an interface wanted to add a new method, all classes that implemented the interface had to be modified so that they all implemented the new method.

The members (fields + methods) of the interface are all public by default
, and is not allowed to be defined as private or protected. Starting from Java 9, methods are allowed to be defined as private, so that certain reusable code can be defined without exposing the method.

The fields of the interface are static and final by default.

```java
public interface InterfaceExample {

    void func1();

    default void func2(){
        System.out.println("func2");
    }

    int x = 123;
    // int y; // Variable 'y' might not have been initialized
    public int z = 0; // Modifier 'public' is redundant for interface fields
    // private int k = 0; // Modifier 'private'
not allowed here
    // protected int l = 0; // Modifier 'protected' not allowed here
    // private void fun3(); // Modifier 'private' not allowed here
}
```

```java
public class InterfaceImplementExample implements InterfaceExample {
    @Override
    public void func1() {
        System.out.println("func1");
    }
}
```

```java
// InterfaceExample ie1 = new InterfaceExample(); // 'InterfaceExample' is abstract; cannot be instantiated
InterfaceExample ie2 = new InterfaceImplementExample();
ie2.func1();
System.out.println(InterfaceExample.x);
```

**3. Compare**

- From a design perspective, abstract classes provide an IS-A relationship, which needs to satisfy the Li-style substitution principle, that is, subclass objects must be able to replace all parent class objects. The interface is more like a LIKE-A relationship. It only provides a method to implement the contract and does not require the interface and the class that implements the interface to have an IS-A relationship.
- From a usage perspective, a class can implement multiple interfaces, but cannot inherit multiple abstract classes.
- Fields of interfaces can only be of static and final type, while fields of abstract classes have no such restriction.
- Members of an interface can only be public, while members of an abstract class can have multiple access rights.

**4. Use options**

Use interface:

- It is necessary for unrelated classes to implement a method. For example, unrelated classes can implement the compareTo() method in the Comparable interface;
- Requires the use of multiple inheritance.

Use abstract classes:

- Need to share code among several related classes.
- Need to be able to control access to inherited members, rather than all being public.
- Requires inheritance of non-static and non-const fields.

In many cases, interfaces take precedence over abstract classes. Because interfaces do not have the strict class hierarchy requirements of abstract classes, they can flexibly add behavior to a class. And starting from Java 8, interfaces can also have default method implementations, making the cost of modifying the interface very low.

- [Abstract Methods and Classes](https://docs.oracle.com/javase/tutorial/java/IandI/abstract.html)
- [In-depth understanding of abstract class and interface](https://www.ibm.com/developerworks/cn/java/l-javainterface-abstract/)
- [When to Use Abstract Class and Interface](https://dzone.com/articles/when-to-use-abstract-class-and-intreface)
- [Java 9 Private Methods in Interfaces](https://www.journaldev.com/12850/java-9-private-methods-interfaces)


### super

- Access the constructor of the parent class: You can use the super() function to access the constructor of the parent class, thereby entrusting the parent class to complete some initialization work. It should be noted that the subclass will definitely call the constructor of the parent class to complete the initialization work. Generally, the default constructor of the parent class
is called. If the subclass needs to call other constructors of the parent class, then the super() function can be used.
- Accessing members of the parent class: If a subclass overrides a method of the parent class, it can be achieved by using the super keyword to reference the method of the parent class.

```java
public class SuperExample {

    protected int x;
    protected int y;

    public SuperExample(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void func() {
        System.out.println("SuperExample.func()");
    }
}
```

```java
public class SuperExtendExample extends SuperExample {

    private int z;

    public SuperExtendExample(int x, int y, int z) {
        super(x, y);
        this.z = z;
    }

    @Override
    public void func() {
        super.func();
        System.out.println("SuperExtendExample.func()");
    }
}
```

```java
SuperExample e = new SuperExtendExample(1, 2, 3);
e.func();
```

```html
SuperExample.func()
SuperExtendExample.func()
```

[Using the Keyword super](https://docs.oracle.com/javase/tutorial/java/IandI/super.html)

### Rewriting and overloading

**1. Override
)**

Exists in the inheritance system, which means that the subclass implements a method that is exactly the same as the parent class in terms of method declaration.

In order to satisfy the Li-style substitution principle, rewriting has the following three restrictions:

- The access permission of the subclass method must be greater than or equal to the parent class method;
- The return type of a subclass method must be the return type of the parent class method or its subtype.
- The exception type thrown by the subclass method must be the exception type thrown by the parent class or its subtype.

Using the @Override annotation, you can let the compiler help check whether the above three constraints are met.

In the following example, SubClass is a subclass of SuperClass, and SubClass overrides the func() method of SuperClass. Among them:

- The access rights of subclass methods are public, which is greater than the protected method of the parent class.
- The return type of the subclass is ArrayList\<Integer\>, which is a subclass of the parent class's return type List\<Integer\>.
- The exception type thrown by the subclass is Exception, which is a subclass of Throwable, the exception thrown by the parent class.
- Subclass overridden methods are annotated with @Override, allowing the compiler to automatically check whether constraints are met.

```java
class SuperClass {
    protected List<Integer> func() throws Throwable {
        return new ArrayList<>();
    }
}

class SubClass extends SuperClass {
    @Override
    public ArrayList<Integer> func() throws Exception {
        return new ArrayList<>();
    }
}
```

When calling a method, first search in this class to see if there is a corresponding method. If not, then check in the parent class to see if it is inherited from the parent class. Otherwise, the parameters mu
st be transformed and converted into the parent class to see if there is a corresponding method. In general, the priority of method calls is:

- this.func(this)
- super.func(this)
- this.func(super)
- super.func(super)


```java
/*
    A
    |
    B
    |
    C
    |
    D
 */


class A {

    public void show(A obj) {
        System.out.println("A.show(A)");
    }

    public void show(C obj) {
        System.out.println("A.show(C)");
    }
}

class B extends A {

    @Override
    public void show(A obj) {
        System.out.println("B.show(A)");
    }
}

class C extends B {
}

class D extends C {
}
```

```java
public static void main(String[] args) {

    A a = new A();
    B b = new B();
    C c = new C();
    D d = new D();

    // show(A obj) exists in A, call it directly
    a.show(a); // A.show(A)
    // show(B obj) does not exist in A, transform B into its parent class A
    a.show(b); // A.show(A)
    // There is show(C obj) inherited from A in B, call it directly
    b.show(c); // A.show(C)
    // Show(D obj) does not exist in B, but there is show(C obj) inherited from A, transforming D into its parent class C
    b.show(d); // A.show(C)

    // It still refers to the B object, so the calling results of ba and b are the same
    A ba = new B();
    ba.show(c); // A.show(C)
    ba.show(d); // A.show(C)
}
```

**2. Overload**

Existing in the same class means that a method has the same name as an existing method, but has at least one difference in parameter type, number, and order.

It should be noted that if the return value is different and everything else is the same, it does not count as overloading.

```java
class OverloadingExample {
    public void show(int x) {
        System.out.println(x);
    }

    public void show(int x, String y) {
        System.out.println(x + " " + y);
    }
}
```

```java
public static void main(String[] args) {
    OverloadingExample example = new OverloadingExample();
    example.show(1);
    example.show(1, "2");
}
```

## 7. Reflection

Each class has a **Class** object that contains information related to the class. When compiling a new class, a .class file with the same name will be generated, and the contents of this file will save the Class object.

Class loading is equivalent to the loading of Class objects. The class is dynamically loaded into the JVM when it is used for the first time. You can also use `Class.forName("com.mysql.jdbc.Driver")` to control the loading of classes. This method will return a Class object.

Reflection can provide runtime class information, and this class can be loaded at runtime, even if the .class of the class does not exist at compile time.

Class and java.lang.reflect together provide support for reflection. The java.lang.reflect class library mainly includes the following three classes:

- **Field**: You can use the get() and set() methods to read and modify the fields associated with the Field object;
- **Method**: You can use the invoke() method to call the m
ethod associated with the Method object;
- **Constructor**: You can use Constructor's newInstance() to create new objects.

**Advantages of Reflection:**

- **Extensibility**: Applications can use user-defined classes from external sources by creating instances of extensible objects using fully qualified names.
- **Class Browser and Visual Development Environment**: A class browser needs to be able to enumerate the members of a class. Visual development environments such as IDEs can benefit from taking advantage of the type information available in reflection to help programmers write correct code.
- **Debugger and Testing Tools**: The debugger needs to be able to inspect a class
private member inside. Testing tools can use reflection to automatically call discoverable API definitions defined in classes to ensure high code coverage in a set of tests.

**Disadvantages of Reflection:**

Although reflection is very powerful, it cannot be abused. If a function can be completed without reflection, then it is best not to use it. Here are a few things we should keep in mind when using reflection techniques.

- **Performance overhead**: Reflection involves dynamic type analysis, so the JVM cannot optimize these codes. Therefore, reflective operations are much less efficient than those non-reflective operations. We should avoid using reflection in frequently executed code or in programs with high performance requirements.

- **Security Restrictions**: Using reflection technology requires that the program must run in an environment without security restrictions. This is a problem if a program must run in a security-restricted environment, such as an applet.

- **Internal Exposure**: Because reflection allows code to perform operations that are not normally allowed (such as accessing private properties and methods), using reflection can cause unintended side effects, which can make the code dysfunctional and undermine portability. Reflective code breaks abstraction, so when the platform changes, the behavior of the code may also change.

- [Trail: The Reflection API](https://docs.oracle.com/javase/tutorial/reflect/index.html)
- [In-depth analysis of Java reflection (1) - Basics](http://www.sczyh30.com/posts/Java/java-reflection-1/)

## 8. Abnormality

Throwable can be used to represent any class that can be thrown as an exception, divided into two types: **Error** and **Exception**. Among them, Error is used to represent errors that cannot be handled by the JVM, and Exception is divided into two types:

- **Checked Exception**: It needs to be captured and processed using the try...catch... statement, and it can recover from the exception;
- **Unchecked exception**: It is a program runtime error. For example, dividing by 0 will throw an Arithmetic Exception, at which point the program will crash and cannot be recovered.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/PPjwP.png" width="600"/> </div><br>

- [Java Excep
tion Interview Questions and Answers](https://www.journaldev.com/2167/java-exception-interview-questions-and-answersl)

- [Java Improvement - Java Exception Handling](https://www.cnblogs.com/Qian123/p/5715402.html)

## 9. Generics

```java
public class Box<T> {
    // T stands for "Type"
    private T t;
    public void set(T t) { this.t = t; }
    public T get() { return t; }
}
```

- [Java Generics Detailed Explanation](https://www.cnblogs.com/Blue-Keroro/p/8875898.html)
- [10 Java Generics Interview Questions](https://cloud.tencent.com/developer/article/1033693)

## 10. Notes

Java annotations are some meta-information attached to the code, used by some tools to parse and use during compilation and runtime, and serve the function of explanation and configuration. Annotations will not and cannot affect the actual logic of the code, they only play a supporting role.

[Annotation implementation principles and custom annotation examples](https://www.cnblogs.com/acm-bingzi/p/javaAnnotation.html)

## 11. Features

### New features in each version of Java

**New highlights in Java SE 8**

1. Lambda Expressions
2. Pipelines and Streams
3. Date and Time API
4. Default Methods
5. Type Annotations
6. Nashhorn JavaScript Engine
7. Concurrent Accumulators
8. Parallel operations
9.PermGen Error Removed

**New highlights in Java SE 7**

1. Strings in Switch Statement
2. Type Inference for Generic Instance Creation
3. Multiple Exception Handling
4. Support for Dynamic Languages
5. Try with Resources
6. Javanio Package
7. Binary Literals, Underscore in literals
8. Diamond Syntax

- [Difference between Java 1.8 and Java 1.7?](http://www.selfgrowth.com/articles/difference-between-java-18-and-java-17)
- [Java 8 Features](http://www.importnew.com/19345.html)

### The difference between Java and C++

- Java is a pure object-oriented language. All objects inherit from java.lang.Object. In order to be compatible with C, C++ supports both object-oriented and process-oriented.
- Java achieves cross-platform features through a virtual machine, but C++ depends on a specific platform.
- Java does not have pointers and its references can be understood as safe pointers, while C++ has pointers like C.
- Java supports automatic garbage collection, while C++ requires manual collection.
- Java does not support multiple inheritance and can only achieve the same purpose by implementing multiple interfaces, while C++ supports multiple inheritance.
- Java does not support operator overloading. Although the addition operation can be performed on two String objects, this is a built-in supported operation in the language and does not belong to operator overloading, while C++ can.
- Java's goto is a reserved word, but it is not available. C++ can use goto.

[What are the main differences between Java and C++?](http://cs-fundamentals.com/tech-interview/java/differences-between-java-and-cpp.php)

### JRE or JDK

- JRE: Java Runtime Environment, the abbreviation of Java Runtime Environmen
t, provides
provides the required environment. It is a JVM program, which mainly includes the standard implementation of JVM and some basic Java class libraries.
- JDK: Java Development Kit, Java development tool kit, provides Java development and running environment. JDK is the core of Java development and integrates JRE and some other tools, such as javac, the compiler that compiles Java source code.

## References

- Eckel B. Java Programming Thoughts[M]. Machinery Industry Press, 2002.
- Bloch J. Effective java[M]. Addison-Wesley Professional, 2017.
