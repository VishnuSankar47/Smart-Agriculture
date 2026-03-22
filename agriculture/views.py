import os
from datetime import date

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect


def _fetchall(sql, params=()):
    with connection.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def _fetchone(sql, params=()):
    with connection.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def _execute(sql, params=()):
    with connection.cursor() as cur:
        cur.execute(sql, params)


def index(request):
    return render(request, 'HomePage.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return render(request, 'logout.html')


def login1(request):
    if request.method != "POST":
        return redirect('/login')
    name = request.POST['un']
    password = request.POST['pass']
    admin = _fetchone("SELECT * FROM login WHERE admin_id=%s AND password=%s", [name, password])
    if admin:
        request.session['lid'] = name
        return redirect('/AdminHomePage')
    user = _fetchone("SELECT * FROM user_register WHERE user_id=%s AND password=%s", [name, password])
    if user:
        request.session['lid'] = name
        return redirect('/UserHome')
    farmer = _fetchone("SELECT status, farmer_id FROM farmer_register WHERE farmer_id=%s AND password=%s", [name, password])
    if farmer:
        status = farmer[0]
        request.session['hid'] = farmer[1]
        request.session['lid'] = name
        if status == 'pending' or status == 'request':
            return HttpResponse("<script>alert('Your request is pending.');window.location='/';</script>")
        elif status == 'rejected':
            return HttpResponse("<script>alert('Your request has been rejected.');window.location='/';</script>")
        elif status == 'approved':
            return redirect('/FarmerHome')
    return HttpResponse("<script>alert('Invalid credentials.');window.location='/login';</script>")


def AdminHomePage(request):
    return render(request, 'Admin/AdminHomePage.html')


def view_farmer_request(request):
    data = _fetchall("SELECT * FROM farmer_register WHERE status='request'")
    return render(request, 'Admin/view_farmer_request.html', {'data': data})


def approveFarm(request, sid):
    _execute("UPDATE farmer_register SET status='approved' WHERE farmer_id=%s", [sid])
    return redirect('/view_farmer_request')


def deletefarmersre(request, sid):
    _execute("DELETE FROM farmer_register WHERE farmer_id=%s", [sid])
    return HttpResponse("<script>alert('Deleted.');window.location='/view_farmer_request';</script>")


def view_approved_farmer(request):
    data = _fetchall("SELECT * FROM farmer_register WHERE status='approved'")
    return render(request, 'Admin/view_approved_farmer.html', {'data': data})


def deletefarmer(request, sid):
    _execute("DELETE FROM farmer_register WHERE farmer_id=%s", [sid])
    return HttpResponse("<script>alert('Deleted.');window.location='/view_approved_farmer';</script>")


def addCategory(request):
    if request.method == "POST":
        name = request.POST['txtname']
        price = request.POST['price']
        farmer_price = request.POST['farmer_price']
        _execute("INSERT INTO category VALUES(null, %s, %s, %s)", [name, price, farmer_price])
        return HttpResponse("<script>alert('Category added.');window.location='/AdminHomePage';</script>")
    return render(request, 'Admin/addCategory.html')


def viewCategory(request):
    data = _fetchall("SELECT * FROM category")
    return render(request, 'Admin/viewCategory.html', {'data': data})


def deleteCategory(request, id):
    _execute("DELETE FROM category WHERE category_id=%s", [id])
    return HttpResponse("<script>alert('Deleted.');window.location='/viewCategory';</script>")


def editCategory(request, id):
    data = _fetchall("SELECT * FROM category WHERE category_id=%s", [id])
    return render(request, 'Admin/editCategory.html', {'data': data})


def updatecategory(request, id):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        farmer_price = request.POST['farmer_price']
        _execute("UPDATE category SET name=%s, price=%s, farmer_price=%s WHERE category_id=%s", [name, price, farmer_price, id])
        return HttpResponse("<script>alert('Updated.');window.location='/viewCategory';</script>")
    return render(request, 'Admin/editCategory.html')


def admin_products_request(request):
    data = _fetchall("SELECT * FROM item_details WHERE status='pending'")
    return render(request, 'Admin/admin_products_request.html', {'data': data})


def approvesell(request, id):
    _execute("UPDATE item_details SET status='approved' WHERE iditem_details=%s", [id])
    return redirect('/admin_products_request')


def ViewFarmerProductApproved(request):
    data = _fetchall("SELECT * FROM item_details WHERE status='approved'")
    return render(request, 'Admin/ViewFarmerProductApproved.html', {'data': data})


def viewbookingitems(request):
    data = _fetchall("SELECT * FROM user_booking")
    return render(request, 'Admin/viewbookingitems.html', {'data': data})


def ViewcompliantAdmin(request):
    data = _fetchall("SELECT * FROM compliant")
    return render(request, 'Admin/ViewcompliantAdmin.html', {'data': data})


def Reply(request, id):
    if request.method == "POST":
        reply = request.POST['TxtReply']
        _execute("UPDATE compliant SET reply=%s, status='replied' WHERE idcompliant=%s", [reply, id])
        return HttpResponse("<script>alert('Reply sent.');window.location='/ViewcompliantAdmin';</script>")
    return render(request, 'Admin/Reply.html')


def FarmerHome(request):
    return render(request, 'Farmer/FarmerHome.html')


def register_farmer(request):
    if request.method == "POST":
        farmer_id = request.POST['farmer_id']
        name = request.POST['name']
        address = request.POST['TxtAddress']
        phone = request.POST['TxtPhone']
        password = request.POST['password']
        pincode = request.POST['pincode']
        city = request.POST['city']
        _execute("INSERT INTO farmer_register VALUES(%s, %s, %s, %s, %s, %s, %s, 'request')", [farmer_id, name, address, phone, password, city, pincode])
        return HttpResponse("<script>alert('Registration submitted.');window.location='/login';</script>")
    return render(request, 'Farmer/register_farmer.html')


def viewProductCategoryFarmer(request):
    data = _fetchall("SELECT * FROM category")
    return render(request, 'Farmer/viewProductCategoryFarmer.html', {'data': data})


def AddFarmerproduct(request, id, pid):
    fid = request.session.get('hid')
    if request.method == "POST":
        quantity = request.POST['quantity']
        total_amount = int(quantity) * int(pid)
        item_description = request.POST['item_description']
        _execute("INSERT INTO item_details VALUES(null, %s, %s, %s, %s, %s, 'pending', %s)", [id, fid, date.today(), quantity, total_amount, item_description])
        return HttpResponse("<script>alert('Item submitted.');window.location='/FarmerHome';</script>")
    return render(request, 'Farmer/AddFarmerproduct.html')


def viewFarmeraddeditem(request):
    fid = request.session.get('hid')
    data = _fetchall("SELECT * FROM item_details WHERE farmer_id=%s AND status='approved'", [fid])
    return render(request, 'Farmer/viewFarmeraddeditem.html', {'data': data})


def Farmersellhistory(request):
    data = _fetchall("SELECT * FROM user_booking")
    return render(request, 'Farmer/Farmersellhistory.html', {'data': data})


def UserHome(request):
    return render(request, 'User/UserHome.html')


def adduser(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['TxtAddress']
        phone = request.POST['TxtPhone']
        email = request.POST['TxtEmail']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        password = request.POST['password']
        _execute("INSERT INTO user_register VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [user_id, first_name, last_name, phone, email, pincode, city, address, state, country, password])
        return HttpResponse("<script>alert('Registered.');window.location='/login';</script>")
    return render(request, 'User/adduser.html')


def viewProductCategoryUser(request):
    data = _fetchall("SELECT * FROM category")
    return render(request, 'User/viewProductCategoryUser.html', {'data': data})


def selctproducts(request, id, sid):
    request.session['sid'] = sid
    data = _fetchall("SELECT * FROM item_details WHERE status='approved' AND category_id=%s", [id])
    return render(request, 'User/selctproducts.html', {'data': data})


def Purchase(request, id, qid):
    sid = request.session.get('sid')
    lid = request.session.get('lid')
    if request.method == "POST":
        total_amount_user = int(qid) * int(sid)
        shipping_address = request.POST['shipping_address']
        _execute("INSERT INTO user_booking VALUES(null, %s, %s, %s, %s, %s, 'ADDED')", [lid, id, date.today(), shipping_address, total_amount_user])
        return HttpResponse("<script>alert('Added to cart.');window.location='/UserHome';</script>")
    return render(request, 'User/Purchase.html')


def Viewcart(request):
    lid = request.session.get('lid')
    data = _fetchall("SELECT * FROM user_booking WHERE user_id=%s AND status='ADDED'", [lid])
    return render(request, 'User/Viewcart.html', {'data': data})


def deleteCart(request, id):
    _execute("DELETE FROM user_booking WHERE iduser_booking=%s", [id])
    return HttpResponse("<script>alert('Removed.');window.location='/Viewcart';</script>")


def Bank(request):
    lid = request.session.get('lid')
    if request.method == "POST":
        cvv_no = request.POST['cvv_no']
        expiry_date = request.POST['expiry_date']
        card_no = request.POST['card_no']
        card_holder_name = request.POST['card_holder_name']
        card = _fetchone("SELECT * FROM bank WHERE card_no=%s AND cvv_no=%s AND card_holder_name=%s AND expiry_date=%s", [card_no, cvv_no, card_holder_name, expiry_date])
        if card:
            _execute("UPDATE user_booking SET status='Paid' WHERE user_id=%s AND status='ADDED'", [lid])
            return HttpResponse("<script>alert('Payment successful!');window.location='/UserHome';</script>")
        return HttpResponse("<script>alert('Invalid card details.');window.location='/Bank';</script>")
    return render(request, 'User/Bank.html')


def Userhistory(request):
    lid = request.session.get('lid')
    data = _fetchall("SELECT * FROM user_booking WHERE user_id=%s", [lid])
    return render(request, 'User/Userhistory.html', {'data': data})


def Sendcompliant(request):
    user_id = request.session.get('lid')
    if request.method == "POST":
        details = request.POST['details']
        _execute("INSERT INTO compliant VALUES(null, %s, %s, %s, null, 'pending')", [user_id, details, date.today()])
        return HttpResponse("<script>alert('Complaint submitted.');window.location='/UserHome';</script>")
    return render(request, 'User/Sendnotification.html')


def Viewcompliant(request):
    user_id = request.session.get('lid')
    data = _fetchall("SELECT * FROM compliant WHERE user_id=%s", [user_id])
    return render(request, 'User/Viewcompliant.html', {'data': data})
