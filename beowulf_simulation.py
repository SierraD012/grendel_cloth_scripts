#Authors: Daniel Fuller, Trevor Barrus, Brennan Mitchell
import os

import maya
import maya.mel as mel #Allows for evaluation of MEL
import pymel.core as pc #Allows for evaluation of MEL (NECESSARY?)
import maya.cmds as mc

from byuam.project import Project
from byuam.environment import Department, Environment

STARTANIM = -0
STARTPRE = -30

#########################
## ESTABLISH CFX SCENE ##
#########################

def generateScene():
    project = Project()
    environment = Environment()

    # Create a global position locator for Beowulf's Starting Location
    mc.currentTime(STARTPRE)
    globalPos = mc.spaceLocator(p=[0,0,0])
    globPos = mc.rename(globalPos, "beowulfGlobalPos")
    mc.select("beowulf_rig_main_Beowulf_primary_global_cc_01")
    mc.select(globPos, add=True)
    mc.pointConstraint(offset=[0,0,0], weight=1) #constrains the globPos position to where Beowulf's rig_main is
    mc.orientConstraint(offset=[0,0,0], weight=1) #orients the globPos to match Beowulf's rig_main (I think it just does the rotation)

    # Get transformation variables from globPos locator
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
    cache_name = "beowulf_"+checkout_body_name+"_anim_main" # this is me doing it arbitrarily but I think the preroll script picks its own name
    cache_file = os.path.join(element.get_dir(), "cache", cache_name + ".abc")
    #print("Expecting mesh alembic with name " + cache_name)
    #we could make a while loop to check if an alembic with this name exists already, if it does increment a suffix number on the filename

    # checkout cfx scene for corresponding shot number
    current_user = environment.get_current_username()
    element = body.get_element(Department.CFX)
    cfx_filepath = element.checkout(current_user)
    print(">GenScene(): cfx_filepath= " + cfx_filepath) # see where it's expecting the file to be/what it's called
    print(">GenScene(): cache_file= " + cache_file) # this is where ABCimporter expects the character geo abc to be


    #open cfx file
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
    getReferenceObjects()

    # Set full cape group transforms to match Beowulf's alembic
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.translateX", tx)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.translateY", ty)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.translateZ", tz)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.rotateX", rx)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.rotateY", ry)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.rotateZ", rz)

    #Set collisionMesh transforms to match Beowulf's alembic
    mc.setAttr("beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth.translateX", tx)
    mc.setAttr("beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth.translateY", ty)
    mc.setAttr("beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth.translateZ", tz)
    mc.setAttr("beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth.rotateX", rx)
    mc.setAttr("beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth.rotateY", ry)
    mc.setAttr("beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth.rotateZ", rz)


def getReferenceObjects():
    #Reference Beowulf's CollisionMesh
    body = project.get_body("beowulf_collision_mesh_cloth")
    element = body.get_element(Department.MODEL)
    collisionMesh_file = element.get_app_filepath()
    mc.file(collisionMesh_file, reference=True)

    # Reference Beowulf's Cape - it comes with both sim and beauty meshes
    body = project.get_body("beowulf_cape")
    element = body.get_element(Department.MODEL)
    cape_sim_file = element.get_app_filepath()
    mc.file(cape_sim_file, reference=True)

    #Should also import the cape chain alembic too?


#######################
##       MAIN        ##
#######################

generateScene()

#######################
## Set Up Simulation ##
#######################

mc.select('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth', replace=True)
mc.viewFit() #Snap View to Body Collider
mc.playbackOptions(animationStartTime=STARTPRE)
mc.playbackOptions(minTime=STARTPRE)
mc.currentTime(STARTPRE)

#### Establish Colliders ###
mc.select('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth', replace=True) #Collider Body
mel.eval('makeCollideNCloth;')
mc.setAttr('nRigid1.thickness', 0.001)


#### Establish nCloth Objects ####
mc.select('beowulf_cape_model_main_beowulf_cape_simMesh', replace=True) #nCloth: Robe
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
#Neckline Constraints
mc.select(clear=True)
cape_neckline_verts = [ '[72]', '[73]', '[78]', '[79]', '[84]', '[85]', '[90]', '[91]', '[96]', '[97]', '[102]',  '[513]', '[517]', '[528]', '[531]', '[542]', '[545]', '[556]', '[559]', '[570]', '[573]', '[584]', '[587]',  '[3031]', '[3034]', '[3041]', '[3044]', '[3065]', '[3068]', '[3073]', '[3076]', '[3097]', '[3100]', '[3105]', '[3108]', '[3129]', '[3132]', '[3137]', '[3140]', '[3161]', '[3164]', '[3169]', '[3172]', '[3193]', '[3196]', '[3201]', '[3204]' ]

for i in cape_neckline_verts:
    mc.select('beowulf_cape_model_main_beowulf_cape_simMesh.vtx' + i, add=True)
mc.select('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth', add=True)
mel.eval('createNConstraint pointToSurface 0;')
mel.eval('setAttr "dynamicConstraintShape1.strengthDropoff[1].strengthDropoff_Position" 1;')
mel.eval('setAttr "dynamicConstraintShape1.strengthDropoff[1].strengthDropoff_FloatValue" 0;')

#Front Constraints
mc.select(clear=True)
cape_front_verts = [ '[42]', '[62]', '[69]', '[70]', '[71]', '[99]', '[101]', '[103]', '[106]', '[116]', '[509]', '[514]', '[575]', '[586]', '[594]', '[597]', '[641]', '[649]', '[1610]', '[1595]', '[1715]', '[1730]', '[2860]', '[2979]', '[3024]', '[3027]', '[3035]', '[3038]', '[3176]', '[3219]', '[3200]', '[3222]', '[3227]', '[3230]', '[3342]', '[3362]' ]

for i in cape_front_verts:
    mc.select('beowulf_cape_model_main_beowulf_cape_simMesh.vtx' + i, add=True)
mc.select('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth', add=True)
mel.eval('createNConstraint pointToSurface 0;')
mel.eval('setAttr "dynamicConstraintShape2.strengthDropoff[1].strengthDropoff_Position" 1;')
mel.eval('setAttr "dynamicConstraintShape2.strengthDropoff[1].strengthDropoff_FloatValue" 0;')


#Set Nucleus Parameters
mc.setAttr('nucleus1.subSteps', 4)
mc.setAttr('nucleus1.maxCollisionIterations', 8)
mc.setAttr('nucleus1.startFrame', STARTPRE)
mc.setAttr('nucleus1.spaceScale', 1.0)
mc.setAttr("nucleus1.usePlane", 1)
mc.setAttr("nucleus1.planeOriginX", tx)
mc.setAttr("nucleus1.planeOriginY", ty)
mc.setAttr("nucleus1.planeOriginZ", tz)
mc.setAttr("nucleus1.windDirectionX", 0.9)  # add in wind here if necessary
mc.setAttr("nucleus1.windDirectionZ", 0.1)
mc.setAttr("nucleus1.timeScale", 2)
# you can try messing with nucleus time scale to increase substeps


#########################
## PREPARE HERO MESHES ##
#########################

#Wrap Colliders to Beowulf's character alembic
#NOTE: if the dynamic constraints freak out, try changing the order that you do (collisionMesh wrap to character mesh) and (create dynamicConstraint)
mc.select('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth', replace=True) #Wrap Body
mc.select('beowulf_rig_main_Beowulf_body_GEO_01', add=True)  #wrap the collision mesh to Beowulf skin
mc.CreateWrap()

#From Brennan: Do your best to only have one thing wrapping per sim - they are slow to calculate
# if you need to adjust the collision mesh for a weird cloth thing, you can duplicate the collisionmesh, adjust the shape/add more or whatever, then make it a blend shape to the original collision mesh. Blend shapes DO require the same exact # of polygons but they're also a lot faster than regular wraps.
#mc.setAttr('wrap1.exclusiveBind', 0) #it looks like this is the default


# Wrap Cape Beauty Mesh to Sim Mesh
mc.select('beowulf_cape_model_main_beowulf_cape_beautyMesh', replace=True)
mc.select('beowulf_cape_model_main_beowulf_cape_simMesh', add=True)
mc.CreateWrap()


#Rename/Group Simulation Objects
mc.rename('nucleus1', 'nucleus_beowulf')
mc.rename('nRigid1', 'nRigid_beowulf_body')
mc.rename('nCloth1', 'nCloth_beowulf_cape')

mc.rename('dynamicConstraint1','constraint_cape_neckline')
mc.rename('dynamicConstraint2','constraint_cape_front')
mc.group('constraint_cape_neckline', 'constraint_cape_front', name='beowulf_capeConstraints')

mc.group('nucleus_beowulf', 'nRigid_beowulf_body', 'nCloth_beowulf_cape', 'beowulf_capeConstraints', name='beowulf_cape_simulation')

#Hide Unnescessary Objects
mc.hide('beowulf_cape_model_main_beowulf_cape_simMesh')
mc.hide('beowulf_cape_model_main_beowulf_cape_clasps') #the chain/clasps are taken care of in the other script
mc.hide('beowulf_cape_model_main_beowulf_cape_clasp_chain')
mc.hide('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth')

#Tag cape object for export
mc.select("beowulf_cape_model_main_beowulf_cape_beautyMesh", replace = True)
import alembic_tagger;
alembic_tagger.go()
