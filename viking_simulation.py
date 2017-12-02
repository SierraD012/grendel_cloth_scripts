# Authors: Brennan Mitchell, Sierra Davis, Ben Romney
import os

import maya
import maya.mel as mel
import pymel.core as pc
import maya.cmds as mc

from byuam.project import Project
from byuam.environment import Department, Environment

STARTANIM = 1
STARTPRE = -50


#########################
## ESTABLISH CFX SCENE ##
#########################

def generateScene():
    project = Project()
    environment = Environment()

    # Create a global position locator for viking's starting location
    mc.currentTime(STARTPRE)
    globalPos = mc.spaceLocator(p=[0,0,0])
    globPos = mc.rename(globalPos, "vikingGlobalPos")
    mc.select("viking_rig_main_Viking_primary_global_cc_01")
    mc.select(globPos, add=True)
    mc.pointConstraint(offset=[0,0,0], weight=1) #constrains the globPos position to where viking's rig_main is
    mc.orientConstraint(offset=[0,0,0], weight=1) #orients the globPos to match viking's rig_main (I think it just does the rotation)

    # Get transformation variables from globPos locator
    global tx
    global ty
    global tz
    global rx
    global ry
    global rz
    tx = mc.getAttr(globPos+".translateX")
    ty = mc.getAttr(globPos+".translateY")
    tz = mc.getAttr(globPos+".translateZ")
    rx = mc.getAttr(globPos+".rotateX")
    ry = mc.getAttr(globPos+".rotateY")
    rz = mc.getAttr(globPos+".rotateZ")

    # get alembic filepath for scene's animation (requires prior export)
    src = mc.file(q=True, sceneName=True)
    src_dir = os.path.dirname(src)
    checkout_element = project.get_checkout_element(src_dir)
    checkout_body_name = checkout_element.get_parent()
    body = project.get_body(checkout_body_name)
    element = body.get_element(Department.ANIM)
    cache_name = "viking_with_facial_rig_main" # this is me doing it arbitrarily but I think the preroll script picks its own name
    cache_file = os.path.join(element.get_dir(), "cache", cache_name + ".abc")
    print("Expecting mesh alembic with name " + cache_name)
    # we could make a while loop to check if an alembic with this name exists already, if it does increment a suffix number on the filename

    # checkout cfx scene for corresponding shot number
    current_user = environment.get_current_username()
    element = body.get_element(Department.CFX)
    cfx_filepath = element.checkout(current_user)
    print(">GenScene(): cfx_filepath= " + cfx_filepath) # see where it's expecting the file to be/what it's called
    print(">GenScene(): cache_file= " + cache_file) # this is where ABCimporter expects the character geo abc to be

    # open cfx file
    if cfx_filepath is not None:
        if not mc.file(q=True, sceneName=True) == '':
            mc.file(save=True, force=True) #save file

        if not os.path.exists(cfx_filepath): #make a new CFX scene file
            print(">GenScene(): CFX scene doesn't exist yet. Creating a new one")
            mc.file(new=True, force=True)
            mc.file(rename=cfx_filepath)
            mc.file(save=True, force=True)
        else:
             mc.file(cfx_filepath, open=True, force=True)

    # import alembic
    command = "AbcImport -mode import \"" + cache_file + "\""

    maya.mel.eval(command)

    #### PULL IN REFERENCE OBJECTS ####
    getReferenceObjects(project)

    # Set full tunic group transforms to match viking's alembic
    mc.setAttr("viking_tunic_model_main_tunic.translateX", tx)
    mc.setAttr("viking_tunic_model_main_tunic.translateY", ty)
    mc.setAttr("viking_tunic_model_main_tunic.translateZ", tz)
    mc.setAttr("viking_tunic_model_main_tunic.rotateX", rx)
    mc.setAttr("viking_tunic_model_main_tunic.rotateY", ry)
    mc.setAttr("viking_tunic_model_main_tunic.rotateZ", rz)

    #Set collisionMesh transforms to match viking's alembic
    mc.setAttr("viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth.translateX", tx)
    mc.setAttr("viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth.translateY", ty)
    mc.setAttr("viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth.translateZ", tz)
    mc.setAttr("viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth.rotateX", rx)
    mc.setAttr("viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth.rotateY", ry)
    mc.setAttr("viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth.rotateZ", rz)


def getReferenceObjects(project):
    #Reference viking's CollisionMesh
    body = project.get_body("viking_collision_mesh_cloth")
    element = body.get_element(Department.MODEL)
    collisionMesh_file = element.get_app_filepath()
    mc.file(collisionMesh_file, reference=True)

    # Reference viking's tunic - it comes with both sim and beauty meshes
    body = project.get_body("viking_tunic")
    element = body.get_element(Department.MODEL)
    tunic_sim_file = element.get_app_filepath()
    mc.file(tunic_sim_file, reference=True)

    #Should also import the bracelet alembic too?


#######################
##       MAIN        ##
#######################

generateScene()

#######################
## Set Up Simulation ##
#######################

mc.select('viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth', replace=True)
mc.viewFit() #Snap View to Body Collider
mc.playbackOptions(animationStartTime=STARTPRE)
mc.playbackOptions(minTime=STARTPRE)
mc.currentTime(STARTPRE)

#### Establish Colliders ###
mc.select('viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth', replace=True) #Collider Body
mel.eval('makeCollideNCloth;')
mc.setAttr('nRigid1.thickness', 0.001)


#### Establish nCloth Objects ####
mc.select('viking_tunic_model_main_tunic_sim_mesh', replace=True) #nCloth: tunic
mel.eval('createNCloth 0;')

mc.setAttr('nClothShape1.thickness', 0.008) #Collision Properties
mc.setAttr('nClothShape1.selfCollideWidthScale', 2.5)
mc.setAttr('nClothShape1.friction', 1.0)
mc.setAttr('nClothShape1.stickiness', 0.4)
mc.setAttr('nClothShape1.stretchResistance', 350.0) #Dynamic Properties
mc.setAttr('nClothShape1.compressionResistance', 100.0)
mc.setAttr('nClothShape1.bendResistance', 1.0)
mc.setAttr('nClothShape1.pointMass', 3.0)
mc.setAttr('nClothShape1.lift', 0.1)
mc.setAttr('nClothShape1.drag', 0.05)
mc.setAttr('nClothShape1.tangentialDrag', 0.2)
mc.setAttr('nClothShape1.damp', 4.0)		#Quality Properties
mc.setAttr('nClothShape1.maxSelfCollisionIterations', 12)
mc.setAttr('nClothShape1.trappedCheck', 1)
mc.setAttr('nClothShape1.pushOut', 0.025)

#### Establish Dynamic Constraints ####
# Neckline Constraints
mc.select(clear=True)
tunic_neckline_verts = [ '[411]', '[414]', '[415]', '[629]', '[630]', '[631]', '[632]', '[633]', '[654]', '[1513]', '[1516]',  '[1517]', '[1722]', '[1723]', '[1724]', '[1725]', '[1745]' ]

for i in tunic_neckline_verts:
    mc.select('viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth.vtx' + i, add=True)
mc.select('viking_tunic_model_main_tunic_sim_mesh', add=True)
mel.eval('createNConstraint pointToSurface 0;')
mel.eval('setAttr "dynamicConstraintShape1.strengthDropoff[1].strengthDropoff_Position" 1;')
mel.eval('setAttr "dynamicConstraintShape1.strengthDropoff[1].strengthDropoff_FloatValue" 0;')

# Front Constraints
#mc.select(clear=True)
#tunic_front_verts = []

#for i in tunic_front_verts:
#    mc.select('viking_tunic_model_main_tunic.vtx' + i, add=True)
#mc.select('viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth', add=True)
#mel.eval('createNConstraint pointToSurface 0;')
#mel.eval('setAttr "dynamicConstraintShape2.strengthDropoff[1].strengthDropoff_Position" 1;')
#mel.eval('setAttr "dynamicConstraintShape2.strengthDropoff[1].strengthDropoff_FloatValue" 0;')


# Set Nucleus Parameters
mc.setAttr('nucleus1.startFrame', STARTPRE)
mc.setAttr('nucleus1.spaceScale', 1.0)
mc.setAttr("nucleus1.usePlane", 1)
mc.setAttr("nucleus1.planeOriginX", tx)
mc.setAttr("nucleus1.planeOriginY", ty)
mc.setAttr("nucleus1.planeOriginZ", tz)
mc.setAttr("nucleus1.windDirectionX", 0.9)  # add in wind here if necessary
mc.setAttr("nucleus1.windDirectionZ", 0.1)
mc.setAttr("nucleus1.subSteps", 12)
mc.setAttr("nucleus1.maxCollisionIterations", 24)
mc.setAttr("nucleus1.timeScale", 1)
# you can try messing with nucleus time scale to increase substeps

# Load cloth preset
#cmds.nodePreset( list='nClothShape1' )
#cmds.nodePreset( save=("nClothShape1","tunic_1") )
#cmds.nodePreset( load=('nClothShape1', 'tunic_1') )


#########################
## PREPARE HERO MESHES ##
#########################

# Wrap Colliders to viking's character alembic
# NOTE: if the dynamic constraints freak out, try changing the order that you do (collisionMesh wrap to character mesh) and (create dynamicConstraint)
mc.select('viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth', replace=True) #Wrap Body
mc.select('viking_rig_main_Viking_body_GEO_01', add=True)  #wrap the collision mesh to viking skin
mc.CreateWrap()

# Wrap bracelets to viking's character alembic
mc.select('viking_tunic_model_main_bracelets', replace=True) #Wrap bracelets
mc.select('viking_rig_main_Viking_body_GEO_01', add=True)  #wrap the bracelets to viking skin
mc.CreateWrap()

# Wrap Tunic Beauty Mesh to Sim Mesh
mc.select('viking_tunic_model_main_tunic_beauty_mesh', replace=True)
mc.select('viking_tunic_model_main_tunic_sim_mesh', add=True)
mc.CreateWrap()

# From Brennan: Do your best to only have one thing wrapping per sim - they are slow to calculate
# if you need to adjust the collision mesh for a weird cloth thing, you can duplicate the collisionmesh,
# adjust the shape/add more or whatever, then make it a blend shape to the original collision mesh.
# Blend shapes DO require the same exact # of polygons but they're also a lot faster than regular wraps.
#mc.setAttr('wrap1.exclusiveBind', 0) #it looks like this is the default

# Rename/Group Simulation Objects
mc.rename('nucleus1', 'nucleus_viking')
mc.rename('nRigid1', 'nRigid_viking_body')
mc.rename('nCloth1', 'nCloth_viking_tunic')

mc.rename('dynamicConstraint1','constraint_tunic_neckline')
#mc.rename('dynamicConstraint2','constraint_tunic_front')
mc.group('constraint_tunic_neckline', name='viking_tunicConstraints')

mc.group('nucleus_viking', 'nRigid_viking_body', 'nCloth_viking_tunic', 'viking_tunicConstraints', name='viking_tunic_simulation')

# Hide Unnescessary Objects
mc.hide('viking_tunic_model_main_tunic_sim_mesh')
#mc.hide('viking_tunic_model_main_tunic_bracelets') # should we handle the bracelets in the other script?
mc.hide('viking_collision_mesh_cloth_model_main_viking_collision_mesh_cloth')

# Set display smoothness
mc.select('viking_tunic_model_main_tunic_sim_mesh', replace=True)
mc.select('viking_tunic_model_main_tunic_beauty_mesh', add=True)
mc.select('viking_tunic_model_main_bracelets', add=True)
cmds.displaySmoothness(du=3, dv=3, pw=16, ps=4, polygonObject=3)

# Tag beauty mesh and bracelets for export
mc.select("viking_tunic_model_main_tunic_beauty_mesh", replace=True)
mc.select('viking_tunic_model_main_bracelets', add=True)
import alembic_tagger;
alembic_tagger.go()
