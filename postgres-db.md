user creation:


```sql

    CREATE USER demo WITH PASSWORD '123';

```
 
db creation:

```sql

    CREATE DATABASE mydb WITH OWNER demo;

```
 

psql restore command: 

```bash

    gunzip < home/ubuntu/ita_ds_prod0309.gz | psql --host=xxxxrds.amazonaws.com --port=5432 --username=xxxx --password mydb

```

psql dump

```bash

    sudo -u postgres pg_dump mydb | gzip -9 > mydb.sql.gz
    pg_dump -h hosturl  -U dbuser  mydb | gzip -9 > mydb.sql.gz

```

Connect to PostgreSQL database

    The following command connects to a database under a specific user. 
    After pressing Enter PostgreSQL will ask for the password of the user.
    
 ```sql
    
    psql -d database -U  user -W
    
 ```
    For example, to connect to dvdrental database under postgres user, you use the following command:

 ```sql

    psql -d dvdrental -U postgres -W
    Password for user postgres:
    dvdrental=#

```

```bash
    # If you want to connect to a database that resides on another host, you add the -h option as follows:

    psql -h host -d database -U user -W
    
    # In case you want to use SSL mode for the connection, just specify it as shown in the following command:

    psql -U user -h host "dbname=db sslmode=require"

```

Switch connection to a new database

    \c dbname username

List available databases

    \l


List available tables

    \dt

Describe a table

    \d table_name

List available schema

    \dn

List available functions

    \df

List available views

    \dv

List users and their roles
    
    \du

Execute the previous command

    SELECT version();

Now, you want to save time typing the previous command again, you can use \g command to execute the previous command:

    \g
    

Command history

    To display command history, you use the \s command.
    \s
    If you want to save the command history to a file, you need to specify the file name followed the \s command as follows:
    \s filename

Execute psql commands from a file

    \i filename
    

Get help on psql commands

    To know all available psql commands, you use the \? command.

    \?

    To get help on specific PostgreSQL statement, you use the \h command.

    For example, if you want to know detailed information on ALTER TABLE statement, you use the following command:

    \h ALTER TABLE

Turn on query execution time

    To turn on query execution time, you use the \timing command.
    dvdrental=# \timing


```sql

DROP DATABASE [IF EXISTS] database_name;

```
Drop a database that has active connections

    To delete the database that has active connections, you can follow these steps:

    First, find the activities associated with the database by querying the pg_stat_activity view:


```sql

    SELECT * FROM pg_stat_activity WHERE datname = '<database_name>';

```

Second, terminate the active connections by issuing the following query:


```sql

    SELECT	pg_terminate_backend (pid) FROM	pg_stat_activity  WHERE	pg_stat_activity.datname = '<database_name>';

```

Notice that if you use PostgreSQL version 9.1 or earlier, use the procpidcolumn instead of the pidcolumn because PostgreSQL changed procidcolumn to pidcolumn since version 9.2

Third, execute the DROP DATABASE statement:


```sql
   
   DROP DATABASE <database_name>;

```

PostgreSQL DROP DATABASE examples

We will use the databases created in the PostgreSQL create database tutorial for the demonstration.

If you haven’t created this database yet, you can use the following CREATE DATABASE statements to create them:

CREATE DATABASE hrdb;
CREATE DATABASE testdb1;

1) Drop a database that has no active connection example

To remove the hrdbdatabase, use the hrdb owner to connect to a database other than hrdbdatabase e.g., postgres and issue the following statement:

```sql

    DROP DATABASE hrdb;

```

2) Drop a database that has active connections example

The following statement deletes the testdb1database:


```sql

    DROP DATABASE testdb1;
```

However, PostgreSQL issued an error as follows:

    ERROR: database "testdb1" is being accessed by other users
    SQL state: 55006
    Detail: There is 1 other session using the database.

To drop the testdb1 database, you need to terminate the active connection and drop the database.

First, query the pg_stat_activityview to find what activities are taking place against the testdb1database:

```sql
    
    SELECT * FROM pg_stat_activity WHERE datname = 'testdb1';

```

PostgreSQL DROP DATABASE - testdb1 activities

    The testdb1database has one connection from localhosttherefore it is safe to terminate this connection and remove the database. 

    Second, terminate the connection to the testdb1database by using the following statement:

```sql

    SELECT
        pg_terminate_backend (pg_stat_activity.pid)
    FROM
        pg_stat_activity
    WHERE
        pg_stat_activity.datname = 'testdb1';
```

Third, issue the DROP DATABASE command to remove the testdb1database:

```sql

    DROP DATABASE testdb1;

```
PostgreSQL drops the testdb1permanently.





```bash

# pg_dump -U username dbname > dump.sql
pg_dump -U postgres postgres > dump.sql
# Extract Schema Only           -s option
pg_dump -U postgres -s postgres > dump.sql
# Extract Data Only 	        -a option
pg_dump -U postgres -a postgres > dump.sql
# Generate DROP statements      -c option
# Export OIDs                   -o option 

pg_dump -h hosturl  -U dbuser  mydb | gzip -9 > mydb.sql.gz
```


