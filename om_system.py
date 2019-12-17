import datetime#used to calculate dates of travel, specifically timedelta object
import sqlite3#database where the order information is stored
from sqlite3 import Error #used to identify errors in running code
from tabulate import tabulate #formats data pulled from sqlite into a table to enhance readability for the user
mydb = "oms_db.db"# DB name as stored in folder

def create_connection(db_file):#function taken from sqlite demo, used to create a cursor when called
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
        return None
conn = create_connection(mydb)


if conn:
    print ("Connected to database: ",conn)  
else:
    print("Error connecting to database.")



#sql = conn.execute("CREATE TABLE orders (crid text, dateplaced text, units int, portoforigin text, edd text, eda text)")
#conn.execute("CREATE TABLE trackorder (crid text, orderplaced text, departorigin text, arrivedomestic text, offload text, readyintermodal text, arrivedc text)")

#sql = conn.execute("CREATE TABLE trackorder (crid text, orderplaced text, departorigin text, arrivedomestic text, offload text, readyintermodal text, arrivedc text)")

#sqloutput = "DROP TABLE orders"

#conn.execute(sqloutput)





#where the user inputs a customer order after it is placed
def input_order():
    order_value = []
    tracking_value = []
    customer_id = input("Enter Customer ID(Corporate abbr. + 4 digit id#): ")
    
    #fills 'crid' column in sqlite table, used as customer initials + last 4 of phone number
    
    while True:
        #ensures all crid's are same length and format to maintain consistency
        if customer_id[:3].isalpha():
            if customer_id[3:].isnumeric():
                break
            else:
                print("please enter a valied CRIID")
            

        else:
            print("Please enter valid CRID")

        customer_id = input("Enter Customer ID(3 digit corporate abbr. + 4 digit id#): ")
    tracking_value.append(customer_id)


    units = input("Total Units Requested: ")
    
    order_placed = datetime.datetime.now()#calls datetime when the order is submitted
    
#quantity of units determines which vendor recieves the order, and which port it will depart from
    if int(units) >= 3000:
        china_lb = [0,6,14,3,2,6]#days between points in the supply chain process from the time the order was placed to when it arrives at the DC
        foreign_port = "Yan Tin"
        _order_timedelta = datetime.datetime.now()
        for item in china_lb:
            travel_date =  _order_timedelta + datetime.timedelta(item)
            tracking_value.append(travel_date.strftime("%x"))
            _order_timedelta = travel_date
        #for loop adding the in-travel time in between locations in the process and returning a list of 7 dates

    elif int(units) >= 500:
        camb_lb = [0,5,12,3,2,6]
        foreign_port = "Sihanoukville"
        _order_timedelta = datetime.datetime.now()
        for item in camb_lb:
            travel_date =  _order_timedelta + datetime.timedelta(item)
            tracking_value.append(travel_date.strftime("%x"))
            _order_timedelta = travel_date


    elif int(units) < 500:
        print("Minimum order amount = 200 ----> Please enter valid amount: ")
        units = input("Total Units Requested: ")
    order_value = list((customer_id, order_placed.strftime("%x"),units,foreign_port, tracking_value[2], tracking_value[-1]))
    #creates a list(order_value) containing the information to be stored in the sqlite3 table
    try:
        sqlresult = conn.execute("INSERT INTO orders (crid,dateplaced,units,portoforigin,edd,eda)VALUES(?,?,?,?,?,?)", order_value)
        sqlresult = conn.execute("INSERT INTO trackorder (crid,orderplaced,departorigin,arrivedomestic,offload,readyintermodal,arriveDC)VALUES(?,?,?,?,?,?,?)", tracking_value)#reaches out to the table to find location to insert data

        result = conn.commit()#this actually runs the SQL and inserts the data         into the database
        if result == None:
            print("*** Data saved to database. ***")
    except Error as e:
        print ("*** Insert error: ",e)
        pass
    

#pulls order data from sqlite table 'orders'
def retrieve_order(order_CRID = None):
    try:

        if order_CRID: #if a value is inserted for order_crid, pull the relevant data for that specific order, to be used in order_summary()
            cursor = conn.execute ("SELECT * FROM orders where crid = '"+order_CRID+"'")
        else:#otherwise pull information for all orders
            cursor = conn.execute ("SELECT * FROM orders")
        header = []
        
        for item in cursor.description:#parse information from table and return column id's in uppercase then append to headers list
            header.append(item[0].upper())
            
        allorders = []
        allorders.append(header)#sets first nested list as header values
        for row in cursor:#returns each row provided by the cursor value
            thisrow=[]
            for x in row:#parses items in each row and adds them to 'thisrow'
                thisrow.append(x)
            allorders.append(thisrow)
        return allorders#returns all orders to be used by view_order()

        
    except Error as e:
        print (e)
        pass  

def retrieve_tracking(trackorder_CRID = None): #pulls the information from the'trackorder' table, which is dervied from the tracking value listed formed in the input_order() function
        try:
            if trackorder_CRID:
                cursor = conn.execute ("SELECT * FROM trackorder where crid = '"+trackorder_CRID+"'")#only pulls tracking information from a specified order
            else:
                cursor = conn.execute ("SELECT * FROM trackorder")#pulls shipping info from all orders, to be used in the tracking feature

            headers = []
            
            for item in cursor.description:
                headers.append(item[0].upper())
            #print(headers)
            allorders = []
            allorders.append(headers)
            for row in cursor:
                #print(row)
                thisrow=[]
                for x in row:
                    thisrow.append(x)
                allorders.append(thisrow)
            return allorders
            
        except Error as e:
            print (e)
            pass  

def order_summary():
        table = retrieve_order()
        print(tabulate(table,headers="firstrow"))
        selected_CRID = input("Select an order to review: \n")
        
        try:
            order_info = retrieve_order(selected_CRID)
            print(tabulate(order_info,headers="firstrow"))

            

            for (point, date) in list(zip(*retrieve_tracking(selected_CRID))):
                print("{} : {}\n".format(point,date))



        except Error as e:  
            print (e)
            pass  





while True:
    print('''Welcome to the IMS.
    1 = place order
    2 = view current orders
    3 = order details
    4 = track order
    enter = exit
    '''
    )

    feature = input("Enter feature: ") 

    if (feature == "1"):
        input_order()

    elif (feature =="2"):
        table = retrieve_order()
        print(tabulate(table,headers="firstrow"))

    elif (feature =="3"): 
        order_summary()

    elif (feature =="4"):
        table = retrieve_tracking()
        print(tabulate(table,headers="firstrow"))

    elif (feature ==""):
        break

