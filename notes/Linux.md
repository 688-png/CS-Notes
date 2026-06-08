#Linux
<!-- GFM-TOC -->
* [Linux](#linux)
    * [Foreword](#foreword)
    * [1. Commonly used operations and concepts] (#一 Commonly used operations and concepts)
        * [shortcut key](#shortcut key)
        * [HELP](#HELP)
        * [Shutdown](#shutdown)
        * [PATH](#path)
        * [sudo](#sudo)
        * [Package Management Tool](#Package Management Tool)
        * [release](#release)
        * [VIM three modes](#vim-three modes)
        * [GNU](#gnu)
        *[Open Source Agreement](#Open Source Agreement)
    * [二、disk](#二disk)
        * [Disk Interface](#diskinterface)
        * [disk file name](#disk file name)
    * [三、Partition](#三区)
        * [Partition table](#partition table)
        * [Boot detection program](#Boot detection program)
    * [Four, file system](#四filesystem)
        * [Partition and File System](#Partition and File System)
        *[composition](#composition)
        * [File Reading](#File Reading)
        * [Disk fragmentation](#disk fragmentation)
        * [block](#block)
        * [inode](#inode)
        * [Directory](#directory)
        * [Log](#log)
        * [Mount](#mount)
        * [Directory Configuration](#Directory Configuration)
    * [五、FILE](#五狗)
        * [File Attributes](#File Attributes)
        * [Basic operations of files and directories](#Basic operations of files and directories)
        * [Modify permissions](#Modify permissions)
        * [Default permissions](#default permissions)
        * [Directory permissions](#Directory permissions)
        * [link](#link)
        * [Get file content](#Get file content)
        * [Command and file search](#command and file search)
    * [6. Compression and Packaging](#6Compression and Packaging)
        * [Compressed file name](#Compressed file name)
        * [Compression command](#compression command)
        * [Package](#包)
    * [七、Bash](#七bash)
        * [Characteristics](#Characteristics)
        * [Variable operation](#Variable operation)
        * [Instruction search order](#Instruction search order)
        * [Data flow redirection](#data flow redirection)
    * [Eight, Pipeline Command](#八 Pipeline Command)
        * [Extraction Instruction](#Extraction Instruction)
        * [Sort command](#Sort command)
        * [Bidirectional output redirection](#bidirectional output redirection)
        * [Character conversion command](#Character conversion command)
        * [Partition command](#Partition command)
    * [Nine, regular expression] (#九regular expression)
        * [grep](#grep)
        * [printf](#printf)
        * [awk](#awk)
    * [10. Process Management](#十 Process Management)
        * [View Process](#View Process)
        * [Process Status](#Process Status)
        * [SIGCHLD](#sigchld)
        * [wait()](#wait)
        * [waitpid()](#waitpid)
        * [Orphan Process](#Orphan Process)
        * [zombie process](#zombie process)
    * [References](#references)
<!-- GFM-TOC -->


## Preface

For ease of understanding, this articl
e starts with common operations and concepts. Although we have tried to simplify it as much as possible, it still involves a lot of content. In the interview, Linux knowledge points are not that important compared to network and operating system knowledge points. You only need to focus on mastering some principles and commands. In order to make it easier for everyone to prepare for the interview, here are some more important knowledge points:

- You can simply use cat, grep, cut and other commands to perform some operations;
- Principles related to file systems, concepts such as inode and block, data recovery;
- Hard links and soft links;
- Process management related, zombie processes and orphan processes, SIGCHLD.

## 1. Common operations and concepts

### Shortcut keys

- Tab: command and file name completion;
- Ctrl+C: Interrupt the running program;
- Ctrl+D: End keyboard input (End Of File, EOF)

### Help

#### 1. --help

An introduction to the basic usage and options of commands.

#### 2.man

man is the abbreviation of manual, which displays the specific information of the command.

When executing `man date`, DATE(1) appears. The number in it represents the type of instruction. Commonly used numbers and their types are as follows:

| Codename | Type |
| :--: | -- |
| 1 | Instructions or executable files that users can operate in the shell environment |
| 5 | Configuration file |
| 8 | Management commands that system administrators can use |

#### 3. info

info is similar to man, but info divides the document into pages, and each page can be jumped.

#### 4.doc

/usr/share/doc stores a complete set of documentation for the software.

### Shut down

#### 1.who

Before shutting down, you need to use the who command to check if there are other users online.

#### 2. sync

In order to speed up the reading and writing of disk files, the file data located in the memory will not be synchronized to the disk immediately, so a sync synchronization operation needs to be performed before shutting down.

#### 3. shutdown

```html
## shutdown [-krhc] time [information]
-k: Will not shut down, just send a warning message to notify all online users
-r: Stop the system service and then restart it
-h: Shut down the system immediately after stopping the service
-c: Cancel an already ongoing shutdown
```

### PATH

The path to the executable file can be declared in the environment variable PATH, separated by :.

```html
/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/dmtsai/.local/bin:/home/dmtsai/bin
```

### sudo

sudo allows ordinary users to use root executable commands, but only users added in the /etc/sudoers configuration file can use this command.

### Package management tools

RPM and DPKG are the two most common types of software package management tools:

- RPM, the full name of Redhat Package Manager, was first developed and implemented by Red Hat Company. It was later accepted by the GNU open source operating system and became an established
software standard for many Linux systems. YUM is based on RPM and has dependencies
Management and software upgrade capabilities.
- Competing with RPM is the DEB package management tool DPKG based on the Debian operating system, which is called Debian Package and is similar in function to RPM.

### Release

A Linux distribution is an integrated version of the Linux kernel and various application software.

| Based on package management tools | Commercial distributions | Community distributions |
| :--: | :--: | :--: |
| RPM | Red Hat | Fedora / CentOS |
| DPKG | Ubuntu | Debian |

### VIM three modes

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191209002818626.png"/> </div><br>



-Command mode: VIM's default mode, which can be used to move the cursor to view content;
- Edit mode (Insert mode): Press "i" and other keys to enter, and you can edit text;
- Bottom-line mode: Press the ":" button to enter, used for operations such as saving and exiting.

In command line mode, the following commands are used to exit or save files.

| Command | Function |
| :--: | :--: |
| :w | Write to disk |
| :w! | Force writing to disk when the file is read-only. Whether it can be written depends on the user's permissions on the file |
| :q | Leave |
| :q! | Force to leave without saving |
| :wq | Write to disk and exit |
| :wq!| Force write to disk and then exit |

### GNU

The GNU Project, translated as the Genuine Project, aims to create a completely free operating system called GNU, whose content software is completely released under the GPL. The full name of GPL is GNU General Public License, which includes the following contents:

- Freedom to run this program for any purpose;
- Freedom to reproduce;
- The freedom to improve this program and to publish improvements publicly.

### Open source agreement

- [Choose an open source license](https://choosealicense.com/)
- [How to choose an open source license? ](http://www.ruanyifeng.com/blog/2011/05/how_to_choose_free_software_licenses.html)

## 2. Disk

### Disk interface

#### 1. IDE

IDE (ATA) stands for Advanced Technology Attachment. The maximum interface speed is 133MB/s. Because the anti-interference performance of the parallel port cable is too poor and the cable takes up a large space, which is not conducive to the internal heat dissipation of the computer, it has been gradually replaced by SATA.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/924914c0-660c-4e4a-bbc0-1df1146e7516.jpg" width="400"/> </div><br>

#### 2. SATA

SATA's full name is Serial ATA, which is an ATA interface that uses a serial port. It has strong anti-interference, has much lower requirements for the length of the data cable than ATA, and supports hot-swappable and other functions. SATA-II has an interface speed of 300MB/s, while the SATA-III standard can achieve transfer speeds of 600MB/s. SATA data cables are also much thinner than ATA, w
hich is beneficial to air circulation in the chassis and makes it easier to organize the cables.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f9f2a16b-4843-44d1-9759-c745772e9bcf.jpg" width=""/> </div><br>

#### 3. SCSI

The full name of SCSI is Small Computer System Interface (Small Computer System Interface). SCSI hard drives are widely used in workstations, personal computers and servers. Therefore, they use more advanced technologies, such as a high disk speed of 15,000 rpm, and the CPU usage is low during transmission. However, the unit price is also more expensive than ATA and SATA hard drives of the same capacity.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f0574025-c514-49f5-a591-6d6a71f271f7.jpg" width=""/> </div><br>

#### 4. SAS

SAS (Serial Attached SCSI) is a new generation of SCSI technology. Like SATA hard drives, it uses serial technology to achieve higher transmission speeds, which can reach 6Gb/s. In addition, the internal space of the system is improved by reducing the connecting lines.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6729baa0-57d7-4817-b3aa-518cbccf824c.jpg" width=""/> </div><br>

### The file name of the disk

Every piece of hardware in Linux is treated as a file, including disks. Disks are named according to the disk interface type. Common disk file names are as follows:

- IDE disk: /dev/hd[a-d]
- SATA/SCSI/SAS disk: /dev/sd[a-p]

The determination of the serial number after the file name is related to the order in which the system detects the disks, and has nothing to do with the slot position in which the disks are inserted.

## 3. Partition

### Partition table

There are two main formats of disk partition tables, one is the more restrictive MBR partition table, and the other is the newer and less restrictive GPT partition table.

#### 1. MBR

In MBR, the first sector is the most important. It contains the master boot record (MBR) and the partition table. The master boot record occupies 446 bytes and the partition table occupies 64 bytes.

The partition table is only 64 bytes and can only store up to 4 partitions. These 4 partitions are primary partitions and extended partitions. There is only one extended partition, which uses other sectors to record additional partition tables. Therefore, more partitions can be divided through extended partitions. These partitions are called logical partitions.

Linux also treats partitions as files. The naming method of partition files is: disk file name + number, such as /dev/sda1. Note that logical partitions are numbered starting from 5.

#### 2. GPT

A sector is the smallest storage unit of a disk, the sector size of older disks is usually 512 bytes, while the latest disks support 4k. In order to be compatible with all disks, GPT uses logical block addresses (Logical Block Address, LBA) on defined sectors. The default size of LBA is 5
12 bytes.

GPT block 1 records the main boot
Record (MBR), followed by 33 blocks to record partition information, and the last 33 blocks are used to back up the partition information. The first of these 33 blocks is the GPT header record. This part records the location and size of the partition table itself and the location of the backup partition. It also contains the check code (CRC32) of the partition table. The operating system can use this check code to determine whether the GPT is correct. If there is an error, you can use the backup partition to restore it.

GPT does not have the concept of extended partitions. They are all primary partitions. Each LBA can be divided into 4 partitions, so a total of 4 * 32 = 128 partitions can be divided.

MBR does not support hard drives above 2.2 TB, while GPT supports up to 2<sup>33</sup> TB = 8 ZB.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/GUID_Partition_Table_Scheme.svg.png" width="400"/> </div><br>

### Boot detection program

#### 1. BIOS

BIOS (Basic Input/Output System), which is a firmware (software embedded in hardware), the BIOS program is stored in read-only memory that will not lose its content after a power outage.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/50831a6f-2777-46ea-a571-29f23c85cc21.jpg"/> </div><br>

BIOS is the first program executed by the computer when it is turned on. This program knows the disk that can be turned on and reads the main boot record (MBR) of the first sector of the disk. The main boot record (MBR) executes the boot management program. This boot management program loads the core files of the operating system.

The boot manager in the Main Boot Record (MBR) provides the following functions: menus, loading core files, and forwarding to other boot managers. The transfer function can be used to achieve multi-boot. You only need to install the boot management program of another operating system on the boot sector of another partition. When starting the boot management program, you can choose to start the current operating system through the menu or transfer it to other boot management programs to start another operating system.

In the figure below, the boot management program in the main boot record (MBR) of the first sector provides two menus: M1 and M2. M1 points to the Windows operating system, and M2 points to the boot sector of other partitions, which contains another boot management program and provides a menu pointing to Linux.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f900f266-a323-42b2-bc43-218fdb8811a8.jpg" width="600"/> </div><br>

To install multiboot, it is best to install Windows first and then Linux. Because the main boot record (MBR) will be overwritten when installing Windows, Linux can choose to install the boot management program in the main boot record (MBR) or the boot sector of other partitions, and can
set the menu of the boot management program.

#### 2. UEFI

BIOS cannot read GPT partition tables, but UEFI can.

## 4. File system

### Partitions and file systems

Formatting a partition is to create a file system on the partition. A partition can usually only be formatted with one file system, but technologies such as disk arrays can format a partition with multiple file systems.

### Composition

The most important components are as follows:

- inode: A file occupies one inode, records the attributes of the file, and records the block number where the content of the file is located;
- block: Record the contents of the file. When the file is too large, it will occupy multiple blocks.

In addition, it also includes:

- superblock: records the overall information of the file system, including the total amount, usage, and remaining amount of inodes and blocks, as well as the format and related information of the file system;
- block bitmap: a bitmap that records whether the block is used.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/BSD_disk.png" width="800"/> </div><br>

### File reading

For the Ext2 file system, when you want to read the contents of a file, first find all the blocks where the file content is located in the inode, and then read the contents of all blocks.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/12a65cc6-20e0-4706-9fe6-3ba49413d7f6.png" width="500px"> </div><br>

For the FAT file system, it does not have an inode, and each block stores the number of the next block.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5b718e86-7102-4bb6-8ca5-d1dd791530c5.png" width="500px"> </div><br>

### Disk fragmentation

It means that the block where the content of a file is located is too scattered, causing the disk head to move too far, thereby reducing the disk read and write performance.

### block

The block sizes supported in the Ext2 file system are 1K, 2K and 4K. Different sizes limit the maximum size of a single file and the file system.

| Size | 1KB | 2KB | 4KB |
| :---: | :---: | :---: | :---: |
| Maximum single file | 16GB | 256GB | 2TB |
| Maximum file system | 2TB | 8TB | 16TB |

A block can only be used by one file, and the unused parts are directly wasted. Therefore, if you need to store a large number of small files, it is best to choose a smaller block.

###inode

The inode specifically contains the following information:

- Permissions (read/write/excute);
- Owner and group (owner/group);
- Capacity;
- Creation or status change time (ctime);
- Last read time (atime);
- Last modification time (mtime);
- Flags that define file characteristics, such as SetUID...;
- The pointer to the actual contents of the file.

inode has the following characteristics:

- Each inode size is fixed at 128 bytes (new ext4 and xfs can be set to 256 bytes);
- Each file will occupy only one inode.

The inode records
the block number where the file content is located, but each block is very small. A large file requires hundreds of thousands of blocks. And the size of an inode is
Due to the limitation, so many block numbers cannot be directly referenced. Therefore, indirect, double indirect, and triple indirect references were introduced. Indirect references allow the reference block recorded by the inode to record reference information.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/inode_with_signatures.jpg" width="600"/> </div><br>

### Directory

When a directory is created, an inode and at least one block are allocated. The content recorded by block is the inode number and file name of all files in the directory.

It can be seen that the inode of the file itself does not record the file name. The file name is recorded in the directory. Therefore, operations such as adding files, deleting files, and changing file names are related to the write permission of the directory.

### Log

If there is a sudden power outage, an error will occur in the file system. For example, the block bitmap was only modified before the power outage, but the data was not actually written into the block.

The ext3/ext4 file system introduces a log function, which can be used to repair the file system.

### Mount

Mounting uses the directory as the entry point of the file system, that is, after entering the directory, the file system data can be read.

### Directory configuration

In order to maintain consistency in the directory structure of different Linux distributions, the Filesystem Hierarchy Standard (FHS) specifies the directory structure of Linux. The three most basic directories are as follows:

- / (root, root directory)
- /usr (unix software resource): All system default software will be installed in this directory;
- /var (variable): stores data files during system or program operation.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/linux-filesystem.png" width=""/> </div><br>

## 5. Documents

### File properties

There are three types of users: file owners, groups, and others. Different users have different file permissions.

When using ls to view a file, the information of a file will be displayed, such as `drwxr-xr-x 3 root root 17 May 6 00:14 .config`. The explanation of this information is as follows:

- drwxr-xr-x: file type and permissions, the first digit is the file type field, and the last 9 digits are the file permissions field
- 3: Number of links
- root: file owner
- root: group to which it belongs
- 17: File size
- May 6 00:14: The time when the file was last modified
- .config: file name

Common file types and their meanings are:

-d: directory
- -: File
-l: link file

In the 9-digit file permission field, every 3 digits are in a group, and there are 3 groups in total. Each group represents the file permissions for the file owner, the group to which it belongs, and other
people. The three digits in a set of permissions are r, w, and x permissions, indicating readable, writable, and executable.

There are three types of file times:

- modification time (mtime): The file will be updated when its content is updated;
- status time (ctime): The file’s status (permissions, attributes) will be updated when it is updated;
- access time (atime): updated when the file is read.

### Basic operations on files and directories

#### 1.ls

List the information of a file or directory. The information of the directory is the files contained in it.

```html
## ls [-aAdfFhilnrRSt] file|dir
-a: List all files
-d : only list the directory itself
-l: List in long data serially, including file attributes and permissions, etc.
```

#### 2. cd

Change the current directory.

```
cd [relative path or absolute path]
```

#### 3. mkdir

Create directory.

```
## mkdir [-mp] directory name
-m: configure directory permissions
-p: Create directories recursively
```

#### 4. rmdir

Delete the directory. The directory must be empty.

```html
rmdir [-p] directory name
-p: Recursively delete directories
```

#### 5. touch

Update the file time or create a new file.

```html
## touch [-acdmt] filename
-a: update atime
-c: Update ctime, if the file does not exist, do not create a new file
-m: update mtime
-d: You can follow the update date without using the current date, or you can use --date="date or time"
-t: The update time can be followed instead of using the current time, the format is [YYYYMMDDhhmm]
```

#### 6. cp

Copy the file. If there are more than two source files, the destination file must be a directory.

```html
cp [-adfilprsu] source destination
-a: equivalent to -dr --preserve=all
-d: If the source file is a linked file, copy the linked file attributes instead of the file itself
-i: If the target file already exists, it will ask before overwriting.
-p: Copy the file together with its attributes
-r: Recursive copy
-u: Update destination only if destination is older than source, or copy only if destination does not exist
--preserve=all: In addition to the permission-related parameters of -p, SELinux attributes, links, xattr, etc. are also copied.
```

#### 7. rm

Delete files.

```html
## rm [-fir] file or directory
-r: Recursive deletion
```

#### 8.mv

Move files.

```html
## mv [-fiu] source destination
## mv [options] source1 source2 source3 .... directory
-f: force means force. If the target file already exists, it will be overwritten directly without asking.
```

### Modify permissions

A set of permissions can be represented by numbers. In this case, the three bits of a set of permissions are regarded as the bits of a binary number. The weight of each bit from left to right is 4, 2, and 1. That is, the numerical weight corresponding to each permission is r: 4, w: 2, x: 1.

```html
## chmod [-R] xyz dirname/filename
```

Example: Change the permissions of the .bashrc file to -rwxr-xr--.

```html
## chmod 754 .bashrc
```

You ca
n also use symbols to set permissions.

```html
## chmod [ugoa] [+-=] [rwx] dirname/filename
- u: owner
- g: group to which it belongs
- o: Others
- a: everyone
- +: add permissions
- -: Remove permissions
- =: Set permissions
```

Example: Add write permissions to the .bashrc file for all users.

```html
## chmod a+w .bashrc
```

###Default permissions

- File default permissions: The file does not have executable permissions by default, so it is 666, which is -rw-rw-rw-.
- Directory default permissions: The directory must be accessible, that is, it must be executable
permissions, so 777 , which is drwxrwxrwx.

You can set or view the default permissions through umask, usually expressed in the form of a mask. For example, 002 means that the permissions of other users have been removed by a permission of 2, which is the write permission. Therefore, the default permissions when creating a new file are -rw-rw-r--.

### Directory permissions

Filenames are not stored in the contents of a file, but in the directory in which the file is located. Therefore, having w permission on a file cannot modify the file name.

Directories store file lists, and the permissions of a directory are the permissions on its file list. Therefore, the r permission of a directory means that the file list can be read; the w permission means that the file list can be modified, specifically, adding, deleting files, and modifying file names; the x permission can make the directory a working directory.

### Link

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1e46fd03-0cda-4d60-9b1c-0c256edaf6b2.png" width="450px"> </div><br>


```html
## ln [-sf] source_filename dist_filename
-s: The default is an entity link, add -s for a symbolic link
-f: If the target file exists, delete the target file first
```

#### 1. Entity link

Create an entry in the directory to record the file name and inode number. This inode is the inode of the source file.

Delete any entry and the file will still exist, as long as the number of references is not 0.

There are the following restrictions: it cannot span file systems and cannot link directories.

```html
## ln /etc/crontab .
## ll -i /etc/crontab crontab
34474855 -rw-r--r--. 2 root root 451 Jun 10 2014 crontab
34474855 -rw-r--r--. 2 root root 451 Jun 10 2014 /etc/crontab
```

#### 2. Symbolic link

The symbolic link file saves the absolute path of the source file, which will be located at the source file when reading. It can be understood as a shortcut to Windows.

When the source file is deleted, the linked file cannot be opened.

Because the path is recorded, a symbolic link can be established for the directory.

```html
## ll -i /etc/crontab /root/crontab2
34474855 -rw-r--r--. 2 root root 451 Jun 10 2014 /etc/crontab
53745909 lrwxrwxrwx. 1 root root 12 Jun 23 22:31 /root/crontab2 -> /etc/crontab
```

### Get file content

#### 1. cat

Get the file contents.

```html
## cat [-AbEnTv] filename
-n: Print l
ine numbers, including blank lines, but -b will not
```

#### 2.tac

Is the reverse operation of cat, printing starts from the last line.

#### 3. more

Different from cat, it can view the file contents page by page, which is more suitable for viewing large files.

#### 4. less

Similar to more, but with the added function of page forwarding.

#### 5. head

Get the first few lines of the file.

```html
## head [-n number] filename
-n: followed by a number, indicating how many lines to display
```

#### 6.tail

It is the reverse operation of head, just getting the next few lines.

#### 7.od

Display binary files in character or hexadecimal format.

### Commands and File Search

#### 1. which

Command search.

```html
## which [-a] command
-a: List all instructions, not just the first one
```

#### 2. whereis

File search. It's faster because it only searches a few specific directories.

```html
## whereis [-bmsu] dirname/filename
```

#### 3. locate

File search. You can search using keywords or regular expressions.

locate uses the /var/lib/mlocate/ database to search. It is stored in memory and updated once a day, so you cannot use locate to search for newly created files. You can use updatedb to update the database immediately.

```html
## locate [-ir] keyword
-r: regular expression
```

#### 4. find

File search. You can search using the file's properties and permissions.

```html
## find [basedir] [option]
example: find . -name "shadow*"
```

**① Time-related options**

```html
-mtime n: List files whose contents were modified on the day n days ago
-mtime +n: List files whose contents were modified n days ago (excluding n days itself)
-mtime -n: List files whose content has been modified within n days (including n days itself)
-newer file: List files newer than file
```

The time ranges for +4, 4 and -4 indications are as follows:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/658fc5e7-79c0-4247-9445-d69bf194c539.png" width=""/> </div><br>

**② Options related to file owner and group**

```html
-uid n
-gid n
-user name
-group name
-nouser: Search for files whose owner does not exist in /etc/passwd
-nogroup: Search for files whose group does not exist in /etc/group
```

**③ Options related to file permissions and names**

```html
-name filename
-size [+-]SIZE: Search for files larger (+) or smaller (-) than SIZE. The specifications of this SIZE are: c: represents byte, k: represents 1024bytes. So, to find files larger than 50KB, just -size +50k
-type TYPE
-perm mode: Search files with permissions equal to mode
-perm -mode: Search files with permissions containing mode
-perm /mode: Search files with permissions containing any mode
```

## 6. Compression and packaging

### Compressed file name

There are many compressed file names under Linux, the common ones are as follows:

| Extension | Compressor |
| -- | -- |
| \*.Z | compress |
|\*.zip | zip |
|\*.gz | gzip|
|\*.bz2 | bzip2 |
|\*.xz | xz |
|\*.tar
| Data packaged by tar program, not compressed |
|\*.tar.gz | Files packaged by the tar program and compressed by gzip |
|\*.tar.bz2 | Files packaged by the tar program and compressed by bzip2 |
|\*.tar.xz | Files packaged by the tar program, compressed by xz |

### Compression instructions

#### 1. gzip

gzip is the most widely used compression command in Linux and can decompress files compressed by compress, zip and gzip.

After gzip compression, the source file no longer exists.

There are 9 different compression levels available.

You can use zcat, zmore, and zless to read the contents of compressed files.

```html
$ gzip [-cdtv#] filename
-c: Output compressed data to the screen
-d: decompress
-t: Check whether the compressed file has errors
-v: Display compression ratio and other information
-#: # means a number, representing the compression level. The larger the number, the higher the compression ratio. The default is 6
```

#### 2. bzip2

Provides higher compression ratio than gzip.

View commands: bzcat, bzmore, bzless, bzgrep.

```html
$ bzip2 [-cdkzv#] filename
-k: keep source files
```

#### 3.xz

Provides better compression than bzip2.

It can be seen that the compression ratios of gzip, bzip2, and xz are constantly optimized. However, it should be noted that the higher the compression ratio, the longer the compression time will be.

View commands: xzcat, xzmore, xzless, xzgrep.

```html
$ xz [-dtlkc#] filename
```

### Packing

The compression command can only compress one file, while the pack can pack multiple files into one large file. Tar can not only be used for packaging, but you can also use gzip, bzip2, and xz to compress the packaged files.

```html
$ tar [-z|-j|-J] [cv] [-f new tar file] filename... ==Package and compress
$ tar [-z|-j|-J] [tv] [-f existing tar file] ==View
$ tar [-z|-j|-J] [xv] [-f existing tar file] [-C directory] ==Unzip
-z: use zip;
-j: use bzip2;
-J: use xz;
-c: Create a new packaging file;
-t: Check what files are in the packaged file;
-x: Unpacking or decompression function;
-v: During the compression/decompression process, display the file name being processed;
-f: filename: the file to be processed;
-C directory: Extract in a specific directory.
```

| Usage | Commands |
| :---: | --- |
| Pack and compress | tar -jcv -f filename.tar.bz2 The name of the file or directory to be compressed |
| View | tar -jtv -f filename.tar.bz2 |
| Decompression | tar -jxv -f filename.tar.bz2 -C Directory to decompress |

## 7. Bash

You can request services from the kernel through the Shell, and Bash is just one type of Shell.

### Features

- Command history: record used commands
-Command and file completion: shortcut key: tab
- Named aliases: e.g. ll is an alias for ls -al
- shell scripts
- Wildcard characters: For example, ls -l /usr/bin/X\* lists all files starting with X under /usr/bin

### Variable operations

To assign a value to a variable directly use =.

To access a variable, you need to add \$ before the
variable, or you can use the form \${};

Output variables using the echo command.

```bash
$x=abc
$ echo $x
$ echo ${x}
```

If there are spaces in the variable content, double quotes or single quotes must be used.

- Special characters within double quotes can retain their original characteristics, for example, x="lang is \$LANG", then the value of x is lang is zh_TW.UTF-8;
- The special characters within single quotes are the special characters themselves. For example, x='lang is \$LANG', then the value of x is lang is \$LANG.

You can use \`instruction\` or \$(instruction) to assign the execution result of the instruction to a variable. For example, version=\$(uname -r), the value of version is 4.15.0-22-generic.

You can use the export command to convert custom variables into environment variables. Environment variables can be used in subprograms. The so-called subprograms are sub-Bash generated by the current Bash.

Bash variables can be declared as arrays and integer numbers. Note that numeric types do not have floating point numbers. If not declared, the default is string type. Variables are declared using the declare command:

```html
$ declare [-aixr] variable
-a: defined as array type
-i: defined as integer type
-x: defined as an environment variable
-r: defined as readonly type
```

Use [ ] to index into an array:

```bash
$ array[1]=a
$ array[2]=b
$ echo ${array[1]}
```

### Instruction search order

- Execute commands with absolute or relative paths, such as /bin/ls or ./ls;
- Find the instruction by alias and execute it;
- Executed by Bash's built-in instructions;
- Execute the first instruction found in the order of the search paths specified by the \$PATH variable.

### Data flow redirection

Redirection refers to using files instead of standard input, standard output, and standard error output.

| 1 | code | operator |
| :---: | :---: | :---:|
| Standard input (stdin) | 0 | \< or \<\< |
| Standard output (stdout) | 1 | &gt; or \>\> |
| Standard error output (stderr) | 2 | 2\> or 2\>\> |

Among them, one arrow indicates redirection in an overwriting manner, while two arrows indicates redirection in an appending manner.

Unnecessary standard output and standard error output can be redirected to /dev/null, which is equivalent to throwing it into the trash.

If you need to redirect standard output and standard error output to a file at the same time, you need to convert one output to another output. For example, 2\>&1 means converting standard error output to standard output.

```bash
$ find /home -name .bashrc > list 2>&1
```

## 8. Pipeline instructions

Pipes use the standard output of one command as the standard input of another command. Pipes can be used when the data needs to be processed in multiple steps before we can get what we want.

Use | between commands to separate individual pipeline commands.

```bash
$ ls -al /etc | less
```

### Fetch instructions

cut splits the data and extracts the desired part.

The segmentation
process proceeds line by line.

```html
$ cut
-d: delimiter
-f: After -d separation, use -f n to take out the nth interval
-c: Take out the interval in character units
```
Example 1: last displays the logged-in information and retrieves the username.

```html
$ last
root pts/1 192.168.201.101 Sat Feb 7 12:35 still logged in
root pts/1 192.168.201.101 Fri Feb 6 12:13 - 18:46 (06:33)
root pts/1 192.168.201.254 Thu Feb 5 22:37 - 23:53 (01:16)

$ last | cut -d ' ' -f 1
```

Example 2: Extract the information output by export and remove all strings after the 12th character.

```html
$ export
declare -x HISTCONTROL="ignoredups"
declare -x HISTSIZE="1000"
declare -x HOME="/home/dmtsai"
declare -x HOSTNAME="study.centos.vbird"
.....(Others omitted).....

$ export | cut -c 12-
```

### Sorting instructions

**sort** is used for sorting.

```html
$ sort [-fbMnrtuk] [file or stdin]
-f : ignore case
-b : Ignore leading spaces
-M: Sort by month name, such as JAN, DEC
-n: use numbers
-r: reverse sort
-u: Equivalent to unique, repeated content only appears once
-t: delimiter, default is tab
-k: Specify the sorting interval
```

Example: The contents of the /etc/passwd file are separated by : and are required to be sorted by the third column.

```html
$ cat /etc/passwd | sort -t ':' -k 3
root:x:0:0:root:/root:/bin/bash
dmtsai:x:1000:1000:dmtsai:/home/dmtsai:/bin/bash
alex:x:1001:1002::/home/alex:/bin/bash
arod:x:1002:1003::/home/arod:/bin/bash
```

**uniq** can take only one duplicate data.

```html
$ uniq [-ic]
-i : ignore case
-c: Count
```

Example: Get the total number of logins for each person

```html
$ last | cut -d ' ' -f 1 | sort | uniq -c
1
6 (unknown
47 dmtsai
4 reboot
7 root
1wtmp
```

### Bidirectional output redirection

Output redirection will redirect the output content to a file, and **tee** can not only complete this function, but also preserve the output on the screen. That is, using the tee command, an output is sent to both the file and the screen.

```html
$ tee [-a] file
```

### Character conversion instructions

**tr** is used to delete characters in a line or replace characters.

```html
$ tr [-ds] SET1 ...
-d: Delete the string SET1 in the line
```

Example, convert all lowercase information output by last to uppercase.

```html
$ last | tr '[a-z]' '[A-Z]'
```

   **col** Convert tab characters to space characters.

```html
$col[-xb]
-x: Convert the tab key to the equivalent space key
```

**expand** Convert tabs to a certain number of spaces, the default is 8.

```html
$ expand [-t] file
-t: The number of tabs converted to spaces
```

**join** Merges rows with the same data together.

```html
$ join [-ti12] file1 file2
-t: delimiter, default is space
-i : ignore case differences
-1: Comparison field used for the first file
-2: Comparison field used by the second file
```

**paste** Pastes two lines directly together.

```html
$ paste [-d] file1 file2
-d: delimiter, default is tab
```

### Partition instructions

**split** Divide a fi
le into multiple files.

```html
$ split [-bl] file PREFIX
-b: Partition by size, you can add units, such as b, k, m, etc.
-l: Partition by row number.
- PREFIX: the leading name of the partition file
```

## 9. Regular expressions

### grep

g/re/p (globally search a regular expression and print), uses regular expressions to globally search and print.

```html
$ grep [-acinv] [--color=auto] Search string filename
-c: Count the number of matching lines
-i: ignore case
-n: output line number
-v: Reverse selection, that is, display the line without search string content
--color=auto: Display the found keywords in color
```

Example: Extract the lines containing the string (note that there is a --color=auto option by default, so the following content displays the string in color in Linux)

```html
$ grep -n 'the' regular_express.txt
8:I can't finish the test.
12:the symbol '*' is represented as start.
15:You are the best is mean you are the no. 1.
16:The world Happy is the same with "glad".
18:google is the best tools for search keyword
```

Example: The regular expression a{m,n} is used to match the character a m\~n times. { and } need to be escaped here because they have special meaning in the shell.

```html
$ grep -n 'a\{2,5\}' regular_express.txt
```

### printf

For formatted output. It does not belong to the pipeline command. You need to use the $() form when transmitting data to printf.

```html
$ printf '%10s %5i %5i %5i %8.2f \n' $(cat printf.txt)
    DmTsai 80 60 92 77.33
     VBird 75 55 80 70.00
       Ken 60 90 70 73.33
```

### awk

It was created by Alfred Aho, Peter Weinberger and Brian Kernighan, and the name awk is the initials of the three founders.

awk processes one line at a time. The smallest unit of processing is a field. The naming method of each field is: \$n
, n is the field number, starting from 1, \$0 represents a whole row.

Example: Get the usernames and IPs of the last five logged-in users. First, use last -n 5 to get all the information of the last five logged-in users. You can see that the username and IP are in column 1 and column 3 respectively. We can use \$1 and \$3 to take out these two fields, and then use print to print.

```html
$ last -n 5
dmtsai pts/0 192.168.1.100 Tue Jul 14 17:32 still logged in
dmtsai pts/0 192.168.1.100 Thu Jul 9 23:36 - 02:58 (03:22)
dmtsai pts/0 192.168.1.100 Thu Jul 9 17:23 - 23:36 (06:12)
dmtsai pts/0 192.168.1.100 Thu Jul 9 08:02 - 08:17 (00:14)
dmtsai tty1 Fri May 29 11:55 - 12:11 (00:15)
```

```html
$ last -n 5 | awk '{print $1 "\t" $3}'
dmtsai 192.168.1.100
dmtsai 192.168.1.100
dmtsai 192.168.1.100
dmtsai 192.168.1.100
dmtsai Fri
```

Matching can be performed based on certain conditions of the field, such as matching the row of data where the field is less than a certain value.

```html
$ awk 'Condition type 1 {Action 1} Condition type 2 {Action 2} ...' filename
```

Example: The third field of the /etc/passwd file is UID, and data with UID less than 10 is processed.

```tex
t
$ cat /etc/passwd | awk 'BEGIN {FS=":"} $3 < 10 {print $1 "\t " $3}'
root 0
bin 1
daemon 2
```

awk variables:

| Variable name | Meaning |
| :--: | -- |
| NF | The total number of fields in each row |
| NR | Which row of data is currently being processed |
| FS | The current delimiter character, the default is the space bar |

Example: Show the row number being processed and how many fields each row has

```html
$ last -n 5 | awk '{print $1 "\t lines: " NR "\t columns: " NF}'
dmtsai lines: 1 columns: 10
dmtsai lines: 2 columns: 10
dmtsai lines: 3 columns: 10
dmtsai lines: 4 columns: 10
dmtsai lines: 5 columns: 9
```

## 10. Process Management

### View process

#### 1.ps

View process information at a certain point in time.

Example: View your own processes

```sh
## ps -l
```

Example: View all processes in the system

```sh
## ps aux
```

Example: View a specific process

```sh
## ps aux | grep threadx
```

#### 2. pstree

View the process tree.

Example: View all process trees

```sh
## pstree -A
```

#### 3. top

Display process information in real time.

Example: Refresh every two seconds

```sh
## top -d 2
```

#### 4. netstat

View processes occupying ports

Example: View processes on a specific port

```sh
## netstat -anp | grep port
```

### Process status

| Status | Description |
| :---: | --- |
| R | running or runnable (on run queue)<br>Executing or executable, when the process is in the execution queue. |
| D | uninterruptible sleep (usually I/O)<br>Uninterruptible blocking, usually IO blocking. |
| S | interruptible sleep (waiting for an event to complete) <br> Interruptible blocking, when the process is waiting for an event to complete. |
| Z | zombie (terminated but not reaped by its parent)<br>Zombie, the process has been terminated but the information has not been obtained by its parent process. |
| T | stopped (either by a job control signal or because it is being traced) <br> Ended, the process can either be ended by a job control signal or because it is being traced. |
<br>

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2bab4127-3e7d-48cc-914e-436be859fb05.png" width="490px"/> </div><br>

### SIGCHLD

When a child process changes its state (stops running, continues running, or exits), two things happen to the parent process:

- Get SIGCHLD signal;
- waitpid() or wait() calls will return.

The SIGCHLD signal sent by the child process contains information about the child process, such as process ID, process status, and the time the process uses the CPU.

When a child process exits, its process descriptor will not be released immediately. This is to allow the parent process to obtain information about the child process. The parent process uses wait() and waitpid() to obtain information about an exited child process.

<div align="center"> <!-- <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/flow.png" width=""/> --> </div><br>

### wait()

```c
pid_t wait(int *stat
us)
```

When the parent process calls wait(), it will block until it receives a SIGCHLD signal for the child process to exit, after which the wait() function will destroy the child process and return.

If successful, the process ID of the collected child process is returned; if the calling process has no child processes, the call will fail, and -1 will be returned, and errno will be set to ECHILD.

The status parameter is used to save some status of the collected child process when it exits. If you don't care how the child process died and just want to destroy the child process, you can set this parameter to NULL.

### waitpid()

```c
pid_t waitpid(pid_t pid, int *status, int options)
```

The function is exactly the same as wait(), but there are two more parameters pid and options that can be controlled by the user.

The pid parameter indicates the ID of a child process, indicating that it only cares about the SIGCHLD signal when this child process exits. if
When pid=-1, it has the same effect as wait(), both caring about the SIGCHLD signal of all child processes exiting.

The options parameter mainly has two options, WNOHANG and WUNTRACED. WNOHANG can make the waitpid() call non-blocking, which means that it will return immediately and the parent process can continue to perform other tasks.

### Orphan process

If a parent process exits while one or more of its child processes are still running, these child processes will become orphan processes.

The orphan processes will be adopted by the init process (process number 1), and the init process will complete status collection for them.

Since the orphan process will be adopted by the init process, the orphan process will not cause harm to the system.

### Zombie process

The process descriptor of a child process will not be released when the child process exits. It will be released only after the parent process obtains the child process information through wait() or waitpid(). If the child process exits but the parent process does not call wait() or waitpid(), then the process descriptor of the child process is still saved in the system. This process is called a zombie process.

The status of the zombie process displayed through the ps command is Z (zombie).

The process numbers that can be used by the system are limited. If a large number of zombie processes are generated, the system will not be able to generate new processes because there are no available process numbers.

To eliminate a large number of zombie processes in the system, you only need to kill its parent process. At this time, the zombie process will become an orphan process and will be adopted by the init process. In this way, the init process will release all the resources occupied by the zombie process, thus ending the zombie process.

## References

- Brother Niao. Brother Niao's Basics of Linux Private Kitchen, Third Edition [J]. 2009.
- [Software package management on Linux platform](https://www.ibm.com/developerworks/cn/li
nux/l-cn-rpmdpkg/index.html)
- [Linux Daemon processes, zombie processes and orphan processes](http://liubigbin.github.io/2016/03/11/Linux-%E4%B9%8B%E5%AE%88%E6%8A%A4%E8%BF%9B%E 7%A8%8B%E3%80%81%E5%83%B5%E6%AD%BB%E8%BF%9B%E7%A8%8B%E4%B8%8E%E5%AD%A4%E5%84%BF%E8%BF%9B%E7%A8%8B/)
- [What is the difference between a symbolic link and a hard link?](https://stackoverflow.com/questions/185899/what-is-the-difference-between-a-symbolic-link-and-a-hard-link)
- [Linux process states](https://idea.popcount.org/2012-12-11-linux-process-states/)
- [GUID Partition Table](https://en.wikipedia.org/wiki/GUID_Partition_Table)
- [Detailed explanation of wait and waitpid functions](https://blog.csdn.net/kevinhg/article/details/7001719)
- [Introduction to IDE, SATA, SCSI, SAS, FC, SSD hard disk types](https://blog.csdn.net/tianlesoftware/article/details/6009110)
- [Akai IB-301S SCSI Interface for S2800,S3000](http://www.mpchunter.com/s3000/akai-ib-301s-scsi-interface-for-s2800s3000/)
- [Parallel ATA](https://en.wikipedia.org/wiki/Parallel_ATA)
- [ADATA XPG SX900 256GB SATA 3 SSD Review – Expanded Capacity and SandForce Driven Speed](http://www.thessdreview.com/our-reviews/adata-xpg-sx900-256gb-sata-3-ssd-review-expanded-capacity-and-sandforce-driven-speed/4/)
- [Decoding UCS Invicta – Part 1](https://blogs.cisco.com/datacenter/decoding-ucs-invicta-part-1)
- [Hard Disk](https://zh.wikipedia.org/wiki/%E7%A1%AC%E7%9B%98)
- [Difference between SAS and SATA](http://www.differencebetween.info/difference-between-sas-and-sata)
- [BIOS](https://zh.wikipedia.org/wiki/BIOS)
- [File system design case studies](https://www.cs.rutgers.edu/\~pxk/416/notes/13-fs-studies.html)
- [Programming Project #4](https://classes.soe.ucsc.edu/cmps111/Fall08/proj4.shtml)
- [FILE SYSTEM DESIGN](http://web.cs.ucla.edu/classes/fall14/cs111/scribe/11a/index.html)
