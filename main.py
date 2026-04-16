import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

# db = pd.read_sql('')

boston_names = pd.read_sql("""
                        SELECT firstName, lastName, employeeNumber, city, officeCode
                        FROM employees AS e
                        JOIN offices as o
                        USING(officeCode)
                        WHERE city = 'Boston';
                        """, conn)

print(boston_names)

# Note that COUNT(*) is not appropriate here because
# we are trying to count the _employees_ in each group.
# So instead we count by some attribute of an employee
# record. The primary key (employeeNumber) is a 
# conventional way to do this
no_employees = pd.read_sql("""
                           SELECT o.officeCode, o.city, COUNT(e.employeeNumber) AS n_employees
                           FROM offices AS o
                           LEFT JOIN employees AS e
                           USING(officeCode)
                           GROUP BY officeCode
                           HAVING n_employees = 0;
                           """, conn)

print(no_employees)

per_office = pd.read_sql("""
                         SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
                         FROM offices AS o
                         JOIN employees AS e
                         USING(officeCode)
                         JOIN customers AS c
                         ON e.employeeNumber = c.salesRepEmployeeNumber
                         GROUP BY officeCode;
                         """, conn)

print(per_office)



conn.close()