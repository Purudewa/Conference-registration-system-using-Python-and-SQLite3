import time
import smtplib
import sqlite3
import uuid
import getpass
import re
import datetime
from prettytable import PrettyTable
conn = sqlite3.connect('OOPD')
c = conn.cursor()

FEES = {0:1000,1:1000,2:1500,3:1200,4:1100,5:1800,6:2000,7:1500}

date = "2020-12-10"

class EI:
 #EVENT INFORMATION
 def ei(self):
    event = PrettyTable(["Event","Title", "Date", "Venue","Timings","Chief Guests","Registration Fees"]) 
    event.add_row(["Workshop1 ", "Role of Classics in Modern Society", "22 December,2020", "IIIT Delhi","10:00  am","Dr. James Anderson,Oxford University","Rs. 1000"]) 
    event.add_row(["Workshop 2", "Modern Literature: The Changing Times", "23 December,2020", "IIIT Delhi","10:00 am","Dr. Hans Longfellow, UT Austin","Rs. 1000"]) 
    event.add_row(["Panel Discussion 1", "Harry Potter and the Millennials", "22 December,2020", "IIIT Delhi","3:00 pm","J. K. Rowling","Rs. 1500"]) 
    event.add_row(["Panel Discussion 2", "Shaping the Impact of Myths in Fiction", "23 December,2020", "IIIT Delhi","3:00 pm","Dr. Harold Snow, Amherst College, London","Rs. 1200"]) 
    event.add_row(["Tutorial 1", "How to Write an Engaging Novel", "24 December,2020", "IIIT Delhi","10:00 am","James Patterson","Rs. 1100"]) 
    event.add_row(["Tutorial 2", "Writing Realistic Horror Fictions", "24 December,2020", "IIIT Delhi","3:00 pm","Stephen King","Rs. 1800"]) 
    event.add_row(["Paper Presentation 1", "Novelist as an Artist in Society", "25 December,2020", "IIIT Delhi","10:00 am","Gilbert Aldair","Rs. 2000"]) 
    event.add_row(["Paper Presentation 2", "Role of Non-Fiction in defining Culture", "25 December,2020", "IIIT Delhi","10:00 am","Dr. Isha Bhatt, Cambridge University","Rs. 1500"]) 
    print(event)
    print("Important Deadlines")
    dates = PrettyTable(["Event","Deadlines"]) 
    dates.add_row(["Last Date for Event Registration", "20 December, 2020"])
    dates.add_row(["Last Date for Submitting Abstracts", "15 December, 2020"])
    dates.add_row(["Last Date for Final Paper Submission", "15 January, 2020"])
    print(dates)


class OI:
 #ORGANIZER_INFORMATION
 def oi(self):
  event = PrettyTable(["Organising member 1","Organising member 2 ","Sponsors"]) 
  event.add_row(["Divisha Bisht, M.Tech. Student. IIIT Delhi","Purudewa Pawar, M.Tech. Student. IIIT    Delhi","Literary Society of India"]) 
  event.add_row(["Contact email: divisha3@gmail.com", "Contact email: purudewa@gmail.com", "Penguin Publishing House, India"]) 
  event.add_row(["Mob. no. 9563456733 ","Mob. no. 9754356787","HaperCollins, India"]) 

  print(event)

class IV:
 def iv(self,s):  
     Pattern = re.compile("(0/91)?[6-9][0-9]{9}") 
     return Pattern.match(s) 

class M:
 #MOBILE NUMBER VALIDATION
 def  m(self):
     s = input('\nMOBILE NO : ')
     if not (IV.iv(self, s)):   
         print ("Invalid Mobile No. Please... Try Again :")
         self.m()
     return s

class PWD:
 #PASSWORD VALIDATION
 def  pwd(self):
     print('\nPlease enter your password\n')
     password = getpass.getpass(prompt= 'Password must be minimum 8 characters and contain atleast one special  character and digit: \n')
     flag = 0
     if (len(password)<8): 
             flag = -1

     regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]+') 	 
     if(regex.search(password) == None): 
       	   flag = -1

     if(re.search(r'\d', password) == None):
           flag = -1
        
     if flag ==-1: 
         print("Not a Valid Password...Try Again..")
         obj = PWD()
     return password 
    
class ML:
 #CONFIRMATION MAIL ABOUT REGISTRATION
 def  ml(self,uid,total,f):
     query = 'select FEES,WS,WS2,TUT,TUT2,PD,PD2,PP,PP2,NAME from USER_DATA where ID = ?;'
     c.execute(query, (uid,))
     conn.commit()
     val =  list(sum(c.fetchmany(), ()))  

     if f==1:
         val[0] = total 

     if val[1] == 'Yes' :
       ws = 'WORKSHOP 1'
     else :
       ws = ''

     if val[2] == 'Yes' :
       ws2 = 'WORKSHOP 2'
     else :
       ws2 = ''

     if val[3] == 'Yes' :
       tut = 'TUTORIAL 1'
     else :
       tut = ''
  
     if val[4] == 'Yes' :
       tut2 = 'TUTORIAL 2'
     else :
       tut2 = ''

     if val[5] == 'Yes' :
       pd = 'PANEL DISCUSSION 1'
     else :
       pd = ''

     if val[6] == 'Yes' :
       pd2 = 'PANEL DISCUSSION 2'
     else :
       pd2 = ''

     if val[7] == 'Yes' :
       pp = 'PAPER PRESENTATION 1'
     else :
       pp = ''
  
     if val[8] == 'Yes' :
       pp2 = 'PAPER PRESENTATION 2'
     else :
       pp2 = ''

     message = """
                            !!!! Confirmation Mail !!!!

          Hello %s
          Thank you for registering at our Conference !!...

          Payment of Rs.%s is received successfully.
          
          **** !!! You will be attending following events at our conference!!! **** 
          %s  %s
          %s  %s
          %s  %s
          %s  %s
          ..........................

          Venue:
          Auditorium
          IIIT Delhi
          pincode :1235

          Best Wishes
          TEAM MICO""" % (val[9], val[0],ws,ws2,tut,tut2,pd,pd2,pp,pp2)
     m = smtplib.SMTP('smtp.gmail.com',587)
     m.ehlo()
     m.starttls()
     send, passw = "oopdproject1@gmail.com", "oopdproject@123"
     m.login(send, passw)
    
     query = 'select EMAIL from USER_DATA where ID = ?;'
     c.execute(query, (uid,))
     conn.commit()
     recv = c.fetchone()    
    
     m.sendmail(send,recv,message)
     m.close()    


class ES:
 #EVENT SELECTION FOR USER
 def  es(self,uid):
     choice = []
     print("Inorder to attend particular event please press 1 !!!\n")
     print("If you don't wish to attend particular event please press 0 !!!\n")
     choice.append(input('WORKSHOPS 1 : '))
     choice.append(input('WORKSHOPS 2 : '))
     choice.append(input('TUTORIALS 1: '))
     choice.append(input('TUTORIALS 2: '))
     choice.append(input('PANEL DISCUSSIONS 1: ')) 
     choice.append(input('PANEL DISCUSSIONS 2: '))
     choice.append(input('PAPER PRESENTATIONS 1: '))
     choice.append(input('PAPER PRESENTATIONS 2: '))
 
     if choice[0] == '1':
             query = 'UPDATE USER_DATA SET WS = ? WHERE ID = ?;' 
             c.execute(query, ('Yes',uid))
             conn.commit()
     else:
             query = 'UPDATE USER_DATA SET WS = ? WHERE ID = ?;' 
             c.execute(query, ('No',uid))
             conn.commit()
            
     if choice[1] == '1':
             query = 'UPDATE USER_DATA SET WS2 = ? WHERE ID = ?;' 
             c.execute(query, ('Yes',uid))
             conn.commit()
     else:
             query = 'UPDATE USER_DATA SET WS2 = ? WHERE ID = ?;' 
             c.execute(query, ('No',uid))
             conn.commit()

     if choice[2] == '1':
             query = 'UPDATE USER_DATA SET TUT = ? WHERE ID = ?;'
             c.execute(query,('Yes',uid))
             conn.commit() 
     else:
             query = 'UPDATE USER_DATA SET TUT = ? WHERE ID = ?;' 
             c.execute(query,('No',uid))
             conn.commit()
            
     if choice[3] == '1':
             query = 'UPDATE USER_DATA SET TUT2 = ? WHERE ID = ?;'
             c.execute(query,('Yes',uid))
             conn.commit() 
     else:
             query = 'UPDATE USER_DATA SET TUT2 = ? WHERE ID = ?;' 
             c.execute(query,('No',uid))
             conn.commit()

     if choice[4] == '1':
             query = 'UPDATE USER_DATA SET PD = ? WHERE ID = ?;' 
             c.execute(query,('Yes',uid))
             conn.commit()
     else:
             query = 'UPDATE USER_DATA SET PD = ? WHERE ID = ?;'
             c.execute(query,('No',uid))
             conn.commit()

     if choice[5] == '1':
             query = 'UPDATE USER_DATA SET PD2 = ? WHERE ID = ?;' 
             c.execute(query,('Yes',uid))
             conn.commit()
     else:
             query = 'UPDATE USER_DATA SET PD2 = ? WHERE ID = ?;'
             c.execute(query,('No',uid))
             conn.commit()  
            
     if choice[6] == '1':
             query = 'UPDATE USER_DATA SET PP = ? WHERE ID = ?;'
             c.execute(query,('Yes',uid))
             conn.commit()
     else:
             query = 'UPDATE USER_DATA SET PP = ? WHERE ID = ?;'
             c.execute(query,('No',uid))
             conn.commit()

     if choice[7] == '1':
             query = 'UPDATE USER_DATA SET PP2 = ? WHERE ID = ?;'
             c.execute(query,('Yes',uid))
             conn.commit()
     else:
             query = 'UPDATE USER_DATA SET PP2 = ? WHERE ID = ?;'
             c.execute(query,('No',uid))
             conn.commit()
     return choice 


class EC:
 #EXISTING USER EVENT MODIFICATION
 def  ec(self,uid):
     choice = []
     print("\nInorder to make changes in particular event please press 1 !!!\n")
     print("If you don't wish to make changes, please press 0 !!!\n")
     choice.append(input('WORKSHOPS 1 : '))
     choice.append(input('WORKSHOPS 2 : '))
     choice.append(input('TUTORIALS 1: '))
     choice.append(input('TUTORIALS 2: '))
     choice.append(input('PANEL DISCUSSIONS 1: ')) 
     choice.append(input('PANEL DISCUSSIONS 2: '))
     choice.append(input('PAPER PRESENTATIONS 1: '))
     choice.append(input('PAPER PRESENTATIONS 2: '))

     if choice[0] == '1':
            query = 'UPDATE USER_DATA SET WS = ? WHERE ID = ?;' 
            c.execute(query, ('Yes',uid))
            conn.commit()
     else:
            query = 'UPDATE USER_DATA SET WS = ? WHERE ID = ?;' 
            c.execute(query, ('No',uid))
            conn.commit()
            
     if choice[1] == '1':
            query = 'UPDATE USER_DATA SET WS2 = ? WHERE ID = ?;' 
            c.execute(query, ('Yes',uid))
            conn.commit()
     else:
            query = 'UPDATE USER_DATA SET WS2 = ? WHERE ID = ?;' 
            c.execute(query, ('No',uid))
            conn.commit()

     if choice[2] == '1':
            query = 'UPDATE USER_DATA SET TUT = ? WHERE ID = ?;'
            c.execute(query,('Yes',uid))
            conn.commit() 
     else:
            query = 'UPDATE USER_DATA SET TUT = ? WHERE ID = ?;' 
            c.execute(query,('No',uid))
            conn.commit()
            
     if choice[3] == '1':
            query = 'UPDATE USER_DATA SET TUT2 = ? WHERE ID = ?;'
            c.execute(query,('Yes',uid))
            conn.commit() 
     else:
            query = 'UPDATE USER_DATA SET TUT2 = ? WHERE ID = ?;' 
            c.execute(query,('No',uid))
            conn.commit()

     if choice[4] == '1':
            query = 'UPDATE USER_DATA SET PD = ? WHERE ID = ?;' 
            c.execute(query,('Yes',uid))
            conn.commit()
     else:
            query = 'UPDATE USER_DATA SET PD = ? WHERE ID = ?;'
            c.execute(query,('No',uid))
            conn.commit()

     if choice[5] == '1':
            query = 'UPDATE USER_DATA SET PD2 = ? WHERE ID = ?;' 
            c.execute(query,('Yes',uid))
            conn.commit()
     else:
            query = 'UPDATE USER_DATA SET PD2 = ? WHERE ID = ?;'
            c.execute(query,('No',uid))
            conn.commit()  
            
     if choice[6] == '1':
            query = 'UPDATE USER_DATA SET PP = ? WHERE ID = ?;'
            c.execute(query,('Yes',uid))
            conn.commit()
     else:
            query = 'UPDATE USER_DATA SET PP = ? WHERE ID = ?;'
            c.execute(query,('No',uid))
            conn.commit()

     if choice[7] == '1':
            query = 'UPDATE USER_DATA SET PP2 = ? WHERE ID = ?;'
            c.execute(query,('Yes',uid))
            conn.commit()
     else:
            query = 'UPDATE USER_DATA SET PP2 = ? WHERE ID = ?;'
            c.execute(query,('No',uid))
            conn.commit()

     return choice


class PM:
 #PAYMENT MODULE
 def  pm(self,choice,email,uid):
    total = 0
    for i in range(8):
        if choice[i] == '1':
            total = total + FEES[i]
    query = 'UPDATE USER_DATA SET FEES = ? WHERE ID = ?;' 
    c.execute(query, (total,uid))
    conn.commit()
    
    print('Total Payment to be done is Rs.',total)
    print('\nPlease...Enter Credit Card Details to make your payment :')
    while(True):
     no = input('CARD NUMBER : ') 
     if (len(no) == 16) and no.isdigit() :
       break   
     else : print('\nPlease enter VALID CARD number of 16 digits')
    while(True):
     no = input('CVV : ') 
     if len(no) == 3 and no.isdigit() :
       break
     else : print('\nPlease enter VALID CVV number of 3 digits')
    obj = M()
    obj.m()
    print("")
    print('\nPLEASE WAIT... UNTIL YOUR TRANSACTION PROCEEDS')
    time.sleep(4)
    print("")
    print('\n-*-*-*-CONGRATULATIONS-*-*-*')
    print('\nPayment successfull')
    print('\nWithin few moments, you will be receiving your invoice copy by mail.')
    
    obj = ML()
    obj.ml(uid,0,0)
    
    print('\nThank You...We are super excited to see you at the conference')
    print('\nHope you find it a mesmerizing conference !!!!')
  
class RM:
 #REIMBURSEMENT MODULE
 def  rm(self,data):
    message = """
                            !!!! Reimbursement Mail !!!!

          Hello %s

          Amount of Rs.%s is being successfully credited to your account.

          Please feel free to drop a mail at : iiitd_conf@iiitd.ac.in
     
          All of your suggestions are highly anticipated for improvements.
   
          ..........................

          Best Wishes
          IIIT DELHI""" % (data[0],data[1])
    m = smtplib.SMTP('smtp.gmail.com',587)
    m.ehlo()
    m.starttls()
    send, passw = "oopdproject1@gmail.com", "oopdproject@123"
    m.login(send, passw)
    recv = data[2]     
    m.sendmail(send,recv,message)
    m.close()     

class TF(M,ML):
 #TOTAL_FEES MODULE FOR EXISTING USER   
 def  tf(self,choice,data,uid):
    total = 0
    for i in range(8):
        if choice[i] == '1':
            total = total + FEES[i]       
    query = 'UPDATE USER_DATA SET FEES = ? WHERE ID = ?;' 
    c.execute(query, (total,uid))
    conn.commit() 
   
    if total > data[0]:
        total = total - data[0] 
        print('According to changes made by you in events.\n')
        print('Extra Payment of Rs.',total,' needs to be done \n')
        print('\nPlease...Enter Credit Card Details to make your payment :')
        while(True):
          no = input('CARD NUMBER : ') 
          if (len(no) == 16) and no.isdigit() :
           break   
          else : print('\nPlease enter VALID CARD number of 16 digits')
        while(True):
          no = input('CVV : ') 
          if len(no) == 3 and no.isdigit() :
           break
          else : print('\nPlease enter VALID CVV number of 3 digits')
        M.m(self)
        print("")
        print('\nPLEASE WAIT... UNTIL YOUR TRANSACTION PROCEEDS')
        time.sleep(4)
        print("")
        print('\n-*-*-*-CONGRATULATIONS-*-*-*')
        print('\nPayment successfull')
        print('\nWithin few moments, you will be receiving your invoice copy by mail.')
    
        ML.ml(self,uid, total, 1)
    
        print('\nThank You...We are super excited to see you at the conference')
        print('\nHope you find it a mesmerizing conference !!!!\n')

    elif total < data[0]: 
        total = -1*(total - data[0]) 
        print('According to changes made by you in events.\n')
        print('Amount of Rs.',total,' will be reimbursed to your account.\n')
        print('Within few moments, you will receive confirmation mail about reimbursement \n \n')  
        message = """
                            !!!! Reimbursement Mail !!!!

          Hello %s

          Amount of Rs.%s is being successfully credited to your account.

          We hope this conference helps you to explored different aspects of your interest.
   
          ..........................

          Best Wishes
          IIIT DELHI""" % (data[1],total)
        m = smtplib.SMTP('smtp.gmail.com',587)
        m.ehlo()
        m.starttls()
        send, passw = "oopdproject1@gmail.com", "oopdproject@123"
        m.login(send, passw)
        recv = data[2]     
        m.sendmail(send,recv,message)
        m.close() 

    else:
        print('According to changes made by you in events.\n')         
        print('You need not pay any extra amount !!!')
        print('Thank You !!!')
        print('Best Wishes')
        print('IIIT DELHI')  

class NU(M,PWD,PM):
 #NEW_USER REGISTRATION MODULE
 def  nu(self):
    uid = str(uuid.uuid1())[:8]
    print("")
    print('              ******* Please enter your details for registration*******\n')
    name = input('NAME : ')
    mob = M.m(self)
    email = input('\nEMAIL ID : ')
    passw = PWD.pwd(self)    
    query = 'insert into USER_DATA(ID,NAME,MOBILE,EMAIL,PASSWORD) values(?,?,?,?,?);'
    c.execute(query, (uid,name,mob,email,passw))
    conn.commit()
    
    print("")
    print('                        -*-*-*-CONGRATULATIONS-*-*-*')
    print('           !!! YOU HAVE SUCCESSFULLY COMPLETED YOUR REGISTRATION :) !!!\n')
    print('Please...Note down your USER-ID for future purpose !!!\n')
    print('Your USER-ID is : \n')
    print(uid)

    print('\n \n !!! Please select the event(s) accordingly you wish to attend !!!\n') 
    obj = ES()
    choice = obj.es(uid)
    PM.pm(self,choice, email, uid)
        
class EU(RM,NU,EC,TF):
 #EXISTING_USER MODULE
 def  eu(self):
    uid = input('\nPlease enter your USER-ID : \n')
    pwd = input('\nPlease enter your PASSWORD : \n')
    query = 'SELECT EXISTS(SELECT 1 FROM USER_DATA WHERE ID=? and PASSWORD=?);'
    c.execute(query, (uid,pwd))    
    conn.commit()
    d = list(c.fetchone())[0]
    if(d):
        query = 'SELECT NAME FROM USER_DATA WHERE ID=?'
        c.execute(query, (uid,))    
        conn.commit()
        d = c.fetchone()
        print('\n') 
        print("Welcome %s" %(d))
    else:
        print("Error, User Id or Password is Incorrect !!!!")
        print("Please...Try Again...")
        self.eu()

    print("\nYou have selected the following events in conference : \n")
    c.execute("SELECT WS,WS2,TUT,TUT2,PD,PD2,PP,PP2 FROM USER_DATA WHERE ID=?", (uid,))
    conn.commit()
    d =  list(sum(c.fetchmany(), ()))
    enc = {0:'WORKSHOP 1',1:'WORKSHOP 2',2:'TUTORIAL',3:'TUTORIAL 2',4:'PANEL DISCUSSION',5:'PANEL DISCUSSION 2',6:'PAPER PRESENTATION',7:'PAPER PRESENTATION 2'}
     
    for i in range(8):
         if d[i] == 'Yes' :
           print(enc[i])

    print("\n")
    print("       If you want to CANCEL your Registration, Please press 1 ...\n")
    print("       If you want to CHANGE your Events, Please press 0 ...\n")
    k = int(input())
    if k==1 :
        query = 'SELECT NAME, FEES, EMAIL FROM USER_DATA WHERE ID=?;'
        c.execute(query, (uid,))
        conn.commit()
        data =  list(sum(c.fetchmany(), ()))
 
        query = 'DELETE FROM USER_DATA WHERE ID = ?;' 
        c.execute(query, (uid,))
        conn.commit()
        print("         Your Registration is successfully cancelled...\n")
        print('Reimbursement process has been started.\n')
        print('Within few moments, you will receive confirmation mail about reimbursement \n \n \n')  
        RM.rm(self,data)
        print('Would you like to again register for the conference if there is change in your thought for moment\n')
        th = int(input('If you are willing to attend, Please press 1 \n Otherwise you may simply press 0...\n Decision is yours !!!'))
        if th:
           NU.nu(self)
        else : print('              Thank You !!! \n            Best Wishes from IIITD !!!')         
 
    else:
        query = 'select FEES,NAME,EMAIL from USER_DATA where ID = ?;'
        c.execute(query, (uid,))
        conn.commit()
        data =  list(sum(c.fetchmany(), ())) 
        choice = EC.ec(self,uid)
        TF.tf(self,choice, data, uid)
        
        
 
class MAIN(EI,OI,EU):
 def __init__(self):
  d = str(datetime.date.today())
  if d <= date:
    #BEGINNING OF REGISTRATION   
    print("")
    print('           -*-*-*-*-*-*-WELCOME TO CONFERENCE REGISTRATION SYSTEM-*-*-*-*-*-*-\n')
    print('\nPlease Check the following event details and organizers details...\n')
    EI.ei(self)
    OI.oi(self)
    print('\n \nIf you are a NEW USER, please press 1\n')
    print('If you are a EXSITING USER, please press 0\n')
    i = int(input())
    if i == 1:
        NU.nu(self)
    else:
        EU.eu(self)
  else:
    print('Sorry !!! The Registration has closed.') 
    

obj = MAIN()
