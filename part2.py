# these should be the only imports you need
import sys
import sqlite3

# write your code here
# usage should be 
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>

err_msg = '''
# usage should be 
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>
'''

db_file = "Northwind_small.sqlite"
conn = sqlite3.connect(db_file)
obj = sys.argv[1]
if obj == 'customers':
    cur = conn.cursor()
    cur.execute("SELECT * FROM Customer;")
    out = cur.fetchall()
    print("ID\t\tCustomer Name")
    for item in out:
        print(item[0], '\t', item[1], sep='')
elif obj == 'employees':
    cur = conn.cursor()
    cur.execute("SELECT * FROM Employee;")
    out = cur.fetchall()
    print("ID\t\tEmployee Name")
    for item in out:
        print(item[0], '\t\t', item[2], ' ', item[1], sep='')
elif obj == 'orders':
    if sys.argv[2].startswith('cust'):
        cust = sys.argv[2][5:]
        cur = conn.cursor()
        cur.execute("SELECT OrderDate FROM 'Order' WHERE CustomerId=?;", (cust,))
        out = cur.fetchall()
        print("Order dates")
        for item in out:
            print(item[0])
    elif sys.argv[2].startswith('emp'):
        emp = sys.argv[2][4:]
        cur = conn.cursor()
        cur.execute("SELECT Id FROM Employee WHERE LastName=?", (emp,))
        eid = cur.fetchall()[0][0]
        cur = conn.cursor()
        cur.execute("SELECT OrderDate FROM 'Order' WHERE EmployeeId=?;", (eid,))
        out = cur.fetchall()
        print("Order dates")
        for item in out:
            print(item[0])
    else:
        raise SyntaxError(err_msg)
else:
    raise SyntaxError(err_msg)


