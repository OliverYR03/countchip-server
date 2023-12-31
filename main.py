from io import BytesIO
from flask import Flask, jsonify, make_response, request, send_file
from flask_cors import CORS
import cv2
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
cors = CORS(app, supports_credentials=True, expose_headers=['count_chips', 'count_type','Blackcount', ])

@app.route("/", methods=['GET'])
def main_route():
    try:
        return jsonify({'GET': ''})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/countchips')
def modificar_imagen():
    try:
        args = request.args
        count_type = args.get('count_type')
        image = cv2.imread('fichasp.jpeg')
        edges = cv2.Canny(image, 40, 150)
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=30)

        chipsCount = 0
        blackCount = 0
        whiteCount = 0

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                color = image[i[1], i[0]]
                if count_type == "WHITE":
                    if np.mean(color) > 128:
                        chipsCount += 1
                        cv2.circle(image, (i[0], i[1]), i[2], (255, 0, 0), 2)
                        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
                elif count_type == "BLACK":
                    if np.mean(color) < 128:
                        chipsCount += 1
                        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
                elif count_type == "BOTH":
                    if np.mean(color) < 128:
                        blackCount += 1
                        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
                    else:
                        whiteCount += 1
                        cv2.circle(image, (i[0], i[1]), i[2], (255, 0, 0), 2)
                        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
                        
        imagenRgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        img_bytes_io = BytesIO()
        plt.imsave(img_bytes_io, imagenRgb)
        img_bytes_io.seek(0)
        print(f"En el tablero se puede ver la cantidad de fichas negras: {chipsCount}")
        
        response = make_response(send_file(img_bytes_io, mimetype='image/jpeg'))
        response.headers['blackCount'] = blackCount
        response.headers['whiteCount'] = whiteCount
        response.headers['count_chips'] = chipsCount
        response.headers['count_type'] = count_type
        
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
