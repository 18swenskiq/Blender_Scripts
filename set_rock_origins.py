import bpy
import mathutils

print("-----------------------------------------------")
print("Squidski's rock climbing grip origin stabilizer")
print("Made because I'm not moving all those verts back to the edge ring myself!")
print("-----------------------------------------------")

# I don't actually know how much of this context stuff is needed, but I copied it from the internet and it works now
area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
override_context = bpy.context.copy()
override_context['window'] = bpy.context.window
override_context['screen'] = bpy.context.screen
override_context['area'] = area
override_context['region'] = area.regions[-1]
override_context['scene'] = bpy.context.scene
override_context['space_data'] = area.spaces.active

rocks = override_context['editable_objects']

# This won't make sense if you are using this for anything other than rock climbing, sorry
print(f"{len(rocks)} objects")

bpy.ops.object.mode_set(mode='OBJECT')

# Vertices of the default cube, we don't want these in origin calculations
undesirable_vertices = []

# Unselect everything
for ob in bpy.data.objects:
    ob.select_set(False)
    
    # If this object is the default cube, put the coordinates of all of its vertices into undesirable_vertices
    if(ob.data.name == 'Cube.001'):
        for c_vert in ob.data.vertices:
            undesirable_vertices.append(c_vert.co)

# Hmm I kinda wanna select everything again
for ob in rocks:
    
    
    print(f"Processing rock #{rocks.index(ob)}...")
    
    ob.select_set(True)
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='EDGE')
    
    # This selects the "open" edges
    bpy.ops.mesh.select_non_manifold()
    
    bpy.ops.mesh.select_mode(type='VERT')
    
    verts = ob.data.vertices
    
    average_these = []
    
    # Now we need to iterate over every vert we have selected and put them in an array so we can get their average
    for vert in verts:
        
        # If the vert is of the cube, ditch it
        if(vert.co in undesirable_vertices):
            continue
        
        # Edge ring confirmed, put the verts in an array so I can get the average positions
        if(vert.select == True):
            average_these.append(vert)
        
    # Get middle of the points
    total_points = 0
    x = 0
    y = 0
    z = 0
    
    for avg in average_these:
        x += avg.co[0]
        y += avg.co[1]
        z += avg.co[2]
        total_points += 1
        
    middle_point = mathutils.Vector((x/total_points, y/total_points, z/total_points))
    
    bpy.context.scene.cursor.location = middle_point
    
    print(bpy.context.scene.cursor.location)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    ob.select_set(False)
    #break
    #bpy.context.scene.cursor.location = 
    
    #ob.select_set(False)