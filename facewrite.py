import cv2
import os
import numpy as np
import dlib

# yüz tanıma modeli yükleme
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# yüz tanıma modeli için özellik çıkarımını yapacak fonksiyon
def extract_face_features(image, detector, predictor):
    # görüntüyü gri tonlamalı hale getir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # yüzleri algıla
    faces = detector(gray)
    
    # yüz hatlarını çıkar
    face_features = None
    for face in faces:
        landmarks = predictor(gray, face)
        face_features = np.array([[point.x, point.y] for point in landmarks.parts()])
    
    return face_features

# kayıt yapılacak yüz sayısı
num_of_samples = 10

# kayıt yapılacak kullanıcının adı
user_name = "Ruslan"
# kayıt için görüntüleri al
cap = cv2.VideoCapture(0)

# kullanıcının yüzünü kaydetmek için kullanılacak dizi




threshold = 0.6

if True:
    user_face_features =[]
   # np.load("data.npy".format(user_name))

    for i in range(num_of_samples):
        ret, frame = cap.read()
        if not ret:
            break

        # kullanıcının yüz özelliklerini çıkar
        face_features = extract_face_features(frame, detector, predictor)
        
        
        if face_features is not None:
            user_face_features.append(face_features)
            # kullanıcının yüzüne çerçeve ekle
            x1, y1 = np.min(face_features, axis=0)
            x2, y2 = np.max(face_features, axis=0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

                # kaydedilen yüz sayısını göster
            cv2.putText(frame, "Sample {}".format(i+1), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Kayit Yuzu", frame)

        # 'q' tuşuna basıldığında çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



    # yüz özelliklerini veritabanına kaydet
    if len(user_face_features) == num_of_samples:
        np.save("data.npy".format(user_name), np.array(user_face_features))
        print("Yuz kaydi basariyla kaydedildi!")
    else:
        print("Yuz kaydi yapilamadi!")


cap.release()
cv2.destroyAllWindows()