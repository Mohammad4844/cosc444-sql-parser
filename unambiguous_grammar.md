## The following is the Grammar with  most Ambiguity removed AND it seperates Boolean Stuff

```
# database tables & fields
<table> := users | orders
<field> := id | email | first_name | last_name | user_id | date | amount
<table-field> := <table>.<field> | <field>                                       // look-ahead for <table>

# basic definitions
<string> := **all legal strings in between single qoutes**
<float> := **all legal floats of the form XX.XX**
<integer> := **all legal integers**
<value> := <string> | <float> | <integer>                                     // use look-ahead for this                         
<alias> := <string>
<function> := UPPER | LOWER | ROUND | LENGTH | ABS | SUM | AVG | COUNT | MAX | MIN
<math-operator> := + | - | * | /
<comparison-operator> := = | != | < | > | <= | >= 

# logic definitions
<term> := <table-field> | <value> | ( <math-expresion> )                              // the production <term> := ( <math-expresion> ) allows brackets, but may introduce cycles that are problematic - so remove this if its casuing issues
<math-expression> := <term> <optional-math-clause> | <function> ( <math-expression> )               // potentially include <math-expression> := ( <select-query> ), which I think is unambiguous if you a look-ahead for SELECT   
<optional-math-clause> := λ | <math-operator> <term> <optional-math-clause>
<boolean-expression> = <math-expression> <comparison-operator> <math-expression> | <table-field> LIKE <string> | <table-field> IS [NOT] NULL              //  look-ahead for <table-field>
<condition> = <boolean-expression> [AND <condition | OR <condition> ]

# lists
<value-list> := <value> [, <value-list>]
<field-list> := <table-field> [, <field-list>]
<assignment-list> := <table-field> = <value> [, <assignment-list>]

# query helpers (mostly for select query)
<select-clause> := * | <field-alias-list>
<field-alias-list> := <field-alias> [, <field-alias-list>]
<field-alias> := <table-field> [AS <alias>] | <function> ( <table-field> ) [AS <alias>]
<table-alias-list> := <table-alias> [, <table-alias-list>]
<table-alias> := <table> [AS <alias>]
<table-clause> := <table> <optional-join-clause>
<optional-join-clause> := λ | <join-clause> <optional-join-clause>
<join-clause> := <join-type> JOIN <table> ON <condition>
<join-type> := RIGHT | LEFT | INNER | FULL
<order-list> := <order-item> [, <order-list>]
<order-item> :=  <table-field> [ASC | DESC]

# basic queries
<insert-query> := INSERT INTO <table> ( <field-list> ) VALUES ( <value-list> )
<update-query> := UPDATE <table> SET ( <assignment-list> ) [WHERE <condition>]
<delete-query> := DELETE FROM <table> [WHERE <condition>]

# select query
<select-query> := SELECT [DISTINCT] <select-clause> FROM <table-clause> [WHERE <condition>] [GROUP BY <field-list>] [HAVING <condition>] [ORDER BY <order-list>]

# big picture sql
<comment> := **any text starting with '/*' and ending with '*/' delimeters**
<statement> := <select-query>; | <insert-query>; | <update-query>; | <delete-query>; | <comment>                // use look-ahead to determine query-type
<sql> := <statement> | <statement> <sql>    
```