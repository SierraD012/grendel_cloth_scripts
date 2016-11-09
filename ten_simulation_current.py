#Authors: Daniel Fuller, Trevor Barrus, Brennan Mitchell
import os

import maya
import maya.mel as mel #Allows for evaluation of MEL
import pymel.core as pc #Allows for evaluation of MEL (NECESSARY?)
import maya.cmds as mc

from byuam.project import Project
from byuam.environment import Department, Environment

'''
THIS CODE IS TO BE RUN FROM THE ANIMATION FILE. Once the pre-roll script is run and a finished alembic has been exported: RUN THIS SCRIPT.

It will:

1. Open the corresponding cfx file (unless one doesn't exist - then it makes its own)
2. Import/place Ten's cloth simulation meshes and objects
3. Set up all colliders and nCloth objects

What this script doesn't do (yet):

1. Organize the outliner (I've been doing it by hand - gotta get better about that)
2. Import the final "Hero" cloth meshes
3. Wrape the "Hero" cloth meshes to the Simulation meshes

Another Note: The Sash has no sim - it's too expensive/fragile. I've just been wrapping the Hero Sash Model to the Hero Robe Model.
At some point we'll need to go back in and create a collider for the sash in some scenes, but for now it looks fine.

MAKE SURE "EXCLUSIVE BIND" IS NOT SELECTED WHEN WRAPPING - ESPECIALLY THE SASH. Smh.

Final Note: Some CFX scenes already have cloth simulations in them.
IN THESE CASES IT'S IMPORTANT TO CREATE YOUR OWN NUCLEUS SEPERATE FROM ANY OTHER ROBES/TAPESTRIES.
I've been naming Ten's nucelus "nucleus_ten"

Feel free to look at some of the other semi-finished scenes. I believe B17 or B19 are good examples.
'''

#########################
## ESTABLISH CFX SCENE ##
#########################

#This code is brought to you in part by Trevor Barrus and the letter G

def generateScene():
    project = Project()
    environment = Environment()

    # Create a global position locator for Ten's Starting Location
    mc.currentTime(0)
    globalPos = mc.spaceLocator(p=[0,0,0])
    globPos = mc.rename(globalPos, "tenGlobalPos")
    mc.select("ten_rig_main_m_global_CTL")
    mc.select(globPos, add=True)
    mc.pointConstraint(offset=[0,0,0], weight=1)
    mc.orientConstraint(offset=[0,0,0], weight=1)

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
    cache_file = os.path.join(element.get_dir(), "cache", "ten_rig_main.abc")

    # checkout cfx scene for corresponding shot number
    current_user = environment.get_current_username()
    element = body.get_element(Department.CFX)
    cfx_filepath = element.checkout(current_user)

    #open cfx file 
    if cfx_filepath is not None:
        if not mc.file(q=True, sceneName=True) == '':
            mc.file(save=True, force=True) #save file

        if not os.path.exists(cfx_filepath):
            mc.file(new=True, force=True)
            mc.file(rename=cfx_filepath)
            mc.file(save=True, force=True)
        else:
            mc.file(cfx_filepath, open=True, force=True)

    # import alembic
    command = "AbcImport -mode import \"" + cache_file + "\""
    maya.mel.eval(command)

    # delete all geo except ten's skin and rename
    geometry = mc.ls(geometry=True)
    transforms = mc.listRelatives(geometry, p=True, path=True)
    mc.select(transforms, r=True)
    for geo in mc.ls(sl=True):
        if(geo != "ten_rig_main_Ten_Skin_RENDER"):
            mc.delete(geo)
    collide = "TEN_ANIM"
    mc.rename("ten_rig_main_Ten_Skin_RENDER", collide)

    # Reference Ten's Robe
    body = project.get_body("ten_robe_sim")
    element = body.get_element(Department.MODEL)
    robe_file = element.get_app_filepath()
    mc.file(robe_file, reference=True)
    
    # set robe transforms to variables above
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.translateX", tx)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.translateY", ty)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.translateZ", tz)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.rotateX", rx)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.rotateY", ry)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.rotateZ", rz)
    
generateScene()


#######################
## Set Up Simulation ##
#######################

#This code is brought to you in part by Brennan Mitchell and viewers like you. Thank you.


mc.select('ten_robe_sim_model_main_ten_collide_body', replace=True)
mc.viewFit() #Snap View to Body Collider
mc.hide('TEN_ANIM')
mc.playbackOptions(animationStartTime=-20)
mc.playbackOptions(minTime=-20)
mc.currentTime(-20)

#Wrap Colliders to Alembic
mc.select('ten_robe_sim_model_main_ten_collide_body', replace=True) #Wrap Body
mc.select('TEN_ANIM', add=True)
mc.CreateWrap()

mc.select('ten_robe_sim_model_main_ten_collide_mitten_l', replace=True) #Wrap Left Mitten
mc.select('TEN_ANIM', add=True)
mc.CreateWrap()

mc.select('ten_robe_sim_model_main_ten_collide_mitten_r', replace=True) #Wrap Right Mitten
mc.select('TEN_ANIM', add=True)
mc.CreateWrap()

#Establish Colliders
mc.select('ten_robe_sim_model_main_ten_collide_body', replace=True) #Collider Body
mel.eval('makeCollideNCloth;')

mc.select('ten_robe_sim_model_main_ten_collide_mitten_l', replace=True) #Collider Left Mitten
mel.eval('makeCollideNCloth;')

mc.select('ten_robe_sim_model_main_ten_collide_mitten_r', replace=True) #Collider Right Mitten
mel.eval('makeCollideNCloth;')

#Establish nCloth Objects
mc.select('ten_robe_sim_model_main_ten_sim_robe', replace=True) #nCloth: Robe
mel.eval('createNCloth 0;')

mc.setAttr('nClothShape1.thickness', 0.003) #Collision Properties: Robe
mc.setAttr('nClothShape1.selfCollideWidthScale', 5.0)
mc.setAttr('nClothShape1.friction', 0.0)
mc.setAttr('nClothShape1.stickiness', 0.1)

mc.setAttr('nClothShape1.stretchResistance', 200.0) #Dynamic Properties: Robe
mc.setAttr('nClothShape1.compressionResistance', 100.0)
mc.setAttr('nClothShape1.bendResistance', 1.0)
mc.setAttr('nClothShape1.damp', 0.8)

mc.select('ten_robe_sim_model_main_ten_sim_pants', replace=True) #nCloth: Pants
mel.eval('createNCloth 0;')

mc.setAttr('nClothShape2.thickness', 0.003) #Collision Properties: Pants
mc.setAttr('nClothShape2.selfCollideWidthScale', 5.0)
mc.setAttr('nClothShape2.friction', 0.0)
mc.setAttr('nClothShape2.stickiness', 0.1)

mc.setAttr('nClothShape2.stretchResistance', 200.0) #Dynamic Properties: Pants
mc.setAttr('nClothShape2.compressionResistance', 100.0)
mc.setAttr('nClothShape2.bendResistance', 1.0)
mc.setAttr('nClothShape2.damp', 0.8)

#Establish Dynamic Constraints

mc.select(clear=True) #Lapel Constraint
robe_lapel_verts = [
'[1004]', '[1371]', '[1373]', '[1410]', '[1418]', '[2600]', '[2592]',
'[1423]', '[1426]', '[1428]', '[1440:1442]', '[1445:1447]', '[1450]',
'[1452:1454]', '[1722]', '[1730]', '[1747:1748]', '[1768]', '[2242]',
'[2394]', '[2403]', '[2406]', '[2408]', '[2410:2411]', '[2417:2424]',
'[2545]', '[2548]', '[2550]', '[2560:2561]', '[2575:2576]']

for i in robe_lapel_verts:
    mc.select('ten_robe_sim_model_main_ten_sim_robe.vtx' + i, add=True)
mc.select('ten_robe_sim_model_main_ten_collide_body', add=True)
mel.eval('createNConstraint pointToSurface 0;')

mc.select(clear=True) #Back Constraint
robe_back_verts = ['[1909:1911]', '[2663:2667]', '[2756]']

for i in robe_back_verts:
    mc.select('ten_robe_sim_model_main_ten_sim_robe.vtx' + i, add=True)
mc.select('ten_robe_sim_model_main_ten_collide_body', add=True)
mel.eval('createNConstraint pointToSurface 0;') 

mc.select(clear=True) #Front Constraint
robe_front_verts = ['[177]', '[180:181]', '[1000]', '[1003]', '[1005:1006]', '[2043]']

for i in robe_front_verts:
    mc.select('ten_robe_sim_model_main_ten_sim_robe.vtx' + i, add=True)
mc.select('ten_robe_sim_model_main_ten_collide_body', add=True)
mel.eval('createNConstraint pointToSurface 0;') 

mc.select(clear=True) #Pants Constraint
pants_verts = [
'[7:8]', '[145:154]', '[335:344]', '[636:658]', '[1017:1037]',
'[1282:1292]', '[1468:1478]', '[382:393]', '[1115:1138]',
'[1521:1532]', '[192:203]', '[738:761]', '[1335:1346]']

for i in pants_verts:
    mc.select('ten_robe_sim_model_main_ten_sim_pants.vtx' + i, add=True)
mc.select('ten_robe_sim_model_main_ten_collide_body', add=True)
mel.eval('createNConstraint pointToSurface 0;') 


#Set Nucleus Parameters (INCOMPLETE - New Nucleus specific to Ten?)
mc.setAttr('nucleus1.subSteps', 15)
mc.setAttr('nucleus1.maxCollisionIterations', 20)
mc.setAttr('nucleus1.startFrame', -20)
mc.setAttr('nucleus1.spaceScale', 0.45)
