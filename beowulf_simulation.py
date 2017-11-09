#Authors: Daniel Fuller, Trevor Barrus, Brennan Mitchell
import os

import maya
import maya.mel as mel #Allows for evaluation of MEL
import pymel.core as pc #Allows for evaluation of MEL (NECESSARY?)
import maya.cmds as mc

from byuam.project import Project
from byuam.environment import Department, Environment

STARTANIM = -5
STARTPRE = -25

#########################
## ESTABLISH CFX SCENE ##
#########################

#This code is brought to you in part by Trevor Barrus and the letter G

def generateScene():
    project = Project()
    environment = Environment()

    # Create a global position locator for Beowulf's Starting Location
    mc.currentTime(STARTANIM)
    globalPos = mc.spaceLocator(p=[0,0,0])
    globPos = mc.rename(globalPos, "beowulfGlobalPos")
    mc.select("grendel_rig_main_Beowulf_primary_global_cc_01")
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
    cache_file = os.path.join(element.get_dir(), "cache", "beowulf_rig_main.abc")

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

    # Reference Beowulf's Sim Robe
    body = project.get_body("beowulf_robe_sim")
    element = body.get_element(Department.MODEL)
    robe_file = element.get_app_filepath()
    mc.file(robe_file, reference=True)
    
    # Reference Beowulf's Beauty/Hero Robe
    body = project.get_body("beowulf_robe")
    element = body.get_element(Department.MODEL)
    robe_hero_file = element.get_app_filepath()
    mc.file(robe_hero_file, reference=True)
    
    # Set Sim Robe transforms to variables above
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.translateX", tx)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.translateY", ty)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.translateZ", tz)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.rotateX", rx)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.rotateY", ry)
    mc.setAttr("ten_robe_sim_model_main_ten_cloth.rotateZ", rz)
    
    # Set Hero Robe transforms to variables above
    mc.setAttr("ten_robe_model_main_TEN_ROBE_HERO.translateX", tx)
    mc.setAttr("ten_robe_model_main_TEN_ROBE_HERO.translateY", ty)
    mc.setAttr("ten_robe_model_main_TEN_ROBE_HERO.translateZ", tz)
    mc.setAttr("ten_robe_model_main_TEN_ROBE_HERO.rotateX", rx)
    mc.setAttr("ten_robe_model_main_TEN_ROBE_HERO.rotateY", ry)
    mc.setAttr("ten_robe_model_main_TEN_ROBE_HERO.rotateZ", rz)
    



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

#Wrap Colliders to Alembic
mc.select('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth', replace=True) #Wrap Body
mc.select('TEN_ANIM', add=True)
mc.CreateWrap()
#mc.setAttr('wrap1.exclusiveBind', 0)

#Establish Colliders
mc.select('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth', replace=True) #Collider Body
mel.eval('makeCollideNCloth;')
mc.setAttr('nRigid1.thickness', 0.001)


#Establish nCloth Objects
mc.select('beowulf_cape_model_main_beowulf_cape_simMesh', replace=True) #nCloth: Robe
mel.eval('createNCloth 0;')

mc.setAttr('nClothShape1.thickness', 0.006) #Collision Properties: Cape
mc.setAttr('nClothShape1.selfCollideWidthScale', 2.5)
mc.setAttr('nClothShape1.friction', 1.0)
mc.setAttr('nClothShape1.stickiness', 0.4)
mc.setAttr('nClothShape1.stretchResistance', 200.0) #Dynamic Properties: Cape
mc.setAttr('nClothShape1.compressionResistance', 100.0)
mc.setAttr('nClothShape1.bendResistance', 1.0)
mc.setAttr('nClothShape1.pointMass', 2.0)
mc.setAttr('nClothShape1.lift', 0.1)
mc.setAttr('nClothShape1.drag', 0.05)
mc.setAttr('nClothShape1.tangentialDrag', 0.2)
mc.setAttr('nClothShape1.damp', 2.5)

#### Establish Dynamic Constraints ####


# These are correct for the new Beowulf cape SIM mesh
mc.select(clear=True) #neckline Constraints
cape_neckline_verts = [ '[72]', '[73]', '[78]', '[79]', '[84]', '[85]', '[90]', '[91]', '[96]', '[97]', '[102]',  '[513]', '[517]', '[528]', '[531]', '[542]', '[545]', '[556]', '[559]', '[570]', '[573]', '[584]', '[587]',  '[3031]', '[3034]', '[3041]', '[3044]', '[3065]', '[3068]', '[3073]', '[3076]', '[3097]', '[3100]', '[3105]', '[3108]', '[3129]', '[3132]', '[3137]', '[3140]', '[3161]', '[3164]', '[3169]', '[3172]', '[3193]', '[3196]', '[3201]', '[3204]' ]

for i in cape_neckline_verts:
    mc.select('beowulf_cape_model_main_beowulf_cape_simMesh.vtx' + i, add=True) #might want to add a dynamic prefix thing like in the other script?
mc.select('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth', add=True) #idk why it came in as a reference with such a long name
mel.eval('createNConstraint pointToSurface 0;')
mel.eval('setAttr "dynamicConstraintShape1.strengthDropoff[1].strengthDropoff_Position" 1;') #test
mel.eval('setAttr "dynamicConstraintShape1.strengthDropoff[1].strengthDropoff_FloatValue" 0;')
#mc.rename('dynamicConstraint1','constraint_cape_neckline') #this may not work if there are already dynamic constraints in the scene

# These are correct for Beowulf's cape SIM mesh
mc.select(clear=True) #front Constraints
cape_front_verts = [ '[42]', '[62]', '[69]', '[70]', '[71]', '[99]', '[101]', '[103]', '[106]', '[116]', '[509]', '[514]', '[575]', '[586]', '[594]', '[597]', '[641]', '[649]', '[1610]', '[1595]', '[1715]', '[1730]', '[2860]', '[2979]', '[3024]', '[3027]', '[3035]', '[3038]', '[3176]', '[3219]', '[3200]', '[3222]', '[3227]', '[3230]', '[3342]', '[3362]' ]

for i in cape_front_verts:
    mc.select('beowulf_cape_model_main_beowulf_cape_simMesh.vtx' + i, add=True)
mc.select('beowulf_collision_mesh_cloth_model_main_beowulf_collision_mesh_cloth', add=True)
mel.eval('createNConstraint pointToSurface 0;') 
mel.eval('setAttr "dynamicConstraintShape2.strengthDropoff[1].strengthDropoff_Position" 1;') #test
mel.eval('setAttr "dynamicConstraintShape2.strengthDropoff[1].strengthDropoff_FloatValue" 0;')
#mc.rename('dynamicConstraint1','constraint_cape_neckline')  #this may not work if there are already dynamic constraints in the scene


#Set Nucleus Parameters
mc.setAttr('nucleus1.subSteps', 4)
mc.setAttr('nucleus1.maxCollisionIterations', 8)
mc.setAttr('nucleus1.startFrame', STARTPRE)
mc.setAttr('nucleus1.spaceScale', 1.0)

#########################
## PREPARE HERO MESHES ##
#########################

#Create Sleeveless Robe for Sash Sim
mc.duplicate('ten_robe_model_main_ten_Hero_Robe')
mc.rename('ten_robe_model_main_ten_Hero_Robe1', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless')

mc.select('ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1861:1862]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1866:1869]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1872:1873]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1878:1881]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1884:1885]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1888]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1891]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1893:1894]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1898:1899]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[2009:2010]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[2021:2022]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[2396:2397]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[2402:2403]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[2412]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[2415]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[2428:2429]', replace=True)
mc.select('ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[968]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[971:972]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[975:976]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[979:980]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[983:984]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[987:988]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[991:992]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[995:996]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[999:1000]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1003:1004]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1007:1008]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1011:1012]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1015:1016]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1019:1020]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1023:1024]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1027:1028]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[1031]', add=True)
mc.delete()

mc.select('ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[0:895]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[4452:4579]', replace=True)
mc.select('ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[968:1639]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[3872:3935]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[4000:4127]', 'ten_robe_model_main_ten_Hero_Robe_Sleeveless.f[4324:4451]', add=True)
mc.delete()

# Wrap Hero Meshes to Sim Meshes
mc.select('ten_robe_model_main_ten_Hero_Robe', replace=True) #Wrap Robe
mc.select('ten_robe_sim_model_main_ten_sim_robe', add=True)
mc.CreateWrap()
#mc.setAttr('wrap4.exclusiveBind', 0)

mc.select('ten_robe_model_main_ten_Hero_Pants', replace=True) #Wrap Pants
mc.select('ten_robe_sim_model_main_ten_sim_pants', add=True)
mc.CreateWrap()
#mc.setAttr('wrap5.exclusiveBind', 0)

mc.select('ten_robe_model_main_ten_Hero_Robe_Sleeveless', replace=True) #Wrap Sleeveless Robe (Exclusive Bind)
mc.select('ten_robe_model_main_ten_Hero_Robe', add=True)
mc.CreateWrap()
#mc.setAttr('wrap6.exclusiveBind', 1)

mc.select('ten_robe_model_main_ten_Hero_Sash', replace=True) #Wrap Sash
mc.select('ten_robe_model_main_ten_Hero_Robe_Sleeveless', add=True)
mc.CreateWrap()
#mc.setAttr('wrap7.exclusiveBind', 0)

#Rename/Group Simulation Objects
mc.rename('nucleus1', 'nucleus_ten') #Nucleus

mc.rename('nRigid1', 'nRigid_ten_body') #nRigid
mc.rename('nRigid2', 'nRigid_ten_mitten_l')
mc.rename('nRigid3', 'nRigid_ten_mitten_r')
mc.group('nRigid_ten_body', 'nRigid_ten_mitten_l', 'nRigid_ten_mitten_r', name='ten_nRigid')

mc.rename('nCloth1', 'nCloth_ten_robe') #nCloth
mc.rename('nCloth2', 'nCloth_ten_pants')
mc.group('nCloth_ten_robe', 'nCloth_ten_pants', name='ten_nCloth')

mc.rename('dynamicConstraint1', 'dynamicConstraint_ten_robe_lapel') #dynamicConstraint
mc.rename('dynamicConstraint2', 'dynamicConstraint_ten_robe_back')
mc.rename('dynamicConstraint3', 'dynamicConstraint_ten_robe_front')
mc.rename('dynamicConstraint4', 'dynamicConstraint_ten_pants')
mc.group('dynamicConstraint_ten_robe_lapel', 'dynamicConstraint_ten_robe_back', 'dynamicConstraint_ten_robe_front', 'dynamicConstraint_ten_pants', name='ten_dynamicConstraint')

mc.group('nucleus_ten', 'ten_nRigid', 'ten_nCloth', 'ten_dynamicConstraint', name='ten_simulation')

#Group Alembic Objects
mc.group('TEN_ANIM', 'TEN_ANIMBase', 'TEN_ANIMBase1', 'TEN_ANIMBase2', name='ten_alembic')

#Group Ten Cloth
mc.group('ten_robe_sim_model_main_ten_cloth', 'ten_robe_model_main_TEN_ROBE_HERO', 'ten_simulation', 'ten_alembic', name='ten_cloth')

#Hide Unnescessary Objects
mc.hide('ten_simulation')
mc.hide('ten_robe_sim_model_main_ten_cloth')
