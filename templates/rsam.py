from library import *
#from flask import Flask, render_template, request, redirect, url_for, session, make_response
# for impoerting the mail
from flask import *
from flask_mail import Mail, Message
import mysql.connector
import random
from flask_recaptcha import * # Import ReCaptcha objects

app = Flask(__name__)
# object for mail
mail=Mail(app)
#create object of library
ob=db()

app.secret_key="nightwing"
# start mail configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'animejusticex@gmail.com'
app.config['MAIL_PASSWORD'] = 'elvewarudarhjetg'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# end configuration

#for captacha verfication
app.config['RECAPTCHA_SITE_KEY'] = '6LcGp9khAAAAALDcV-FKUr-IzKOWwn3jvpPtitV0' # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = '6LcGp9khAAAAABQjXooadWBkRyfU5__OLqRKWPmX' # <-- Add your secret key
recaptcha = ReCaptcha(app) # Create a ReCaptcha object by passing in 'app' as parameter
#end

@app.route("/", methods=['POST','GET'])
def login():

    return render_template("login.html")


@app.route("/product")
def product():
    x=ob.getdata("member")
    return render_template("product.html",mydata=x['data'])

@app.route("/Resistration")
def Resistration():
    return render_template("Resistration.html") 

@app.route("/service")
def service():
    mycon=mysql.connector.connect(host="127.0.0.1",user="root",password="",database="project")
    cur=mycon.cursor()
    cur.execute("select * from member")
    data=cur.fetchall()
    return render_template("service.html",mydata=data)

#insert data registered form 
@app.route("/insert", methods=['POST','GET'])
def insertdata():
    message=""
    if(request.method=="POST"):
        user=request.form['xuser']
        email=request.form['xmail']
        phone=request.form['xphone']
        password=request.form['xpass']
        vpass=request.form['xvpass']
        myfile=request.files['xfile']
        filename=myfile.filename
        myfile.save("static/upload/" + filename)
        dt={"user":user,"email":email,"phone":phone,"password":password,"vpass":vpass,"image":filename}
        retValue=ob.insertdata("member",dt)
        if(retValue['count']>=1):
            message="You have Succesfully registered Yourself"
        else:
            message="You are not registered"
        return render_template("Resistration.html",mydata=message)
    else:
        return render_template("404.html")
# for authentication for login / logout
@app.route("/auth", methods=['GET','POST'])
def login_auth():
    if not recaptcha.verify(): # Use verify() method to see if ReCaptcha is filled out
        message = 'Please Verify Human Verification' # Send success message
        return render_template("login.html", mydata=message)
    elif(request.method=="POST"):
        email=request.form['xemail']
        pas=request.form['xpass']
        condi={"email":email,"password":pas}
        retValue=ob.getdata("member",condi)
        if(retValue['count']>=1):
            session['username']=retValue['data'][0][1]
            session['image']=retValue['data'][0][6]
            session['login']=True
            #for creating cookies
            if("rem" in request.form):
                resp = make_response(render_template("home.html"))
                resp.set_cookie('email',email)
                resp.set_cookie('password',pas)
                return resp
            else:
                return render_template("home.html")
        else:
            message="Email or password is not found"
            return redirect("/")
    else:
        return render_template("404.html")

# for destroying the session
@app.route("/logout")
def logout():
    session.pop("login")
    session.pop("username")
    session.pop("image")
    session.clear()
    # for destroying the cookie
    resp = make_response(render_template("login.html"))
    resp.set_cookie('email','', expires=10)
    resp.set_cookie('password','', expires=10)
    return resp

# for sending the email (static)
@app.route("/send_mail")
def send_mail():
    msg = Message('Test Mail for Testing Application', sender = 'animejusticex@gmail.com', recipients = ['rajpurohitdeepak54@gmail.com'])
    msg.body = "hello; "
    mail.send(msg)
    return redirect("/")

@app.route("/forget")
def forget():
        return render_template("/forget.html")
    
@app.route("/Email-auth",methods=['POST','GET'])
def forget_auth():
    if(request.method=="POST"):
        session['email']=email=request.form['xemail']
        condi={"email":email}
        retValue=ob.getSingleData("member","email",email)
        # for otp generation
        session['otp']=otp=random.randint(111111,999999)
        if(retValue['count']>=1):
            msg = Message('Forget Password configration', sender = 'animejusticex@gmail.com', recipients = [email])
            msg.body = "This OTP -> "+ str(otp) +" for forgetpassword Please do not share otp to anyone"
            mail.send(msg)
            return render_template("reset.html")
        else:
            message="Email or password is not found"
            return redirect("/forget")
    else:
        return render_template("404.html")

@app.route("/verify", methods=['GET',"POST"])
def verify():
    if(request.method=="POST"):
        user_otp=request.form['xotp']
        if(str(user_otp)==str(session['otp'])):
            newpass=request.form['xpass']
            if(request.form['xvpas']==newpass):
                st=ob.update("member",{"password":newpass},{"email":session['email']})
                message=("password is updated click on <a href='/'>Login</a> ")
                return render_template("reset.html",data=message)
            else:
                message="Your Password and confirm password is not match"
                return render_template("reset.html",data=message)
        else:
            message="Your OTP is Match Please Insert Correct OTP" + str(session['otp'])
            return render_template("reset.html",data=message)
    else:
        return render_template("404.html")

if __name__ == '__main__':
   app.run(debug=True)