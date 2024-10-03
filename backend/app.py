from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from flask_cors import CORS
from apps.calculator.utils import analyze_image
from schema import ImageData

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

@app.route('/')
def root():
    return jsonify({"message": "Server is running"})

@app.route('/calculate', methods=['POST'])
def run():
    # Parse incoming JSON request body
    data = request.get_json()
    
    # Decode the image data
    image_data = base64.b64decode(data['image'].split(",")[1])  # Assumes data:image/png;base64,<data>
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)
    
    # Analyze the image with the utility function
    responses = analyze_image(image, dict_of_vars=data['dict_of_vars'])
    
    # Prepare the response
    response_data = [response for response in responses]
    print('response in route: ', response_data)
    
    return jsonify({"message": "Image processed", "data": response_data, "status": "success"})

if __name__ == "__main__":
    app.run(host='localhost', port=8900, debug=True)
