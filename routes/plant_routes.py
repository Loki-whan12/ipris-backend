import base64
import json
from flask import Blueprint, request, jsonify
from db_init import db
from models import Plant
from utils import get_plant_use_wikipedia, get_plant_uses_pfaf
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

plant_bp = Blueprint('plant_bp', __name__)

# Load the trained model from the same directory
model = load_model('plant_classifier_model.h5')

# Create a new plant
@plant_bp.route('/create', methods=['POST'])
def create_plant():
    try:
        data = request.form
        plant_info = data.get('plant_info')
        plant_uses = data.get('plant_uses')
        username = data.get('username')

        # Check types and print a small portion of the data
        print(f'plant_info type: {type(plant_info)}')
        print(f'plant_uses type: {type(plant_uses)}')

        if 'image_data' not in request.files:
            return jsonify({"error": "No image data"}), 400

        file = request.files['image_data']
        filename = file.filename
        image_data = file.read()

        # Parse the JSON strings to dictionaries
        plant_info_dict = json.loads(plant_info) if plant_info else {}
        plant_uses_dict = json.loads(plant_uses) if plant_uses else {}

        # Print the keys of the parsed dictionaries to verify structure
        print(f'plant_info_dict keys: {list(plant_info_dict.keys())}')
        print(f'plant_uses_dict keys: {list(plant_uses_dict.keys())}')

        new_plant = Plant(
            filename=filename,
            image_data=image_data,
            plant_info=json.dumps(plant_info_dict),
            plant_uses=json.dumps(plant_uses_dict),
            username=username,
        )

        db.session.add(new_plant)
        db.session.commit()

        return jsonify({"message": "Plant created successfully"}), 201
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

@plant_bp.route('/<username>', methods=['GET'])
def get_plants_by_username(username):
    try:
        plants = Plant.query.filter_by(username=username).all()
        if not plants:
            return jsonify({"error": "No plants found for the user"}), 404
        
        plants_data = []
        for plant in plants:
            # Debugging output
            print(f'Retrieved plant_info (raw): {type(plant.plant_info)}')
            print(f'Retrieved plant_uses (raw): {type(plant.plant_uses)}')
            
            plant_info = plant.plant_info
            plant_uses = plant.plant_uses
            
            # Parse only if they are strings
            if isinstance(plant_info, str):
                plant_info_dict = json.loads(plant_info)
            else:
                plant_info_dict = plant_info
            
            if isinstance(plant_uses, str):
                plant_uses_dict = json.loads(plant_uses)
            else:
                plant_uses_dict = plant_uses

            # Verify conversion
            print(f'Converted plant_info: {type(plant_info_dict)}')
            print(f'Converted plant_uses: {type(plant_uses_dict)}')
            
            
            plants_data.append({
                'id': plant.id,
                'filename': plant.filename,
                'image_data': base64.b64encode(plant.image_data).decode('utf-8'),
                'plant_info': plant_info_dict,
                'plant_uses': plant_uses_dict,
                'username': plant.username
            })

        return jsonify(plants_data), 200
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


# Get all plants
@plant_bp.route('/all', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    if plants:
        return jsonify([{'id': plant.id, 'filename': plant.filename,
                         'image_data': base64.b64encode(plant.image_data).decode('utf-8'),
                         'plant_info': plant.plant_info, 'plant_uses': plant.plant_uses, 'username': plant.username} for plant in plants])
    return jsonify({'message': 'No plant found'}), 404


# Check if a plant has been uploaded before
@plant_bp.route('/count/<string:username>', methods=['GET'])
def plant_count(username):
    plant_count = db.session.query(Plant).filter_by(username=username).count()
    if plant_count == 0:
        return jsonify({'message': 'No plant saved'}), 404
    return jsonify({'plant_count': plant_count}), 200


# Delete a plant
@plant_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if plant is None:
        return jsonify({'message': 'Plant not found'}), 404
    db.session.delete(plant)
    db.session.commit()
    return jsonify({'message': 'Plant deleted successfully'}), 200

@plant_bp.route('/uses/<string:common_name>/<string:botanical_name>', methods=['GET'])
def plant_uses(common_name, botanical_name):
    if "-" in common_name:
        common_name = common_name.replace('-', ' ')
    if '-' in botanical_name:
        botanical_name = botanical_name.replace('-', ' ')
    uses = get_plant_uses_pfaf(common_name, botanical_name)
    if uses:
        return jsonify({'plant_uses': uses, 'type': 'dict'}), 200
    else:
        wikipedia_info = get_plant_use_wikipedia(common_name)
        return jsonify({'plant_uses': wikipedia_info, 'type': 'dict'}), 200
    
@plant_bp.route('/check-if-plant/', methods=['POST'])
def check_if_plant():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Prepare the image for prediction
        img = image.load_img(file, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize the image

        # Make a prediction
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions[0]) 
        confidence = np.max(predictions)

        # Set a threshold to determine if it's a plant
        confidence_threshold = 0.5

        if confidence < confidence_threshold:
            result = "Not a plant"
        else:
            # Convert class_indices to a list of class names
            class_names = list(train_generator.class_indices.keys())

            # Get the corresponding class name
            result = class_names[predicted_class]

        return jsonify({"result": result, "confidence": confidence}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
  