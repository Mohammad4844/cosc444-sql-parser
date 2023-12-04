# Cosc 444 SQL Parser

Cosc 444 Final Project

Project title: SQL Parser

Team members: Mohammad Arjamand Ali, Ezzat Abdel Khalek, Ibrahim Berro, Safauldeen Alrufaye

## Assumptions
1. Assume that databases, tables and fields are already defined/created.
2. Although using capital letters for keywords (SELECT, INSERT) is the convention in SQL, it allows lowercase keywords (select, insert). We instead will only allow capital letter versions of keywords.
3. Nothing that requires any logic is included (since then we wouldn’t be able to define a grammar). This includes checking the datatype and scoping fields (like users.first_name would require us to check if first_name was in the users table, so it is not included).

## Scope (subset of sql we will implement)
1. Basic queries: INSERT, UPDATE and DELETE
2. The SELECT query
    - Functions: COUNT, SUM, AVG, MAX, and MIN
    - Joins:  INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN
    - Aggregate functions: GROUP BY, HAVING, and ORDER BY
3. Clauses: WHERE, SET and VALUES
4. Aliases (using the ‘as’ keyword), DISTINCT, Wildcards
5. Comments
6. Predefined Tables / Fields
7. We are supporting basic data types like numbers & strings, but NOT arrays
8. Recursive aspect: SQL allows subqueries within SELECT

## Grammar:
* For this grammar, let's assume we have 2 tables, users and orders, with the following fields in the database:
users: id, email, first_name, last_name
orders: id, user_id, date, amount
* Also, since SQL doesn’t care about spacing, assume that a single space in this Grammar denote any number of spaces (single space, multiple spaces, no space, newline, etc)

<br>

```
# database tables & fields
<table> := users | orders
<field> := id | email | first_name | last_name | user_id | date | amount
<table-field> := <table>.<field> | <field>

# basic definitions
<string> := **all legal strings in between single qoutes**
<integer> := **all legal integers**
<float> := **all legal floats of the form XX.XX**
<alias> := <string>
<operator> := + | - | * | / | = | != | < | > | <= | >= 
<function> := SUM | AVG | COUNT | MAX | MIN | UPPER | LOWER

# logic definitions
<term> := <table-field> | <string> | <float> | <integer> | (<expression>)
<expression> := <term> | <term> <operator> <term> | <function> ( <expression> ) | <table-field> LIKE <string> | ( <select-query> )
<condition> = <expression> | <expression> AND <condition> | <expression> OR <condition>

# lists
<field-list> := <table-field> | <table-field>, <field-list>
<expression-list> := <expression> | <expression>, <expression-list>
<assignment-list> := <table-field> = <value> | <table-field> = <value>, <assignment-list>

# query helpers (mostly for select query)
<distinct-clause> := λ | DISTINCT
<select-clause> := * | <field-alias-list>
<field-alias-list> := <field-alias> | <field-alias>, <field-alias-list>
<field-alias> := <table-field> | <table-field> as <alias>
<table-alias-list> := <table-alias> | <table-alias>, <table-alias-list>
<table-alias> := <table> | <table> as <alias>
<table-clause> := <table> | <table> <join> JOIN <table> ON <condition>
<join> := RIGHT | LEFT | INNER | FULL
<where-clause> := λ | WHERE <condition>
<group-clause> := λ | GROUP BY <field-list>
<having-clause> := λ | HAVING <condition>
<order-clause> := λ | <order-list>
<order-list> := <table-field> <order-direction> | <table-field> <order-direction>, <order-list>
<order-direction> := λ | ASC | DESC

# basic queries
<insert-query> := INSERT INTO <table> ( <field-list> ) VALUES ( <expression-list> )
<update-query> := UPDATE <table> SET ( <assignment-list> )
<delete-query> := DELETE FROM <table> <where-clause>

# select query
<select-query> := SELECT <distinct-clause> <select-clause> FROM <table-clause> <where-clause> <group-clause> <having-cause> <order-clause>

# big picture sql
<comment> := /*<string>*/
<statement> := <select-query>; | <insert-query>; | <update-query>; | <delete-query>; | <comment>
<sql> := <statement> | <statement> <sql>

```



