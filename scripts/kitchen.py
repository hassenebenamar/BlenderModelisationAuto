import bpy
import mathutils
import random
import json
import os

# Constants
NUM_RENDERS = 75
OUTPUT_DIR = 'D:/Polytech/5A/TAI/output/First Batch/kitchen'
REFERENCE_OBJECT_NAME = 'Center'  # Name of your reference object (e.g., Camera)

# Movement constraints for specific objects: (x_range, y_range, z_range)
constraints = {
    'washing_machine_001': (0.5, 0.2, 0), 
    'kitchen_table_001': (0.6, 0, 0),
    'scratching_post_001': (0.15, 1.5, 0),
    'fridge_001': (0, 2, 0)
}

# Camera movement ranges
camera_movement_ranges = {
    'Camera': (0, 0, -3.6, 0.9, 0, 0),  # Updated y-range from 2.01 to 6.51
}

# List of objects to exclude from any movement
excluded_objects = {
    'CW1a',
    'CW1a.001',
    'CW1a.002',
    'LIGHT_PENDANT'
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
    Translate relative position to directional terms (reference position would be the center)
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

# Function to generate a random color
def generate_random_color():
    r = random.uniform(0, 1)  # Random float between 0 and 1 for red component
    g = random.uniform(0, 1)  # Random float between 0 and 1 for green component
    b = random.uniform(0, 1)  # Random float between 0 and 1 for blue component
    a = 1.0  # Alpha value fixed at 1
    return [r, g, b, a]

# Function to change the color of an object
def change_object_color(obj, color):
    print(color)
    if obj.data.materials:
        mat = obj.data.materials[0]  # Get the first material
        if mat.use_nodes:
            if 'Principled BSDF' in mat.node_tree.nodes:
                principled_bsdf = mat.node_tree.nodes['Principled BSDF']
                print(principled_bsdf.inputs['Subsurface Color'].default_value)
                principled_bsdf.inputs['Subsurface Color'].default_value = color
                

# Function to get the initial color of an object
def get_initial_object_color(obj):
    if obj.data.materials:
        mat = obj.data.materials[0]  # Get the first material
        if mat.use_nodes:
            if 'Principled BSDF' in mat.node_tree.nodes:
                principled_bsdf = mat.node_tree.nodes['Principled BSDF']
                color = principled_bsdf.inputs['Subsurface Color'].default_value
                colorValue = [round(color[i], 3) for i in range(4)]
                return colorValue

# Function to get the color of an object
def get_object_color(obj):
    if obj.data.materials:
        mat = obj.data.materials[0]  # Get the first material
        if mat.use_nodes:
            if 'Principled BSDF' in mat.node_tree.nodes:
                principled_bsdf = mat.node_tree.nodes['Principled BSDF']
                color = principled_bsdf.inputs['Subsurface Color'].default_value
                colorValue = [round(color[i], 3) for i in range(4)]
                if colorValue == [0.8, 0.8, 0.8, 1]:
                    return "Texture file"
                else:
                    return colorValue


def resetCameraPosition(cameraObj, position):
    if cameraObj:
        cameraObj.location = position


# Store the initial positions
initial_positions = {obj.name: obj.location.copy() for obj in bpy.data.objects if obj.name not in excluded_objects}
initial_colors = {obj.name: get_initial_object_color(obj) for obj in bpy.data.objects if obj.type not in ['CAMERA', 'LIGHT']}

# Store the initial camera position
camera = bpy.data.objects.get('Camera')
initial_camera_position = camera.location.copy()

# Main script
for render_count in range(NUM_RENDERS):
    # Randomize the location of each constrained object
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
        if obj.name != REFERENCE_OBJECT_NAME:
            # Exclude objects like Camera or PointLight from color fetching
            if obj.type not in ['CAMERA', 'LIGHT']:
                color = get_object_color(obj)
            else:
                color = "No color"
            directions = get_direction_from_relative_position(obj.location, mathutils.Vector((0.0, 0.0, 0.0)))
            positions_and_directions[obj.name] = {
                'relative_position': list(obj.location),
                'directions': directions,
                'color': color,
            }

    # Update the scene
    bpy.context.view_layer.update()

    # Define the render file path
    render_file_path = os.path.join(OUTPUT_DIR, f'kitchen_render_{render_count}.png')
    bpy.context.scene.render.filepath = render_file_path
    bpy.ops.render.render(write_still=True)

    # Write positions to a JSON file
    json_file_path = os.path.join(OUTPUT_DIR, f'kitchen_render_{render_count}_positions.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(positions_and_directions, json_file, indent=4)

    # Reset positions for constrained objects
    for obj_name in constraints.keys():
        if obj_name not in excluded_objects:
            obj = bpy.data.objects.get(obj_name)
            if obj:
                obj.location = initial_positions[obj_name]
                if obj_name in initial_colors:
                    initial_color = initial_colors[obj_name]
                    change_object_color(obj, initial_color)

    # # Reset the camera's position
    # resetCameraPosition(camera, initial_camera_position)
    
# Note: You will need to implement logic for resetting positions if required.
