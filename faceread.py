import cv2
import os
import numpy as np
import dlib

# yüz tanıma modeli yükleme
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# yüz özelliklerini çıkaracak fonksiyon
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

# kayıt yapılan yüz verilerini yükle
user_name = "Ruslan"
user_face_features = np.load("data.npy".format(user_name))


# eşleşme için belirlenen threshold değeri
threshold = 0.6

# kamera açma
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # kullanıcının yüz özelliklerini çıkar
    face_features = extract_face_features(frame, detector, predictor)

    # yüz özelliklerini kaydedilen yüz verileriyle karşılaştır
    if face_features is not None:
        match_scores = []
        #for user_face_feature in user_face_features:
            # öklid uzaklığı hesapla
        dist = np.linalg.norm(user_face_features - face_features)
        match_scores.append(dist)


       
        # eşleşme oranını kontrol et
        if np.min(match_scores) < threshold:
            # eşleşme olduğunda mesaj yazdır
            cv2.putText(frame, "Hosgeldiniz {}".format(user_name), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # eşleşme olmadığında uyarı yazdır
            cv2.putText(frame, "Kimliginiz dogrulanamadi!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Yuz Tanima", frame)

    # 'q' tuşuna basıldığında çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
