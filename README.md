# IA- Contador de Fichas 
Este proyecto está realizado con las siguientes tecnologías:
+ Python
+ Flask
+ Flask_Cors
+ OpenCV
+ Numpy
+ Matplotlib
---

# Guía de uso de nuestra IA

## Paso 1: Creación del entorno virtual
Para trabajar con un entorno virtual vamos a ejecutar el siguiente comando en la terminal.

```bash
python -m venv venv
```
## Paso 2:  Activación del entorno virtual
Para instalar las dependecías, primero vamos a activar el entorno virtual

```bash
venv/Scripts/activate
```

## Paso 3:  Instalación de dependencias
Para la correcta instalación de las dependencias necesarias vamos a ejecutar el siguiente comando en la terminar

```bash
pip install -r requirements.txt
```

## Paso 4: Ejecución del servidor Flask
Para la ejecución de nuestro servidor Flask, ejecutaremos:

```bash
flask --app main run
```
---

# Documentación:

## Importación de librerías

Importación de librerías necesarías para la ejecución de nuestro proyecto.

```bash
from io import BytesIO
from flask import Flask, jsonify, make_response, request, send_file
from flask_cors import CORS
import cv2
import numpy as np
import matplotlib.pyplot as plt
```

## Declaración de la app y exposición de los headers a través de Cors:

Estas 2 lineas nos permite trabajar con los headers a través de un front como React o Angular

```bash
app = Flask(__name__)
cors = CORS(app, supports_credentials=True, expose_headers=['count_chips', 'count_type','Blackcount', ])
```

## Definición de ruta Main (/)

Esta ruta se mostrará como principal a través de la web, dónde para visualizar un correcto despliegue se mostrará un json GET: ' '.

```bash
@app.route("/", methods=['GET'])
def main_route():
    try:
        return jsonify({'GET': ''})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

## Definición de ruta (/countchips)

Definición de la ruta de nuestro identificador de fichas con inteligencia artificial

```bash
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
```
---
#### Creación de variables

Creación de variables donde:
+ `args = request.args`: Requerimos una argumento que se obtiene a través de la URL.
+ `count_type = args.get('count_type')`: Asignamos el nombre de la variables como count_type.
+ `image = cv2.imread('fichasp.jpeg')`: Creamos la variable para la imagen y pedimos a cv2 que lo lea.
+ `edges = cv2.Canny(image, 40, 150)`: Creamos la variable edge para la detección de bordes con Cv2.Canny.
+ `circles = cv2.HoughCircles(...`: Establecemos los parametros de los circulos con cv2.HoughCircles.

+ `chipsCount = 0 ...`: Declaración de variables para almacenar la cantidad de fichas por color y juntas.
```bash
        args = request.args
        count_type = args.get('count_type')
        image = cv2.imread('fichasp.jpeg')
        edges = cv2.Canny(image, 40, 150)
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=30)

        chipsCount = 0
        blackCount = 0
        whiteCount = 0
```

### Condicional para buscar fichas

Con este bucle iteraremos en la imagen con la finalidad de buscar fichas con el diametro que hemos establecido anteriormente

```bash
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
```
---

#### Condicional

Comprobamos si la variable circles está vacía 

```bash
if circles is not None:
    circles = np.uint16(np.around(circles))
```

#### bucle for

Esta línea itera sobre cada círculo detectado. Se asume que circles es un array de NumPy donde cada fila contiene información sobre un círculo detectado.

```bash
for i in circles[0, :]:
        color = image[i[1], i[0]]
```

#### Condicional Count_type

Esta linea comprueba si el argumento obtenido a través del header, donde por cada color imprimirá un color de borde diferente y contará la cantidad de fichas que se encuentren.

Donde:  
+ ``count_type == "WHITE"`` En caso de que el usuario digite BLANCO, se mostrará un color azul e incrementará la variable chipsCount en +1
+ ``count_type == "BLACK"`` En caso de que el usuario digite NEGRO, se mostrará un color rojo e incrementará la variable chipsCount en +1
+ ``count_type == "BOTH"`` En caso de que el usuario digite AMBOS, se realizará una condicional donde por cada color se mostrará un borde diferente y se incrementarán las variables blackCount +1 y whiteCount +1

```bash
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
```

#### Conversión de la imagen en variable a JPEG para mostrarse en la web

Con estas lineas podremos visualizar la imagen de python en nuestra web

```bash
      imagenRgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
      img_bytes_io = BytesIO()
      plt.imsave(img_bytes_io, imagenRgb)
      img_bytes_io.seek(0)
      print(f"En el tablero se puede ver la cantidad de fichas negras: {chipsCount}")
```

#### Declaración de HEADERS como respuesta para el front

En estas lineas establecemos los response headers y retornarnos nuestro response.

```bash
      response = make_response(send_file(img_bytes_io, mimetype='image/jpeg'))
      response.headers['blackCount'] = blackCount
      response.headers['whiteCount'] = whiteCount
      response.headers['count_chips'] = chipsCount
      response.headers['count_type'] = count_type
        
        return response
```

#### Exception

Devolución de un exception en caso de encontrarnos con un problema

```bash
    except Exception as e:
            return jsonify({'error': str(e)}), 500
```

#### Final

Aseguramos que el servidor Flask solo se inicie cuando ejecutas directamente este script

```bash
if __name__ == '__main__':
    app.run(debug=True)
``
