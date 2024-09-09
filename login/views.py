from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db import connection

import hashlib
from django.shortcuts import redirect
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection
import hashlib
import random
from datetime import timedelta
from datetime import datetime
# Create your views here.
def image_uploader(request):
    if request.method=="POST":
        file = request.FILES['file']
        image_handle(file)
    return render(request,'image_upload.html')

def image_handle(f):
    with open('static/images/driver_image/'+f.name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def make_starttime():
    min = random.randint(20,100)
    end_time = datetime.now()
    end_time = str(end_time)
    end_time, nano_sec =end_time.split('.')
    print(end_time)
    return end_time
def make_endtime():
    min = random.randint(20,100)
    end_time = datetime.now() + timedelta(minutes=min)
    end_time=str(end_time)
    end_time,nano_sec =end_time.split('.')
    print(end_time)
    return end_time

def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password,hash):
    if make_pw_hash(password) == hash :
        return True
    return False

def login(request):
    # p="123456"
    # cursor = connection.cursor()
    # sql = "UPDATE UBERPROJECT.PERSON SET PASSWORD=%s WHERE PASSWORD=%s"
    # cursor.execute(sql, [make_pw_hash(p),p])
    # connection.commit()
    # cursor.close()
    # cursor = connection.cursor()
    # sql = "SELECT PASSWORD FROM UBERPROJECT.PERSON"
    # cursor.execute(sql)
    # result = cursor.fetchall()
    # cursor.close()
    # cursor = connection.cursor()
    # for x in range(2,18):
    #    sql = "SELECT PASSWORD FROM UBERPROJECT.PERSON  WHERE PERSON_ID=%s"
    #    cursor.execute(sql, [x])
    #   result = cursor.fetchall()
    #   sql = "UPDATE UBERPROJECT.PERSON SET PASSWORD=%s WHERE PASSWORD=%s"
    #  cursor.execute(sql, [make_pw_hash(result[0][0]),result[0][0]])
    #  connection.commit()
    #  print(result[0][0])
    # cursor.close()
    # print(result[16][0])
    return render(request, 'login.html')

def login1(request):
    if request.method == "POST":
        mail = request.POST["email"]
        phone = request.POST["phoneno"]
        password = request.POST["pass"]
        print(mail + password + phone)
        cursor = connection.cursor()
        sql = "SELECT PASSWORD FROM PERSON WHERE EMAIL=%s"
        cursor.execute(sql, [mail])
        result = cursor.fetchall()
        cursor.close()
        msg = "You dont have an account. Please signup first."
        msg1 = "Wrong Password"
        if result:
            if check_hash(password, result[0][0]):
            ##if(password == '12345'):
                print("yes")
                cursor = connection.cursor()
                sql = "SELECT PERSON_ID FROM PERSON WHERE EMAIL=%s;"
                cursor.execute(sql, [mail])
                res = cursor.fetchall()
                cursor.close()
                logged_in_user = res[0][0]
                request.session["logged_in_user"] = logged_in_user
                print(res[0][0])
                return redirect('/user_login')
            else:
                print("no")
                return render(request, 'login1.html', {"status": msg1})
        else:
            print("nothing")
            return render(request, 'login.html', {"status": msg})
    return render(request, 'login1.html')

def signup(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        gender = request.POST["gender"]
        mail = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        city = request.POST["city"]
        # state=request.POST["state"]
        zip = request.POST["zip"]
        pas = request.POST["pass"]
        cpas = request.POST["cpass"]
        rating = str('0')
        no_of_p_rated = str('0')
        if pas != cpas:
            msg = "password and confirm password doesnot match"
            return render(request, 'signup.html', {"status": msg})
        cursor = connection.cursor()
        sql = "SELECT EMAIL FROM PERSON WHERE EMAIL LIKE %s"
        cursor.execute(sql, [mail])
        result = cursor.fetchall()
        if result:
            msg = "This EMAIL id is already registered"
            return render(request, 'signup.html', {"status": msg})
        else:
            sql = "SELECT MAX(TO_NUMBER(PERSON_ID)) FROM PERSON"
            cursor.execute(sql)
            result = cursor.fetchall()
            person_id = result[0][0] + 1
            sql = "INSERT INTO PERSON (PERSON_ID,FIRST_NAME,LAST_NAME,ZIP_CODE,CITY,PASSWORD,GENDER,EMAIL,DATE_OF_BIRTH,RATING,NO_OF_PERSON_RATED) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,TO_DATE(%s, 'DD MON,YYYY'),%s,%s)"
            cursor.execute(sql,
                           [result[0][0] + 1, fname, lname, zip, city, make_pw_hash(pas), gender, mail, dob, rating,
                            no_of_p_rated])
            connection.commit()
            sql = "INSERT INTO PERSON_NUMBER VALUES (%s,%s);"
            cursor.execute(sql, [person_id, phone])
            connection.commit()
            sql = "INSERT INTO UBER_USER (UBER_USER_ID,HOME_LOCATION) VALUES (%s,%s);"
            cursor.execute(sql, [person_id, city])
            connection.commit()
            cursor.close()
            return redirect('/login')
    return render(request, 'signup.html')
def signup_driver(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        gender = request.POST["gender"]
        mail = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        city = request.POST["city"]
        zip = request.POST["zip"]
        driver_li = request.POST["driver_li"]
        nid = request.POST["nid"]
        trans_type = request.POST["trans_type"]
        brand = request.POST["brand"]
        model = request.POST["model"]
        trans_li = request.POST["trans_li"]
        pas = request.POST["pass"]
        cpas = request.POST["cpass"]
        rating = str('0')
        no_of_p_rated = str('0')
        file = request.FILES['file']
        file_name = str(file.name)
        file_name = 'static/images/driver_image/' + file_name
        print(file_name)
        if pas != cpas:
            msg = "password and confirm password doesnot match"
            return render(request, 'signup.html', {"status": msg})
        cursor = connection.cursor()
        sql = "SELECT EMAIL FROM PERSON WHERE EMAIL LIKE %s"
        cursor.execute(sql, [mail])
        result = cursor.fetchall()
        if result:
            msg = "This EMAIL id is already registered"
            return render(request, 'signup.html', {"status": msg})
        else:
            image_handle(file)
            sql = "SELECT MAX(TO_NUMBER(PERSON_ID)) FROM PERSON"
            cursor.execute(sql)
            result = cursor.fetchall()
            person_id = result[0][0] + 1
            sql = "INSERT INTO PERSON (PERSON_ID,FIRST_NAME,LAST_NAME,ZIP_CODE,CITY,PASSWORD,GENDER,EMAIL,DATE_OF_BIRTH,RATING,NO_OF_PERSON_RATED) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,TO_DATE(%s, 'DD MON,YYYY'),%s,%s)"
            cursor.execute(sql,
                           [result[0][0] + 1, fname, lname, zip, city, make_pw_hash(pas), gender, mail, dob, rating,
                            no_of_p_rated])
            connection.commit()
            sql = "INSERT INTO PERSON_NUMBER VALUES (%s,%s);"
            cursor.execute(sql, [person_id, phone])
            connection.commit()
            sql = "INSERT INTO DRIVER VALUES (%s,%s,%s,%s);"
            cursor.execute(sql, [person_id, file_name, nid, driver_li])
            connection.commit()
            sql = "SELECT MAX(TO_NUMBER(TRANS_ID)) FROM TRANSPORT"
            cursor.execute(sql)
            result = cursor.fetchall()
            trans_id = result[0][0] + 1
            sql = "INSERT INTO TRANSPORT VALUES (%s,%s,%s,%s,%s,%s);"
            cursor.execute(sql, [trans_id, person_id, brand, model, trans_li, trans_type])
            connection.commit()
            cursor.close()
            return redirect('/login')
    return render(request, 'signup_driver.html')
def user_login(request):
    if request.method == "POST":
        get_from = request.POST['from']
        get_where = request.POST['where']
        print(get_from)
        print(get_where)
        request.session["start_location"] = get_from
        request.session["end_location"] = get_where
    return render(request, 'user_login.html')
def user_driver_map(request):

    return render(request, 'user_driver_map.html')
def payment_bkash(request):
    return render(request, 'payment_bkash.html')
def payment_rocket(request):
    return render(request, 'payment_rocket.html')
def payment_nexus(request):
    return render(request, 'payment_nexus.html')
def payment_cash(request):
    return render(request, 'payment_cash.html')
def payment(request):
    logged_in_user = request.session.get('logged_in_user')
    cost = request.GET.get('taka')
    print(cost)
    request.session["expected_fare"] = cost
    rate = request.GET.get('rate')
    print(rate)
    cursor = connection.cursor()
    cursor.callproc('SET_PROMO_STATUS', [logged_in_user])
    sql = "SELECT MAX(TO_NUMBER(PAYMENT_ID)) FROM PAYMENT"
    cursor.execute(sql)
    newPayment_id = cursor.fetchall()
    cursor.close()
    id = str(newPayment_id[0][0] + 1)

    cursor = connection.cursor()
    sql = "INSERT INTO PAYMENT (PAYMENT_ID,NET_AMOUNT,PAYMENT_RATE) VALUES(%s,%s,%s)"
    cursor.execute(sql, [id, cost, rate])
    cursor.callproc('SET_PAYMENT', [logged_in_user, id])
    cursor.close()

    cursor = connection.cursor()
    sql = "SELECT NET_AMOUNT FROM PAYMENT WHERE PAYMENT_ID=" + id
    cursor.execute(sql)
    taka = cursor.fetchall()
    cursor.close()

    money = {'value': taka[0][0],
             }
    print(taka)
    print("samiraaaaaaaaaa")
    return JsonResponse({'net_amount_after_promo': taka[0][0]})

def confirmation(request):
    logged_in_user = request.session.get('logged_in_user')
    print(logged_in_user)

    cursor = connection.cursor()
    sql = "SELECT DRIVER_ID FROM DRIVER";

    cursor.execute(sql)
    r_id = cursor.fetchall()
    ids = []
    print(len(r_id))
    for i in range(0,len(r_id)):
        ids.append(int(r_id[i][0]))
    print(ids)

    ab = random.choice(ids)
    ab = int(ab);
    print(ab)
    driver_id = ab
    id = str(driver_id)
    request.session["driver_id"] = id
    cursor.close()

    cursor = connection.cursor()
    sql = "SELECT MAX(TO_NUMBER(REQUEST_ID)) FROM REQUEST;"
    cursor.execute(sql)
    r_id = cursor.fetchall()
    request_id = r_id[0][0] + 1
    sql = "SELECT TRANS_ID FROM TRANSPORT WHERE DRIVER_ID =" + id + ";"
    cursor.execute(sql)
    t_id = cursor.fetchall()
    trans_id = t_id[0][0]
    sql = "INSERT INTO REQUEST  VALUES(%s,%s,%s,%s)"
    cursor.execute(sql, [request_id, trans_id, id, logged_in_user])
    connection.commit()
    age = cursor.callfunc('AGE', int, [id])
    sql = "SELECT (P.FIRST_NAME || ' ' || P.LAST_NAME), PN.PHONE_NO, D.IMAGE,T.BRAND,T.MODEL,T.TRANS_LICENSE FROM PERSON P JOIN PERSON_NUMBER PN ON (P.PERSON_ID = PN.PERSON_ID) JOIN DRIVER D ON (P.PERSON_ID = D.DRIVER_ID) JOIN TRANSPORT T ON (T.DRIVER_ID = D.DRIVER_ID) WHERE P.PERSON_ID =" + id + " ;"
    cursor.execute(sql)
    result = cursor.fetchall()
    sql = "SELECT FIRST_NAME FROM PERSON WHERE PERSON_ID =" + logged_in_user + ";"
    cursor.execute(sql)
    user = cursor.fetchall()
    print(user[0][0])
    cursor.close()
    row = {'person_name': result[0][0],
           'number': result[0][1],
           'image': result[0][2],
           'brand': result[0][3],
           'model': result[0][4],
           'trans_license': result[0][5],
           'user_name': user[0][0],
           'AGE': age,
           }
    driver_info = []
    driver_info.append(row)
    print(result)

    cursor = connection.cursor();
    check = cursor.callfunc('CHECK_PROMO', int, [logged_in_user]);
    cursor.close()
    return render(request, 'confirmation_page.html', {'info': driver_info, 'check': check})

def accident(request):
    driver_id = 14
    id = str(driver_id)
    id = request.session.get('driver_id')
    # id=str(20)
    cursor = connection.cursor()
    ##driver_id = numpy.random.random_integers(13, 18) Hard code for now##
    sql = "SELECT COUNT(*) FROM ACCIDENT WHERE DRIVER_ID=" + id + ";"
    cursor.execute(sql)
    accident_by_driver = cursor.fetchall()
    print(accident_by_driver[0][0])
    information100 = []
    time100 = []
    if (accident_by_driver[0][0] != 0):
        sql = "SELECT T.BRAND, T.MODEL, T.TRANS_TYPE,T.TRANS_LICENSE, TO_DATE(A.OCCUR_TIME, 'YYYY-MM-DD hh24:mi:ss') FROM ACCIDENT A LEFT JOIN TRANSPORT T ON (A.TRANS_ID = T.TRANS_ID) WHERE A.TRANS_ID=(SELECT TRANS_ID FROM TRANSPORT WHERE DRIVER_ID=%s);"
        cursor.execute(sql, [id])
        driver_info100 = cursor.fetchall()
        row1 = {'brand': driver_info100[0][0],
                'model': driver_info100[0][1],
                'type': driver_info100[0][2],
                'trans_license': driver_info100[0][3],
                }
        information100.append(row1)
    for x in range(accident_by_driver[0][0]):
        t = driver_info100[x][4]
        print(t)
        t.strftime('%m/%d/%Y')
        print(t)
        tx = (t,)
        time100.append(tx)
    # sql = "SELECT T.BRAND, T.MODEL, T.TRANS_TYPE,T.TRANS_LICENSE FROM  DRIVER D JOIN TRANSPORT T ON D.DRIVER_ID = T.DRIVER_ID WHERE D.DRIVER_ID = " + id + ";"
    ##sql = "SELECT D.IMAGE, D.DRIVING_LICENSE FROM UBERPROJECT.DRIVER D WHERE D.DRIVER_ID = "+id+";"
    # cursor.execute(sql)
    # driver_info = cursor.fetchall()
    # sql = "SELECT A.OCCUR_TIME FROM ACCIDENT A JOIN DRIVER D ON D.DRIVER_ID=A.DRIVER_ID WHERE D.DRIVER_ID="+ id + ";"
    # cursor.execute(sql)
    # time = cursor.fetchall()
    # print(len(time))
    # row = { 'brand': driver_info[0][0],
    #   'model': driver_info[0][1],
    #    'type': driver_info[0][2],
    #     'trans_license': driver_info[0][3],
    #      }
    # information = []
    # information.append(row)
    # print(information)
    # print(time[0][0])
    print(information100)
    # print(information)
    print(time100)
    # print(time)
    return render(request, 'accident.html', {'info': information100, 'time': time100})
def trans_accident(request):
    driver_id = 14
    id = str(driver_id)
    id = request.session.get('driver_id')
    # id=str(20)
    cursor = connection.cursor()
    sql = "SELECT COUNT(*) FROM ACCIDENT WHERE TRANS_ID = (SELECT TRANS_ID FROM TRANSPORT WHERE DRIVER_ID = " + id + ");"
    cursor.execute(sql)
    accident_by_transport = cursor.fetchall()
    print(accident_by_transport[0][0])
    information100 = []
    if accident_by_transport[0][0] != 0:
        sql = "SELECT D.DRIVING_LICENSE, P.FIRST_NAME, P.LAST_NAME,PN.PHONE_NO,A.OCCUR_TIME FROM ACCIDENT A JOIN DRIVER D ON (A.DRIVER_ID = D.DRIVER_ID) JOIN PERSON P ON (P.PERSON_ID = D.DRIVER_ID) JOIN PERSON_NUMBER PN ON (D.DRIVER_ID = PN.PERSON_ID) WHERE D.DRIVER_ID = " + id + ";"
        cursor.execute(sql)
        driver_info100 = cursor.fetchall()
        print(driver_info100)
        row1 = {'driving_license': driver_info100[0][0],
                'first_name': driver_info100[0][1],
                'last_name': driver_info100[0][2],
                'phone': driver_info100[0][3],
                }
        information100.append(row1)
    time100 = []
    for x in range(accident_by_transport[0][0]):
        t = driver_info100[x][4]
        print(t)
        t.strftime('%m/%d/%Y')
        print(t)
        tx = (t,)
        time100.append(tx)
    ##driver_id = numpy.random.random_integers(13, 18) Hard code for now##
    # sql = "SELECT D.DRIVING_LICENSE, P.FIRST_NAME, P.LAST_NAME FROM PERSON P JOIN DRIVER D ON D.DRIVER_ID = P.PERSON_ID WHERE D.DRIVER_ID = " + id + ";"
    ##sql = "SELECT D.IMAGE, D.DRIVING_LICENSE FROM UBERPROJECT.DRIVER D WHERE D.DRIVER_ID = "+id+";"
    # cursor.execute(sql)
    # driver_info = cursor.fetchall()
    # sql = "SELECT PN.PHONE_NO FROM  DRIVER D JOIN PERSON_NUMBER PN ON D.DRIVER_ID = PN.PERSON_ID WHERE D.DRIVER_ID =" + id + ";"
    # cursor.execute(sql)
    # driver_info2 = cursor.fetchall()
    # sql = "SELECT A.OCCUR_TIME FROM ACCIDENT A JOIN DRIVER D ON D.DRIVER_ID=A.DRIVER_ID WHERE D.DRIVER_ID=" + id + ";"
    # cursor.execute(sql)
    # time = cursor.fetchall()
    # print(len(time))
    # row = {'driving_license': driver_info[0][0],
    #    'first_name': driver_info[0][1],
    #     'last_name': driver_info[0][2],
    #      'phone': driver_info2[0][0],
    #       }
    # information = []
    # information.append(row)
    # print(information)
    print(information100)
    # print(time)
    print(time100)
    # print(time[0][0])
    return render(request, 'trans_accident.html', {'info': information100, 'time': time100})
def accident_report(request):
    if request.method == "POST" :
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        phone = request.POST["phone"]
        date  = request.POST["date"]
        time  = request.POST["time"]
        sec = random.randint(1,59)
        sec=str(sec)
        time=time+':'+sec
        date= date+' '+time
        print(fname + ' ' +lname+ ' ' +phone+ ' ' +date+ ' ' +time)
        print(fname)
        cursor = connection.cursor()
        sql = "SELECT P.PERSON_ID FROM PERSON P JOIN PERSON_NUMBER PN ON(P.PERSON_ID = PN.PERSON_ID) WHERE P.FIRST_NAME =%s AND P.LAST_NAME =%s  AND PN.PHONE_NO =%s;"
        cursor.execute(sql,[fname,lname,phone])
        driver = cursor.fetchall()
        print(driver[0][0])
        driver_id=str(driver[0][0])
        sql = "SELECT MAX(TO_NUMBER(REPORT_ID)) FROM ACCIDENT"
        cursor.execute(sql)
        result = cursor.fetchall()
        sql = "SELECT TRANS_ID FROM TRANSPORT WHERE DRIVER_ID =" + driver_id + ";"
        cursor.execute(sql)
        trans_id = cursor.fetchall()
        print(result[0][0]+1)
        print(trans_id[0][0])
        print(date)
        sql = "INSERT INTO ACCIDENT  VALUES(%s,%s,%s,TO_DATE(%s, 'YYYY-MM-DD hh24:mi:ss'))"
        cursor.execute(sql, [result[0][0] + 1, trans_id[0][0], driver_id, date])
        connection.commit()
        cursor.close()
    return render(request,'accident_report.html')
def user_profile_trip(request) :
    id =request.session.get('logged_in_user')
    cursor = connection.cursor()
    sql = "SELECT COUNT(*) FROM TRIP WHERE USER_ID =" + id +";"
    cursor.execute(sql)
    no_of_trip = cursor.fetchall()
    sql = "SELECT T.START_TIME,T.END_TIME,T.START_LOCATION,T.END_LOCATION,P.NET_AMOUNT, PE.FIRST_NAME,PE.LAST_NAME,PN.PHONE_NO FROM TRIP T JOIN PAYMENT P ON (T.PAYMENT_ID = P.PAYMENT_ID) JOIN PERSON PE ON (T.DRIVER_ID = PE.PERSON_ID) JOIN PERSON_NUMBER PN ON (PE.PERSON_ID = PN.PERSON_ID) WHERE T.USER_ID =" + id +";"
    cursor.execute(sql)
    trip = cursor.fetchall()
    cursor.close()
    trip_number = no_of_trip[0][0]
    information=[]
    for x in range(trip_number):
        st = trip[x][0]
        et = trip[x][1]
        st.strftime('%m/%d/%Y')
        et.strftime('%m/%d/%Y')
        sl = trip[x][2]
        el = trip[x][3]
        fare = trip[x][4]
        dfn = trip[x][5]
        dln = trip[x][6]
        dpn = trip[x][7]
        row = {
            'start_location': sl,
            'end_location': el,
            'trip_fare': fare,
            'driver_first_name': dfn,
            'driver_last_name': dln,
            'driver_phone_no': dpn,
            'start_time': st,
            'end_time': et,
        }
        information.append(row)
    return render(request,'user_profile_trip.html',{'info':information})
def for_trip_info(request):
    start_time = request.GET.get('datetime')
    start_time = str(start_time)
    print(start_time)
    request.session["start_time"] = start_time
    request.session["trip_start_time"] = start_time
    print(request.session.get('trip_start_time'))
    print("i am in trip info")
    return redirect('/')
def rating(request):
    print("called")
    print(request.session.get('trip_start_time'))
    rating_value = int(request.GET.get('rating'))
    print(rating_value)
    start = request.session.get('start_location')
    end = request.session.get('end_location')
    s_time = request.session.get('trip_start_time')
    s_time = make_starttime()
    # del request.session['start_time']
    e_time = make_endtime()
    e_fare = request.session.get('expected_fare')
    print(start)
    print(end)
    print(s_time)
    print(e_time)
    print(e_fare)
    start_time = str(s_time)
    end_time = str(e_time)
    start_location = str(start)
    end_location = str(end)
    expected_fair = str(e_fare)
    print(start_time)
    print(end_time)
    # start_time='2020-12-4 21:12:13'
    cursor = connection.cursor()
    sql = "SELECT MAX(TO_NUMBER(TRIP_ID)) FROM TRIP;"
    cursor.execute(sql)
    trip = cursor.fetchall()
    trip_id = str(trip[0][0] + 1)
    sql = "SELECT MAX(TO_NUMBER(PAYMENT_ID)) FROM PAYMENT;"
    cursor.execute(sql)
    payment = cursor.fetchall()
    payment_id = str(payment[0][0])
    sql = "SELECT REQUEST_ID,DRIVER_ID,USER_ID FROM REQUEST WHERE REQUEST_ID = (SELECT MAX(TO_NUMBER(REQUEST_ID)) FROM REQUEST);"
    cursor.execute(sql)
    other_info = cursor.fetchall()
    request_id = str(other_info[0][0])
    driver_id = str(other_info[0][1])
    user_id = str(other_info[0][2])
    print(
        trip_id + ' ' + start_time + ' ' + end_time + ' ' + expected_fair + ' ' + start_location + ' ' + end_location + ' ' + driver_id + ' ' + user_id + ' ' + request_id + ' ' + payment_id)
    sql = "INSERT INTO TRIP VALUES (%s,TO_DATE(%s, 'YYYY-MM-DD hh24:mi:ss'),TO_DATE(%s, 'YYYY-MM-DD hh24:mi:ss'),%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(sql, [trip_id, start_time, end_time, expected_fair, start_location, end_location, driver_id, user_id,
                         request_id, payment_id])
    connection.commit()
    print("inserted in trip")
    new_rating = cursor.callfunc('CALCULATE_RATING', int, [driver_id, rating_value])
    print(new_rating)
    sql = "UPDATE PERSON SET RATING = %s WHERE PERSON_ID = %s;"
    cursor.execute(sql, [new_rating, driver_id])
    connection.commit()
    cursor.close()
    return redirect('/')
def payment_page(request):
    return render(request,'payment.html');

