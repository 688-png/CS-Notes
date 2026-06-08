#JavaIO
<!-- GFM-TOC -->
* [Java IO](#java-io)
    * [1. Overview](#一OVERVIEW)
    * [2. Disk operation](#二diskoperation)
    * [Three, byte operation] (#Three-byte operation)
        * [Realize file copy](#Realize file copy)
        * [Decorator Mode](#Decorator Mode)
    * [Four, character operation](#four character operation)
        * [Encoding and Decoding](#Encoding and Decoding)
        * [String encoding method](#string-encoding method)
        * [Reader and Writer](#reader-and-writer)
        * [Achieve line-by-line output of the contents of a text file](#Achieve line-by-line output of the contents of a text file)
    * [五、Object Operation](#五ObjectOperation)
        * [Serialization](#serialization)
        * [Serializable](#serializable)
        * [transient](#transient)
    *[6.Network Operation](#6network operation)
        * [InetAddress](#inetaddress)
        * [URL](#url)
        * [Sockets](#sockets)
        * [Datagram](#datagram)
    * [七、NIO](#七nio)
        * [Stream&Block](#Stream&Block)
        * [Channel and Buffer](#Channel and Buffer)
        * [Buffer status variable](#buffer status variable)
        * [file-nio-instance](#file-nio-instance)
        * [Selector](#selector)
        * [socket NIO instance](#socket-nio-instance)
        * [Memory mapped file](#memory mapped file)
        * [Compare](#Compare)
    * [Eight. Reference materials](#八 Reference Materials)
<!-- GFM-TOC -->


## 1. Overview

Java's I/O can be roughly divided into the following categories:

- Disk operation: File
- Byte operations: InputStream and OutputStream
- Character operations: Reader and Writer
- Object operation: Serializable
- Network operation: Socket
- New input/output: NIO

## 2. Disk operations

The File class can be used to represent file and directory information, but it does not represent the contents of the file.

List all files in a directory recursively:

```java
public static void listAllFiles(File dir) {
    if (dir == null || !dir.exists()) {
        return;
    }
    if (dir.isFile()) {
        System.out.println(dir.getName());
        return;
    }
    for (File file : dir.listFiles()) {
        listAllFiles(file);
    }
}
```

Starting from Java7, you can use Paths and Files instead of File.

## 3. Byte operations

### Implement file copy

```java
public static void copyFile(String src, String dist) throws IOException {
    FileInputStream in = new FileInputStream(src);
    FileOutputStream out = new FileOutputStream(dist);

    byte[] buffer = new byte[20 * 1024];
    int cnt;

    // read() reads at most buffer.length bytes
    //Returns the actual number of reads
    // When -1 is returned, it means reading eof, which is the end of the file.
    while ((cnt = in.read(buffer, 0, buffer.length)) != -1) {
        out.write(buffer, 0, cnt);
    }

    in.close();
    out.close();
}
```

### Decorator pattern

Java I/O is implemented using the decorator pattern. Taking InputStream as an example,

- InputStream is an abstract
component;
- FileInputStream is a subclass of InputStream and is a specific component that provides input operations for byte streams;
- FilterInputStream belongs to the abstract decorator, which is used to decorate components and provide additional functions for components. For example, BufferedInputStream provides caching capabilities for FileInputStream.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/9709694b-db05-4cce-8d2f-1c8b09f4d921.png" width="650px"> </div><br>

When instantiating a byte stream object with caching function, you only need to add another layer of BufferedInputStream object to the FileInputStream object.

```java
FileInputStream fileInputStream = new FileInputStream(filePath);
BufferedInputStream bufferedInputStream = new BufferedInputStream(fileInputStream);
```

The DataInputStream decorator provides input operations for more data types, such as int, double and other basic types.

## 4. Character operations

### Encoding and decoding

Encoding is converting characters into bytes, while decoding is reassembling bytes into characters.

If the encoding and decoding processes use different encoding methods, garbled characters will appear.

- In GBK encoding, Chinese characters occupy 2 bytes and English characters occupy 1 byte;
- In UTF-8 encoding, Chinese characters occupy 3 bytes and English characters occupy 1 byte;
- In UTF-16be encoding, Chinese characters and English characters both occupy 2 bytes.

The be in UTF-16be refers to Big Endian, which is Big Endian. Correspondingly, there is also UTF-16le, le refers to Little Endian, which is the little end.

Java's memory encoding uses double-byte encoding UTF-16be. This does not mean that Java only supports this encoding method, but that the char type is encoded using UTF-16be. The char type occupies 16 bits, which is two bytes. Java uses this double-byte encoding to allow a Chinese or
Either English can be stored using a char.

### String encoding method

String can be regarded as a character sequence. You can specify an encoding method to encode it into a byte sequence, or you can specify an encoding method to decode a byte sequence into a String.

```java
String str1 = "Chinese";
byte[] bytes = str1.getBytes("UTF-8");
String str2 = new String(bytes, "UTF-8");
System.out.println(str2);
```

When calling the parameterless getBytes() method, the default encoding is not UTF-16be. The advantage of double-byte encoding is that one char can be used to store Chinese and English. This advantage is no longer needed when converting String to bytes[] byte array, so double-byte encoding is no longer needed. The default encoding of getBytes() is platform-dependent, generally UTF-8.

```java
byte[] bytes = str1.getBytes();
```

### Reader and Writer

Whether it is disk or network transmission, the smallest storage unit is bytes, not characters. However, the data that is manipulated in the program is usually in the form of characters, so it i
s necessary to provide methods for operating on characters.

- InputStreamReader implements decoding from byte stream to character stream;
- OutputStreamWriter implements character stream encoding into byte stream.

### Realize line-by-line output of the contents of a text file

```java
public static void readFileContent(String filePath) throws IOException {

    FileReader fileReader = new FileReader(filePath);
    BufferedReader bufferedReader = new BufferedReader(fileReader);

    String line;
    while ((line = bufferedReader.readLine()) != null) {
        System.out.println(line);
    }

    // The decorator pattern makes BufferedReader combine a Reader object
    // When calling the close() method of BufferedReader, the close() method of Reader will be called.
    // So just one close() call is enough
    bufferedReader.close();
}
```

## 5. Object operations

### Serialization

Serialization is to convert an object into a byte sequence to facilitate storage and transmission.

- Serialization: ObjectOutputStream.writeObject()
- Deserialization: ObjectInputStream.readObject()

Static variables will not be serialized because serialization only saves the state of the object, and static variables belong to the state of the class.

### Serializable

The serialized class needs to implement the Serializable interface. It is just a standard and does not need to implement any methods. However, if serialization is performed without implementing it, an exception will be thrown.

```java
public static void main(String[] args) throws IOException, ClassNotFoundException {

    A a1 = new A(123, "abc");
    String objectFile = "file/a1";

    ObjectOutputStream objectOutputStream = new ObjectOutputStream(new FileOutputStream(objectFile));
    objectOutputStream.writeObject(a1);
    objectOutputStream.close();

    ObjectInputStream objectInputStream = new ObjectInputStream(new FileInputStream(objectFile));
    A a2 = (A) objectInputStream.readObject();
    objectInputStream.close();
    System.out.println(a2);
}

private static class A implements Serializable {

    private int x;
    private String y;

    A(int x, String y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public String toString() {
        return "x = " + x + " " + "y = " + y;
    }
}
```

### transient

The transient keyword prevents some properties from being serialized.

The array elementData that stores data in ArrayList is decorated with transient because this array is dynamically expanded and not all the space is used, so there is no need for all contents to be serialized. By overriding the serialization and deserialization methods, it is possible to serialize only the part of the data that contains content in the array.

```java
private transient Object[] elementData;
```

## 6. Network operation

Network support in Java:

- InetAddress: used to represent hardware resources on the network, that is, IP addresses;
- URL: Uniform Resource Locator;
- Sockets: Use TC
P protocol to implement network communication;
- Datagram: Use UDP protocol to implement network communication.

### InetAddress

There is no public constructor, and instances can only be created through static methods.

```java
InetAddress.getByName(String host);
InetAddress.getByAddress(byte[] address);
```

### URL

Byte stream data can be read directly from the URL.

```java
public static void main(String[] args) throws IOException {

    URL url = new URL("http://www.baidu.com");

    /* byte stream */
    InputStream is = url.openStream();

    /* character stream */
    InputStreamReader isr = new InputStreamReader(is, "utf-8");

    /* Provide caching function */
    BufferedReader br =
new BufferedReader(isr);

    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }

    br.close();
}
```

### Sockets

- ServerSocket: server-side class
- Socket: client class
- The server and client perform input and output through InputStream and OutputStream.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1e6affc4-18e5-4596-96ef-fb84c63bf88a.png" width="550px"> </div><br>

### Datagram

- DatagramSocket: communication class
- DatagramPacket: Data packet class

## 7. NIO

The new input/output (NIO) library was introduced in JDK 1.4 and made up for the shortcomings of the original I/O, providing high-speed, block-oriented I/O.

### Streams and blocks

The most important difference between I/O and NIO is the way data is packaged and transmitted. I/O processes data in a stream, while NIO processes data in a block.

Stream-oriented I/O processes data one byte at a time: an input stream produces one byte of data, and an output stream consumes one byte of data. It is very easy to create filters for streaming data, chaining several filters so that each filter is responsible for only part of a complex processing mechanism. The downside is that stream-oriented I/O is often quite slow.

Block-oriented I/O processes data one block at a time, and processing data in blocks is much faster than processing data in streams. But block-oriented I/O lacks some of the elegance and simplicity of stream-oriented I/O.

The I/O packages and NIO are well integrated, and java.io.\* has been reimplemented on top of NIO, so now it can take advantage of some of NIO's features. For example, some classes in the java.io.\* packages contain methods for reading and writing data in chunks, which makes processing faster even in stream-oriented systems.

### Channels and buffers

#### 1. Channel

A channel is an emulation of a stream in an original I/O package through which data can be read and written.

The difference between a channel and a stream is that a stream can only move in one direction (a stream must be a subclass of InputStream or OutputStream), while a channel is bidirectional and can be used for reading, writing, or both.

Channels include the following types:

- FileChannel: read and write
data from files;
- DatagramChannel: read and write data in the network through UDP;
- SocketChannel: read and write data in the network through TCP;
- ServerSocketChannel: Can monitor new incoming TCP connections and create a SocketChannel for each new incoming connection.

#### 2. Buffer

All data sent to a channel must first be placed in a buffer, and similarly, any data read from a channel must first be read into a buffer. In other words, data will not be read or written directly to the channel, but will first go through the buffer.

A buffer is essentially an array, but it's more than just an array. Buffers provide structured access to data and can also track the system's read/write processes.

Buffers include the following types:

-ByteBuffer
-CharBuffer
-ShortBuffer
-IntBuffer
-LongBuffer
- FloatBuffer
-DoubleBuffer

### Buffer status variable

- capacity: maximum capacity;
- position: the number of bytes currently read and written;
- limit: The number of bytes that can be read and written.

Example of the change process of state variables:

① Create a new buffer with a size of 8 bytes. At this time, the position is 0 and limit = capacity = 8. The capacity variable does not change and will be ignored in the following discussion.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1bea398f-17a7-4f67-a90b-9e2d243eaa9a.png"/> </div><br>

② Read 5 bytes of data from the input channel and write it into the buffer. At this time, the position is 5 and the limit remains unchanged.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/80804f52-8815-4096-b506-48eef3eed5c6.png"/> </div><br>

③ Before writing the buffer data to the output channel, you need to call the flip() method. This method sets limit to the current position and position to 0.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/952e06bd-5a65-4cab-82e4-dd1536462f38.png"/> </div><br>

④ Take 4 bytes from the buffer into the output buffer, and set position to 4 at this time.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b5bdcbe2-b958-4aef-9151-6ad963cb28b4.png"/> </div><br>

⑤ Finally, you need to call the clear() method to clear the buffer. At this time, position and limit are both set to the initial position.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/67bf5487-c45d-49b6-b9c0-a058d8c68902.png"/> </div><br>

### File NIO instance

The following shows an example of using NIO to quickly copy files:

```java
public static void fastCopy(String src, String dist) throws IOException {

    /* Get the input byte stream of the source file */
    FileInputStream fin = new FileInputStream(src);

    /* Get the file channel of the input byte stream */
    FileChannel fcin = fin.getChannel();

    /* Get the output byte stream of the target file */
    FileOutputStream fout = new FileOutputStream(
dist);

    /* Get the output byte stream
file channel */
    FileChannel fcout = fout.getChannel();

    /* Allocate 1024 bytes for buffer */
    ByteBuffer buffer = ByteBuffer.allocateDirect(1024);

    while (true) {

        /* Read data from the input channel into the buffer */
        int r = fcin.read(buffer);

        /* read() returns -1 indicating EOF */
        if (r == -1) {
            break;
        }

        /* Switch between reading and writing */
        buffer.flip();

        /* Write the contents of the buffer to the output file */
        fcout.write(buffer);

        /* Clear buffer */
        buffer.clear();
    }
}
```

### Selector

NIO is often called non-blocking IO, mainly because NIO's non-blocking characteristics are widely used in network communication.

NIO implements the Reactor model in IO multiplexing. A thread Thread uses a selector to listen to events on multiple channels in a polling manner, so that one thread can handle multiple events.

By configuring the monitored channel Channel to be non-blocking, when the IO event on the Channel has not yet arrived, it will not enter the blocking state and wait, but will continue to poll other Channels to find the Channel where the IO event has arrived for execution.

Because the overhead of creating and switching threads is high, using one thread to process multiple events instead of one thread to process one event has good performance for IO-intensive applications.

It should be noted that only the socket Channel can be configured as non-blocking, but FileChannel cannot, and it makes no sense to configure non-blocking for FileChannel.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/093f9e57-429c-413a-83ee-c689ba596cef.png" width="350px"> </div><br>

#### 1. Create a selector

```java
Selector selector = Selector.open();
```

#### 2. Register the channel to the selector

```java
ServerSocketChannel ssChannel = ServerSocketChannel.open();
ssChannel.configureBlocking(false);
ssChannel.register(selector, SelectionKey.OP_ACCEPT);
```

The channel must be configured in non-blocking mode, otherwise there is no point in using the selector, because if the channel is blocked on an event, the server cannot respond to other events and must wait for this event to be processed before processing other events. Obviously this runs counter to the role of the selector.

When registering the channel to the selector, you also need to specify the specific events to be registered, which mainly include the following categories:

- SelectionKey.OP_CONNECT
- SelectionKey.OP_ACCEPT
- SelectionKey.OP_READ
- SelectionKey.OP_WRITE

They are defined in SelectionKey as follows:

```java
public static final int OP_READ = 1 << 0;
public static final int OP_WRITE = 1 << 2;
public static final int OP_CONNECT = 1 << 3;
public static final int OP_ACCEPT = 1 << 4;
```

It can be seen that each event can be regarded as a bit field to form an event set integer. For
example:

```java
int interestSet = SelectionKey.OP_READ | SelectionKey.OP_WRITE;
```

#### 3. Listen for events

```java
int num = selector.select();
```

Use select() to listen for arriving events, which will block until at least one event arrives.

#### 4. Get arriving events

```java
Set<SelectionKey> keys = selector.selectedKeys();
Iterator<SelectionKey> keyIterator = keys.iterator();
while (keyIterator.hasNext()) {
    SelectionKey key = keyIterator.next();
    if (key.isAcceptable()) {
        // ...
    } else if (key.isReadable()) {
        // ...
    }
    keyIterator.remove();
}
```

#### 5. Event loop

Because one select() call cannot process all events, and the server may need to monitor events all the time, the code for processing events on the server is generally placed in an infinite loop.

```java
while (true) {
    int num = selector.select();
    Set<SelectionKey> keys = selector.selectedKeys();
    Iterator<SelectionKey> keyIterator = keys.iterator();
    while (keyIterator.hasNext()) {
        SelectionKey key = keyIterator.next();
        if (key.isAcceptable()) {
            // ...
        } else if (key.isReadable()) {
            // ...
        }
        keyIterator.remove();
    }
}
```

### Socket NIO instance

```java
public class NIOServer {

    public static void main(String[] args) throws IOException {

        Selector selector = Selector.open();

        ServerSocketChannel ssChannel = ServerSocketChannel.open
();
        ssChannel.configureBlocking(false);
        ssChannel.register(selector, SelectionKey.OP_ACCEPT);

        ServerSocket serverSocket = ssChannel.socket();
        InetSocketAddress address = new InetSocketAddress("127.0.0.1", 8888);
        serverSocket.bind(address);

        while (true) {

            selector.select();
            Set<SelectionKey> keys = selector.selectedKeys();
            Iterator<SelectionKey> keyIterator = keys.iterator();

            while (keyIterator.hasNext()) {

                SelectionKey key = keyIterator.next();

                if (key.isAcceptable()) {

                    ServerSocketChannel ssChannel1 = (ServerSocketChannel) key.channel();

                    // The server will create a SocketChannel for each new connection
                    SocketChannel sChannel = ssChannel1.accept();
                    sChannel.configureBlocking(false);

                    // This new connection is mainly used to read data from the client
                    sChannel.register(selector, SelectionKey.OP_READ);

                } else if (key.isReadable()) {

                    SocketChannel sChannel = (SocketChannel) key.channel();
                    System.out.println(readDataFromSocketChannel(sChannel));
                    sChannel.close();
                }

                keyIterator.remove();
            }
        }
    }

    private static String readDataFromSocketChannel(SocketChannel sChannel) throws IOException {

        ByteBuffer buffer = ByteBuffer.
allocate(1024);
        StringBuilder data = new StringBuilder();

        while (true) {

            buffer.clear();
            int n = sChannel.read(buffer);
            if (n == -1) {
                break;
            }
            buffer.flip();
            int limit = buffer.limit();
            char[] dst = new char[limit];
            for (int i = 0; i < limit; i++) {
                dst[i] = (char) buffer.get(i);
            }
            data.append(dst);
            buffer.clear();
        }
        return data.toString();
    }
}
```

```java
public class NIOClient {

    public static void main(String[] args) throws IOException {
        Socket socket = new Socket("127.0.0.1", 8888);
        OutputStream out = socket.getOutputStream();
        String s = "hello world";
        out.write(s.getBytes());
        out.close();
    }
}
```

### Memory mapped file

Memory-mapped file I/O is a method of reading and writing file data that can be much faster than conventional stream-based or channel-based I/O.

Writing to a memory mapped file can be dangerous, as simple operations such as changing a single element of an array can directly modify the file on disk. There is no separation between modifying data and saving data to disk.

The following line of code maps the first 1024 bytes of the file into memory. The map() method returns a MappedByteBuffer, which is a subclass of ByteBuffer. Therefore, the newly mapped buffer can be used like any other ByteBuffer, and the operating system will take care of performing the mapping when needed.

```java
MappedByteBuffer mbb = fc.map(FileChannel.MapMode.READ_WRITE, 0, 1024);
```

### Comparison

The main differences between NIO and ordinary I/O are the following two points:

- NIO is non-blocking;
- NIO is block-oriented, I/O is stream-oriented.

## 8. Reference materials

- Eckel B, Eckel, Haopeng, et al. Java Programming Thoughts [M]. Machinery Industry Press, 2002.
- [IBM: Getting Started with NIO](https://www.ibm.com/developerworks/cn/education/java/j-nio/j-nio.html)
- [Java NIO Tutorial](http://tutorials.jenkov.com/java-nio/index.html)
- [A brief analysis of Java NIO](https://tech.meituan.com/nio.htm
l)
- [IBM: In-depth analysis of the working mechanism of Java I/O](https://www.ibm.com/developerworks/cn/java/j-lo-javaio/index.html)
- [IBM: In-depth analysis of Chinese coding issues in Java](https://www.ibm.com/developerworks/cn/java/j-lo-chinesecoding/index.html)
- [IBM: Advanced understanding of Java serialization](https://www.ibm.com/developerworks/cn/java/j-lo-serial/index.html)
- [The difference between NIO and traditional IO](http://blog.csdn.net/shimiso/article/details/24990499)
- [Decorator Design Pattern](http://stg-tud.github.io/sedc/Lecture/ws13-14/5.3-Decorator.html#mode=document)
- [Socket Multicast](http://labojava.blogspot.com/2012/12/socket-multicast.html)
