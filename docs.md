# Documentation - Blender Modelisation Auto

## Introduction

Le projet se déroule dans le cadre de l'étude de modèle d'apprentissage automatique vision-language (LLM-VM). Afin d'évaluer ce genre de modèles, on utilise généralement des images réelles. 
Cette manière d'évaluer a pour inconvénient de dépendre de données ne pouvant être contrôlées (ex : biais présent dans les données).

Il existe déjà des jeux de données synthétiques en libre accès comme CLEVR mais ces derniers ne sont pas réalistes.

<img src="https://cdn.discordapp.com/attachments/1183508687923453956/1197284426502119524/clevr.jpg?ex=65bab503&is=65a84003&hm=d9193f0ca3edb7d69f54d64b62cd2b442666d0b1909a9bcc1c390ad9e6689e74&" alt="CLEVR" width=75%>

Le but de ce projet est donc de créer de manière semi-automatique un jeu de données constitué d'images de synthèse annotées, réalisées à l'aide de Python et d'un logiciel de modélisation 3D, ici Blender. 

## Documentation du code

Les différents scripts présents dans le dossier "scripts" ont tous la même architecture, seules certains valeurs propres à chaque scène sont modifiées (ainsi que les paths).
Voici le pseudo-code de la fonction principale du programme (ce pseudo-code n'agit que sur les positions des modèles):

<img src="https://cdn.discordapp.com/attachments/1183508687923453956/1197304961554448504/image.png?ex=65bac823&is=65a85323&hm=6a67d2024ce208178ed3f2c8ac48b1cf107aac48ebb99bf8a47a5189feb4c562&" alt="pseudo_code-BlenderModelisation">

### Constants

```python
- NUM_RENDERS # The number of rendering iterations the script will perform.
- OUTPUT_DIR # The directory where the output images and corresponding JSON files will be saved.
- REFERENCE_OBJECT_NAME # The name of the reference object in the scene, used as a reference point for positioning other objects. We currently use the center of the scene.
- constraints # A dictionary defining movement constraints for specific objects. Each key is an object name with a tuple indicating the range of movement in the x, y, and z dimensions.
- camera_movement_ranges # A dictionary indicating the range of movement for the camera. Each key is a camera name with a tuple specifying the minimum and maximum movement in the x, y, and z dimensions.
- excluded_objects # A set of object names that should be excluded from any movement or modifications.
```

### Functions

```python
- randomize_object_location_symmetric(obj, x_range, y_range, z_range)
# Function to randomly change object location within given ranges (in a symmetric manner)
# obj : Blender object
# x_range, y_range, z_range : float
- randomize_object_location_non_symmetric(obj, x_min, x_max, y_min, y_max, z_min, z_max)
# Function to randomly change object location within given ranges (in a non symmetric manner)
# obj : Blender object
# x_min, x_max, y_min, y_max, z_min, z_max : float
- get_direction_from_relative_position(object_position, reference_position)
# Function to translate the relative position to directional terms (reference position is the center (0, 0, 0) in our code)
# object_postion : mathutils.Vector()
# reference_position : mathutils.Vector()
# returns directions : array
- generate_random_color()
# Function to generate a random color
# returns [r, g, b, a] array of random floats
- change_object_color(obj, color)
# Function to change the color of an object
# obj : Blender object
# color : array of floats
- get_initial_object_color(obj)
# Function to get the initial color of an object
# obj : Blender object
# returns colorValue  ([r, g, b, a] array)
- get_object_color(obj)
# Function to get the color of an object
# obj : Blender object
# returns colorValue ([r, g, b, a] array) or the string "Texture file" if the color is an external Texture file.
- resetCameraPositon(cameraObj, position)
# Function to reset the camera position after moving it during runtime.
# cameraObj : Camera Blender Object
# position : mathutils.Vector()
```