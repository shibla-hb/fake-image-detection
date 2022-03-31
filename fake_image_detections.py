from flask import Flask, render_template, request, session, redirect
import datetime
from DBConnection import Db


app = Flask(__name__)
app.secret_key="abc"


@app.route('/',methods=['get','post'])
def login():
    if request.method=="POST":
        username=request.form['textfield']
        password=request.form['textfield2']
        db = Db()
        qry=db.selectOne("select*from login where username='"+username+"' and password='"+password+"'")
        if qry is not None:
            uid=qry['login_id']
            values=db.selectOne("select * from user where user_id='"+str(uid)+"'")
            session['photo']=values['photo']
            print(session['photo'])
            session['name']=values['username']
            session['lid']=uid
            session['log']='log'

            return '''<script>alert('login successfully');window.location="/home"</script>'''
        else:
            return '''<script>alert('user not found');window.location="/"</script>'''
    else:
      return render_template('index.html')
@app.route('/registration',methods=['get','post'])
def registerform():
    if request.method=="POST":
        Name=request.form['textfield7']
        Gender=request.form['RadioGroup1']
        Place=request.form['textfield5']
        Post=request.form['textfield4']
        Pin=request.form['textfield3']
        Photo=request.files['fileField']
        date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        Photo.save(r"C:\Users\HP\PycharmProjects\fake_image_detections\static\photo\\"+date+'.jpg')
        path="/static/photo/"+date+'.jpg'
        PhoneNO=request.form['textfield2']
        Email=request.form['textfield']
        Password=request.form['textfield6']
        confirmpassword=request.form['textfield8']
        db = Db()
        if Password==confirmpassword:

           qry=db.insert("insert into login VALUES ('','"+Email+"','"+confirmpassword+"')")
           db.insert("insert into user VALUES ('"+str(qry)+"','"+Name+"','"+ Gender+"','"+Place+"','"+ Post+"','"+Pin+"','"+str(path)+"','"+ PhoneNO+"','"+Email+"')")
           return '''<script>alert('success');window.location="/"</script>'''
        else:
            return '''<script>alert('password mismatch');window.location="/registration"</script>'''
    else:

       return render_template('register.html')
@app.route('/view')
def viewprofile():
    if session['log']=="log":
        db=Db()
        qry=db.selectOne("select * from user where user_id='"+str(session['lid'])+"' ")
        return render_template('viewprofile.html',data=qry)
    else:
        # return '''<script>alert('you are logged out');window.location="/"</script>'''
        return redirect('/')
@app.route('/home')
def home():
   if session['log']=='log':
        return render_template('dashboard.html')
   else:
       return redirect('/')


@app.route('/upload_image')
def imageupload():

        return render_template('upld_img.html')

@app.route('/logout')
def logout():
    session.clear()
    session['log']=""
    return redirect('/')
if __name__ == '__main__':
    app.run()


