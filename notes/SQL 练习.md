# SQL 练习
<!-- GFM-TOC -->
* [SQL 练习](#sql-练习)
    * [595. Big Countries](#595-big-countries)
    * [627. Swap Salary](#627-swap-salary)
    * [620. Not Boring Movies](#620-not-boring-movies)
    * [596. Classes More Than 5 Students](#596-classes-more-than-5-students)
    * [182. Duplicate Emails](#182-duplicate-emails)
    * [196. Delete Duplicate Emails](#196-delete-duplicate-emails)
    * [175. Combine Two Tables](#175-combine-two-tables)
    * [181. Employees Earning More Than Their Managers](#181-employees-earning-more-than-their-managers)
    * [183. Customers Who Never Order](#183-customers-who-never-order)
    * [184. Department Highest Salary](#184-department-highest-salary)
    * [176. Second Highest Salary](#176-second-highest-salary)
    * [177. Nth Highest Salary](#177-nth-highest-salary)
    * [178. Rank Scores](#178-rank-scores)
    * [180. Consecutive Numbers](#180-consecutive-numbers)
    * [626. Exchange Seats](#626-exchange-seats)
<!-- GFM-TOC -->


## 595. Big Countries

https://leetcode.com/problems/big-countries/description/

### Description

```html
+-----------------+------------+------------+--------------+---------------+
| name            | continent  | area       | population   | gdp           |
+-----------------+------------+------------+--------------+---------------+
| Afghanistan     | Asia       | 652230     | 25500100     | 20343000      |
| Albania         | Europe     | 28748      | 2831741      | 12960000      |
| Algeria         | Africa     | 2381741    | 37100000     | 188681000     |
| Andorra         | Europe     | 468        | 78115        | 3712000       |
| Angola          | Africa     | 1246700    | 20609294     | 100990000     |
+-----------------+------------+------------+--------------+---------------+
```

查找面积超过 3,000,000 或者人口数超过 25,000,000 的国家。

```html
+--------------+-------------+--------------+
| name         | population  | area         |
+--------------+-------------+--------------+
| Afghanistan  | 25500100    | 652230       |
| Algeria      | 37100000    | 2381741      |
+--------------+-------------+--------------+
```

### Solution

```sql
SELECT name,
    population,
    area
FROM
    World
WHERE
    area > 3000000
    OR population > 25000000;
```

### SQL Schema

SQL Schema 用于在本地环境下创建表结构并导入数据，从而方便在本地环境调试。

```sql
DROP TABLE
IF
    EXISTS World;
CREATE TABLE World ( NAME VARCHAR ( 255 ), continent VARCHAR ( 255 ), area INT, population INT, gdp INT );
INSERT INTO World ( NAME, continent, area, population, gdp )
VALUES
    ( 'Afghanistan', 'Asia', '652230', '25500100', '203430000' ),
    ( 'Albania', 'Europe', '28748', '2831741', '129600000' ),
    ( 'Algeria', 'Africa', '2381741', '37100000', '1886810000' ),
    ( 'Andorra', 'Europe', '468', '78115', '37120000' ),
    ( 'Angola', 'Africa', '1246700', '20609294', '1009900000' );
```

## 627. Swap Salary

https://leetcode.com/problems/swap-salary/description/

### Description

```html
| id | name | sex | salary |
|----|------|-----|----
----|
| 1 | A | m | 2500 |
| 2 | B | f | 1500 |
| 3 | C | m | 5500 |
| 4 | D | f | 500 |
```

Invert the sex field using just one SQL query.

```html
| id | name | sex | salary |
|----|------|-----|--------|
| 1 | A | f | 2500 |
| 2 | B | m | 1500 |
| 3 | C | f | 5500 |
| 4 | D | m | 500 |
```

### Solution

The result of XORing two equal numbers is 0, and the result of XORing 0 with either number is this number.

The sex field has only two values: 'f' and 'm', and has the following rules:

```
'f' ^ ('m' ^ 'f') = 'm' ^ ('f' ^ 'f') = 'm'
'm' ^ ('m' ^ 'f') = 'f' ^ ('m' ^ 'm') = 'f'
```

Therefore, XOR the sex field with 'm' ^ 'f', and finally the sex field can be reversed.

```sql
UPDATE salary
SET sex = CHAR ( ASCII(sex) ^ ASCII( 'm' ) ^ ASCII( 'f' ) );
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS salary;
CREATE TABLE salary ( id INT, NAME VARCHAR ( 100 ), sex CHAR ( 1 ), salary INT );
INSERT INTO salary (id, NAME, sex, salary)
VALUES
    ( '1', 'A', 'm', '2500' ),
    ( '2', 'B', 'f', '1500' ),
    ( '3', 'C', 'm', '5500' ),
    ( '4', 'D', 'f', '500' );
```

## 620. Not Boring Movies

https://leetcode.com/problems/not-boring-movies/description/

### Description


```html
+---------+-----------+---------------+-----------+
| id | movie | description | rating |
+---------+-----------+---------------+-----------+
| 1 | War | great 3D | 8.9 |
| 2 | Science | fiction | 8.5 |
| 3 | irish | boring | 6.2 |
| 4 | Ice song | Fantacy | 8.6 |
| 5 | House card| Interesting| 9.1 |
+---------+-----------+---------------+-----------+
```

Find movies with an odd id and a description other than boring, in descending order of rating.

```html
+---------+-----------+---------------+-----------+
| id | movie | description | rating |
+---------+-----------+---------------+-----------+
| 5 | House card| Interesting| 9.1 |
| 1 | War | great 3D | 8.9 |
+---------+-----------+---------------+-----------+
```

### Solution

```sql
SELECT
    *
FROM
    cinema
WHERE
    id % 2 = 1
    AND description != 'boring'
ORDER BY
    rating DESC;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS cinema;
CREATE TABLE cinema ( id INT, movie VARCHAR ( 255 ), description VARCHAR ( 255 ), rating FLOAT ( 2, 1 ) );
INSERT INTO cinema (id, movie, description, rating)
VALUES
    ( 1, 'War', 'great 3D', 8.9 ),
    (2, 'Science', 'fiction', 8.5),
    (3, 'irish', 'boring', 6.2),
    (4, 'Ice song', 'Fantacy', 8.6),
    (5, 'House card', 'Interesting', 9.1);
```

## 596. Classes More Than 5 Students

https://leetcode.com/problems/classes-more-than-5-students/description/

### Description

```html
+---------+----------------+
| student | class |
+---------+----------------+
| A | Math |
| B | English |
| C | Math |
| D | Biology |
| E | Math |
| F | Computer |
| G | Math |
| H | Math |
| I | Math |
+---------+----------------+
```

Find classes with five or more students.

```html
+---------+
| class
|
+---------+
| Math |
+---------+
```

### Solution

After grouping the class co
lumn, use the count summary function to count the number of records in each group, and then use HAVING to filter. HAVING filters on a grouping basis, while WHERE filters on a per-record (row) basis.

```sql
SELECT
    class
FROM
    courses
GROUP BY
    class
HAVING
    count( DISTINCT student ) >= 5;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS courses;
CREATE TABLE courses ( student VARCHAR ( 255 ), class VARCHAR ( 255 ) );
INSERT INTO courses (student, class)
VALUES
    ( 'A', 'Math' ),
    ( 'B', 'English' ),
    ( 'C', 'Math' ),
    ( 'D', 'Biology' ),
    ( 'E', 'Math' ),
    ( 'F', 'Computer' ),
    ( 'G', 'Math' ),
    ( 'H', 'Math' ),
    ( 'I', 'Math' );
```

## 182. Duplicate Emails

https://leetcode.com/problems/duplicate-emails/description/

### Description

Email address list:

```html
+----+---------+
| Id | Email |
+----+---------+
| 1 | a@b.com |
| 2 | c@d.com |
| 3 | a@b.com |
+----+---------+
```

Find duplicate email addresses:

```html
+---------+
| Email |
+---------+
| a@b.com |
+---------+
```

### Solution

Group emails and use COUNT for counting. If the result is greater than or equal to 2, it means that the emails are duplicated.

```sql
SELECT
    Email
FROM
    Person
GROUP BY
    Email
HAVING
    COUNT( * ) >= 2;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Person;
CREATE TABLE Person ( Id INT, Email VARCHAR ( 255 ) );
INSERT INTO Person (Id, Email)
VALUES
    (1, 'a@b.com' ),
    (2, 'c@d.com' ),
    (3, 'a@b.com' );
```


## 196. Delete Duplicate Emails

https://leetcode.com/problems/delete-duplicate-emails/description/

### Description

Email address list:

```html
+----+---------+
| Id | Email |
+----+---------+
| 1 | john@example.com |
| 2 | bob@example.com |
| 3 | john@example.com |
+----+---------+
```

Remove duplicate email addresses:

```html
+----+------------------+
| Id | Email |
+----+------------------+
| 1 | john@example.com |
| 2 | bob@example.com |
+----+------------------+
```

### Solution

Only keep the one with the smallest ID among the same emails, and then delete the others.

Connection query:

```sql
DELETE p1
FROM
    Person p1,
    Person p2
WHERE
    p1.Email = p2.Email
    AND p1.Id > p2.Id
```

Subquery:

```sql
DELETE
FROM
    Person
WHERE
    id NOT IN (
        SELECT id
        FROM (
            SELECT min( id ) AS id
            FROM Person
            GROUP BY email
        ) AS m
    );
```

It should be noted that the above solution nests an additional SELECT statement. If this is not done, an error will occur: You can't specify target table 'Person' for update in FROM clause. This incorrect solution is demonstrated below.

```sql
DELETE
FROM
    Person
WHERE
    id NOT IN (
        SELECT min( id ) AS id
        FROM Person
        GROUP BY email
    );
```

Reference: [pMySQL Error 1093 - Can't specify target table for update in FROM clause](https://stackoverflow.com/questions/45494/mysql-error-1093-cant-specify-target-table-for-update-in-from-clause)

### SQL
Schema

Same as 182.

## 175. Combine Two Tables

https://leetcode.com/problems/combine-two-tables/description/

### Description

Person table:

```html
+-------------+---------+
| Column Name | Type |
+-------------+---------+
| PersonId | int |
| FirstName | varchar |
| LastName | varchar |
+-------------+---------+
PersonId is the
primary key column for this table.
```

Address table:

```html
+-------------+---------+
| Column Name | Type |
+-------------+---------+
| AddressId | int |
| PersonId | int |
| City | varchar |
| State | varchar |
+-------------+---------+
AddressId is the primary key column for this table.
```

Find FirstName, LastName, City, State data regardless of whether a user has filled in address information.

### Solution

Involving the Person and Address tables, when performing a join operation on these two tables, because the information in the Person table needs to be retained, even if there is no associated information in the Address table, it must be retained. At this time, you can use left outer join and place the Person table on the left side of LEFT JOIN.

```sql
SELECT
    FirstName,
    LastName,
    City,
    State
FROM
    Person P
    LEFT JOIN Address A
    ON P.PersonId = A.PersonId;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Person;
CREATE TABLE Person ( PersonId INT, FirstName VARCHAR ( 255 ), LastName VARCHAR ( 255 ) );
DROP TABLE
IF
    EXISTS Address;
CREATE TABLE Address ( AddressId INT, PersonId INT, City VARCHAR ( 255 ), State VARCHAR ( 255 ) );
INSERT INTO Person ( PersonId, LastName, FirstName )
VALUES
    (1, 'Wang', 'Allen' );
INSERT INTO Address (AddressId, PersonId, City, State)
VALUES
    ( 1, 2, 'New York City', 'New York' );
```

## 181. Employees Earning More Than Their Managers

https://leetcode.com/problems/employees-earning-more-than-their-managers/description/

### Description

Employee table:

```html
+----+-------+--------+-----------+
| Id | Name | Salary | ManagerId |
+----+-------+--------+-----------+
| 1 | Joe | 70000 | 3 |
| 2 | Henry | 80000 | 4 |
| 3 | Sam | 60000 | NULL |
| 4 | Max | 90000 | NULL |
+----+-------+--------+-----------+
```

Find information about employees whose salary is greater than their manager's salary.

### Solution

```sql
SELECT
    E1.NAME AS Employee
FROM
    Employee E1
    INNER JOIN Employee E2
    ON E1.ManagerId = E2.Id
    AND E1.Salary > E2.Salary;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Employee;
CREATE TABLE Employee (Id INT, NAME VARCHAR (255), Salary INT, ManagerId INT);
INSERT INTO Employee (Id, NAME, Salary, ManagerId)
VALUES
    (1, 'Joe', 70000, 3),
    (2, 'Henry', 80000, 4),
    (3, 'Sam', 60000, NULL ),
    (4, 'Max', 90000, NULL);
```

## 183. Customers Who Never Order

https://leetcode.com/problems/customers-who-never-order/description/

### Description

Customers table:

```html
+----+-------+
| Id | Name |
+----+-------+
| 1 | Joe |
| 2 | Henry |
| 3 | Sam |
| 4 | Max |
+----+-------+
```

Orders table:

`
``html
+----+------------+
| Id | CustomerId |
+----+------------+
| 1 | 3 |
| 2 | 1 |
+----+------------+
```

Find information about customers without orders:

```html
+-----------+
| Customers |
+-----------+
| Henry |
| Max |
+-----------+
```

### Solution

left external link

```sql
SELECT
    C.Name AS Customers
FROM
    Customers C
    LEFT JOIN Orders O
    ON C.Id = O.CustomerId
WHERE
    O.CustomerId IS NULL;
```

subquery

```sql
SELECT
    Name AS Customers
FROM
    Customers
WHERE
    ID NOT IN (
        SELECT CustomerId
        FROM Orders
    );
```

### SQL Schema

```sql
DROP TABLE
IF
    EXIST
S Customers;
CREATE TABLE Customers ( Id INT, NAME VARCHAR ( 255 ) );
DROP TABLE
IF
    EXISTS Orders;
CREATE TABLE Orders ( Id INT, CustomerId INT );
INSERT INTO Customers ( Id, NAME )
VALUES
    ( 1, 'Joe' ),
    ( 2, 'Henry' ),
    ( 3, 'Sam' ),
    ( 4, 'Max' );
INSERT INTO Orders ( Id, CustomerId )
VALUES
    ( 1, 3 ),
    ( 2, 1 );
```

## 184. Department Highest Salary

https://leetcode.com/problems/department-highest-salary/description/

### Description

Employee 表：

```html
+----+-------+--------+--------------+
| Id | Name  | Salary | DepartmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 70000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
+----+-------+--------+--------------+
```

Department 表：

```html
+----+----------+
| Id | Name     |
+----+----------+
| 1  | IT       |
| 2  | Sales    |
+----+----------+
```

查找一个 Department 中收入最高者的信息：

```html
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| Sales      | Henry    | 80000  |
+------------+----------+--------+
```

### Solution

创建一个临时表，包含了部门员工的最大薪资。可以对部门进行分组，然后使用 MAX() 汇总函数取得最大薪资。

之后使用连接找到一个部门中薪资等于临时表中最大薪资的员工。

```sql
SELECT
    D.NAME Department,
    E.NAME Employee,
    E.Salary
FROM
    Employee E,
    Department D,
    ( SELECT DepartmentId, MAX( Salary ) Salary 
     FROM Employee 
     GROUP BY DepartmentId ) M
WHERE
    E.DepartmentId = D.Id
    AND E.DepartmentId = M.DepartmentId
    AND E.Salary = M.Salary;
```

### SQL Schema

```sql
DROP TABLE IF EXISTS Employee;
CREATE TABLE Employee ( Id INT, NAME VARCHAR ( 255 ), Salary INT, DepartmentId INT );
DROP TABLE IF EXISTS Department;
CREATE TABLE Department ( Id INT, NAME VARCHAR ( 255 ) );
INSERT INTO Employee ( Id, NAME, Salary, DepartmentId )
VALUES
    ( 1, 'Joe', 70000, 1 ),
    ( 2, 'Henry', 80000, 2 ),
    ( 3, 'Sam', 60000, 2 ),
    ( 4, 'Max', 90000, 1 );
INSERT INTO Department ( Id, NAME )
VALUES
    ( 1, 'IT' ),
    ( 2, 'Sales' );
```


## 176. Second Highest Salary

https://leetcode.com/problems/second-highest-salary/description/

### Description

```html
+----+--------+
| Id | Salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
```

查找工资第二高的员工。

```html
+----------------
-----+
| SecondHighestSalary |
+---------------------+
| 200 |
+---------------------+
```

Not found returns null instead of returning no data.

### Solution

In order to return null when no data is found, another layer of SELECT needs to be placed outside the query result.

```sql
SELECT
    ( SELECT DISTINCT Salary
     FROM Employee
     ORDER BY Salary DESC
     LIMIT 1, 1 ) SecondHighestSalary;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Employee;
CREATE TABLE Employee (Id INT, Salary INT);
INSERT INTO Employee (Id, Salary)
VALUES
    (1, 100),
    (2,200),
    (3, 300);
```

## 177. Nth Highest Salary

### Description

Find the employee with the Nth highest salary.

### Solution

```sql
CREATE FUNCTIONge
tNthHighestSalary ( N INT ) RETURNS INT BEGIN

SET N = N - 1;
RETURN (
    SELECT (
        SELECT DISTINCT Salary
        FROM Employee
        ORDER BY Salary DESC
        LIMIT N, 1
    )
);

END
```

### SQL Schema

Same as 176.


## 178. Rank Scores

https://leetcode.com/problems/rank-scores/description/

### Description

Score sheet:

```html
+----+-------+
| Id | Score |
+----+-------+
| 1 | 3.50 |
| 2 | 3.65 |
| 3 | 4.00 |
| 4 | 3.85 |
| 5 | 4.00 |
| 6 | 3.65 |
+----+-------+
```

Sort the scores and tally the rankings.

```html
+-------+------+
| Score | Rank |
+-------+------+
| 4.00 | 1 |
| 4.00 | 1 |
| 3.85 | 2 |
| 3.65 | 3 |
| 3.65 | 3 |
| 3.50 | 4 |
+-------+------+
```

### Solution

To count the ranking of a certain score, just count the number of scores that are greater than or equal to the score.

| Id | score | The number of scores greater than or equal to this score | Ranking |
| :---: | :---: | :---: | :---: |
| 1 | 4.1 | 3 | 3 |
| 2 | 4.2 | 2 | 2 |
| 3 | 4.3 | 1 | 1 |

Use the join operation to find the records corresponding to a score that are greater than or equal to its value:

```sql
SELECT
	*
FROM
    Scores S1
    INNER JOIN Scores S2
    ON S1.score <= S2.score
ORDER BY
    S1.score DESC, S1.Id;
```

| S1.Id | S1.score | S2.Id | S2.score |
| :---: | :---: | :---: | :---: |
|3| 4.3| 3 |4.3|
|2| 4.2| 2| 4.2|
|2| 4.2 |3 |4.3|
|1| 4.1 |1| 4.1|
|1| 4.1 |2| 4.2|
|1| 4.1 |3| 4.3|

You can see that each S1.score has several corresponding records. We then group it and count the number of each group as 'Rank'

```sql
SELECT
    S1.score 'Score',
    COUNT(*) 'Rank'
FROM
    Scores S1
    INNER JOIN Scores S2
    ON S1.score <= S2.score
GROUP BY
    S1.id, S1.score
ORDER BY
    S1.score DESC, S1.Id;
```

| score | Rank |
| :---: | :---: |
| 4.3 | 1 |
| 4.2 | 2 |
| 4.1 | 3 |

The above solution seems fine, but for the following data, it gets wrong results:

| Id | score |
| :---: | :---: |
| 1 | 4.1 |
| 2 | 4.2 |
| 3 | 4.2 |

| score | Rank |
| :---: | :--: |
| 4.2 | 2 |
| 4.2 | 2 |
| 4.1 | 3 |

And the result we want is:

| score | Rank |
| :---: | :--: |
| 4.2 | 1 |
| 4.2 | 1 |
| 4.1 | 2 |

The connection status is as follows:

| S1.Id | S1.score | S2.Id | S2.score |
| :---: | :------: | :---: | :------: |
| 2 | 4.2 | 3 | 4.2 |
| 2 | 4.2 | 2 | 4.2 |
| 3 | 4.2 | 3 | 4.2 |
| 3 | 4.2 | 2 | 4.1 |
| 1 | 4.1 | 3 | 4.2 |
| 1
| 4.1 | 2 | 4.2 |
| 1 | 4.1 | 1 | 4.1 |

The result we want is to put the records with the same score in the same ranking, and the same score only occupies one position. For example, the scores above, the records with Id=2 and Id=3 have the same score, and the highest, they are tied for first place. The record with Id=1 should be ranked second, not third. So when performing COUNT counting statistics, we need to use COUNT(DISTINCT S2.score) to count the same score only once.

```sql
SELECT
    S1.score 'Score',
    COUNT( DISTINCT S2.score ) 'Rank'
FROM
    Scores S1
    INNER JOIN Scores S2
    ON S1.score <= S2.score
GROUP BY
    S1.id, S1.score
ORDER BY
    S1.score DESC;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Scores;
CREATE TABLE Scores (Id INT, Score DECIMAL (3, 2));
INSERT INTO Scores (Id, Score)
VALUES
    (1, 4.1),
    (2, 4.1),
    (3, 4.2),
    (4, 4.2),
    (5, 4.3),
    (6, 4.3);
```

## 180. Consecutive Numbers

https://leetcode.com/problems/consecutive-numbers/description/

### Description

Digital table:

```html
+----+-----+
| Id | Num |
+----
+-----+
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 1 |
| 6 | 2 |
| 7 | 2 |
+----+-----+
```

Find numbers that appear three times in a row.

```html
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1 |
+-----------------+
```

### Solution

```sql
SELECT
    DISTINCT L1.num ConsecutiveNums
FROM
    Logs L1,
    Logs L2,
    Logs L3
WHERE L1.id = l2.id - 1
    AND L2.id = L3.id - 1
    AND L1.num = L2.num
    AND l2.num = l3.num;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS LOGS;
CREATE TABLE LOGS (Id INT, Num INT);
INSERT INTO LOGS (Id, Num)
VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 1),
    (6, 2),
    (7, 2);
```

## 626. Exchange Seats

https://leetcode.com/problems/exchange-seats/description/

### Description

The seat table stores the students corresponding to the seats.

```html
+---------+---------+
| id | student |
+---------+---------+
| 1 | Abbot |
| 2 | Doris |
| 3 | Emerson |
| 4 | Green |
| 5 | Jeames |
+---------+---------+
```

Two students in adjacent seats are required to be exchanged. If the last seat is an odd number, the students in this seat will not be exchanged.

```html
+---------+---------+
| id | student |
+---------+---------+
| 1 | Doris |
| 2 | Abbot |
| 3 | Green |
| 4 | Emerson |
| 5 | Jeames |
+---------+---------+
```

### Solution

Use multiple unions.

```sql
## Process even ids and reduce id by 1
## For example, 2,4,6,... becomes 1,3,5,...
SELECT
    s1.id - 1 AS id,
    s1.student
FROM
    seat s1
WHERE
    s1.id MOD 2 = 0 UNION
## Handle odd ids and add 1 to the id. But if the largest id is an odd number, no processing will be done
## For example, 1,3,5,... becomes 2,4,6,...
SELECT
    s2.id + 1 AS id,
    s2.student
FROM
    seat s2
WHERE
    s2.id MOD 2 = 1
    AND s2.id != ( SELECT max( s3.id ) FROM seat s3 ) UNION
## If the largest id is an odd number, take out this number separately
SELECT
s4.id AS id,
    s4.student
FROM
    seat s4
WHERE
    s4.id MOD 2 = 1
    AND s4.id = ( SELECT max( s5.id ) FROM seat s5 )
ORDER BY
    id;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS seat;
CREATE TABLE seat ( id INT, student VARCHAR ( 255 ) );
INSERT INTO seat (id, student)
VALUES
    ( '1', 'Abbot' ),
    ( '2', 'Doris' ),
    ( '3', 'Emerson' ),
    ( '4', 'Green' ),
    ( '5', 'James' );
```
