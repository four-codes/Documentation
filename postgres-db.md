user creation:

    CREATE USER demo WITH PASSWORD '123';
 
db creation:

    CREATE DATABASE mydb WITH OWNER demo;

psql restore command: 

    gunzip < home/ubuntu/ita_ds_prod0309.gz | psql --host=xxxxrds.amazonaws.com --port=5432 --username=xxxx --password mydb
    
psql dump 

    sudo -u postgres pg_dump mydb | gzip -9 > mydb.sql.gz
    
Connect to PostgreSQL database

    The following command connects to a database under a specific user. After pressing Enter PostgreSQL will ask for the password of the user.
    psql -d database -U  user -W


    For example, to connect to dvdrental database under postgres user, you use the following command:

    psql -d dvdrental -U postgres -W
    Password for user postgres:
    dvdrental=#

    If you want to connect to a database that resides on another host, you add the -h option as follows:

    psql -h host -d database -U user -W
    

    In case you want to use SSL mode for the connection, just specify it as shown in the following command:

    psql -U user -h host "dbname=db sslmode=require"


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
