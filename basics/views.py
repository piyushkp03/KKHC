from django.http import request
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Products,medicines,usercart,orders
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from paytm import Checksum
#4389-7600-3507-6969

#totalamt=0
#prolist=[]
cartno=0
#cartemail=""
#z=[]
#cartorbuy1=''
#p=orders.objects.last() 
#oid=p.id
#print("the last order is ",oid,p)
#prname=''
#prprice=''
#usname=''
#addr=''
#ph=''

# Create your views here.
MERCHANT_KEY = 'qfJSH_1qdir&3HjO'

def delete(request):
    removeitem=request.POST['remove']
    print(removeitem)
    y=usercart.objects.get(pk=removeitem)
    y.delete()
    return redirect('cart')
def yourorders(request):
    yorder=orders.objects.filter(email=request.user.email)
    return render(request,'yourorders.html',{'order':yorder})

def buydirect():
    print("Direct buy details are:",usname,addr, prname,ph, prprice)
    x=orders(name=usname,email=cartemail,address=addr,phone=ph,pid=str(cartemail)+str(oid),pname=prname,pprice=prprice) 
    print("Order from buy direct is :",x)
    x.save()
def buyfromcart():
    datas=usercart.objects.filter(email=cartemail) 
    print("details from the cart bought is:",usname,addr,ph,prname,prprice)
    for x in datas:
        y=orders(name=usname,email=cartemail,address=addr,phone=ph,pid=str(cartemail)+str(oid),pname=x.pname,pprice=x.pprice) 
        y.save()
        print("Orders from buy cart is :",y)
        datas.delete()



@csrf_exempt
def handlerequest(request): 
    
    global oid  
    print("In handlerequest data's are,", cartorbuy1,usname,prname, prprice,addr,ph,oid)
   
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            
            if cartorbuy1=='fromcart':
                buyfromcart()
            else:
                buydirect()
                #usercart.objects.filter(email=cartemail).delete()
            print('order successful') 
            oid+=1
                    
            
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})


def checkout(request):
    global prname,prprice,usname,addr,ph,oid 
    if request.method=='POST':
        if request.user.is_authenticated:  
            print("checking for last order..")
            p=orders.objects.last()  
            print("last order is:",p) 

            oid=p.id 
            print("oid is",oid,"current email is", cartemail)
        
            
            print("Inside without updating",cartemail)

            prname=request.POST.get('pname',False) 
            print (prname)
            prprice=request.POST.get('pprice',False) 
            print(prprice)
            usname=request.POST.get('name',False) 
            print(usname)
            addr=request.POST.get('address',False) 
            print (addr)
            ph=request.POST.get('phone',False) 
            print(ph)
            print("Checkout details are : ",prname,prprice,usname,addr,ph,oid)
  
            


            
                # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
                # Request paytm to transfer the amount to your account after payment by user
            param_dict = {

                        'MID': 'yIjMtl03527914536186',
                        'ORDER_ID': str(request.user.email)+"orderid"+str(oid),
                        'TXN_AMOUNT': str(prprice),
                        'CUST_ID': cartemail,
                        'INDUSTRY_TYPE_ID': 'Retail',
                        'WEBSITE': 'WEBSTAGING',
                        'CHANNEL_ID': 'WEB',
                        'CALLBACK_URL':'https://kkhealthcare.herokuapp.com/handlerequest',

                }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'paytm.html', {'param_dict': param_dict})
        else:
            messages.error(request,"Please login to shop..")
            return redirect('home')

    return render(request, 'userdetails.html')



def index(request):
    global cartno,oid 
    m=orders.objects.all() 
    for f in m: 
        print(f.id,f)
    p=orders.objects.last() 

    oid=p.id
    print("home page data:",cartno,oid,m)
   
    if request.user.is_authenticated:
        print("The user email is at left",request.user.email)
        data=usercart.objects.filter(email=request.user.email)
        cartno=len(data)
        print("Number of items in cart",cartno)
        return render(request,"index.html",{'cartno':cartno})
    return render(request,"index.html")
def userdetails(request):
    global cartorbuy1, cartemail
    if not request.user.is_authenticated:
        messages.error(request,"Please login to shop...")
        return redirect('home')
    if request.method== 'POST': 
        cartemail=request.user.email

       
        pname=request.POST.get('pname', False)
    
        price=request.POST.get('price', False)
        cartorbuy1=request.POST.get('buyorcart',False)
        print("The price is+",price)
    

        print("The data to be checked are",oid, "email is:",cartemail,"cart or buy?",cartorbuy1,price)
        return render(request,'userdetails.html',{'price':price,'name':pname,'pid':oid,'cartorbuy': cartorbuy1,'mailid': cartemail})
    return render(request,'userdetails.html')


def aboutus(request):

    global cartno 
    print(cartemail,oid, cartorbuy1,prname, prprice, usname,addr,ph)
   
    if request.user.is_authenticated:
        data=usercart.objects.filter(email=request.user.email)
        cartno=len(data)
        print("Number of items in cart",cartno)
    return render(request,"aboutus.html",{'cartno':cartno})

def gallery(request):
    global cartno
    if request.user.is_authenticated:
        data=usercart.objects.filter(email=request.user.email)
        cartno=len(data)

    syp=medicines.objects.filter(pcategory="Syrup")
    tab=medicines.objects.filter(pcategory="Tablet")
    syrup=[]
    tablet=[]
    x=[]
    print("Number of items in cart",cartno)
    for i in range(len(syp)):
        if i%3==0 and i!=0:
            syrup.append(x)
            x=[]

        x.append(syp[i])
        if i==len(syp)-1 and len(x)<=3 and len(x)!=0:
            syrup.append(x)
    x=[]
    print(syrup)
    for i in range(len(tab)):
        if i%3==0 and i!=0:
            tablet.append(x)
            x=[]


        x.append(tab[i])
        if i==len(tab)-1 and len(x)<=3 and len(x)!=0:
            tablet.append(x)
    print(tablet)
    data=[syrup,tablet]
    data1=['Syrup','Tablet']
    datazip=zip(data, data1)
   
    return render(request,"gallery.html",{'datazip':datazip,'cartno':cartno})

def products(request):
    global cartno,searchcalled,prolist
    searchcalled=False
    prolist=[]
        
   
    if not request.user.is_authenticated:
        messages.error(request,"Please login to shop!")
        return redirect('home')
    else:
        data=usercart.objects.filter(email=request.user.email)
        cartno=len(data)
     
        prolist.append(Products.objects.all())
        print(prolist,"items in acart",cartno)
       
        return render(request,"products.html",{'prolist':prolist,'cartno':cartno})
def aftersearch(request):
    if request.user.is_authenticated:
        data=usercart.objects.filter(email=request.user.email)
    cartno=len(data)
    return render(request,"products.html",{'prolist':prolist,'cartno':cartno})


def searchfield(request):
    global cartno,searchcalled,prolist
    searchcalled=True
    if request.user.is_authenticated:
        data=usercart.objects.filter(email=request.user.email)
        cartno=len(data)
    prolist=[]
    

    searchvalue=request.POST['searchfield']
    x=set(Products.objects.values_list('pcategory',flat=True))
    print("Number of items in cart",cartno)
    for val in x:
        if searchvalue.lower() in str(val.lower()):
            print(searchvalue,val)
            prolist.append(Products.objects.filter(pcategory=val))
            print("True")
        else:
            print("False")
    print("The lists are",prolist)
    return render(request,"products.html",{'prolist':prolist,'cartno':cartno})




def cart(request):
    global cartno,total

    
    if not request.user.is_authenticated:
        messages.error(request,"Please login to shop!")
        return redirect('home')
    else:
        data=usercart.objects.filter(email=request.user.email)
        total=sum([x.pprice for x in data])
        print(data)
        cartno=len(data)
        print("Number of items in cart",cartno)
        return render(request,"cart.html",{'data':data,'length':len(data),'total':total})
   

   
    
def signupuser(request):

    # messages.error(request,"checking error")

    if(request.method=='POST'):
        uname=request.POST['uname']
        email=request.POST['email']
        passw=request.POST['pass']
        cnfpass=request.POST["cnfpass"]
        print(uname,email,passw,cnfpass)
        print(type(passw))
        print(passw==cnfpass)
        if not uname.isalnum():
            messages.error(request,"Username must only contain no and letters")
            return redirect('home')

        if (passw != cnfpass):
            messages.error(request,"Passwords should match")
            return redirect('home')

        if(passw==cnfpass):

            myuser=User.objects.create_user(uname, email, passw)
            myuser.save()
            messages.success(request, "User registered successfully")
            return redirect('home')

    else:
        return HttpResponse('404..Not Found')



    return render(request,'index.html')

def loginuser(request):
    uname = request.POST['uname']
    passw = request.POST['passw']
    l=User.objects.all()
    print(l)
    for u in l:
        print(u)
    usr=authenticate( username=uname, password=passw)
    print(usr)
    if usr is not None:
        login(request, usr)
        messages.success(request, "Logged in successfully")
        return redirect("home")
    else:
        messages.error(request, "Invalid credentials")
        return redirect('home')


def loginuser1(request):
    uname = request.POST['uname']
    passw = request.POST['passw']
    l=User.objects.all()
    print("The request loginuser1",request)
    for u in l:
        print(u)
    usr=authenticate( username=uname, password=passw)
    print(usr)
    if usr is not None:
        login(request, usr)
        messages.success(request, "Logged in successfully")
        return redirect("hospitalpage1")
    else:
        messages.error(request, "Invalid credentials")
        return redirect('hospitalpage1')



def logoutuser(request):
    logout(request)
    messages.success(request,"Logged out")
    return redirect('home')

def addtocart(request):
    global cartno
  
    
    if request.user.is_authenticated:
        data=usercart.objects.filter(email=request.user.email)
        cartno=len(data)
        usr=request.user.email
        iname=request.POST['itemname']
        iprice=request.POST['itemprice']
        icat=request.POST['itemcategory']
        iwt=request.POST['itemwt']
        iflavor=request.POST['itemflavor']
        iimage=request.POST['itemimage']
        a = usercart(email = usr,pname=iname, pcategory = icat, pprice = iprice,pimage=iimage, pwt = iwt)
        a.save()
        print("After adding to cart",prolist)
        
        if searchcalled:
            return redirect('aftersearch')
        else:
            return redirect('products')
    else:
        messages.error(request,"Please login to shop")
        return redirect('home')




