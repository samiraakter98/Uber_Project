from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db import connection


# Create your views here.
def list_accidents(request):
    # cursor = connection.cursor()
    # sql = "INSERT INTO JOBS VALUES(%s,%s,%s,%s)"
    # cursor.execute(sql,['NEW_JOB','Something New',4000,8000])
    # connection.commit()
    # cursor.close()

    cursor = connection.cursor()
    sql = "SELECT * FROM UBERPROJECT.ACCIDENT"
    cursor.execute(sql)
    result = cursor.fetchall()

    # cursor = connection.cursor()
    # sql = "SELECT * FROM JOBS WHERE MIN_SALARY=%s"
    # cursor.execute(sql,[4000])
    # result = cursor.fetchall()

    cursor.close()
    dict_result = []

    for r in result:
        REPORT_ID = r[0]
        TRANS_ID = r[1]
        DRIVER_ID = r[2]
        OCCUR_TIME = r[3]
        row = {'REPORT_ID': REPORT_ID, 'TRANS_ID': TRANS_ID, 'DRIVER_ID': DRIVER_ID, 'OCCUR_TIME': OCCUR_TIME}
        dict_result.append(row)

    # return render(request,'list_jobs.html',{'jobs' : Job.objects.all()})
    return render(request, 'list_accident.html', {'ACCIDENT': dict_result})