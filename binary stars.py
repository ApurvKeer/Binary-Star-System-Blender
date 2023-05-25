import bpy
import math

bpy.ops.mesh.primitive_uv_sphere_add(radius=2, enter_editmode=False, align='WORLD', location=(-4, 0, 0))
bpy.ops.object.shade_smooth()
bpy.data.objects["Sphere"].name = "star1"

bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(8, 0, 0), rotation = (52, 44, 84))
bpy.ops.object.shade_smooth()
bpy.data.objects["Sphere"].name = "star2"

bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))

s1 = bpy.data.objects["star1"]
s2 = bpy.data.objects["star2"]
c = bpy.data.objects["Empty"]

s1.parent = c
s2.parent = c

bpy.context.scene.frame_set(0)
c.keyframe_insert(data_path ="rotation_euler")

bpy.context.scene.frame_set(120)
c.rotation_euler[2] = math.radians(360) 
c.keyframe_insert(data_path ="rotation_euler")

fcurves = c.animation_data.action.fcurves
for fcurve in fcurves:
    for kf in fcurve.keyframe_points:
        kf.interpolation = 'LINEAR'

       
material_basic = bpy.data.materials.new(name= "Sun")
material_basic.use_nodes = True
        
bpy.context.object.active_material = material_basic
        
principled_node = material_basic.node_tree.nodes.get('Principled BSDF')        
principled_node.inputs[7].default_value = 1
        
mix_rgb = material_basic.node_tree.nodes.new('ShaderNodeMixRGB')
mix_rgb.location = (-300, 300)
mix_rgb.blend_type = 'ADD'
        
hue_sat = material_basic.node_tree.nodes.new('ShaderNodeHueSaturation')
hue_sat.location = (-600, 300)
hue_sat.inputs[0].default_value = 0.49
        
bump = material_basic.node_tree.nodes.new('ShaderNodeBump')
bump.location = (-300, -100)
bump.inputs[0].default_value = 0.125
        
colorramp = material_basic.node_tree.nodes.new('ShaderNodeValToRGB')
colorramp.location = (-800, -100)
colorramp.color_ramp.elements[0].position = (0.359)
colorramp.color_ramp.elements.new(0.458)
colorramp.color_ramp.elements[1].color = (0.5, 0.025, 0.009, 1)
colorramp.color_ramp.elements.new(0.550)
colorramp.color_ramp.elements[2].color = (1, 0.208, 0.003, 1)
colorramp.color_ramp.elements.new(0.667)
colorramp.color_ramp.elements[3].color = (0.75, 0.527, 0.111, 1)
colorramp.color_ramp.elements[4].color = (1, 1, 1, 1)
        
tex_noise = material_basic.node_tree.nodes.new('ShaderNodeTexNoise')
tex_noise.location = (-1100, -300)
tex_noise.inputs[1].default_value = 45
tex_noise.inputs[2].default_value = 32
        
tex_img = material_basic.node_tree.nodes.new('ShaderNodeTexImage')
tex_img.image = bpy.data.images.load(filepath="C:\\Users\\91987\\OneDrive\\Documents\\Blender\\2k_sun.jpg")
#bpy.ops.image.open(filepath="C:\\Users\\91987\\OneDrive\\Documents\\Blender\\2k_sun.jpg", directory="C:\\Users\\91987\\OneDrive\\Documents\\Blender\\", files=[{"name":"2k_sun.jpg", "name":"2k_sun.jpg"}], relative_path=True, show_multiview=False)
tex_img.location = (-1000, 200)

mat_out = material_basic.node_tree.nodes.get('Material Output')
mat_out.location = (1000, 300)
        
fresnel = material_basic.node_tree.nodes.new('ShaderNodeFresnel')
fresnel.location = (400, 400)
fresnel.inputs[0].default_value = 1.250
        
emission = material_basic.node_tree.nodes.new('ShaderNodeEmission')
emission.location = (400, 100)
emission.inputs[0].default_value = (1, 0.211, 0.022, 1)
emission.inputs[1].default_value = 2
        
mix_shader = material_basic.node_tree.nodes.new('ShaderNodeMixShader')
mix_shader.location = (700, 300)
        
link = material_basic.node_tree.links.new
        
link(tex_img.outputs[0], hue_sat.inputs[4])
link(tex_img.outputs[1], bump.inputs[2])
link(tex_noise.outputs[1], colorramp.inputs[0])
link(colorramp.outputs[0], mix_rgb.inputs[2])
link(hue_sat.outputs[0], mix_rgb.inputs[1])
link(bump.outputs[0], principled_node.inputs[19])
link(mix_rgb.outputs[0], principled_node.inputs[0])
link(mix_rgb.outputs[0], principled_node.inputs[17])
link(principled_node.outputs[0], mix_shader.inputs[1])
link(fresnel.outputs[0], mix_shader.inputs[0])
link(emission.outputs[0], mix_shader.inputs[2])
link(mix_shader.outputs[0], mat_out.inputs[0])        
        


mat = bpy.data.materials["Sun"]
             
if s1.data.materials:
    s1.data.materials[0] = mat
else:
    s1.data.materials.append(mat)
    
if s2.data.materials:
    s2.data.materials[0] = mat
else:
    s2.data.materials.append(mat)                
             
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = 0,0,0,1               

bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

for node in tree.nodes:
    tree.nodes.remove(node)

render_layers = tree.nodes.new(type='CompositorNodeRLayers')
render_layers.location = 0,0
        
glare = tree.nodes.new(type = 'CompositorNodeGlare')
glare.location = 500,100
glare.glare_type = 'FOG_GLOW'
glare.quality = 'HIGH'
glare.mix = 0.9
glare.threshold = 0.4
glare.size = 9       
        
filter = tree.nodes.new(type = 'CompositorNodeFilter')
filter.location = 700,-100
filter.filter_type = 'SHARPEN'
filter.inputs[0].default_value = 0.5
        
viewer = tree.nodes.new(type = 'CompositorNodeViewer')
viewer.location = 1000,-100

comp_node = tree.nodes.new('CompositorNodeComposite')   
comp_node.location = 1000,100

links = tree.links
link = links.new(render_layers.outputs[0], glare.inputs[0])
link = links.new(glare.outputs[0], comp_node.inputs[0])
link = links.new(glare.outputs[0], viewer.inputs[0])
link = links.new(glare.outputs[0], filter.inputs[1])
        
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location = (71.781, -130.74, 24.104), rotation = (math.radians(80.8), math.radians(0.00027), math.radians(28.8)))

bpy.data.cameras["Camera"].lens = 300



