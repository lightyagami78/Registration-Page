from email import message
from select import select
from library import *
# from flask import Flask, render_template, request, redirect, url_for,session
from flask import *
import mysql.connector
import random
from flask_bcrypt import Bcrypt
# for importing the mail

from flask_recaptcha import * # Import ReCaptcha objects

from flask_mail import *
app = Flask(__name__)
app.secret_key = 'levi_ackeramann'


#object for encryption
bcrypt = Bcrypt()
#create object of library
ob=db()
# start mail configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lyagmi938@gmail.com'
app.config['MAIL_PASSWORD'] = 'krhsradlptdesrmp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_SITE_KEY'] = '6LdjTfkhAAAAAPvMPegpmqa6Q8drKHXyF35W5g3s' # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = '6LdjTfkhAAAAANGoVGbIWkxWKXYQj5eQCf5uEGXi' # <-- Add your secret key
recpatcha = ReCaptcha(app)# Create a ReCaptcha object by passing in 'app' as parameter

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/product")
def product():
    x=ob.getdata("member")
    return render_template("product.html",mydata=x['data'])

@app.route("/registeration")
def form():
    return render_template("registeration.html") 

@app.route("/service")
def service():
    mycon=mysql.connector.connect(host="127.0.0.1",user="root",password="",database="project")
    cur=mycon.cursor()
    cur.execute("select * from member")
    data=cur.fetchall()
    return render_template("service.html",mydata=data)

   
@app.route("/insert", methods=['POST','GET'])
def insertdata():
    message=""
    if(request.method=="POST"):
        username=request.form['xname']
        email=request.form['xmail']
        phone=request.form['xphone']
        password=request.form['xpass']
        vpass=request.form['xvpass']
        myfile=request.files['xfile']
        filename=myfile.filename
        myfile.save("static/upload/" + filename)
        pw_hash = bcrypt.generate_password_hash(password)
        dt={"username":username,"email":email,"phone":phone,"password":pw_hash.decode(),"vpass":vpass,"image":filename}
        retValue=ob.insertdata("member",dt)
        if(retValue['count']>=1):
            session['message']="You have Succesfully registered Yourself"
        else:
            session['message']="You are not registered"
        return redirect("/registeration")
    else:
        return redirect("/",mydata=message)

@app.route("/auth", methods=['POST','GET'])
def login_auth():
    if not recpatcha.verify(): # Use verify() method to see if ReCaptcha is filled out
        message = 'Please Verify you are Human' # Send success message
        return render_template("login.html",mydata=message)
    if(request.method=="POST"):
        email=request.form['xmail']
        pas=request.form['xpass']
        retValue= ob.getSingleData("member","email",email)
        if(bcrypt.check_password_hash(retValue['data'][4],pas)==True):
            session['username']=retValue['data'][1]
            session['image']=retValue['data'][6]
            session['login']=True
            #for creating cookies
            if("rem" in request.form):
                resp = make_response(render_template("home.html"))
                resp.set_cookie('email', email)
                resp.set_cookie('password',pas)
                return resp
            else:
                message="Email or password is not found"
                return render_template("home.html",data=message)
        else:
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


@app.route("/forget")
def forget():
    return render_template("/forget.html")


@app.route("/Email-auth",methods=['POST','GET'])
def forget_auth():
    if(request.method=="POST"):
        session['email']=email=request.form['xemail']
        condi={"email":email}
        retValue=ob.getSingleData("member","email",email)
        # for OTP generation
        session['otp']=otp=random.randint (111111,999999)
        if(retValue['count']>=1):
            msg= Message('Forget Password Configuration',sender ='lyagmi938@gmail.com',recipients = [email])
            msg.body = "This OTP" + str(otp) +"for Forgetpassword. PLease do not share your OTP to anyone"
            mail.send(msg)
            return render_template("reset.html")
        else:
            return redirect("/forget")
    else:
        return render_template("404.html")

@app.route("/verify", methods=['GET',"POST"])
def verify():
    if(request.method=="POST"):
        user_otp=request.form['xotp']
        # comparing session OTP to user OTP
        if(str(user_otp)==str(session['otp'])):
            newpass=request.form['xpass']
            if(request.form['xvpas']==newpass):
                st=ob.update("member",{"password":newpass},{"email":session['email']})
                message=("password is updated ")
                return render_template("reset.html",data=message)
            else:
                message="Your Password and confirm password is not match"
                return render_template("reset.html",data=message)
        else:
            message="Your OTP is Match Please Insert Correct OTP" + str(session['otp'])
            return render_template("reset.html",data=message)
    else:
        return render_template("404.html")



# This is used to execute some code only if the file was run directly, and not imported.
if __name__ == '__main__':
# When running from Python code, passing debug=True enables debug mode, which is mostly equivalent.
   app.run(debug=True)