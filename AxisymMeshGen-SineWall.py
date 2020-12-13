import numpy as np
import math

# print(r'')

# f = open('cube.stl','r')                # 'w' to write, 'a' to append, 'r+' to read and write
# f.close()                               # always close the files you open
n   = 480
h   = 400.00
th  = math.radians(5.0)
r0  = 22.00
a   = 8.00
la  = 20.00
dh  = h/n
m   = -0.02

with open('blockMeshDict.orig', 'r') as f:          # with this command you don't need to close the file
    with open('blockMeshDict','w') as out:
        out.write(f.read())
        out.write('\nvertices\n(\n')    
        for i in range(0, n+1):
            r = r0 + m * i* dh + a * math.sin(i*dh/la*2*math.pi)# 
            z = i * dh
            x = r * math.cos(th/2)
            y = r * math.sin(th/2)
            out.write(''.join(["\t","(","0 "         ,"0 "           ,str(z),")\n"]))
            out.write(''.join(["\t","(",str(x)," "   ,str(-y)," "    ,str(z),")\n"]))
            out.write(''.join(["\t","(",str(x)," "   ,str(y)," "     ,str(z),")\n"]))
        out.write(");\n\n")

        out.write('\nblocks\n(\n')
        for i in range(0,3*n,3):
            out.write(''.join(['\thex (',str(i),' ', str(i+1),' ',str(i+2),' ',str(i),' ',str(i+3),' ',str(i+4),' ',str(i+5),' ',str(i+3),') (16 1 1) simpleGrading (0.666 1 1)\n']))
        out.write(");\n\n")

        out.write("edges\n(\n);\n\n")
        out.write("faces\n(\n);\n\n")

        out.write("defaultPatch\n{\n\tname walls;\n\ttype wall;\n}\n\n")

        out.write('\nboundary\n(\n')

        out.write('\tinlet\n\t{\n\t\ttype\tpatch;\n\t\tfaces')
        out.write('\t((0 1 2 0));\n\t}\n')

        out.write('\tatmosphere\n\t{\n\t\ttype\tpatch;\n\t\tfaces')
        out.write(''.join(['\t((',str(3*n),' ',str(3*n+1),' ',str(3*n+2),' ',str(3*n),'));\n\t}\n']))


        out.write('\twedge0\n\t{\n\t\ttype\twedge;\n\t\tfaces\n\t\t(\n')
        for i in range(0,3*n,3):
            out.write(''.join(['\t\t\t(',str(i),' ',str(i+1),' ',str(i+4),' ',str(i+3),')\n']))
        out.write('\t\t);\n\t}\n')

        out.write('\twedge1\n\t{\n\t\ttype\twedge;\n\t\tfaces\n\t\t(\n')
        for i in range(0,3*n,3):
            out.write(''.join(['\t\t\t(',str(i),' ',str(i+2),' ',str(i+5),' ',str(i+3),')\n']))
        out.write('\t\t);\n\t}\n);\n')
#(
#    inlet
#    {
#        type    patch;
#        faces   ((v0 v1 v2 v0));
#    }

#    atmosphere
#    {
#        type    patch;
#        faces   ((v3 v4 v5 v3));
#    }

#    wedge1
#    {
#        type    wedge;
#        faces   ((v0 v2 v5 v3));
#    }
#);




    # f_contents = f.read()               # reads all the contents at once
    # f_contents = f.read(100)            # reads the first 100 characters of the file
    # f_contents = f.readline()           # returns each line one at the time
    # f_contents = f.readlines()          # returns a list of sperated lines
    # f.tell()                            # returns the position that wer are currently at
    # f.seek(0)                           # takes us back to 0 position