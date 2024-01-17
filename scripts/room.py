import bpy
import random
import json
import os

# Constants
NUM_RENDERS = 8
OUTPUT_DIR = 'D:/Polytech/5A/TAI/output/'
REFERENCE_OBJECT_NAME = 'Camera'  # Name of your reference object (e.g., Camera)

# Movement constraints for specific objects: (x_range, y_range, z_range)
constraints = {
    # 'bed_001': (0.3, 0.5, 0),  # The bed can only move on the x-axis in a [-0.3, 0.3] range.
    'closet_001': (0, 0.35, 0),  # The closet can only move on the x-axis in a [-0.5, 0.5] range.
    # 'sofa_001': (0.6, 0, 0),  # The sofa can only move on the x-axis in a [-0.6, 0.6] range.
    'lamp_001': (0, 0.25, 0)
}

# Camera movement ranges
camera_movement_ranges = {
    'Camera': (0, 0, -3.6, 0.9, 0, 0),  # Updated y-range from 2.01 to 6.51
}

# List of objects to exclude from any movement
excluded_objects = {
    'dumbbell_001',
    'dumbbell_001.001',
    'door_001'
}


# Function to randomly change object location within given ranges
def randomize_object_location_symmetric(obj, x_range, y_range, z_range):
    obj.location.x += random.uniform(-x_range, x_range) if x_range != 0 else 0
    obj.location.y += random.uniform(-y_range, y_range) if y_range != 0 else 0
    obj.location.z += random.uniform(-z_range, z_range) if z_range != 0 else 0


# Function to randomly change object location within given non-symmetric ranges
def randomize_object_location_non_symmetric(obj, x_min, x_max, y_min, y_max, z_min, z_max):
    obj.location.x += random.uniform(x_min, x_max)
    obj.location.y += random.uniform(y_min, y_max)
    obj.location.z += random.uniform(z_min, z_max)

def get_direction_from_relative_position(object_position, reference_position):
    """
    Translate relative position to directional terms.
    """
    rel_x = object_position.x - reference_position.x
    rel_y = object_position.y - reference_position.y
    rel_z = object_position.z - reference_position.z

    directions = []

    if rel_x > 0:
        directions.append('right')
    elif rel_x < 0:
        directions.append('left')

    if rel_y > 0:
        directions.append('front')
    elif rel_y < 0:
        directions.append('back')

    if rel_z > 0:
        directions.append('up')
    elif rel_z < 0:
        directions.append('down')

    return directions if directions else ['center']

# Function to change the color of an object
def change_object_color(obj, color):
    if obj.data.materials:
        mat = obj.data.materials[0]  # Get the first material
        if mat.use_nodes:
            if 'Principled BSDF' in mat.node_tree.nodes:
                principled_bsdf = mat.node_tree.nodes['Principled BSDF']
                principled_bsdf.inputs['Subsurface Color'].default_value = color


def resetCameraPosition(cameraObj, position):
    if cameraObj:
        cameraObj.location = position


# Store the initial positions
initial_positions = {obj.name: obj.location.copy() for obj in bpy.data.objects if obj.name not in excluded_objects}
initial_colors = {}

# Store the initial camera position
camera = bpy.data.objects.get('Camera')
initial_camera_position = camera.location.copy()

# If the sofa has a material, store its initial color
sofa_obj = bpy.data.objects.get('sofa_001')

# Main script
for render_count in range(NUM_RENDERS):
    # Randomize the location of each constrained object
    # Change the sofa's color
    # if sofa_obj:
    #     print("Changing color of sofa")
    #     specific_color = [0.865, 0.418, 1.0, 1.0]  # RGBA
    #     change_object_color(sofa_obj, specific_color)

    # Collect positions and directions in a dictionary
    positions_and_directions = {}

    for obj_name, (x_range, y_range, z_range) in constraints.items():
        if obj_name not in excluded_objects:
            obj = bpy.data.objects.get(obj_name)
            if obj:
                randomize_object_location_symmetric(obj, x_range, y_range, z_range)
                positions_and_directions[obj_name] = list(obj.location)

    # if camera:
    #     x_min, x_max, y_min, y_max, z_min, z_max = camera_movement_ranges['Camera']
    #     randomize_object_location_non_symmetric(camera, x_min, x_max, y_min, y_max, z_min, z_max)
    #
    # # Format camera position for the file name
    # cameraPosition = camera.location
    # cameraPosition_str = '_'.join(f'{coord:.4f}' for coord in cameraPosition)

        # Get reference object position
        reference_object = bpy.data.objects.get(REFERENCE_OBJECT_NAME)
        reference_position = reference_object.location if reference_object else None

        # Collect relative positions and directions in a dictionary for all objects
        positions_and_directions = {}
        for obj in bpy.data.objects:
            # Exclude the camera
            if obj.name != REFERENCE_OBJECT_NAME:
                relative_position = obj.location - reference_position
                directions = get_direction_from_relative_position(obj.location, reference_position)
                positions_and_directions[obj.name] = {
                    'relative_position': list(relative_position),
                    'directions': directions
                }

    # Update the scene
    bpy.context.view_layer.update()

    # Define the render file path
    render_file_path = os.path.join(OUTPUT_DIR, f'bedroom_render_{render_count}.png')
    bpy.context.scene.render.filepath = render_file_path
    bpy.ops.render.render(write_still=True)

    # Write positions to a JSON file
    json_file_path = os.path.join(OUTPUT_DIR, f'bedroom_render_{render_count}_positions.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(positions_and_directions, json_file, indent=4)

    # Reset positions for constrained objects
    for obj_name in constraints.keys():
        if obj_name not in excluded_objects:
            obj = bpy.data.objects.get(obj_name)
            if obj:
                obj.location = initial_positions[obj_name]

    # # Reset the camera's position
    # resetCameraPosition(camera, initial_camera_position)

    # # Reset the sofa's color
    # if sofa_obj and 'sofa_001' in initial_colors:
    #     change_object_color(sofa_obj, initial_colors['sofa_001'])

# Note: You will need to implement logic for resetting positions if required.
