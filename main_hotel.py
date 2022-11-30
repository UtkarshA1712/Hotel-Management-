import mysql.connector
mycon=mysql.connector.connect(host='localhost', user='root', passwd='ansh')
mycursor=mycon.cursor(buffered=True)
mycursor.execute('CREATE DATABASE IF NOT EXISTS hotel')

mycon=mysql.connector.connect(host='localhost', user='root', passwd='ansh', database='hotel')
mycursor=mycon.cursor(buffered=True)

#all the tables
mycursor.execute("CREATE TABLE IF NOT EXISTS client(Name varchar(50) NOT NULL, Phone_no varchar(11) PRIMARY KEY NOT NULL, Days int, People int, Rooms int)")
mycursor.execute("CREATE TABLE IF NOT EXISTS rooms(Total_rooms int NOT NULL DEFAULT 200, Occupied_rooms int DEFAULT 0, Vacant_rooms int DEFAULT 200, Rooms_underService int DEFAULT 0)")
mycursor.execute('CREATE TABLE IF NOT EXISTS updated_rooms(Vacant_rooms int, Occupied_rooms int)')
mycursor.execute("CREATE TABLE IF NOT EXISTS amount(Phone_no varchar(11) references client(Phone_no), Total_amount int)")
mycursor.execute("CREATE TABLE IF NOT EXISTS tour_amount(cabs int, hours int, amount int)")
mycursor.execute('CREATE TABLE IF NOT EXISTS restaurant_amount(Phone_no varchar(11) PRIMARY KEY, Quantity int, Amount_Payable int)')
mycursor.execute('CREATE TABLE IF NOT EXISTS gaming(Phone_no varchar(11) PRIMARY KEY, Hours int, Amount int)')
mycursor.execute('CREATE TABLE IF NOT EXISTS laundary(Phone_no varchar(11) PRIMARY KEY, Quantity int, Amount int)')

#title
welcome_variable='*****WELCOME TO STAR HOTEL*****'
print('\n\n',welcome_variable.center(100),'\n')

#menu
print()
chkin='1. Check IN'
stour='2. Go on a TOUR'
crestaurantbill='3. Calculate Restaurant Bill'
cgamingbill='4. Calculate Gaming Rent'
customerd='5. Customer Details'
laund='6. Laundry'
chkout='7. Check OUT'
print(chkin.center(20), end='\t')
print(stour.center(20), end='\t')
print(crestaurantbill.center(20), end='\t')
print(cgamingbill.center(20), end='\t')
print('\n',laund.center(30), end='\t')
print(customerd.center(20), end='\t')
print(chkout.center(20), end='\t')
print()
print()

choice=int(input('Please Enter Your Choice: '))

#check in features
if choice==1:
        import datetime
        name=input('\tEnter your name: ')
        number=input('\tEnter your phone number: ')
        days_0=int(input('\tEnter the number of days to stay: '))
        people=int(input('\tEnter the number of people: '))
        room=int(input('\tEnter the number of rooms needed: '))
        chkindate=datetime.date.today()
        print('\tCheck-IN Date:',chkindate)
        chkoutdate=datetime.date.today()+datetime.timedelta(days=days_0)
        print('\tCheck-OUT Date:',chkoutdate)
        mycursor.execute('INSERT INTO client VALUES(%s,%s,%s,%s,%s)',(name,number,days_0,people,room))
        rooms_vac=200-room
        rooms_occ=room
        mycursor.execute('INSERT INTO rooms VALUES(%s,%s,%s,%s)',(200,rooms_occ,rooms_vac,0))
        mycon.commit()
        
        mycursor.execute('SELECT Occupied_rooms FROM rooms')
        up_rooms_occ=mycursor.fetchall()
        update_rooms=0
        for item in range (0,len(up_rooms_occ)):
                update_rooms+=up_rooms_occ[item][0]
        mycursor.execute("SELECT Vacant_rooms FROM rooms")
        up_rooms_vac=mycursor.fetchall()
        up_rooms_2=0
        for item in range(0, len(up_rooms_vac)):
                up_rooms_1=200-up_rooms_vac[item][0]
                up_rooms_2+=up_rooms_1
        up_rooms_vac_1=200-up_rooms_2
        mycursor.execute('INSERT INTO updated_rooms VALUES(%s,%s)',(up_rooms_vac_1, update_rooms))
        
        mycursor.execute('INSERT INTO amount VALUES(%s,%s)',(number,((5000*room)*days_0)))
        mycon.commit()
        tour=input('\tShould a guided tour be included in the package (Yes/No): ')
        if tour=='Yes' or tour=='yes':
                tour_1='UPDATE amount SET Total_amount=Total_amount+5000 WHERE Phone_no='+number
                mycursor.execute(tour_1)
                mycon.commit()
            
        member=input('\tDo you wish to become a MEMBER to avail 30% DISCOUNT (Yes/No/Already): ')
        if member=='Yes' or member=='yes' or member=='Already' or member=='already':
                amount_1='SELECT Total_amount FROM amount WHERE Phone_no='+number
                mycursor.execute(amount_1)
                member_amount=mycursor.fetchone()
                after_member_amount=(member_amount[0]*30)/100
                member_amt='UPDATE amount SET Total_amount='+str(after_member_amount)+'WHERE Phone_no='+number
                mycursor.execute(member_amt)
                mycon.commit()
                mycursor.execute('SELECT Total_amount FROM amount')
                final_amount=mycursor.fetchone()
                print('\t\tTHE FINAL AMOUNT IS :', final_amount[0])
        else:
                amount_1='SELECT Total_amount FROM amount WHERE Phone_no='+number
                mycursor.execute(amount_1)
                final_amount=mycursor.fetchone()
                print('\n\t\tTHE FINAL AMOUNT IS:', final_amount[0])

#tour
elif choice==2:
        cabst=int(input('\nEnter the no of cabs you want: '))
        hourst=int(input('\nFor how many hours do you wanna use our service: '))
        amountt=(cabst*2000)+(hourst*200)
        
        mycursor.execute('INSERT INTO tour_amount VALUES(%s,%s,%s)',(cabst,hourst,amountt))
        mycon.commit()
        update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amountt)
        mycursor.execute(update_amount)
        mycon.commit()
        
        print()
        print("The total amount payable for: ", end='\n')
        
        mycursor.execute('SELECT amount FROM tour_amount')
        amount_for_tour=mycursor.fetchone()
        
        cabs_variable="Cabs: "
        print('\n\t',cabs_variable)
        print('\t',cabst,'X 2000 =', amountt-(hourst*200))
        hours_variable="Hours: "
        print('\n\t',hours_variable)
        print('\t',hourst,'X 200 =', amountt-((cabst*2000)))
        total_variable="Total: "
        print('\n\t',total_variable)
        total_tour=mycursor.fetchone()
        print('\t',total_tour[0])

#restaurant bill
elif choice==3:
        veg_comb='1. Vegetarian Combo\t\tRs. 3000'
        nonveg_comb='2. Non-Vegetarian Combo\t\tRs. 5000'
        both='3. Vegetarian and Non-Vegetarian Combo\t\tRs. 8000'
        chinese='4. Chinese PLatter\t\tRs. 4500'
        italian='5. Italian Platter\t\tRs. 6000'
        print(veg_comb.center(20))
        print(nonveg_comb.center(20))
        print(both.center(20))
        print(chinese.center(20))
        print(italian.center(20))

        number=int(input('Enter your Phone Number: '))
        choice_1=int(input('\tEnter your choice: '))
        
        if choice_1==1:
                quantity=int(input('\tEnter quantity of food needed: '))
                amount=quantity*3000
                mycursor.execute('INSERT INTO restaurant_amount values(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        elif choice_1==2:
                quantity=(input('\tEnter quantity of food needed: '))
                amount=quantity*5000
                mycursor.execute('INSERT INTO restaurant_amount values(%s,%s,%s)',(room_id,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        elif choice_1==3:
                quantity=(input('\tEnter quantity of food needed: '))
                amount=quantity*8000
                mycursor.execute('INSERT INTO restaurant_amount values(%s,%s,%s)',(room_id,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        elif choice_1==4:
                quantity=(input('\tEnter quantity of food needed: '))
                amount=quantity*4500
                mycursor.execute('INSERT INTO restaurant_amount values(%s,%s,%s)',(room_id,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        elif choice_1==5:
                quantity=(input('\tEnter quantity of food needed: '))
                amount=quantity*6000
                mycursor.execute('INSERT INTO restaurant_amount values(%s,%s,%s)',(room_id,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()

#gaming bill
elif choice==4:
        tt='\t1. Tabble Tennis\t\tRs 1000'
        bowl='\t2. Bowling Alley\t\tRs 1000'
        snook='\t3. Snooker\t\tRs 1000'
        pmpl='\t4. PUBG MOBILE Premier League\t\tRs 1000'
        video='\t5. Video Games\t\tRs 1000'
        swimming='\t6. Swimming Pool\t\tRs 1000'
        lawn='\t7. Lawn Tennis\t\tRs 1000'
        golf='\t8. Golf Course\t\tRs 1000'
        
        number=int(input('Enter your Phone Number: '))
        choice_2=int(input('\tEnter your choice: '))
        
        if choice_2==1:
                hours_gaming=int(input('Enter the number of hours: '))
                amount_gaming=hours_gaming*1000
                mycursor.execute('INSERT INTO gaming VALUES(%s,%s,%s)',(number,hours_gaming,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount_gaming)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_2==2:
                hours_gaming=int(input('Enter the number of hours: '))
                amount_gaming=hours_gaming*1000
                mycursor.execute('INSERT INTO gaming VALUES(%s,%s,%s)',(room_id,hours_gaming,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount_gaming)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_2==3:
                hours_gaming=int(input('Enter the number of hours: '))
                amount_gaming=hours_gaming*1000
                mycursor.execute('INSERT INTO gaming VALUES(%s,%s,%s)',(room_id,hours_gaming,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount_gaming)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_2==4:
                hours_gaming=int(input('Enter the number of hours: '))
                amount_gaming=hours_gaming*1000
                mycursor.execute('INSERT INTO gaming VALUES(%s,%s,%s)',(room_id,hours_gaming,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount_gaming)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_2==5:
                hours_gaming=int(input('Enter the number of hours: '))
                amount_gaming=hours_gaming*1000
                mycursor.execute('INSERT INTO gaming VALUES(%s,%s,%s)',(room_id,hours_gaming,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount_gaming)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_2==6:
                hours_gaming=int(input('Enter the number of hours: '))
                amount_gaming=hours_gaming*1000
                mycursor.execute('INSERT INTO gaming VALUES(%s,%s,%s)',(room_id,hours_gaming,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount_gaming)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_2==7:
                hours_gaming=int(input('Enter the number of hours: '))
                amount_gaming=hours_gaming*1000
                mycursor.execute('INSERT INTO gaming VALUES(%s,%s,%s)',(room_id,hours_gaming,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount_gaming)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_2==8:
                hours_gaming=int(input('Enter the number of hours: '))
                amount_gaming=hours_gaming*1000
                mycursor.execute('INSERT INTO gaming VALUES(%s,%s,%s)',(room_id,hours_gaming,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount_gaming)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()

#customer details
elif choice==5:
        phone_no=(input('Enter your PHONE NO: '))
        
        cust='SELECT * FROM client WHERE Phone_no='+phone_no
        mycursor.execute(cust)
        details=mycursor.fetchall()
        
        print('\t\t**##CUSTOMER DETAILS##**')
        print('\tCustomer Name:',details[0][0])
        print('\tNo. of Days of Stay:',details[0][1])
        print('\tNo. of People Staying:',details[0][2])
        print('\tNo. of Rooms Taken:',details[0][3])

#laundary details
elif choice==6:
        print('\t1. Shirts\t\tRs. 30')
        print('\t2. T-Shirts\t\tRs. 30')
        print('\t3. Pants\t\tRs. 30')
        print('\t4. Jeans\t\tRs. 30')
        print('\t5. Sarees\t\tRs. 30')
        print('\t6. Chudithar\t\tRs. 30')
        print('\t7. Frock\t\tRs. 30')
        print('\t8. Skirts\t\tRs. 30')
        print('\t9. Trousers\t\tRs. 30')
        print('\t10. Innerwear\t\tRs. 30')
        
        choice_3=int(input('Enter your choice: '))
        number=input('\tEnter your Phone Number: ')
        
        if choice_3==1:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_3==2:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_3==3:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_3==4:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_3==5:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_3==6:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_3==7:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_3==8:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_3==9:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
        if choice_3==10:
                quantity=int(input('\tEnter the quantity of clothes: '))
                amount=quantity*30
                mycursor.execute('INSERT INTO laundary VALUES(%s,%s,%s)',(number,quantity,amount))
                mycon.commit()
                update_amount='UPDATE TABLE amount set Total_amount=Total_amount+'+str(amount)+'WHERE Phone_no='+number
                mycursor.execute(update_amount)
                mycon.commit()
                
#check out features
elif choice==7:
        phone_number=input('Enter your Phone Number: ')
        
        phoneno='SELECT Total_amount FROM amount WHERE Phone_no='+phone_number
        mycursor.execute(phoneno)
        total_amount=mycursor.fetchone()
        
        print('\tTOTAL AMOUNT PAYABLE IS:', total_amount[0])
        ext='\n\nTHANK YOU FOR VISITING STAR HOTEL!!'
        print(ext.center(100))

        #deleting client data
        
        rooms_updating='SELECT Rooms FROM client WHERE Phone_no='+phone_number
        mycursor.execute(rooms_updating)
        mycon.commit()
        rooms_updating_1=mycursor.fetchone()
        rooms_updating_2=str(rooms_updating_1[0])
        rooms_updating_3='UPDATE rooms SET Vacant_rooms=Vacant_rooms+'+rooms_updating_2
        mycursor.execute(rooms_updating_3)
        mycon.commit()
        rooms_updating_4='UPDATE rooms SET Occupied_rooms=Occupied_rooms-'+str(rooms_updating_1[0])
        mycursor.execute(rooms_updating_4)
        mycon.commit()
        delete='DELETE FROM client WHERE Phone_no='+phone_number
        mycursor.execute(delete)
        mycon.commit()
