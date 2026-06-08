<!-- GFM-TOC -->
* [1.Basic](#一basic)
* [2. Create table](#2 Create table)
* [3. Modification table](#三modification table)
* [四、INSERT](#四INSERT)
* [五、UPDATE](#五UPDATES)
*[6.Delete](#6Delete)
* [Seven. Query](#七query)
    * [DISTINCT](#distinct)
    * [LIMIT](#limit)
* [eight, sort](#八sort)
* [Nine, filter](#九filter)
* [十, wildcard](#十wildcard)
* [Eleven, calculated field](#Eleven calculated field)
* [Twelve, function](#twelve function)
    * [Summary](#summary)
    * [Text Processing](#textprocessing)
    * [Date and Time Processing](#Date and Time Processing)
    * [Numerical processing](#numerical processing)
* [Thirteen, grouping](#十三组)
* [Fourteen, subquery](#四四subquery)
* [Fifteen, connection](#十五Connection)
    * [Inner connection](#inner connection)
    * [Self-connection](#self-connection)
    * [natural connection](#natural connection)
    * [Outer connection](#Outer connection)
* [Sixteen, combination query](#六 Combination query)
* [Seventeen, view](#七VIEW)
* [Eighteen, stored procedure](#eighteen stored procedure)
* [Nineteen, cursor](#九九cursor)
* [Twenty, Trigger](#TWENTY Trigger)
* [Twenty-one, affairs management](#十一事management)
* [Twenty-two, character set](# Twenty-two character set)
* [Twenty-three, permission management](#十三 permission management)
* [References](#references)
<!-- GFM-TOC -->


# 1. Basics

The schema defines how data is stored, what kind of data is stored, and how the data is decomposed. Both databases and tables have schemas.

The value of the primary key is not allowed to be modified or reused (the deleted primary key value cannot be assigned to the primary key of a new data row).

SQL (Structured Query Language), standard SQL is managed by the ANSI Standards Committee, so it is called ANSI SQL. Each DBMS has its own implementation, such as PL/SQL, Transact-SQL, etc.

SQL statements are not case-sensitive, but whether database table names, column names, and values ​​are case-sensitive depends on the specific DBMS and configuration.

SQL supports the following three types of comments:

```sql
# Comment
SELECT *
FROM mytable; -- comments
/* Note 1
   Note 2 */
```

Database creation and use:

```sql
CREATE DATABASE test;
USE test;
```

# 2. Create table

```sql
CREATE TABLE mytable (
  # int type, not empty, auto-increment
  id INT NOT NULL AUTO_INCREMENT,
  # int type, not nullable, default value is 1, not nullable
  col1 INT NOT NULL DEFAULT 1,
  # Variable length string type, up to 45 characters, can be empty
  col2 VARCHAR(45) NULL,
  # Date type, can be empty
  col3 DATE NULL,
  # Set the primary key to id
  PRIMARY KEY (`id`));
```

# 3. Modify table

Add column

```sql
ALTER TABLE mytable
ADD col CHAR(20);
```

Delete column

```sql
ALTER TABLE mytable
DROP COLUMN col;
```

Delete table

```sql
DROP TABLE mytable;
```

# 4. Insert

Normal insert

```sql
INSERT INTO mytable(col1, col2)
VALUES(val1, val2);
```

Insert retrieved data

```sql
INSERT INTO mytable1(col1, col2)
SELECT col1, col2
FROM mytable2;
```

Insert the contents of a table into a new table

```sql
CREATE TABLE newtable AS
SELECT * FROM mytable;
```

# 5. Update

```sql
UPDATE mytable
SET col = val
WHERE id = 1;
```

# 6. Delete

```sql
DELETE FROM mytable
WHERE id = 1;
```

**TRUNCATE TABLE** can clear the table, that is, delete all rows.

```sql
TRUNCATE TABLE mytable;
```

Be sure to use the WHERE clause when using update and delete operations, otherwise the data in the entire table will be destroyed. You can use the SELECT statement to test first to prevent incorrect deletion.

# 7. Query

## DISTINCT

The same value will appear only once. It operates on all columns, which means that all columns must have the same value to be considered the same.

```sql
SELECT DISTINCT col1, col2
FROM mytable;
```

## LIMIT

Limit the number of rows returned. It can have two parameters. The first parameter is the starting row, starting from 0; the second parameter is the total number of rows returned.

Return the first 5 rows:

```sql
SELECT *
FROM mytable
LIMIT 5;
```

```sql
SELECT *
FROM mytable
LIMIT 0, 5;
```

Return to line 3 \~ 5:

```sql
SELECT *
FROM mytable
LIMIT 2, 3;
```

# 8. Sorting

- **ASC** : ascending order (default)
- **DESC** : Descending order

You can sort by multiple columns and specify a different sorting method for each column:

```sql
SELECT *
FROM mytable
ORDER BY col1 DESC, col2 ASC;
```

# 9. Filter

The data without filtering is very large, resulting in excess data being transferred over the network, wasting network bandwidth. Therefore, try to use SQL statements to filter unnecessary data instead of transmitting all data to the client and then filtering it by the client.

```sql
SELECT *
FROM mytable
WHERE col IS NULL;
```

The following table shows the operators available for the WHERE clause

| Operator | Description |
| :---: | :---: |
| = | equals |
| &lt; | less than |
| &gt; | greater than |
| &lt;&gt; != | Not equal to |
| &lt;= !&gt; | Less than or equal to |
| &gt;= !&lt; | Greater than or equal to |
| BETWEEN | Between two values |
| IS NULL | is a NULL value |

It should be noted that NULL is different from 0 and the empty string.

**AND and OR** are used to join multiple filter criteria. Prioritize AND processing. When a filter expression involves multiple ANDs and ORs, () can be used to determine the priority, making the priority relationship clearer.

The **IN** operator is used to match a set of values, and can also be followed by a SELECT clause to match a set of values ​​obtained by a subquery.

The **NOT** operator is used to negate a condition.

# ten
, wildcard

Wildcards are also used in filter statements, but they can only be used with text fields.

- **%** matches \>=0 any characters;

- **\_** matches ==1 any character;

- **[ ]** can match characters within the set, for example [ab] will match the characters a or b. Use the caret ^ to negate it, that is, it does not match the characters in the set.

Use Like for wildcard matching.

```sq
l
SELECT *
FROM mytable
WHERE col LIKE '[^AB]%'; -- any text not starting with A and B
```

Don't abuse wildcards, wildcards at the beginning will make matching very slow.

# 11. Calculated fields

Converting and formatting data on the database server is often much faster than on the client, and reducing the amount of data converted and formatted can reduce network traffic.

Calculated fields usually need to use **AS** to get aliases, otherwise the field names are calculated expressions when output.

```sql
SELECT col1 * col2 AS alias
FROM mytable;
```

**CONCAT()** is used to concatenate two fields. Many databases will use spaces to fill a value to the column width, so the connection result will have some unnecessary spaces. Use **TRIM()** to remove leading and trailing spaces.

```sql
SELECT CONCAT(TRIM(col1), '(', TRIM(col2), ')') AS concat_col
FROM mytable;
```

# 12. Function

The functions of each DBMS are different and therefore not portable. The following are mainly MySQL functions.

## Summary

|Function |Description|
| :---: | :---: |
| AVG() | Returns the average of a column |
| COUNT() | Returns the number of rows in a column |
| MAX() | Returns the maximum value of a column |
| MIN() | Returns the minimum value of a column |
| SUM() |Returns the sum of values in a column |

AVG() ignores NULL rows.

Use DISTINCT to summarize different values.

```sql
SELECT AVG(DISTINCT col1) AS avg_col
FROM mytable;
```

## Text processing

| Function | Description |
| :---: | :---: |
| LEFT() | The character on the left |
| RIGHT() | The character on the right |
| LOWER() | Convert to lowercase characters |
| UPPER() | Convert to uppercase characters |
| LTRIM() | Remove left spaces |
| RTRIM() | Remove spaces on the right |
| LENGTH() | Length |
| SOUNDEX() | Convert to speech value |

Among them, **SOUNDEX()** can convert a string into an alphanumeric pattern that describes its phonetic representation.

```sql
SELECT *
FROM mytable
WHERE SOUNDEX(col1) = SOUNDEX('apple')
```

## Date and time processing


- Date format: YYYY-MM-DD
- Time format: HH:\<zero-width space\>MM:SS

|Function | Description|
| :---: | :---: |
| ADDDATE() | Add a date (day, week, etc.) |
| ADDTIME() | Add a time (hour, minute, etc.) |
| CURDATE() | Returns the current date |
| CURTIME() | Return the current time |
| DATE() |Returns the date part of the datetime|
| DATEDIFF() |Calculate the difference between two dates|
| DATE_ADD() | Highly flexible date operation function |
| DATE_FORMAT() | Returns a formatted date or time string |
| DAY()| Returns the day part of a date|
|DAYOFWEEK() |For a date, return the corresponding day of the week|
| HOUR() |Returns the hour part of a time|
| MINUTE() |Returns the minute part of a time|
| MONTH() |Returns the month part of a date|
| NOW() | Returns the current date and time |
| SECOND() |Returns the seconds part of a time|
| TIME() |Returns the time part of a datetime|
| YEAR() |Returns the year part of a date|

```sql
mysql> SELEC
T NOW();
```

```
2018-4-14 20:25:11
```

## Numerical processing

| Function | Description |
| :---: | :---: |
| SIN() | sine |
| COS() | cosine |
| TAN() | tangent |
| ABS() | Absolute value |
| SQRT() | Square root |
| MOD() | Remainder |
| EXP() | index |
| PI() | Pi |
| RAND() | Random number |

# Thirteen, grouping

Place rows with the same data values in the same group.

You can use summary functions to process the same grouped data, such as finding the average of grouped data, etc.

In addition to grouping by the specified grouping field, the specified grouping field will also be automatically sorted by the field.

```sql
SELECT col, COUNT(*) AS num
FROM mytable
GROUP BY col;
```

GROUP BY automatically sorts by grouping fields, and ORDER BY can also sort by summary fields.

```sql
SELECT col, COUNT(*) AS num
FROM mytable
GROUP BY col
ORDER BY num;
```

WHERE filters rows, HAVING filters groups, and row filtering should precede group filtering.

```sql
SELECT col, COUNT(*) AS num
FROM mytable
WHERE col > 2
GROUP BY col
HAVING num >= 2;
```

Grouping rules:

- The GROUP BY clause appears after the WHERE clause and before the ORDER BY clause;
- Except for summary fields, each field in the SELECT statement must be given in the GROUP BY clause;
- NULL rows will be grouped separately;
- Most SQL implementations do not support GROUP BY data types with variable length columns.

# 14. Subquery

Only data from one field can be returned in a subquery.

You can use the results of a subquery as filter conditions for a WHRER statement:

```sql
SELECT *
FROM mytable1
WHERE col1 IN (SELECT col2
               FROM mytable2);
```

The following statement can retrieve the customer's order quantity. The subquery statement will be executed once for each customer retrieved by the first query:

```sql
SELECT cust_name, (SELECT COUNT(*)
                   FROM Orders
                   WHERE Orders.cust_id = Customers.cust_id)
                   AS orders_num
FROM Customers
ORDER BY c
ust_name;
```

# 15. Connection

Joins are used to join multiple tables, using the JOIN keyword, and conditional statements using ON instead of WHERE.

Joins can replace subqueries and are generally faster than subqueries.

You can use AS to alias column names, calculated fields, and table names. Aliasing table names is to simplify SQL statements and connect the same table.

## Inner join

Inner joins are also called equivalent joins and use the INNER JOIN keyword.

```sql
SELECT A.value, B.value
FROM tablea AS A INNER JOIN tableb AS B
ON A.key = B.key;
```

Instead of explicitly using INNER JOIN, you can use a normal query and join the columns to be joined in the two tables using an equivalence method in WHERE.

```sql
SELECT A.value, B.value
FROM tablea AS A, tableb AS B
WHERE A.key = B.key;
```

##Self-connection

Self-join can be regarded as a kind of inner join, except that the connected table is itself.

An employee table contains employee names and departments to which emp
loyees belong. We want to find the names of all employees in the same department as Jim.

subquery version

```sql
SELECT name
FROM employee
WHERE department = (
      SELECT department
      FROM employee
      WHERE name = "Jim");
```

Self-connected version

```sql
SELECT e1.name
FROM employee AS e1 INNER JOIN employee AS e2
ON e1.department = e2.department
      AND e2.name = "Jim";
```

## Natural connection

Natural joins connect columns with the same name through equivalence testing. There can be multiple columns with the same name.

The difference between inner join and natural join: inner join provides connected columns, while natural join automatically joins all columns with the same name.

```sql
SELECT A.value, B.value
FROM tablea AS A NATURAL JOIN tableb AS B;
```

## Outer join

Outer joins retain rows that are not related. It is divided into left outer join, right outer join and full outer join. The left outer join is to retain the unassociated rows of the left table.

Retrieve order information for all customers, including customers who do not have order information yet.

```sql
SELECT Customers.cust_id, Customer.cust_name, Orders.order_id
FROM Customers LEFT OUTER JOIN Orders
ON Customers.cust_id = Orders.cust_id;
```

customers table:

| cust_id | cust_name |
| :---: | :---: |
| 1 | a |
| 2 | b |
| 3 | c |

orders table:

| order_id | cust_id |
| :---: | :---: |
|1 | 1 |
|2 | 1 |
|3 | 3 |
|4 | 3 |

Result:

| cust_id | cust_name | order_id |
| :---: | :---: | :---: |
| 1 | a | 1 |
| 1 | a | 2 |
| 3 | c | 3 |
| 3 | c | 4 |
| 2 | b | Null |

# 16. Combined query

Use **UNION** to combine two queries. If the first query returns M rows and the second query returns N rows, then the result of the combined query is generally M+N rows.

Each query must contain the same columns, expressions, and aggregate functions.

By default, identical rows will be removed. If you need to keep the same rows, use UNION ALL.

Only one ORDER BY clause can be included, and it must be at the end of the statement.

```sql
SELECT col
FROM mytable
WHERE col = 1
UNION
SELECT col
FROM mytable
WHERE col =2;
```

# 17. View

A view is a virtual table that does not contain data, so it cannot be indexed.

Operations on views are the same as operations on ordinary tables.

Views have the following benefits:

- Simplify complex SQL operations, such as complex joins;
- Only use part of the data from the actual table;
- Ensure data security by only giving users permission to access views;
- Change data format and presentation.

```sql
CREATE VIEW myview AS
SELECT Concat(col1, col2) AS concat_col, col3*col4 AS compute_col
FROM mytable
WHERE col5 = val;
```

# 18. Stored procedure

Stored procedures can be thought of as batch processing of a series of SQL operations.

Benefits of using stored procedures:

- Code encapsulation ensures a certain degree of security;
- Code reuse;
- High performance since it is pre-compiled.

Creating a stored procedure in the command line r
equires a custom delimiter, because the command line ends with ; and the stored procedure also contains a semicolon, so this part of the semicolon will be mistakenly regarded as the terminator, causing a syntax error.

Contains three parameters: in, out and inout.

To assign a value to a variable, you need to use the select into statement.

Only one variable can be assigned a value at a time, and collection operations are not supported.

```sql
delimiter //

create procedure myprocedure(out ret int)
    begin
        declare y int;
        select sum(col1)
        from mytable
        into y;
        select y*y into ret;
    end //

delimiter;
```

```sql
call myprocedure(@ret);
select @ret;
```

# 19. Cursor

Cursors can be used in stored procedures to traverse a result set.

Cursors are mainly used in interactive applications where the user needs to browse and modify any row in the data set.

Four steps for using cursors:

1. Declare the cursor, this process does not actually retrieve the data;
2. Open the cursor;
3. Get the data;
4. Close the cursor;

```sql
delimiter //
create procedure myprocedure(out ret int)
    begin
        declare done boolean default 0;

        declare mycursor cursor for
        select col1 from mytable;
        # Defines a continue handler. When the condition sqlstate '02000' occurs, set done = 1 will be executed.
        declare continue handler f
or sqlstate '02000' set done = 1;

        open mycursor;

        repeat
            fetch mycursor into ret;
            select ret;
        until done end repeat;

        close mycursor;
    end //
 delimiter;
```

# Twenty, trigger

Triggers will automatically execute when a table executes the following statements: DELETE, INSERT, UPDATE.

The trigger must specify whether to execute automatically before or after the statement is executed. Use the BEFORE keyword to execute before and the AFTER keyword to execute after. BEFORE is used for data validation and purification, and AFTER is used for audit trails to record modifications to another table.

The INSERT trigger contains a virtual table named NEW.

```sql
CREATE TRIGGER mytrigger AFTER INSERT ON mytable
FOR EACH ROW SELECT NEW.col into @result;

SELECT @result; -- Get results
```

The DELETE trigger contains a virtual table named OLD and is read-only.

The UPDATE trigger contains a virtual table named NEW and a virtual table named OLD, where NEW can be modified and OLD is read-only.

MySQL does not allow the use of CALL statements in triggers, that is, stored procedures cannot be called.

# 21. Affairs management

Basic terminology:

- Transaction refers to a set of SQL statements;
- Rollback refers to the process of undoing the specified SQL statement;
- Commit refers to writing the unstored SQL statement results into the database table;
- A savepoint refers to a temporary placeholder set in a transaction for which you can issue a rollback (unlike rolling back the entire transaction).

The SELECT statement cannot
be rolled back, and there is no point in rolling back the SELECT statement; CREATE and DROP statements cannot be rolled back either.

MySQL's transaction submission defaults to implicit submission. Every time a statement is executed, the statement is regarded as a transaction and then submitted. When a START TRANSACTION statement occurs, implicit commit will be turned off; when a COMMIT or ROLLBACK statement is executed, the transaction will automatically close and implicit commit will be restored.

Set autocommit to 0 to suppress autocommit; the autocommit flag is per-connection, not server-specific.

If a retention point is not set, ROLLBACK will fall back to the START TRANSACTION statement; if a retention point is set and specified in ROLLBACK, it will fall back to that retention point.

```sql
START TRANSACTION
// ...
SAVEPOINT delete1
// ...
ROLLBACK TO delete1
// ...
COMMIT
```

# Twenty-two, character set

Basic terminology:

- Character set is a collection of letters and symbols;
- Encoded as an internal representation of a character set member;
- Proofing characters specify how to compare, mainly used for sorting and grouping.

In addition to specifying the character set and collation for the table, you can also specify the column:

```sql
CREATE TABLE mytable
(col VARCHAR(10) CHARACTER SET latin COLLATE latin1_general_ci )
DEFAULT CHARACTER SET hebrew COLLATE hebrew_general_ci;
```

You can specify proofreading when sorting and grouping:

```sql
SELECT *
FROM mytable
ORDER BY col COLLATE latin1_general_ci;
```

# 23. Permission management

MySQL account information is stored in the mysql database.

```sql
USE mysql;
SELECT user FROM user;
```

**Create Account**

Newly created accounts do not have any permissions.

```sql
CREATE USER myuser IDENTIFIED BY 'mypassword';
```

**Modify account name**

```sql
RENAME USER myuser TO newuser;
```

**Delete Account**

```sql
DROP USER myuser;
```

**View Permissions**

```sql
SHOW GRANTS FOR myuser;
```

**Grant Permissions**

Accounts are defined in the form username@host, and username@% uses the default host name.

```sql
GRANT SELECT, INSERT ON mydatabase.* TO myuser;
```

**DELETE PERMISSION**

GRANT and REVOKE control access at several levels:

- The entire server, using GRANT ALL and REVOKE ALL;
- The entire database, use ON database.\*;
- For a specific table, use ON database.table;
- specific columns;
- Specific stored procedures.

```sql
REVOKE SELECT, INSERT ON mydatabase.* FROM myuser;
```

**Change Password**

Encryption must be done using the Password() function.

```sql
SET PASSWROD FOR myuser = Password('new_password');
```

# References

- BenForta. SQL must be known and mastered [M]. People's Posts and Telecommunications Press, 2013.
