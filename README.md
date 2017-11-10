# grendel_cloth_scripts

Uses a Python script for resetting the rig rotations.
Uses .mel scripts to add negative frames to the scene.
Has a simple GUI for selecting rig to target



Steps for PREROLL scripts:
1) Select all rig pieces/controls, skipping the locked ones
2) Set keyframe on all rig controls at frame 0 (or a few frames before)
3) Move to frame -25 (or earlier), clear rotation/scale on all rig pieces to put it back into A-Pose
    - We shouldn't necessarily have to move the rig back to origin to do this - doing so might cause problems when we attach cloth to the rig because it has to fly back from origin over to its scene starting position and could cause the cloth to rip off in the process
4) Set A-Pose keyframe on all rig controls at frame -25 (or earlier), so the rig slowly moves from A-Pose into its starting position for the actual scene by the time frame 0 comes around
5) Make sure the correct object is tagged for alembic export (might need to do this manually)
6) Export an alembic of the character mesh, from STARTPRE (-25 ish) to end of scene - we'll use this to wrap to the collision mesh



Steps for SIMULATION scripts:
1) Generate CFX Scene:
		- Create a position locator and set it to the rig's primary control position
		- Pull in the alembic exported from the previous (PREROLL) scripts
		- Checkout the CFX file for this scene or create a new one if it doesn't exist yet
		- Reference the cloth models (sim AND beauty/hero), and translate them to match the character alembic's global position using the position locator from earlier) 
2) Wrap the character's collision mesh to the character's beauty/hero mesh (they should be at the same global position)
3) Create nCloth, nucleus, nRigid collider, and dynamic constraint objects and set all custom parameters 
		- Note that the dynamic constraints are attached to the character's collision mesh, not the actual rigged geo!
4) Wrap the cloth beauty mesh to the cloth sim mesh 
5) Group related objects, rename them & their groups for clarity, hide unnecessary objects (sim meshes, etc)
6) Export an alembic of the simmed cloth beauty mesh? 
