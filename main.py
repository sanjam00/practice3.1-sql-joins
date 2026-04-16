import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

# db = pd.read_sql('')

# Select the names of all employees in Boston.
boston_names = pd.read_sql("""
                        SELECT firstName, lastName, employeeNumber, city, officeCode
                        FROM employees AS e
                        JOIN offices as o
                        USING(officeCode)
                        WHERE city = 'Boston';
                        """, conn)

print(boston_names)

# Are there any offices that have zero employees?
# Note that COUNT(*) is not appropriate here because we are trying to count the _employees_ in each group.
# So instead we count by some attribute of an employee record. 
# The primary key (employeeNumber) is a conventional way to do this
no_employees = pd.read_sql("""
                           SELECT o.officeCode, o.city, COUNT(e.employeeNumber) AS n_employees
                           FROM offices AS o
                           LEFT JOIN employees AS e
                           USING(officeCode)
                           GROUP BY officeCode
                           HAVING n_employees = 0;
                           """, conn)

print(no_employees)

# How many customers are there per office?
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

# Display the names of every individual product that each employee has sold as a dataframe.
sold_product = pd.read_sql("""
                           SELECT firstName, lastName, productName
                           FROM employees AS e
                           JOIN customers AS c
                           ON e.employeeNumber = c.salesRepEmployeeNumber
                           JOIN orders
                           USING(customerNumber)
                           JOIN orderDetails
                           USING(orderNumber)
                           JOIN products
                           USING(productCode);
                           """, conn)

print(sold_product)

# Display the number of products each employee has sold.
total_products_sold = pd.read_sql("""
                             SELECT employeeNumber, firstName, SUM(quantityOrdered) AS total_products_sold
                             FROM employees AS e
                             JOIN customers AS c
                             ON e.employeeNumber = c.salesRepEmployeeNumber
                             JOIN orders AS o
                             USING(customerNumber)
                             JOIN orderDetails
                             USING(orderNumber)
                             GROUP BY firstName, lastName
                             ORDER BY lastName
                             """, conn)

print(total_products_sold)

more_than_200 = pd.read_sql("""
                            SELECT firstName, lastName, COUNT(productCode) AS different_products_sold
                            FROM employees AS e
                            JOIN customers AS c
                            ON e.employeeNumber = c.salesRepEmployeeNumber
                            JOIN orders
                            USING(customerNumber)
                            JOIN orderDetails
                            USING(orderNumber)
                            GROUP BY firstName, lastName
                            HAVING different_products_sold > 200
                            ORDER BY lastName
                            """, conn)

print(more_than_200)

conn.close()