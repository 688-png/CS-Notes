#Socket
<!-- GFM-TOC -->
* [Socket](#socket)
    * [一、I/O model](#一io-model)
        * [Blocking I/O](#blocking-io)
        * [Non-blocking I/O](#non-blocking-io)
        * [I/O multiplexing](#io-multiplexing)
        * [Signal driver I/O](#signal driver-io)
        * [Asynchronous I/O](#asynchronous-io)
        * [Comparison of five major I/O models](#五大-io-model comparison)
    * [2. I/O multiplexing](#二io-multiplexing)
        * [select](#select)
        * [poll](#poll)
        * [Compare](#Compare)
        * [epoll](#epoll)
        * [Working Mode](#workingmode)
        * [Application Scenario](#Application Scenario)
    * [References](#references)
<!-- GFM-TOC -->


## 1. I/O model

An input operation usually consists of two stages:

- Wait for data to be ready
-Copy data from kernel to process

For input operations on a socket, the first step usually involves waiting for data to arrive from the network. When the awaited data arrives, it is copied to a buffer in the kernel. The second step is to copy the data from the kernel buffer to the application buffer.

Unix has five I/O models:

- Blocking I/O
- Non-blocking I/O
- I/O multiplexing (select and poll)
- Signal driven I/O (SIGIO)
- Asynchronous I/O (AIO)

### Blocking I/O

The application process is blocked until data is copied from the kernel buffer to the application process buffer.

It should be noted that during the blocking process, other application processes can also execute, so blocking does not mean that the entire operating system is blocked. Because other application processes can still execute, no CPU time is consumed, and the CPU utilization of this model will be relatively high.

In the figure below, recvfrom() is used to receive data from Socket and copy it to the buffer buf of the application process. Here recvfrom() is treated as a system call.

```c
ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags, struct sockaddr *src_addr, socklen_t *addrlen);
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1492928416812_4.png"/> </div><br>

### Non-blocking I/O

After the application process executes the system call, the kernel returns an error code. The application process can continue to execute, but it needs to continuously execute system calls to know whether the I/O is completed. This method is called polling.

This model has lower CPU utilization because the CPU has to handle more system calls.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1492929000361_5.png"/> </div><br>

### I/O multiplexing

Use select or poll to wait for data, and can wait for any of multiple sockets to become readable. This process will block, return when a socket is readable, and then use recvfrom to copy the data from the kernel to the process.

It allows a single process to handle multiple I/O events. Also known as Event Driven I/O, event-driven I/O.

If a web server does not have I/O multiplexing, the
n each Socket connection needs to create a thread for processing. If there are tens of thousands of simultaneous connections, then the same number of threads will need to be created. Compared with multi-process and multi-thread technology, I/O reuse does not require the overhead of process thread creation and switching, and the system overhead is smaller.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1492929444818_6.png"/> </div><br>

### Signal driven I/O

The application process uses the sigaction system call, the kernel returns immediately, and the application process can continue to execute, which means that the application process is non-blocking during the waiting for data phase. The kernel sends a SIGIO signal to the application process when the data arrives. After the application process receives it, it calls recvfrom in the signal handler to copy the data from the kernel to the application process.

Compared with the polling method of non-blocking I/O, signal-driven I/O has higher CPU utilization.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1492929553651_7.png"/> </div><br>

### Asynchronous I/O

The application process will return immediately when executing the aio_read system call. The application process can continue to execute without being blocked. The kernel will send a signal to the application process after all operations are completed.

The difference between asynchronous I/O and signal-driven I/O is that the signal of asynchronous I/O is to notify the application process that I/O is completed, while the signal of signal-driven I/O is to notify the application process that I/O can start.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1492930243286_8.png"/> </div><br>

### Comparison of the five major I/O models

- Synchronous I/O: The phase where data is copied from the kernel buffer to the application process buffer (the second phase), and the application process blocks.
- Asynchronous I/O: The second phase application process will not block.

Synchronous I/O includes blocking I/O, non-blocking I/O, I/O multiplexing and signal-driven I/O. The main difference between them is in the first stage.

Non-blocking I/O, signal-driven I/O, and asynchronous I/O do not block in the first phase.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1492928105791_3.png"/> </div><br>

## 2. I/O reuse

select/poll/epoll are all specific implementations of I/O multiplexing. select appeared earliest, followed by poll, and then epoll.

### select

```c
int select(int n, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);
```

select allows an application to monitor a set of file descriptors, waiting for one or more descriptors to become ready to complete an I/O operation.

- fd_set uses an array
Implementation, the array size is defined using FD_SETSIZ
E, so only fewer than FD_SETSIZE number of descriptors can be listened to. There are three types of descriptor types: readset, writeset, and exceptset, which correspond to descriptor sets for read, write, and exception conditions respectively.

- timeout is a timeout parameter. Calling select will block until an event with a descriptor arrives or the waiting time exceeds timeout.

- The return result of a successful call is greater than 0, the return result of an error is -1, and the return result of a timeout is 0.

```c
fd_set fd_in, fd_out;
struct timeval tv;

//Reset the sets
FD_ZERO( &fd_in );
FD_ZERO( &fd_out );

// Monitor sock1 for input events
FD_SET( sock1, &fd_in );

// Monitor sock2 for output events
FD_SET( sock2, &fd_out );

// Find out which socket has the largest numeric value as select requires it
int largest_sock = sock1 > sock2 ? sock1 : sock2;

// Wait up to 10 seconds
tv.tv_sec = 10;
tv.tv_usec = 0;

// Call the select
int ret = select(largest_sock + 1, &fd_in, &fd_out, NULL, &tv );

// Check if select actually succeed
if(ret==-1)
    // report error and abort
else if (ret == 0)
    // timeout; no event detected
else
{
    if ( FD_ISSET( sock1, &fd_in ) )
        // input event on sock1

    if ( FD_ISSET( sock2, &fd_out ) )
        //output event on sock2
}
```

### poll

```c
int poll(struct pollfd *fds, unsigned int nfds, int timeout);
```

The function of poll is similar to select, and it also waits for one of a set of descriptors to become ready.

The descriptor in poll is an array of type pollfd. The definition of pollfd is as follows:

```c
struct pollfd {
               int fd; /* file descriptor */
               short events; /* requested events */
               short revents; /* returned events */
           };
```


```c
// The structure for two events
struct pollfd fds[2];

// Monitor sock1 for input
fds[0].fd = sock1;
fds[0].events = POLLIN;

// Monitor sock2 for output
fds[1].fd = sock2;
fds[1].events = POLLOUT;

// Wait 10 seconds
int ret = poll( &fds, 2, 10000 );
// Check if poll actually succeed
if(ret==-1)
    // report error and abort
else if (ret == 0)
    // timeout; no event detected
else
{
    // If we detect the event, zero it out so we can reuse the structure
    if (fds[0].revents & POLLIN)
        fds[0].revents = 0;
        // input event on sock1

    if (fds[1].revents & POLLOUT)
        fds[1].revents = 0;
        //output event on sock2
}
```

### Compare

#### 1. Function

The functions of select and poll are basically the same, but they differ in some implementation details.

- select will modify the descriptor, but poll will not;
- The descriptor type of select is implemented using an array, and the FD_SETSIZE size defaults to 1024, so it can only listen to less than 1024 descriptors by default. If you want to monitor more descriptors, you need to modify FD_SETSIZE and then recompile; poll has no limit on the number of descriptors;
- poll provides more event types and has higher descriptor
reuse than select.
- If one thread calls select or poll on a certain descriptor, and another thread closes the descriptor, the result of the call will be uncertain.

#### 2. Speed

Both select and poll are slow, and each call requires copying all descriptors from the application process buffer to the kernel buffer.

#### 3. Portability

Almost all systems support select, but only newer systems support poll.

###epoll

```c
int epoll_create(int size);
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout);
```

epoll_ctl() is used to register a new descriptor with the kernel or change the status of a file descriptor. Registered descriptors will be maintained in a red-black tree in the kernel. Through the callback function, the kernel will add the I/O-ready descriptors to a linked list for management. The process can get the descriptor of the event completion by calling epoll_wait().

As can be seen from the above description, epoll only needs to copy the descriptor from the process buffer to the kernel buffer once, and the process does not need to poll to obtain the descriptor of event completion.

epoll only works on Linux OS.

epoll is more flexible than select and poll and has no limit on the number of descriptors.

epoll is more friendly to multi-threaded programming. If one thread calls epoll_wait() and another thread closes the same descriptor, it will not generate errors such as select and pol.
l 的不确定情况。

```c
// Create the epoll descriptor. Only one is needed per app, and is used to monitor all sockets.
// The function argument is ignored (it was not before, but now it is), so put your favorite number here
int pollingfd = epoll_create( 0xCAFE );

if ( pollingfd < 0 )
 // report error

// Initialize the epoll structure in case more members are added in future
struct epoll_event ev = { 0 };

// Associate the connection class instance with the event. You can associate anything
// you want, epoll does not use this information. We store a connection class pointer, pConnection1
ev.data.ptr = pConnection1;

// Monitor for input, and do not automatically rearm the descriptor after the event
ev.events = EPOLLIN | EPOLLONESHOT;
// Add the descriptor into the monitoring list. We can do it even if another thread is
// waiting in epoll_wait - the descriptor will be properly added
if ( epoll_ctl( epollfd, EPOLL_CTL_ADD, pConnection1->getSocket(), &ev ) != 0 )
    // report error

// Wait for up to 20 events (assuming we have added maybe 200 sockets before that it may happen)
struct epoll_event pevents[ 20 ];

// Wait for 10 seconds, and retrieve less than 20 epoll_event and store them into epoll_event array
int ready = epoll_wait( pollingfd, pevents, 20, 10000 );
// Check if epoll actually succeed
if ( ret == -1 )
    // report error and abort
else if ( ret == 0 )
    // timeout; no event detected
else
{
    // Check if any events detected
    for ( int i = 0
; i < ready; i++ )
    {
        if ( pevents[i].events & EPOLLIN )
        {
            // Get back our connection pointer
            Connection * c = (Connection*) pevents[i].data.ptr;
            c->handleReadEvent();
         }
    }
}
```


### Working mode

The epoll descriptor event has two trigger modes: LT (level trigger) and ET (edge trigger).

#### 1. LT mode

When epoll_wait() detects the arrival of a descriptor event, it notifies the process of this event. The process does not need to handle the event immediately. The process will be notified again the next time epoll_wait() is called. It is the default mode and supports both Blocking and No-Blocking.

#### 2. ET mode

Different from the LT mode, the process must process the event immediately after the notification, and will not be notified of the arrival of the event the next time epoll_wait() is called.

It greatly reduces the number of times the epoll event is triggered repeatedly, so it is more efficient than LT mode. Only No-Blocking is supported to avoid starving tasks that process multiple file descriptors due to blocking read/blocking write operations on one file handle.

### Application scenarios

It is easy to have the illusion that just using epoll is enough. Both select and poll are obsolete. In fact, they have their own usage scenarios.

#### 1. select application scenario

The timeout parameter precision of select is microseconds, while poll and epoll are milliseconds. Therefore, select is more suitable for scenarios with high real-time requirements, such as the control of nuclear reactors.

select is more portable and is supported by almost all major platforms.

#### 2. poll application scenarios

Poll has no limit on the maximum number of descriptors. If the platform supports it and the real-time requirements are not high, poll should be used instead of select.

#### 3. epoll application scenarios

It only needs to be run on the Linux platform, there are a large number of descriptors that need to be polled at the same time, and these connections are preferably long-lived connections.

If you need to monitor less than 1,000 descriptors at the same time, there is no need to use epoll, because the advantages of epoll are not reflected in this application scenario.

There are many changes in the descriptor status that need to be monitored, and they are all very short-lived, so there is no need to use epoll. Because all descriptors in epoll are stored in the kernel, every time the status of the descriptor needs to be changed, a system call needs to be made through epoll_ctl(). Frequent system calls reduce efficiency. And the descriptor of epoll is stored in the kernel and is not easy to debug.

## References

- Stevens W R, Fenner B, Rudoff A M. UNIX network programming[M]. Addison-Wesley Professional, 2004.
- http://man7.org/linux/man-pages/man2/select.2.html
- http://man7.org/linux/man-pages/man2/poll.2.html
- [Boost application performance using asynchronous I/O](https://www.ibm.com/developerworks/linux/library/l-async/)
- [Synchronous and Asy
nchronous I/O](https://msdn.microsoft.com/en-us/library/windows/desktop/aa365683(v=vs.85).aspx)
- [Linux IO mode and detailed explanation of select, poll, and epoll](https://segmentfault.com/a/1190000003063859)
- [poll vs select vs event-based](https://daniel.haxx.se/docs/poll-vs-select.html)
- [select / poll / epoll: practical difference for system architects](http://www.ulduzsoft.com/2014/01/select-poll-epoll-practical-difference-for-system-architects/)
- [Browse the source code of userspace/glibc/sysdeps/unix/sysv/linux/ online](https://code.woboq.org/userspace/glibc/sysdeps/unix/sysv/linux/)
