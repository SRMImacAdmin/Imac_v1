import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from imac_main.scripts import timetest
from imac_main.scripts import emailmanager


def fbsignupwrite(uid, name, email, empid, dept, password):
    ref = db.reference('users')
    ref.child(uid).set({
        'name': name,
        'email': email,
        'empid': empid,
        'dept': dept,
        'type': 'Faculty',
        'password': password,
        'approved': False
    })
    ref = db.reference('unapproved_users')
    ref.child(uid).set({
        'name': name,
        'empid': empid,
        'dept': dept,
        'type': 'Account Pending',
        'email': email,
    })
    return uid

def fbloginread(uid):
    ref = db.reference('users')
    return ref.child(uid).get()

def fbbookingreq(uid, name, email, empid, dept, acc_type, title, booking_type, lab_no, sysid, date, time_from, time_till, stud_emails, details):
    ref = db.reference('unapproved_requests')
    s_nos = sysid.split(',')
    ref.child(uid).set({
        'name': name,
        'email': email,
        'empid': empid,
        'dept': dept,
        'acc_type': acc_type,
        'title': title,
        'booking_type': booking_type,
        'type': 'Booking Request Pending',
        "sys_no": sysid,
        "lab_no": lab_no,
        "date": date,
        "time_from": time_from,
        "time_till": time_till,
        'stud_emails': stud_emails,
        'details': details
    })
    ref = db.reference('users')
    sysid = sysid.replace("System No - ", "")
    if "," in sysid:
        sysid = sysid.split(",")
        for i in sysid:
            sys_no = i.replace('"', "")
            data = {
                'title': title,
                'booking_type': booking_type,
                'lab_no': lab_no,
                'sys_no': sys_no,
                'date': date,
                'time_from': time_from,
                'time_till': time_till,
                'stud_emails': stud_emails,
                'status': 'Pending...',
                'details': details
            }
            ref.child(uid).child("booking history").child(f"lab {lab_no}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)       
    else:
        sys_no = sysid.replace('"', "")
        data = {
            'title': title,
            'booking_type': booking_type,
            'lab_no': lab_no,
            'sys_no': sys_no,
            'date': date,
            'time_from': time_from,
            'time_till': time_till,
            'stud_emails': stud_emails,
            'status': 'Pending...',
            'details': details
            }
        ref.child(uid).child("booking history").child(f"lab {lab_no}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)
    
    if acc_type == "Admin":
        fbapprove_booking(uid)

def getuserapproval_list():
    ref = db.reference('unapproved_users')
    return ref.get()

def get_unapproved_booking_requests():
    ref = db.reference('unapproved_requests')
    return ref.get()


def fbapprove_user(uid):
    ref = db.reference('unapproved_users')
    ref.child(uid).delete()
    ref = db.reference('users')
    ref.child(uid).child("approved").set(True)

def fbapprove_booking(uid):
    unapproved_booking_list = get_unapproved_booking_requests()
    print(unapproved_booking_list)
    ref = db.reference('users')
    bookingid = unapproved_booking_list[uid]
    lab=bookingid['lab_no']
    date=bookingid['date']
    time_from=bookingid['time_from']
    time_till=bookingid['time_till']
    sysid=bookingid['sys_no']
    stud_emails=bookingid['stud_emails']
    name=bookingid['name']
    title=bookingid['title']
    booking_type=bookingid['booking_type']
    email=bookingid['email']
    dept=bookingid['dept']
    acc_type=bookingid['acc_type']

    data = {
        'title': title,
        'booking_type': booking_type,
        'lab_no': lab,
        'sys_no': sysid,
        'date': date,
        'time_from': time_from,
        'time_till': time_till,
        'status': 'Approved by Admin',
        'details': bookingid['details']
    }

    sysid = sysid.replace("System No - ", "")

    if "," in sysid:
        sysid = sysid.split(",")
        for i in sysid:
            sys_no = i.replace('"', "")
            ref.child(uid).child("booking history").child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)       
    else:
        sys_no = sysid.replace('"', "")
        ref.child(uid).child("booking history").child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)
    
    ref = db.reference('booked_seats')
    data = {
        'name': name,
        'email': email,
        'dept': dept,
        'acc_type': acc_type,
        'title': title,
        'booking_type': booking_type,
        'approved_by': 'Approved by Admin',
        "uid": uid,
        'time_from': time_from,
        'time_till': time_till,
        'details': bookingid['details']
    }

    if type(sysid) == list:
        for i in sysid:
            sys_no = i.replace('"', "")
            ref.child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)
    else:
        sys_no = sysid.replace('"', "")
        ref.child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)
    ref = db.reference('unapproved_requests')
    ref.child(uid).delete()
    for s_email in stud_emails.split(","):
        try:
            emailmanager.send_email(s_email, title, name, date, time_from, time_till, lab)
        except Exception as e:
            print(e)



def fbcancel_booking(uid, labno, seatno, date, time_from, time_till):
    ref = db.reference('users')
    print(date)
    bookingid = ref.child(uid).child("booking history").child(labno).child(date).child(time_from+" "+time_till).child(seatno).get()
    title=bookingid['title']
    booking_type=bookingid['booking_type']
    lab=bookingid['lab_no']
    date=bookingid['date']
    time_from=bookingid['time_from']
    time_till=bookingid['time_till']
    sysid=bookingid['sys_no']

    data = {
        'title': title,
        'booking_type': booking_type,
        'lab_no': lab,
        'sys_no': sysid,
        'date': date,
        'time_from': time_from,
        'time_till': time_till,
        'status': 'Cancelled by User',
        'details': bookingid['details']
    }
    print(data)
    ref.child(uid).child("booking history").child(labno).child(date).child(time_from+" "+time_till).child(seatno).set(data)
    ref = db.reference('booked_seats')
    ref.child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(seatno).delete()


def fbreject_booking(uid):
    unapproved_booking_list = get_unapproved_booking_requests()
    bookingid = unapproved_booking_list[uid]
    title=bookingid['title']
    booking_type=bookingid['booking_type']
    lab=bookingid['lab_no']
    date=bookingid['date']
    time_from=bookingid['time_from']
    time_till=bookingid['time_till']
    sysid=bookingid['sys_no']
    details = bookingid['details']
    ref = db.reference('users')

    data = {
        'title': title,
        'booking_type': booking_type,
        'lab_no': lab,
        'sys_no': sysid,
        'date': date,
        'time_from': time_from,
        'time_till': time_till,
        'status': 'Rejected by admin',
        'details': details
    }
    print(data)
    sysid = sysid.replace("System No - ", "")
    sysid = sysid.split(",")
    for i in sysid:
        sys_no = i.replace('"', "")
        sys_no = sys_no.strip()
        ref.child(uid).child("booking history").child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)  
    
    ref = db.reference('unapproved_requests')
    ref.child(uid).delete()
    

def test_reject(uid):
    unapproved_booking_list = get_unapproved_booking_requests()
    print(unapproved_booking_list)
    ref = db.reference('users')
    bookingid = unapproved_booking_list[uid]
    title=bookingid['title']
    booking_type=bookingid['booking_type']
    lab=bookingid['lab_no']
    date=bookingid['date']
    time_from=bookingid['time_from']
    time_till=bookingid['time_till']
    sysid=bookingid['sys_no']
    name=bookingid['name']
    email=bookingid['email']
    dept=bookingid['dept']
    acc_type=bookingid['acc_type']

    data = {
        'title': title,
        'booking_type': booking_type,
        'lab_no': lab,
        'sys_no': sysid,
        'date': date,
        'time_from': time_from,
        'time_till': time_till,
        'status': 'Approved by Admin',
        'details': bookingid['details']
    }

    sysid = sysid.replace("System No - ", "")

    if "," in sysid:
        sysid = sysid.split(",")
        for i in sysid:
            sys_no = i.replace('"', "")
            ref.child(uid).child("booking history").child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)       
    else:
        sys_no = sysid.replace('"', "")
        ref.child(uid).child("booking history").child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)
    
    ref = db.reference('booked_seats')
    data = {
        'name': name,
        'email': email,
        'dept': dept,
        'acc_type': acc_type,
        'title': title,
        'booking_type': booking_type,
        'approved_by': 'Approved by Admin',
        "uid": uid,
        'time_from': time_from,
        'time_till': time_till,
        'details': bookingid['details']
    }

    if type(sysid) == list:
        for i in sysid:
            sys_no = i.replace('"', "")
            ref.child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)
    else:
        sys_no = sysid.replace('"', "")
        ref.child(f"lab {lab}").child(date).child(time_from+" "+time_till).child(sys_no).set(data)
    ref = db.reference('unapproved_requests')
    ref.child(uid).delete()


def get_booked_seats(lab, date, time_from, time_till):
    ref = db.reference('booked_seats')
    booked_seats = ref.child(f"lab {lab}").child(date).get()
    result = {}
    for key in booked_seats.keys():
        time_range = key.split(" ")
        test = timetest.is_overlap([time_from, time_till], time_range)
        if test:
            result.update(booked_seats[key])
    return result
    

def get_booking_history(uid, acc_type):
    if acc_type != "Admin":
        ref = db.reference('users')
        booking_history = ref.child(uid).child("booking history").get()
        return booking_history
    else:
        ref = db.reference('booked_seats')
        return ref.get()


def fbstoreseats(): 
    ref = db.reference("seats_row")
    sys_no = 0
    lab = 4
    for row in range(1,9):
        for col in range(1,9):
            if row == 1 and col == 5:
                data = {
                'sys_no': "Pillar",
                'status': '',
                'uid': '',
                'time_from': '',
                'time_till': '',
                'details': '',
            }
            elif row == 2 and col == 5:
                data = {
                'sys_no': "Piller",
                'status': '',
                'uid': '',
                'time_from': '',
                'time_till': '',
                'details': '',
            }
            elif row == 6 and col == 5:
                data = {
                'sys_no': "Piller",
                'status': '',
                'uid': '',
                'time_from': '',
                'time_till': '',
                'details': '',
            }
            elif row == 7 and col == 5:
                data = {
                'sys_no': "Piller",
                'status': '',
                'uid': '',
                'time_from': '',
                'time_till': '',
                'details': '',
            }
            else:
                sys_no += 1
                data = {
                    'sys_no': sys_no,
                    'status': '',
                    'uid': '',
                    'time_from': '',
                    'time_till': '',
                    'details': '',
                }
            ref.child(f"lab {lab}").child(f"{col}").child(f"row {col}").set(data)
    

def gethistory(date_from, date_till):
    if date_from == '':
        date_from = '1997-10-11'
    if date_till == '':
        date_till = '3030-10-11'
    ref = db.reference("booked_seats")
    result = {}
    for lab in range(1,5):
        booked_seats = ref.child(f"lab {lab}").get()
        if booked_seats != None:
            for date, value in booked_seats.items():
                test = timetest.check_date_time_range(date_from, date_till, date)
                print(date, '-' ,test)
                if test:
                    result[f"lab {lab}"] = result.get(f"lab {lab}", {})
                    result[f"lab {lab}"][date] = {}
                    result[f"lab {lab}"][date].update(booked_seats[date])
    print(result)
    
    return result

def store(path, data):
    ref = db.reference(path)
    ref.set(data)

def get_data(path):
    ref = db.reference(path)
    return ref.get()


def getallseats(lab):
    ref = db.reference("seats")
    return ref.child(f"lab {lab}").get()


if __name__ == "__main__":
    cred = credentials.Certificate('imac_main/scripts/serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://i-mac-portal-lab-database-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
    fbstoreseats()

