from flask import Flask, render_template, request, session, redirect
import datetime
from DBConnection import Db

import numpy as np
# import matplotlib.pyplot as plt
np.random.seed(2)
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping


from PIL import Image, ImageChops, ImageEnhance
import os
import itertools


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


@app.route('/upload_image',methods=['get','post'])
def imageupload():
    if request.method=="POST":
        photo=request.files['filefield']
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        photo.save(r"C:\Users\HP\PycharmProjects\fake_image_detections\static\upld_images\\" + date + '.jpg')
        path = "/static/upld_images/" + date + '.jpg'

        def convert_to_ela_image(path, quality):
            temp_filename = 'temp_file_name.jpg'
            ela_filename = 'temp_ela.png'

            image = Image.open(path).convert('RGB')
            image.save(temp_filename, 'JPEG', quality=quality)
            temp_image = Image.open(temp_filename)

            ela_image = ImageChops.difference(image, temp_image)

            extrema = ela_image.getextrema()
            max_diff = max([ex[1] for ex in extrema])
            if max_diff == 0:
                max_diff = 1
            scale = 255.0 / max_diff

            ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

            return ela_image

        # real_image_path = r'C:\Users\HP\PycharmProjects\fake_image_detections\static\upld_images'
        # Image.open(real_image_path)
        #
        # convert_to_ela_image(real_image_path, 90)
        #
        # fake_image_path = r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Tp\Tp_D_NRN_S_N_ani10171_ani00001_12458.jpg'
        # Image.open(fake_image_path)
        #
        # convert_to_ela_image(fake_image_path, 90)

        image_size = (128, 128)

        def prepare_image(image_path):
            return np.array(convert_to_ela_image(image_path, 90).resize(image_size)).flatten() / 255.0

        X = []  # ELA converted images
        Y = [] #0 for fake, 1 for real

        import random
        path = r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Au\\'
        for dirname, _, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('jpg') or filename.endswith('png'):
                    full_path = os.path.join(dirname, filename)
                    X.append(prepare_image(full_path))
                    Y.append(1)
                    if len(Y) % 500 == 0:
                        print(f'Processing {len(Y)} images')

                        print(len(X), len(Y))
                        X = np.array(X)
                        Y = to_categorical(Y, 2)
                        X = X.reshape(-1, 128, 128, 3)

                        X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=5)
                        X = X.reshape(-1, 1, 1, 1)
                        print(len(X_train), len(Y_train))
                        print(len(X_val), len(Y_val))

                        path = r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Tp\\'
                        for dirname, _, filenames in os.walk(path):
                            for filename in filenames:
                                if filename.endswith('jpg') or filename.endswith('png'):
                                    full_path = os.path.join(dirname, filename)
                                    X.append(prepare_image(full_path))
                                    Y.append(0)
                                    if len(Y) % 500 == 0:
                                        print(f'Processing {len(Y)} images')

                                        print(len(X), len(Y))
                                        X = np.array(X)
                                        Y = to_categorical(Y, 2)
                                        X = X.reshape(-1, 128, 128, 3)

                                        X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2,
                                                                                          random_state=5)
                                        X = X.reshape(-1, 1, 1, 1)
                                        print(len(X_train), len(Y_train))
                                        print(len(X_val), len(Y_val))

        return "ok"




    else:
        return render_template('upld_img.html')

@app.route('/logout')
def logout():
    session.clear()
    session['log']=""
    return redirect('/')
if __name__ == '__main__':
    app.run()


