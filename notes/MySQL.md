#MySQL
<!-- GFM-TOC -->
* [MySQL](#mysql)
    * [一、index](#一index)
        * [B+ Tree principle](#b-tree-principle)
        * [MySQL Index](#mysql-index)
        * [Index Optimization](#index optimization)
        * [Advantages of index](#Advantages of index)
        * [Conditions for using index](#Conditions for using index)
    * [2. Query performance optimization] (#2 Query performance optimization)
        * [Use Explain for analysis](#Use-explain-for analysis)
        * [Optimize data access](#optimize data access)
        * [Reconstruct query method](#Reconstruct query method)
    * [三、Storage Engine](#三综合engine)
        * [InnoDB](#innodb)
        * [MyISAM](#myisam)
        * [Compare](#Compare)
    * [Four, data type](#four data type)
        * [integer type](#integer type)
        * [Floating point number](#Floating point number)
        * [string](#string)
        * [time&date](#time&date)
    * [五、分](#五分)
        * [Horizontal split](#horizontal split)
        * [vertical split](#vertical split)
        * [Sharding strategy](#sharding-strategy)
        * [Problems with Sharding](#sharding-problems)
    * [6.Copy](#6Copy)
        * [Master-slave replication](#master-slave replication)
        * [Read-write separation](#read-write separation)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Index

### B+ Tree principle

#### 1. Data structure

B Tree refers to Balance Tree, which is also a balanced tree. A balanced tree is a search tree in which all leaf nodes are at the same level.

B+ Tree is implemented based on B Tree and leaf node sequential access pointers. It has the balance of B Tree and improves the performance of interval queries through sequential access pointers.

In B+ Tree, the keys in a node are from the left
To the right non-decreasing arrangement, if the left and right adjacent keys of a pointer are key<sub>i</sub> and key<sub>i+1</sub> respectively, and are not null, then all the keys pointed to by the pointer are greater than or equal to key<sub>i</sub> and less than or equal to key<sub>i+1</sub>.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/33576849-9275-47bb-ada7-8ded5f5e7c73.png" width="350px"> </div><br>

#### 2. Operation

When performing a search operation, first perform a binary search on the root node to find a pointer where the key is located, and then recursively search on the node pointed by the pointer. Until the leaf node is found, then perform a binary search on the leaf node to find the data corresponding to the key.

Insertion and deletion operations will destroy the balance of the balanced tree. Therefore, after the insertion and deletion operations, the tree needs to be split, merged, rotated, etc. to maintain the balance.

#### 3. Comparison with red-black trees

Balanced trees such as red-black trees can also be used to implement indexes, but file systems and database systems generally use B+ Trees as index structures because B+ trees have higher performance when accessing disk data.

(1) B+ trees have lower tree heights

The tree height of a balanced tree is O(h)=O(log<sub>d</sub>N), where d is the out-degree of each node. The out-degree of the red-black tree is 2, and the out-degree of the B+ Tree is generally very large, so the tree height h of the red-black tree is obviously much larger than that of the B+ Tree.

(2) Principle of disk access

The operating system generally divides the memory and disk into fixed-size blocks, each block is called a page, and the memory and disk exchange data in units of pages. The database system sets the size of a node in the index to the page size so that a node can be fully loaded in a single I/O.

If the data is not on the same disk block, it is usually necessary to move the brake arm for seeking, and the brake arm's physical structure causes inefficiency in movement, thereby increasing disk data read time. The B+ tree has a lower tree height than the red-black tree. The number of seeks is proportional to the tree height. Accessing the same disk block only requires a short disk rotation time, so the B+ tree is more suitable for reading disk data.

(3) Disk read-ahead characteristics

In order to reduce disk I/O operations, the disk is often not read strictly on demand, but read ahead every time. During the read-ahead process, the disk reads sequentially. Sequential reading does not require disk seeking and only requires
For a short disk spin time, the speed will be very fast. And you can take advantage of the read-ahead feature, and adjacent nodes can also be preloaded.

### MySQL index

Indexes are implemented at the storage engine layer, not at the server layer, so different storage engines have different index types and implementations.

#### 1. B+Tree index

Is the default index type for most MySQL storage engines.

Because there is no longer a need to perform a full table scan and only need to search the tree, the search speed is much faster.

Because of the orderliness of B+ Tree, in addition to searching, it can also be used for sorting and grouping.

You can specify multiple columns as index columns, and multiple index columns together form the key.

Applicable to full key value, key value range and key prefix search, where key prefix search is only applicable to leftmost prefix search. The index cannot be used if the search is not in the order of the indexed columns.

InnoDB's B+Tree index is divided into primary index and auxiliary index. The data field of the leaf node of the main index records complete data records. This indexing method is called a clustered index. Because data rows cannot be stored in two different places, a table can only have one clustered index.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/45016e98-6879-4709-8569-262b2d6d60b9.png" width="350px"> </div><br>

The data field of the leaf node of the auxiliary index records the value of the primary key. Therefore, when using the auxiliary index to search, you need to find the primary key value first, and then search in the primary index.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7c349b91-050b-4d72-a7f8-ec86320307ea.png" width="350px"> </div><br>

#### 2. Hash index

Hash indexes can be looked up in O(1) time, but ordering is lost:

- Cannot be used for sorting and grouping;
- Only supports precise search and cannot be used for partial search and range search.

The InnoDB storage engine has a special feature called "adaptive hash index". When an index value is used very frequently, a hash index will be created on top of the B+Tree index, so that the B+Tree index has some of the advantages of a hash index, such as fast hash search.

#### 3.
Full text index

The MyISAM storage engine supports full-text indexing, which is used to find keywords in the text instead of directly comparing for equality.

The search condition uses MATCH AGAINST instead of plain WHERE.

Full-text indexing is implemented using an inverted index, which records the mapping of keywords to the documents in which they are located.

The InnoDB storage engine also supports full-text indexing in MySQL 5.6.4.

#### 4. Spatial data index

The MyISAM storage engine supports spatial data index (R-Tree), which can be used for geographic data storage. Spatial data indexes index data from all dimensions and can effectively use any dimension for combined queries.

GIS-related functions must be used to maintain the data.

### Index optimization

#### 1. Independent columns

When making a query, the index column cannot be part of an expression or a parameter of a function, otherwise the index cannot be used.

For example, the following query cannot use an index on the actor_id column:

```sql
SELECT actor_id FROM sakila.actor WHERE actor_id + 1 = 5;
```

#### 2. Multi-column index

When you need to use multiple columns as conditions for a query, using a multi-column index has better performance than using multiple single-column indexes. For example, in the following statement, it is best to set actor_id and film_id as multi-column indexes.

```sql
SELECT film_id, actor_ id FROM sakila.film_actor
WHERE actor_id = 1 AND film_id = 1;
```

#### 3. Order of index columns

Put the most selective index columns first.

Index selectivity refers to the ratio of unique index values ​​to the total number of records. The maximum value is 1, at which time each record has a unique index corresponding to it. The higher the selectivity, the higher the discrimination of each record and the higher the query efficiency.

For example, in the results shown below, customer_id is more selective than staff_id, so it is best to put the customer_id column in front of the multi-column index.

```sql
SELECT COUNT(DISTINCT staff_id)/COUNT(*) AS staff_id_selectivity,
COUNT(DISTINCT customer_id)/COUNT(*) AS customer_id_selectivity,
COUNT(*)
FROM payment;
```

```html
   staff_id_sel
Activity: 0.0001
customer_id_selectivity: 0.0373
               COUNT(*): 16049
```

#### 4. Prefix index

For columns of type BLOB, TEXT, and VARCHAR, you must use a prefix index to index only the first part of the character.

The selection of prefix length needs to be determined based on index selectivity.

#### 5. Covering index

The index contains the values of all the fields that need to be queried.

Has the following advantages:

- Indexes are usually much smaller than the size of the data rows, and reading only the index can greatly reduce data access.
- Some storage engines (e.g. MyISAM) only cache indexes in memory and rely on the operating system to cache the data. Therefore, accessing only the index eliminates the need for system calls (which are often time consuming).
- For the InnoDB engine, there is no need to access the primary index if the secondary index can cover the query.

### Advantages of indexing

- Significantly reduces the number of data rows that the server needs to scan.

- Help the server avoid sorting and grouping, and avoid creating temporary tables (B+Tree indexes are ordered and can be used for ORDER BY and GROUP BY operations. Temporary tables are mainly created during the sorting and grouping process, and no sorting and grouping are required, so there is no need to create temporary tables).

- Turn random I/O into sequential I/O (B+Tree index is ordered and will store adjacent data together).

### Index usage conditions

- For very small tables, in most cases a simple full table scan is more efficient than indexing;

- For medium to large tables, indexes are very effective;

- But for extremely large tables, the cost of creating and maintaining indexes will increase. In this case, you need to use a technology that can directly distinguish a set of data that needs to be queried, rather than matching record by record. For example, you can use partitioning technology.

## 2. Query performance optimization

### Use Explain for analysis

Explain is used to analyze SELECT query statements. Developers can optimize query statements by analyzing Explain results.

The more important fields are:

- select_type: Query type, including simple query, joint query, subquery, etc.
- key: the index used
- rows: number of rows scanned

### Optimize data access

#### 1. Reduce the amount of data requested

- Return only necessary columns: it is best not to use SELECT * statements.
- Return only necessary rows: Use the LIMIT statement to limit the data returned.
- Cache data for repeated queries: Using cache can avoid queries in the database, especially for the data to be queried.
When queries are frequently repeated, the query performance improvement brought by caching will be very obvious.

#### 2. Reduce the number of rows scanned by the server

The most efficient way is to use an index to cover the query.

### Reconstruct query method

#### 1. Split large query

If a large query is executed at once, it may lock a lot of data at once, occupy the entire transaction log, exhaust system resources, and block many small but important queries.

```sql
DELETE FROM messages WHERE create < DATE_SUB(NOW(), INTERVAL 3 MONTH);
```

```sql
rows_affected = 0
do {
    rows_affected = do_query(
    "DELETE FROM messages WHERE create < DATE_SUB(NOW(), INTERVAL 3 MONTH) LIMIT 10000")
} while rows_affected > 0
```

#### 2. Decompose large join query

Decompose a large join query into a single table query for each table, and then perform the correlation in the application. The benefits of doing so are:

- Make caching more efficient. For join queries, if one of the tables changes, the entire query cache becomes unavailable. For multiple queries after decomposition, even if one table changes, the query cache for other tables can still be used.
- Decompose it into multiple single-table queries. The cached results of these single-table queries are more likely to be used by other queries, thereby reducing redundant record queries.
- Reduce lock contention;
- Connecting at the application layer makes it easier to split the database, making it easier to achieve high performance and scalability.
- The efficiency of the query itself may also be improved. For example, in the following example, using IN() instead of a join query allows MySQL to query in ID order, which may be more efficient than a random join.

```sql
SELECT * FROM tag
JOIN tag_post ON tag_post.tag_id=tag.id
JOIN post ON tag_post.post_id=post.id
WHERE tag.tag='mysql';
```

```sql
SELECT * FROM tag WHERE tag='mysql';
SELECT * FROM tag_post WHERE tag_id=1234;
SELECT * FROM post WHERE post.id IN (123
,456,567,9098,8904);
```

## 3. Storage engine

### InnoDB

It is the default transactional storage engine of MySQL. Only when you need features that it does not support, other storage engines will be considered.

Four standard isolation levels are implemented, and the default level is REPEATABLE READ. Under the repeatable read isolation level, phantom reads are prevented through multi-version concurrency control (MVCC) + Next-Key Locking.

The main index is a clustered index, which saves data in the index to avoid directly reading the disk, thus greatly improving query performance.

Many optimizations have been made internally, including predictable reads when reading data from disk, adaptive hash indexes that can speed up read operations and are automatically created, insert buffers that can speed up insert operations, etc.

Supports true online hot backup. Other storage engines do not support online hot backup. To obtain a consistent view, you need to stop writing to all tables. In a mixed read-write scenario, stopping writing may also mean stopping reading.

### MyISAM

The design is simple and the data is stored in a compact format. For read-only data, or if the table is small and can tolerate repair operations, you can still use it.

Provides a large number of features, including compressed tables, spatial data indexes, etc.

Transactions are not supported.

Row-level locks are not supported, and only the entire table can be locked. Shared locks will be added to all tables that need to be read when reading, and exclusive locks will be added to the table when writing. But while the table is being read, new records can also be inserted into the table. This is called concurrent insertion (CONCURRENT INSERT).

Check and repair operations can be performed manually or automatically, but unlike transaction recovery and crash recovery, some data may be lost, and the repair operation is very slow.

If the DELAY_KEY_WRITE option is specified, when each modification is completed, the modified index data will not be written to disk immediately, but will be written to the key buffer in memory. The corresponding index block will only be written to disk when the key buffer is cleared or the table is closed. This method can greatly improve write performance, but when the database or host crashes, it will cause index damage and requires repair operations.

### Compare

- Transaction: InnoDB is transactional and can use Commit and Rollback statements.

- Concurrency: MyISAM only supports table-level locks, while InnoDB also supports row-level locks.

- Foreign keys: InnoDB supports foreign keys.

- Backup: InnoDB supports online hot backup.

- Crash recovery: The probability of corruption after MyISAM crashes is much higher than that of InnoDB, and the recovery speed is also slower.

- Other features: MyISAM supports compressed tables and spatial data indexes.

## 4. Data type

###
integer

TINYINT, SMALLINT, MEDIUMINT, INT, and BIGINT use 8, 16, 24, 32, and 64-bit storage space respectively. In general, the smaller the column, the better.

The number in INT(11) only specifies the number of characters displayed by the interactive tool, and is meaningless for storage and calculation.

### Floating point number

FLOAT and DOUBLE are floating point types, and DECIMAL is a high-precision decimal type. The CPU natively supports floating-point operations, but does not support DECIMAl type calculations, so DECIMAL calculations are more expensive than floating-point types.

FLOAT, DOUBLE and DECIMAL can all specify the column width. For example, DECIMAL(18, 9) means a total of 18 bits, 9 bits are used to store the decimal part, and the remaining 9 bits are used to store the integer part.

### string

There are mainly two types: CHAR and VARCHAR, one is fixed length and the other is variable length.

VARCHAR This variable-length type saves space because only the necessary content needs to be stored. However, when executing UPDATE, the row may become longer than the original. When the size that can be accommodated by one page is exceeded, additional operations must be performed. MyISAM will split the rows into different fragments for storage, while InnoDB needs to split the page to fit the rows into the page.

During storage and retrieval, spaces at the end of VARCHAR are preserved and spaces at the end of CHAR are removed.

### Time and date

MySQL provides two similar date and time types: DATETIME and TIMESTAMP.

#### 1. DATETIME

Capable of saving dates and times from the year 1000 to 9999 with seconds accuracy, using 8 bytes of storage.

It has nothing to do with time zone.

By default, MySQL displays DATETIME values ​​in a sortable, unambiguous format, such as "2008-01-16 22:37:08", which is the way to represent dates and times as defined by the ANSI standard.

#### 2. TIMESTAMP

Same as UNIX timestamp, saves the number of seconds since midnight (Greenwich Mean Time) on January 1, 1970, uses 4 bytes, and can only represent the years from 1970 to 2038.

It is related to time zones, which means that the specific time represented by a timestamp in different time zones is different.

MySQL provides the FROM_UNIXTIME() function to convert UNIX timestamps to dates, and the UNIX_TIMESTAMP() function to convert dates to UNIX timestamps.

Default
Below, if the value of the TIMESTAMP column is not specified when inserting, the value will be set to the current time.

TIMESTAMP should be used whenever possible because it is more space efficient than DATETIME.

## 5. Segmentation

### Horizontal segmentation

Horizontal sharding, also known as Sharding, splits records in the same table into multiple tables with the same structure.

When the data in a table continues to increase, Sharding is an inevitable choice. It can distribute the data to different nodes in the cluster, thereby caching the pressure of a single database.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/63c2909f-0c5f-496f-9fe5-ee9176b31aba.jpg" width=""> </div><br>

### Vertical split

Vertical segmentation is to split a table into multiple tables by columns, usually based on the density of column relationships. Vertical segmentation can also be used to split frequently used columns and infrequently used columns into different tables.

Using vertical segmentation at the database level will deploy it into different libraries according to the density of tables in the database. For example, the original e-commerce database will be vertically segmented into a product database, a user database, etc.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e130e5b8-b19a-4f1e-b860-223040525cf6.jpg" width=""> </div><br>

### Sharding strategy

- Hash modulo: hash(key) % N;
- Range: It can be an ID range or a time range;
- Mapping table: Use a separate database to store mapping relationships.

### Problems with Sharding

#### 1. Transaction issues

Use distributed transactions to solve, such as XA interface.

#### 2. Connection

The original connection can be decomposed into multiple single-table queries, and then connected in the user program.

#### 3. ID uniqueness

- Use Globally Unique ID (GUID)
- Specify an ID range for each shard
- Distributed ID generators (such as Twitter’s Snowflake algorithm)

## 6. Copy

### Master-slave replication

Mainly involves three threads: binlog thread, I/O thread and SQL thread.

-
**binlog thread**: Responsible for writing data changes on the main server to the binary log (Binary log).
- **I/O thread**: Responsible for reading binary logs from the master server and writing to the relay log (Relay log) of the slave server.
- **SQL thread**: Responsible for reading the relay log, parsing out the data changes that have been performed by the master server and replaying them in the slave server (Replay).

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/master-slave.png" width=""> </div><br>

### Read and write separation

The master server handles write operations and read operations with high real-time requirements, while the slave server handles read operations.

The reasons why read-write separation can improve performance are:

- The master and slave servers are responsible for their own reading and writing, which greatly alleviates lock contention;
- The slave server can use MyISAM to improve query performance and save system overhead;
- Increase redundancy and improve availability.

Read and write separation is often implemented through a proxy. The proxy server receives read and write requests from the application layer and then decides which server to forward them to.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/master-slave-proxy.png" width=""> </div><br>

## References

- BaronScbwartz, PeterZaitsev, VadimTkacbenko, et al. High-performance MySQL[M]. Electronic Industry Press, 2013.
- Jiang Chengyao. MySQL technology insider: InnoDB storage engine [M]. Machinery Industry Press, 2011.
- [20+ best experiences in MySQL performance optimization](https://www.jfox.info/20-tiao-mysql-xing-nen-you-hua-de-zui-jia-jing-yan.html)
- [Server Guide Data Storage | MySQL (09) Distributed dilemmas and countermeasures caused by sub-databases and tables](http://blog.720ui.com/2017/mysql_core_09_multi_db_table2/ "Server Guide Data Storage | MySQL (09)
Distributed dilemmas and countermeasures caused by databases and sub-tables")
- [How to create unique row ID in sharded databases?](https://stackoverflow.com/questions/788829/how-to-create-unique-row-id-in-sharded-databases)
- [SQL Azure Federation – Introduction](http://geekswithblogs.net/shaunxu/archive/2012/01/07/sql-azure-federation-ndash-introduction.aspx "Title of this entry.")
- [Data structure and algorithm principles behind MySQL index](http://blog.codinglabs.org/articles/theory-of-mysql-index.html)
- [MySQL performance optimization artifact Explain usage analysis](https://segmentfault.com/a/1190000008131735)
- [How Sharding Works](https://medium.com/@jeeyoungk/how-sharding-works-b4dec46b3f6)
- [Practice of sub-database and sub-table of Dianping order system](https://tech.meituan.com/dianping_order_db_sharding.html)
- [B + tree](https://zh.wikipedia.org/wiki/B%2B%E6%A0%91)
