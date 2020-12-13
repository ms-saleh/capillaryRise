import re

import numpy as np

# print(r'')

# f = open('cube.stl','r')                # 'w' to write, 'a' to append, 'r+' to read and write
# f.close()                               # always close the files you open

U_C = [1.0, 1.0, 1.0]  # Upper corner of the bounding box
L_C = [-1.0, -1.0, -1.0]  # Lower corner of the bounding box
Del = 0.002

# (upperPoint,LowerPoint)
topBox = np.array([[U_C[0], U_C[1], U_C[2]+Del], [L_C[0], L_C[1], U_C[2]-Del]])
bottomBox = np.array([[U_C[0], U_C[1], L_C[2]+Del],
                      [L_C[0], L_C[1], L_C[2]-Del]])

backBox = np.array([[U_C[0], U_C[1]+Del, U_C[2]],
                    [L_C[0], U_C[1]-Del, L_C[2]]])
frontBox = np.array([[U_C[0], L_C[1]+Del, U_C[2]],
                     [L_C[0], L_C[1]-Del, L_C[2]]])

rightBox = np.array([[U_C[0]+Del, U_C[1], U_C[2]],
                     [U_C[0]-Del, L_C[1], L_C[2]]])
leftBox = np.array([[L_C[0]+Del, U_C[1], U_C[2]],
                    [L_C[0]-Del, L_C[1], L_C[2]]])


def inside(point, box):
    """Return True when the point is inside the box otherwise False"""
    return (np.all(np.greater_equal(point, box[1, :])) and np.all(np.less_equal(point, box[0, :])))


with open('negGyroMesh-ascii.stl', 'r') as f:          # with this command you don't need to close the file
    with open('backandforth.stl', 'w') as bf:
        bf.write('solid backandforth\n')
        with open('topandbottom.stl', 'w') as tb:
            tb.write('solid topandbottom\n')
            with open('leftandright.stl', 'w') as lr:
                lr.write('solid leftandright\n')
                with open('innerwall.stl', 'w') as iw:
                    iw.write('solid innerwall\n')

                    line = f.readline()
                    linelist = []
                    midPoint = np.array([0.0, 0.0, 0.0])

                    while len(line) > 0:
                        words = line.split()
                        if words[0] == 'facet' or words[0] == 'outer' or words[0] == 'endloop':
                            linelist.append(line)
                        elif words[0] == 'vertex':
                            midPoint += np.array([float(words[1]),
                                                  float(words[2]), float(words[3])])
                            linelist.append(line)
                        elif words[0] == 'endfacet':
                            midPoint = midPoint/3
                            linelist.append(line)
                            if inside(midPoint, topBox) or inside(midPoint, bottomBox):
                                tb.write(''.join(linelist))
                            elif inside(midPoint, backBox) or inside(midPoint, frontBox):
                                bf.write(''.join(linelist))
                            elif inside(midPoint, rightBox) or inside(midPoint, leftBox):
                                lr.write(''.join(linelist))
                            else:
                                iw.write(''.join(linelist))
                            midPoint = np.array([0.0, 0.0, 0.0])
                            linelist = []
                        line = f.readline()
                    bf.write('endsolid backandforth')
                    tb.write('endsolid topandbottom')
                    lr.write('endsolid leftandright')
                    iw.write('endsolid innerwall')




    # f_contents = f.read()               # reads all the contents at once
    # f_contents = f.read(100)            # reads the first 100 characters of the file
    # f_contents = f.readline()           # returns the each line at the time
    # f_contents = f.readlines()          # returns a list of each lines
    # f.tell()                            # returns the position that wer are currently at
    # f.seek(0)                           # takes us back to 0 position
