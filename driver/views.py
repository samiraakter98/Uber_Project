from django.shortcuts import render
from django.shortcuts import render
from django.db import connection
import hashlib
from django.utils.autoreload import autoreload_started
import random
# Create your views here.
def driver_profile(request):
    cursor = connection.cursor()
    ##driver_id = numpy.random.random_integers(13, 18) Hard code for now##
    id = request.session.get('driver_id')
    age = cursor.callfunc('AGE', int, [id])
    sql = "SELECT D.IMAGE, D.DRIVING_LICENSE, P.FIRST_NAME, P.LAST_NAME, P.RATING, T.BRAND, T.MODEL, T.TRANS_TYPE,T.TRANS_LICENSE FROM PERSON P JOIN DRIVER D ON D.DRIVER_ID = P.PERSON_ID JOIN TRANSPORT T ON D.DRIVER_ID = T.DRIVER_ID WHERE D.DRIVER_ID = "+id+";"
    ##sql = "SELECT D.IMAGE, D.DRIVING_LICENSE FROM UBERPROJECT.DRIVER D WHERE D.DRIVER_ID = "+id+";"
    cursor.execute(sql)
    driver_info = cursor.fetchall()
    sql="SELECT PN.PHONE_NO, P.EMAIL FROM PERSON P JOIN DRIVER D ON D.DRIVER_ID = P.PERSON_ID JOIN PERSON_NUMBER PN ON D.DRIVER_ID = PN.PERSON_ID WHERE D.DRIVER_ID ="+id+";"
    cursor.execute(sql)
    driver_info2 = cursor.fetchall()
    row={'image':driver_info[0][0],
         'license':driver_info[0][1],
         'first_name':driver_info[0][2],
         'last_name' :driver_info[0][3],
         'rating':driver_info[0][4],
         'brand': driver_info[0][5],
         'model':driver_info[0][6],
         'type' :driver_info[0][7],
         'trans_license':driver_info[0][8],
         'phone':driver_info2[0][0],
         'email':driver_info2[0][1],
         'AGE': age,
         }
    driverInfo = []
    driverInfo.append(row)
    print(driverInfo)
    return render(request, 'driver_profile.html', {'driverInformation': driverInfo})

