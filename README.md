# capillaryRise
Includes files and folders used in capillary rise modeling in OpenFOAM

Utilities:
splitSTL #Coded in python and takes two list of coordinates of upper and lower corners of the bounding box. The main input is a binary STL generated in nTop. The outputs are four STL files:
boundaries: topandbottom.stl backanfforth.stl leftandright.stl
inner walles: innerwalls.stl