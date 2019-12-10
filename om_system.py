import datetime
import sqlite3
from sqlite3 import Error 
from tabulate import tabulate
mydb = "oms_db.db"

def create_connection(db_file):
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



#conn.execute("CREATE TABLE orders (crid text, dateplaced text, units int, portoforigin text, edd text, eda text)")
#conn.execute("CREATE TABLE trackorder (crid text, orderplaced text, departorigin text, arrivedomestic text, offload text, readyintermodal text, arrivedc text)")

#sql = conn.execute("CREATE TABLE trackorder (crid text, orderplaced text, departorigin text, arrivedomestic text, offload text, readyintermodal text, arrivedc text)")

#sqloutput = "DROP TABLE trackorder"

#conn.execute(sqloutput)


#order_Dict = {}
#tracking_Dict = {}



#import datetime
def input_order():
    order_value = []
    tracking_value = []
    customer_id = input("Enter Customer ID(Corporate abbr. + 4 digit id#): ")
    #print(len(customer_id))

    if len(customer_id) != 7:
        print("Please enter valid CRID")
        customer_id = input("Enter Customer ID(Corporate abbr. + 4 digit id#): ")
    #elif len(customer_id) <= 6:
        print("Please enter valid CRID")
        customer_id = input("Enter Customer ID(Corporate abbr. + 4 digit id#): ")
        
    #elif customer_id[3:].isnumeric == False:
        #print("Please enter valid CRID")
        #customer_id = input("Enter Customer ID(Corporate abbr. + 4 digit id#): ")
    elif len(customer_id) == 7:
        tracking_value.append(customer_id)
        print("Order Saved")

    else:
        
        pass

    units = input("Total Units Requested: ")
    
    order_placed = datetime.datetime.now()
    print(tracking_value)
    


    if int(units) >= 3000:
        china_lb = [0,6,14,3,2,6]
        foreign_port = "Yan Tin"
        _order_timedelta = datetime.datetime.now()
        for item in china_lb:
            travel_date =  _order_timedelta + datetime.timedelta(item)
            tracking_value.append(travel_date.strftime("%x"))
            _order_timedelta = travel_date

    elif int(units) < 3000:
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

    try:
        sqlresult = conn.execute("INSERT INTO orders (crid,dateplaced,units,portoforigin,edd,eda)VALUES(?,?,?,?,?,?)", order_value)
        sqlresult = conn.execute("INSERT INTO trackorder (crid,orderplaced,departorigin,arrivedomestic,offload,readyintermodal,arriveDC)VALUES(?,?,?,?,?,?,?)", tracking_value)

        result = conn.commit()#this actually runs the SQL and inserts the data         into the database
        if result == None:
            print("*** Data saved to database. ***")
    except Error as e:
        print ("*** Insert error: ",e)
        pass
    


def retrieve_order(order_CRID = None):
    try:
        if order_CRID:
            cursor = conn.execute ("SELECT * FROM orders where crid = '"+order_CRID+"'")
        else:
            cursor = conn.execute ("SELECT * FROM orders")
        header = []
        
        for item in cursor.description:
            header.append(item[0].upper())
            
        allorders = []
        allorders.append(header)
        for row in cursor:
            thisrow=[]
            for x in row:
                thisrow.append(x)
            allorders.append(thisrow)
        return allorders

        
    except Error as e:
        print (e)
        pass  

def retrieve_tracking(order_CRID):
        try:
            cursor = conn.execute ("SELECT * FROM trackorder where crid = '"+order_CRID+"'")
            
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
            #tracking_dates = list(zip(*allorders))

            #print(tracking_dates)
            #for (point, date) in list(zip(*allorders)):#tracking_dates[1:]:
                #print("{} : {}".format(point,date))


        
        except Error as e:
            print (e)
            pass  

def order_summary():
        table = retrieve_order()
        print(tabulate(table,headers="firstrow"))
        selected_CRID = input("Select an order to review: \n")
        #cursor = conn.cursor()

        #cursor.execute("SELECT * from orders WHERE crid = "+command)
        #summary = cursor.fetchall()
        #print(summary)
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
    3 = order summary
    4 = track order
    enter = exit
    '''
    )


#feature = input("Enter feature: ")



    feature = input("Enter feature: ") 

    if (feature == "1"):
        input_order()

    elif (feature =="2"):
        table = retrieve_order()
        print(tabulate(table,headers="firstrow"))


        
        #for row in list(zip(*retrieve_order())):
            #print(row)
            #print(row)
            #thisrow = "  --> "
            #for item in row:
                #thisrow += str(item)+"  "
            #print(thisrow)
        #print(retrieve_order())
        
        
    elif (feature =="3"):

        #for row in retrieve_order():
            #thisrow = "  --> "
            #print(row)
            #for item in row:
                #   thisrow += str(item)+"  "
            #print (thisrow)  
        order_summary()
    elif (feature =="4"):
        selected_CRID = input("Select an order to review: ")
        for (point, date) in retrieve_tracking(selected_CRID):
            print("{} : {}".format(point,date))
    elif (feature ==""):
        break








"""def view_order():
    print("CURRENT ORDERS:")
    for o_id in order_Dict:
        print(o_id)
        
        
    o_name = input("Enter order to inspect: ")
    for x, y in order_Dict.items():
        if x == o_name:
            print("CRID : {}\n".format(x))
            for x,y in order_Dict[o_name].items():
                print("{} : {}".format(x,y))
        else:
            pass
def track_order():
    print("\nCURRENT ORDERS:")
    for t_id in tracking_Dict:
        print(t_id)
        
        
    t_name = input("Enter order to track: ")
    for x, y in tracking_Dict.items():
        if x == t_name:
            print("\nCRID : {}\n".format(x))
            for x,y in tracking_Dict[t_name].items():
                print("{} : {}".format(x,y))
        else:
            pass
 
 """