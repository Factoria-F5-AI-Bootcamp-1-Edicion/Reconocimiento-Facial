from source.recognition import FaceRecognition
# pip install cmake dlib==19.22 -- pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl

if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()