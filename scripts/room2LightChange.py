import bpy
import mathutils
import random
import json
import os

# Constants
NUM_RENDERS = 55
OUTPUT_DIR = 'D:/Polytech/5A/TAI/output/Fifth Batch/bedroom_sofa_change'
REFERENCE_OBJECT_NAME = 'Center'  # Name of your reference object (e.g., Camera)

# Movement constraints for specific objects: (x_range, y_range, z_range)
constraints = {
    'bed_001': (0.15, 0, 0),  # The bed can only move on the x-axis in a [-0.3, 0.3] range.
    'closet_001': (0, 0.5, 0),  # The closet can only move on the x-axis in a [-0.5, 0.5] range.
    #'sofa_001': (0.35, 0, 0),  # The sofa can only move on the x-axis in a [-0.6, 0.6] range.
    'office_table_001': (0, 0.35, 0)
}

# Camera movement ranges
camera_movement_ranges = {
    'Camera': (0, 0, -3.6, 0.9, 0, 0),  # Updated y-range from 2.01 to 6.51
}

# List of objects to exclude from any movement
excluded_objects = {
    'dumbbell_001',
    'dumbbell_001.001',
    'door_001',
    'LIGHT_PENDANT',
    'CW1a.001',
    'Light.001'
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

# Function to generate a random color
def generate_random_light_color():
    r = random.uniform(0, 1)  # Random float between 0 and 1 for red component
    g = random.uniform(0, 1)  # Random float between 0 and 1 for green component
    b = random.uniform(0, 1)  # Random float between 0 and 1 for blue component
    return [r, g, b]

# Function to get the color of an object
def get_light_color(obj):
    if obj.type == 'LIGHT':
        color = obj.data.color  # get the light color
        colorValues = [round(color[i], 2) for i in range(3)]
        return colorValues

# Function to change the color of an object
def change_light_color(obj, color):
    print("Light new color", color)
    if obj.type == 'LIGHT':
        obj.data.color = color #set the light color

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

light_main = bpy.data.objects.get('Light_main')
light_power = light_main.data.energy
initial_light_color = light_main.data.color

# If the sofa has a material, store its initial color
sofa_obj = bpy.data.objects.get('sofa_001')
closet_obj = bpy.data.objects.get('closet_001')
desk_obj = bpy.data.objects.get('office_table_001')

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

    if light_main:
        color = generate_random_light_color()
        change_light_color(light_main, color)

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
            if obj.type == 'LIGHT':
                color = get_light_color(obj)
                lightPower = obj.data.energy
            elif obj.type == 'CAMERA':
                color = "No color"
            else:
                color = get_object_color(obj)
            directions = get_direction_from_relative_position(obj.location, mathutils.Vector((0.0, 0.0, 0.0)))
            positions_and_directions[obj.name] = {
                'relative_position': list(obj.location),
                'directions': directions,
                'color': color,
            }
            if obj.type == 'LIGHT':
                positions_and_directions[obj.name]['light_power'] = lightPower

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
                if obj_name in initial_colors:
                    initial_color = initial_colors[obj_name]
                    change_object_color(obj, initial_color)
                
    #Reset sofa position
    # if sofa_obj:
    #     sofa_obj.location = initial_positions["sofa_001"]

    # Reset the main light color
    light_main.data.color = (1.0, 1.0, 1.0)
    # # Reset the camera's position
    # resetCameraPosition(camera, initial_camera_position)

    # Reset the sofa's color
    #if sofa_obj and 'sofa_001' in initial_colors:
        #change_object_color(sofa_obj, initial_colors['sofa_001'])

# Note: You will need to implement logic for resetting positions if required.
