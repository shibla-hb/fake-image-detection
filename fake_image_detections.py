from flask import Flask, render_template, request, session, redirect
import datetime
from DBConnection import Db

import numpy as np
import matplotlib.pyplot as plt
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
        path1 = "/static/upld_images/" + date + '.jpg'

        def convert_to_ela_image(path, quality):
            temp_filename = 'temp_file_name.jpg'
            ela_filename = 'temp_ela.png'

            image = Image.open(path1).convert('RGB')
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

        real_image_path = r'C:\Users\HP\PycharmProjects\fake_image_detections\static\upld_images'
        Image.open(real_image_path)

        convert_to_ela_image(real_image_path, 90)

        fake_image_path = r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Tp\Tp_D_NRN_S_N_ani10171_ani00001_12458.jpg'
        Image.open(fake_image_path)

        convert_to_ela_image(fake_image_path, 90)

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

                                        def build_model():
                                            model = Sequential()
                                            model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='valid',
                                                             activation='relu', input_shape=(128, 128, 3)))
                                            model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='valid',
                                                             activation='relu', input_shape=(128, 128, 3)))
                                            model.add(MaxPool2D(pool_size=(2, 2)))
                                            model.add(Dropout(0.25))
                                            model.add(Flatten())
                                            model.add(Dense(256, activation='relu'))
                                            model.add(Dropout(0.5))
                                            model.add(Dense(2, activation='softmax'))
                                            return model

                                        model = build_model()
                                        model.summary()
                                        epochs = 30
                                        batch_size = 32
                                        init_lr = 1e-4
                                        optimizer = Adam(lr=init_lr, decay=init_lr / epochs)
                                        model.compile(optimizer=optimizer, loss='binary_crossentropy',
                                                      metrics=['accuracy'])
                                        early_stopping = EarlyStopping(monitor='val_acc',
                                                                       min_delta=0,
                                                                       patience=2,
                                                                       verbose=0,
                                                                       mode='auto')
                                        hist = model.fit(X_train,
                                                         Y_train,
                                                         batch_size=batch_size,
                                                         epochs=epochs,
                                                         validation_data=(X_val, Y_val),
                                                         callbacks=[early_stopping])
                                        model.save(r'C:\Users\IDZ\Downloads\FakeImageDetector_master\model_casia_run1.h5')

                                        fig, ax = plt.subplots(2, 1)
                                        ax[0].plot(hist.history['loss'], color='b', label="Training loss")
                                        ax[0].plot(hist.history['val_loss'], color='r', label="validation loss",
                                                   axes=ax[0])
                                        legend = ax[0].legend(loc='best', shadow=True)

                                        ax[1].plot(hist.history['accuracy'], color='b', label="Training accuracy")
                                        ax[1].plot(hist.history['val_accuracy'], color='r', label="Validation accuracy")
                                        legend = ax[1].legend(loc='best', shadow=True)

                                        def plot_confusion_matrix(cm, classes,
                                                                  normalize=False,
                                                                  title='Confusion matrix',
                                                                  cmap=plt.cm.Blues):
                                            """
                                            This function prints and plots the confusion matrix.
                                            Normalization can be applied by setting `normalize=True`.
                                            """
                                            plt.imshow(cm, interpolation='nearest', cmap=cmap)
                                            plt.title(title)
                                            plt.colorbar()
                                            tick_marks = np.arange(len(classes))
                                            plt.xticks(tick_marks, classes, rotation=45)
                                            plt.yticks(tick_marks, classes)

                                            if normalize:
                                                cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

                                            thresh = cm.max() / 2.
                                            for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
                                                plt.text(j, i, cm[i, j],
                                                         horizontalalignment="center",
                                                         color="white" if cm[i, j] > thresh else "black")
                                            plt.tight_layout()
                                            plt.ylabel('True label')
                                            plt.xlabel('Predicted label')

                                            # Predict the values from the validation dataset
                                            Y_pred = model.predict(X_val)
                                            # Convert predictions classes to one hot vectors
                                            Y_pred_classes = np.argmax(Y_pred, axis=1)
                                            # Convert validation observations to one hot vectors
                                            Y_true = np.argmax(Y_val, axis=1)
                                            # compute the confusion matrix
                                            confusion_mtx = confusion_matrix(Y_true, Y_pred_classes)
                                            # plot the confusion matrix
                                            plot_confusion_matrix(confusion_mtx, classes=range(2))

                                            class_names = ['fake', 'real']
                                            real_image_path = r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Au\Au_ani_00001.jpg'
                                            image = prepare_image(real_image_path)
                                            image = image.reshape(-1, 128, 128, 3)
                                            y_pred = model.predict(image)
                                            y_pred_class = np.argmax(y_pred, axis=1)[0]
                                            print(f'Class: {class_names[y_pred_class]} Confidence: {np.amax(y_pred) * 100:0.2f}')

                                            fake_image_path = r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Tp\Tp_D_NRN_S_N_ani10171_ani00001_12458.jpg'
                                            image = prepare_image(fake_image_path)
                                            image = image.reshape(-1, 128, 128, 3)
                                            y_pred = model.predict(image)
                                            y_pred_class = np.argmax(y_pred, axis=1)[0]
                                            print(f'Class: {class_names[y_pred_class]} Confidence: {np.amax(y_pred) * 100:0.2f}')

                                            fake_image = os.listdi(r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Tp\\')
                                            correct = 0
                                            total = 0
                                            for file_name in fake_image:
                                                if file_name.endswith('jpg') or filename.endswith('png'):
                                                    fake_image_path = os.path.join(
                                                        r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Tp\\',
                                                        file_name)
                                                    image = prepare_image(fake_image_path)
                                                    image = image.reshape(-1, 128, 128, 3)
                                                    y_pred = model.predict(image)
                                                    y_pred_class = np.argmax(y_pred, axis=1)[0]
                                                    total += 1
                                                    if y_pred_class == 0:
                                                        correct += 1
                                                        #             print(f'Class: {class_names[y_pred_class]} Confidence: {np.amax(y_pred) * 100:0.2f}')

                                                        print(f'Total: {total}, Correct: {correct}, Acc: {correct / total * 100.0}')
                                                        real_image = os.listdir(r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Au\\')
                                                        correct_r = 0
                                                        total_r = 0

                                                        for file_name in real_image:
                                                            if file_name.endswith('jpg') or filename.endswith('png'):
                                                                real_image_path = os.path.join(
                                                                    r'C:\Users\IDZ\Downloads\FakeImageDetector_master\casia\CASIA2\Au\\',
                                                                    file_name)
                                                                image = prepare_image(real_image_path)
                                                                image = image.reshape(-1, 128, 128, 3)
                                                                y_pred = model.predict(image)
                                                                y_pred_class = np.argmax(y_pred, axis=1)[0]
                                                                total_r += 1
                                                                if y_pred_class == 1:
                                                                    correct_r += 1
                                                                    #             print(f'Class: {class_names[y_pred_class]} Confidence: {np.amax(y_pred) * 100:0.2f}')

                                                                    correct += correct_r
                                                                    total += total_r
                                                                    print(
                                                                        f'Total: {total_r}, Correct: {correct_r}, Acc: {correct_r / total_r * 100.0}')
                                                                    print(
                                                                        f'Total: {total}, Correct: {correct}, Acc: {correct / total * 100.0}')

        # return "ok"




    else:
        return render_template('upld_img.html')

@app.route('/logout')
def logout():
    session.clear()
    session['log']=""
    return redirect('/')
if __name__ == '__main__':
    app.run()


