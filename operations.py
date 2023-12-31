import json
import string
import random
from json import JSONDecodeError

def Register(type,member_json_file,admin_json_file,Full_Name,Address,Email,Password):
    '''Register Function || Return True if registered successfully else False'''
    if type.lower()=='admin':
        f=open(admin_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Address":Address,
            "Email":Email,
            "Password":Password,
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
        return True
    elif type.lower()=='member':
        f=open(member_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Address":Address,
            "Email":Email,
            "Password":Password,
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
        return True
    else:
        return False

def Login(type,members_json_file,admin_json_file,Email,Password):
    '''Login Functionality || Return True if successfully logged in else False'''
    d=0
    if type.lower()=='admin':
        f=open(admin_json_file,'r+')
    else:
        f=open(members_json_file,'r+')
    try:
        content=json.load(f)
    except JSONDecodeError:
        return False
    for i in range(len(content)):
        if content[i]["Email"]==Email and content[i]["Password"]==Password:
            d=1
            break
    f.seek(0)
    f.truncate()
    json.dump(content,f)
    f.close()
    if d==0:
        return False
    return True

def AutoGenerate_ProductID():
    '''Return a autogenerated random product ID'''
    product_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=4))
    return product_ID

def AutoGenerate_OrderID():
    '''Return a autogenerated random product ID'''
    Order_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=3))
    return Order_ID

def Create_Product(owner,product_json_file,product_ID,product_name,manufacturer_name,price,discount,total_stock_available):
    '''Creating a product || Return True if successfully created else False'''
    f=open(product_json_file,'r+')
    d={
        "Created By":owner,
        "Product ID": product_ID, 
        "Product Name": product_name, 
        "Manufacturer Name": manufacturer_name,
            "Price": price,
            "Discount": discount,
            "Total Stock Available":total_stock_available
    }
    try:
        content=json.load(f)
        if d not in content:
            content.append(d)
            f.seek(0)
            f.truncate()
            json.dump(content,f)
    except JSONDecodeError:
        l=[]
        l.append(d)
        json.dump(l,f)
    f.close()
    return True

def Read_Products(owner,product_json_file):
    '''Reading Products created by the admin(owner)'''
    f=open(product_json_file,"r+")
    content=json.load(f)
    d=[]
    for i in content:
        if i['Created By']==owner:
            d.append(i)
    f.close()
    return d

def Read_Product_By_ID(product_json_file,product_ID,Details):
    '''Reading product by ID'''
    f=open(product_json_file,"r+")
    content=json.load(f)
    for i in content:
        if i['Product ID']==product_ID:
            Details.append(i)
            break
    f.close()
    return Details
    

def Update_Product(product_json_file,product_ID,detail_to_be_updated,new_value):
    '''Updating Product || Return True if successfully updated else False'''
    d=0
    f=open(product_json_file,'r+')
    content2=json.load(f)
    for i in range(len(content2)):
        if content2[i]["Product ID"]==product_ID and detail_to_be_updated in content2[i].keys() and detail_to_be_updated!="Product ID":
            content2[i][detail_to_be_updated]=new_value
            d=1
            break
    f.seek(0)
    f.truncate()
    json.dump(content2,f)
    f.close()
    if d==1:
        return True
    return False

    
def Delete_Product(product_json_file,product_ID):
    '''Deleting Product || Return True if successfully deleted else False'''
    f=open(product_json_file,'r+')
    try:
        content=json.load(f)
        for i in content:
            if i['Product ID']==product_ID:
                del content[content.index(i)]
                f.seek(0)
                f.truncate()
                json.dump(content,f)
    except JSONDecodeError:
        return False    
    
    f.close()
    return True

def Update_Member(member_json_file,name,detail_to_be_updated,new_value):
    '''Updating Member Details || Return True if successfully updated else False'''
    f=open(member_json_file,'r+')
    d={detail_to_be_updated:new_value}
    
    try:
        content=json.load(f)
        for i in content:
            if i['Full Name']==name:
                content[content.index(i)].update(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
    except JSONDecodeError:
        return False
    
    f.close()
    return True

def Place_Order(order_json_file,ordered_by,delivery_address,product_json_file,product_ID,Quantity,Order_ID):
    '''Placing Order, Calculate the Price after discount and Total cost of the order || Return True if order placed successfully else False'''
    pf=open(product_json_file,'r+')
    content=json.load(pf)
    for i in content:
        if i["Product ID"]==product_ID:
            product_name = i["Product Name"]
            price = i["Price"]
            discount = i["Discount"]
            stock=i["Total Stock Available"]
            break
    pf.close()
    if stock ==0 or stock<Quantity:
        return False
    else:
        f=open(order_json_file,'r+')
        price_after_discount = float(float(price)-((float(price)*float(discount[:-1]))/100))
        d={"Order ID": Order_ID, 
            "Product Name": product_name, 
            "Price": price, 
            "Discount": discount, 
            "Price after Discount": price_after_discount,
            "Quantity": Quantity,
            "Total Cost": Quantity*price_after_discount,
            "Ordered By": ordered_by, 
            "Delivering to": delivery_address
            }

        try:
            content=json.load(f)
            content.append(d)
            f.seek(0)
            f.truncate()
            json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()

        pf1=open(product_json_file,'r+')
        content=json.load(pf1)
        
        for i in content:
            if i["Product ID"]==product_ID:
                
                dd={'Total Stock Available':int(i["Total Stock Available"])-Quantity}
                content[content.index(i)].update(dd)
                break

        try:
            pf1.seek(0)
            pf1.truncate()
            json.dump(content,pf1)
        except JSONDecodeError:
            return False
        
        pf1.close()

        return True
    


def Order_History(order_json_file,Name,details):
    '''Append the order information into details list'''
    f=open(order_json_file,'r+')
    try:
        content=json.load(f)
        for i in content:
            if i['Ordered By']==Name:
                details.append(i)
    except JSONDecodeError:
        return False
    
    f.close()
    return True

