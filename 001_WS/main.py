from flask import Flask,render_template,request
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uropen
import requests
import pandas as pd
import mysql.connector
app = Flask(__name__)
from db_connect import create_db,create_table,insert_table

# Importing module


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin123",
  database="new_flip"

)

print(mydb)

cur=mydb.cursor()
db_name="new_flip"
tb_name="flip_info"


create_db(cur,db_name)
create_table(cur,tb_name)
# Printing the connection object



@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")
@app.route("/review",methods=["GET","POST"])
def results():
    if request.method=="POST":
        try:
            searchString=request.form["name"].replace(" ","")
            scrap = "https://www.flipkart.com/search?q="+searchString
            print(scrap)
            scrap_1 = uropen(scrap)
            scarp_detail = scrap_1.read()
            scarp_bs = bs(scarp_detail, "html.parser")
            # print(scarp_bs)

            scrap_2 = scarp_bs.find_all("div", {"class": "_1AtVbE col-12-12"})
            # print(scrap_2)
            del scrap_2[0:2]
            mobile=scrap_2[1].a["href"]
            # print(mobile)
            total_mobile="https://www.flipkart.com"+mobile
            print(total_mobile)
            all_mobile=bs(total_mobile,"html.parser")
            print(all_mobile)
            all_m=requests.get(all_mobile)
            all_details=bs(all_m.text,"html.parser")

            mobile_review=all_details.find_all("div",class_="_16PBlm")
            print( mobile_review)




            review=[]
            for com in mobile_review:
                try:
                    phone_name = all_details.find_all("span",{"class":"B_NuCI"})[0].text
                except:
                    phone_name= "product name not avilable"
                try:
                    phone_price = all_details.find_all("div", {"class": "_30jeq3 _16Jk6d"})[0].text
                except:
                    phone_price="Product price not availble"
                try:
                    phone_header = com.find_all("p", {"class": "_2-N8zT"})[0].text
                except:
                    phone_header="product Review Heading not  availble"
                try:
                    phone_comment = com.find_all("div", {"class": "t-ZTKy"})
                    comment=phone_comment[0].div.div.text
                except:
                    comment="product Review Not Available"
                try:
                    phone_rev_name=com.find_all("p",{"class":"_2sc7ZR _2V5EHH"})[0].text
                except:
                    phone_rev_name="name not Available"
                mydict={"name": phone_name, "price": phone_price,  "header": phone_header, "comment": comment,"rev_name": phone_rev_name}
                review.append(mydict)
                print(review)
                insert_quary = f"insert into {db_name}.{tb_name} values (%(name)s,%(price)s,%(header)s,%(comment)s,%(rev_name)s); "
                cur.executemany(insert_quary,review)
                mydb.commit()
            return render_template("result.html",reviews1=review[0:(len(review)-1)])

        except:
            return "somthing Wrong"







app.run()