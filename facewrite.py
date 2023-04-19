import time
import cv2
import face_recognition
import os

# tanınan yüzlerin özellikleri
known_faces = []

# tanınan yüzlerin isimleri
known_names = []

# tanınan yüzlerin kaydedileceği dosya yolu
known_faces_dir = 'known_faces'

# tanınan yüzlerin dosya uzantısı
file_extension = '.jpg'

# önceden kaydedilmiş yüzleri oku
for filename in os.listdir(known_faces_dir):
    name = os.path.splitext(filename)[0]
    known_names.append(name)

    file_path = os.path.join(known_faces_dir, filename)
    image = face_recognition.load_image_file(file_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(face_encoding)

# canlı video akışı yakalayıcısı
cap = cv2.VideoCapture(0)

while True:
    # video akışından bir kare al
    ret, frame = cap.read()
    
    # kareyi yüzleri tanımak için işle
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # yüzleri tanımla ve kaydet
    for face_encoding, face_location in zip(face_encodings, face_locations):
        # yüz tanıma işlemi
        matches = face_recognition.compare_faces(known_faces, face_encoding)

        # yüzü tanımak için kullanılan en iyi eşleşmenin dizini
        best_match_index = -1
        best_match_distance = 1.0

        for i in range(len(matches)):
            if matches[i]:
                face_distance = face_recognition.face_distance([known_faces[i]], face_encoding)[0]
                if face_distance < best_match_distance:
                    best_match_index = i
                    best_match_distance = face_distance

        # yüzü kaydetmek için eğer tanınmadıysa
        if best_match_index == -1:
            # yüzü tanımlamak için bir isim girdisi al
            name = input("Yeni bir yüz tanımlandı, lütfen ismini girin: ")

            # yüzü kaydet
            known_faces.append(face_encoding)
            known_names.append(name)

            # yüzü dosya olarak kaydet
            file_path = os.path.join(known_faces_dir, name + file_extension)
            cv2.imwrite(file_path, frame)

            print(f"{name} isimli yüz kaydedildi.")

        # yüz daha önce kaydedilmişse dosya ismini yazdır
        else:
            name = known_names[best_match_index]
            print(f"{name} isimli yüz tanındı.")

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)

            # yüz ismini dikdörtgenin üstüne yaz
            cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)


    # kareyi ekranda göster
    cv2.imshow('Video', frame)

    # q tuşuna basarak çıkış yap
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
