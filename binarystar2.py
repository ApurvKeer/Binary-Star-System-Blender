import bpy
import math

#two star models with motions

class Model_OT(bpy.types.Operator):   
    bl_label = "Add Model Stars"
    bl_idname = "modelstars.addonbasic_operator"

    def execute(self, context):
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(10, 0, 0))
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(-10, 0, 0))

        
        bpy.ops.mesh.primitive_uv_sphere_add(radius = 5, enter_editmode=False, align='WORLD', location=(-8, 0, 0))
        bpy.ops.object.shade_smooth()
        bpy.data.objects["Sphere"].name = "star1"

        bpy.ops.mesh.primitive_uv_sphere_add(radius = 1, enter_editmode=False, align='WORLD', location=(20, 0, 0), rotation = (52, 44, 84))
        bpy.ops.object.shade_smooth()
        bpy.data.objects["Sphere"].name = "star2"

        s1 = bpy.data.objects["star1"]
        s2 = bpy.data.objects["star2"]
        e1 = bpy.data.objects["Empty"]
        e2 = bpy.data.objects["Empty.001"]        
        
        s1.parent = e1
        s2.parent = e2

        bpy.context.scene.frame_set(0)
        e1.keyframe_insert(data_path ="rotation_euler")
        e2.keyframe_insert(data_path ="rotation_euler")

        bpy.context.scene.frame_set(120)
        e1.rotation_euler[2] = math.radians(360) 
        e1.keyframe_insert(data_path ="rotation_euler")
        e2.rotation_euler[2] = math.radians(360) 
        e2.keyframe_insert(data_path ="rotation_euler")
        
        bpy.context.scene.frame_end = 120

        fcurves1 = e1.animation_data.action.fcurves
        for fcurve1 in fcurves1:
            for kf1 in fcurve1.keyframe_points:
                kf1.interpolation = 'LINEAR'
                
        fcurves2 = e2.animation_data.action.fcurves
        for fcurve2 in fcurves2:
            for kf2 in fcurve2.keyframe_points:
                kf2.interpolation = 'LINEAR'        
       
        return {'FINISHED'}

#blue star material

class BlueTexture_OT(bpy.types.Operator):   
    bl_label = "Add Blue Star Texture"
    bl_idname = "bluestar.addonbasic_operator"

    def execute(self, context):
        
        s1 = bpy.data.objects["star1"]
        s2 = bpy.data.objects["star2"]
        
        blue_mat = bpy.data.materials.new(name= "Blue")
        blue_mat.use_nodes = True
        
        bpy.context.object.active_material = blue_mat
        
        principled_node = blue_mat.node_tree.nodes.get('Principled BSDF')        
        principled_node.inputs[7].default_value = 1
        principled_node.location = (0, 300)
        
        mat_out = blue_mat.node_tree.nodes.get('Material Output')
        mat_out.location = (700, 300)
        
        noise1 = blue_mat.node_tree.nodes.new('ShaderNodeTexNoise')
        noise1.location = (-900, 300)
        noise1.inputs[2].default_value = 20.8
        noise1.inputs[4].default_value = 1
        
        noise2 = blue_mat.node_tree.nodes.new('ShaderNodeTexNoise')
        noise2.location = (-900, 0)
        noise2.inputs[2].default_value = 4.8
        noise2.inputs[3].default_value = 16
        noise2.inputs[4].default_value = 0
        
        cramp1 = blue_mat.node_tree.nodes.new('ShaderNodeValToRGB')
        cramp1.location = -600, 300
        cramp1.color_ramp.elements[0].position = 0.359
        cramp1.color_ramp.elements.new(0.493)
        cramp1.color_ramp.elements[1].color = 0, 0.058, 1, 1
        cramp1.color_ramp.elements.new(0.618)
        cramp1.color_ramp.elements[2].color = 0.006, 0.526, 1, 1
        cramp1.color_ramp.elements[3].position = 0.866
        
        cramp2 = blue_mat.node_tree.nodes.new('ShaderNodeValToRGB')
        cramp2.location = -600, 0
        cramp2.color_ramp.elements[0].position = 0.528
        cramp2.color_ramp.elements.new(0.583)
        cramp2.color_ramp.elements[1].color = 0.02, 0, 1, 1
        cramp2.color_ramp.elements.new(0.650)
        cramp2.color_ramp.elements[2].color = 0.039, 0.453, 1, 1
        cramp2.color_ramp.elements[3].position = 0.757
        
        mix_rgb = blue_mat.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_rgb.location = (-300, 100)
        mix_rgb.blend_type = 'ADD'
        mix_rgb.inputs[0].default_value = 1
        
        fresnel = blue_mat.node_tree.nodes.new('ShaderNodeFresnel')
        fresnel.location = (300, 400)
        fresnel.inputs[0].default_value = 1.950
        
        emission = blue_mat.node_tree.nodes.new('ShaderNodeEmission')
        emission.location = (300, 200)
        emission.inputs[0].default_value = (0.017, 0, 1, 1)
        emission.inputs[1].default_value = 3
        
        mix_shader = blue_mat.node_tree.nodes.new('ShaderNodeMixShader')
        mix_shader.location = 500, 300
        
        link = blue_mat.node_tree.links.new
        
        link(noise1.outputs[1], cramp1.inputs[0])
        link(noise2.outputs[1], cramp2.inputs[0])
        link(cramp1.outputs[0], mix_rgb.inputs[1])
        link(cramp2.outputs[0], mix_rgb.inputs[2])
        link(mix_rgb.outputs[0], principled_node.inputs[0])
        link(mix_rgb.outputs[0], principled_node.inputs[17])
        link(principled_node.outputs[0], mix_shader.inputs[1])
        link(fresnel.outputs[0], mix_shader.inputs[0])
        link(emission.outputs[0], mix_shader.inputs[2])
        link(mix_shader.outputs[0], mat_out.inputs[0])
        
        mat = bpy.data.materials["Blue"]
             
        if s1.data.materials:
            s1.data.materials[0] = mat
        else:
            s1.data.materials.append(mat)
            
        if s2.data.materials:
            s2.data.materials[0] = mat
        else:
            s2.data.materials.append(mat)                
                     
        return {'FINISHED'}

class Composite_OT(bpy.types.Operator):   
    bl_label = "Add Glare Effect"
    bl_idname = "composite.addonbasic_operator"

    def execute(self, context):
        
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree

        for node in tree.nodes:
            tree.nodes.remove(node)

        render_layers = tree.nodes.new(type='CompositorNodeRLayers')
        render_layers.location = 0,0
        
        glare = tree.nodes.new(type = 'CompositorNodeGlare')
        glare.location = 500,100
        glare.glare_type = 'FOG_GLOW'
        glare.quality = 'LOW'
        glare.mix = 0.5
        glare.threshold = 0.1
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
       
        return {'FINISHED'}

class Rendering_OT(bpy.types.Operator):   
    bl_label = "Rendering properties"
    bl_idname = "render.addonbasic_operator"

    def execute(self, context):
        
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location = (63.307, -30.028, 5.7311), rotation = (math.radians(82.8), math.radians(22.5), math.radians(60.4)))
        bpy.data.cameras["Camera"].lens = 300
        
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = 0,0,0,1
        
        bpy.context.scene.render.engine = 'CYCLES'

        bpy.context.scene.cycles.samples = 32

       
        return {'FINISHED'}    


classes = [Model_OT, BlueTexture_OT, Composite_OT, Rendering_OT]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

bpy.ops.modelstars.addonbasic_operator()
bpy.ops.bluestar.addonbasic_operator()
bpy.ops.composite.addonbasic_operator()
bpy.ops.render.addonbasic_operator()














