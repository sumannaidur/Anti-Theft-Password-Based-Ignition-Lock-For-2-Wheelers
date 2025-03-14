from flask import Flask, jsonify
import cv2
import face_recognition

app = Flask(__name__)

AUTHORIZED_FACE_ENCODING = None  # Load your authorized face encoding here

def load_authorized_face():
    global AUTHORIZED_FACE_ENCODING
    image = face_recognition.load_image_file("naidu.jpg")  # Replace with your image
    AUTHORIZED_FACE_ENCODING = face_recognition.face_encodings(image)[0]

@app.route("/face_unlock", methods=["POST"])
def face_unlock():
    print("Face unlock request received")
    cap = cv2.VideoCapture(0)
    success, frame = cap.read()
    cap.release()

    if not success:
        print("Error accessing camera")
        return jsonify({"status": "ERROR"}), 500

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([AUTHORIZED_FACE_ENCODING], face_encoding)
        if True in matches:
            print("Face recognized successfully")
            return jsonify({"status": "SUCCESS"})

    print("Face not recognized")
    return jsonify({"status": "FAILURE"})

if __name__ == "__main__":
    load_authorized_face()
    app.run(host="0.0.0.0", port=5000)
