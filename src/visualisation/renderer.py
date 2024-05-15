import json
import sys
from math import sin, cos, pi as PI

from direct.gui.DirectGui import OnscreenText
from direct.interval.IntervalGlobal import Sequence
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, PointLight
from panda3d.core import Geom, GeomTriangles, GeomNode
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter
from panda3d.core import LVector3
from panda3d.core import RigidBodyCombiner, NodePath
from panda3d.core import TextNode
from panda3d.core import loadPrcFileData

loadPrcFileData("", "fullscreen true")
loadPrcFileData("", "win-origin 0 0")
loadPrcFileData("", "undecorated true")
loadPrcFileData("", "win-size 1920 1080")

sequence_started = False

# helper function for normalizing vector to length 1
def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec

# The purpose is to generate a basic structure for 3D geometry.
def createGeometry():
    # A vertex is a data point that defines a point in 3D space. It contains a  position (x/y/z) and a color.

    # This creates the format for a vertex, with positions and normals.
    format = GeomVertexFormat.getV3n3()
    # Creates a container for vertex data, named piece, using the specified format and a hint "UHStatic",
    #   indicating that the data won't change frequently.
    vdata = GeomVertexData('piece', format, Geom.UHStatic)

    # Two instances, vertex and normal, are created.
    # They are used to write data into the vdata.
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')

    # Is created with the GeomVertexData (vdata) to form a geometry container (scene)
    # This geometry can later be added to a node for rendering
    scene = Geom(vdata)

    return scene, (vertex, normal)


# The purpose is to take a geom object, encapsulate it within a geomnode named scene,
# then attach this geomnode to the rendernode and return a nodepath to the rendered geometry.
# This function is a convenient way to organize/integrate geometry into a Panda3D scene.
def createGeomNode(geom):
    # Creates a geomnode named scene
    node = GeomNode('scene')

    # Unpacks the returned tuple from the geom argument
    scene,_ = geom

    # Adding the geom object to the geomnode
    node.addGeom(scene)

    # Creates a nodepath by attaching the geomnode to the render node
    renderedNode = render.attachNewNode(node)

    return renderedNode

def makeAABox(pMin, pMax):
    geom = createGeometry()
    addAABox(pMin, pMax, geom)
    return createGeomNode(geom)

# Extends an existing geometry
def addAABox(pMin, pMax, geom):
    # Unpack the geometry tuple into scene and the vertex/normal writers
    scene, (vertex, normal) = geom

    # Get number of vertices in the existing geometry
    vertCnt = vertex.getVertexData().get_num_rows()

    # Calculate the midpoint and ranges of the bounding box
    ranges = tuple(zip(pMin, pMax))
    xMid, yMid, zMid = [0.5 * sum(range) for range in ranges]
    xRange, yRange, zRange = ranges

    # Add vertices and normals to create the bounding box
    for x in xRange:
        for y in yRange:
            for z in zRange:
                #print(xRange, yRange, zRange)
                vertex.addData3(x, y, z)
                normal.addData3(normalized(x-xMid, y-yMid, z-zMid))

    #   5---7
    #  /|  /|
    # 1---3 |
    # | 4-|-6
    # |/  |/
    # 0---2
    # Define indices for creating the box faces
    faceIdcs = (
        (0, 2, 3, 1),
        (2, 6, 7, 3),
        (6, 4, 5, 7),
        (4, 0, 1, 5),
        (0, 4, 6, 2),
        (1, 3, 7, 5)
    )

    # Generate triangle indices for each face
    triangleIdcsPerFace = (((p1, p4, p2), (p2, p4, p3)) for p1, p2,  p3, p4 in faceIdcs)
    triangleIdcs = sum(triangleIdcsPerFace, ()) #flatten tuple

    # Create geomtriangles for the bounding box
    tris = GeomTriangles(Geom.UHStatic)
    for i1, i2, i3 in triangleIdcs:
        tris.addVertices(vertCnt+i1, vertCnt+i2, vertCnt+i3)

    # Add the geomtriangles to the existing geometry
    scene.addPrimitive(tris)


def addAmbientLight(intensity=0.5):
    aLight = AmbientLight('ambientLight')
    aLightColor = tuple(3 * [intensity] + [1])
    aLight.setColor(aLightColor)
    aLightNP = render.attachNewNode(aLight)
    render.setLight(aLightNP)


def addPointLight(pos, intensity=1):
    pLight = PointLight('plight')
    pLightColor = tuple(3 * [intensity] + [1])
    pLight.setColor(pLightColor)
    pLight.attenuation = (0, 0, 0.05)
    pLightNP = render.attachNewNode(pLight)
    pLightNP.setPos(*pos)
    render.setLight(pLightNP)


#def buildPieces(startingPoint, color):
def buildPieces(piecePosition, bridgePosition, color):
    block = RigidBodyCombiner("block")
    blocknp = NodePath(block)
    blocknp.reparentTo(render)

    x_offset = piecePosition[0]
    y_offset = piecePosition[1]
    bridge_x = bridgePosition[0]
    bridge_y = bridgePosition[1]

    #top part
    box = makeAABox((-1 + x_offset,-1 + y_offset,-1),(0 + x_offset,0 + y_offset,0))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = makeAABox((0 + x_offset,-1 + y_offset,-1),(1 + x_offset,0 + y_offset,0))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = makeAABox((-1 + x_offset, 0 + y_offset, -1), (0 + x_offset,1 + y_offset,0))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = makeAABox((0 + x_offset, 0 + y_offset, -1), (1 + x_offset, 1 + y_offset,0))
    box.setColor(*color)
    box.reparentTo(blocknp)

    #bridge part
    box = makeAABox((-1 + x_offset + bridge_x, -1 + y_offset + bridge_y, -2), (0 + x_offset, 0 + y_offset, -1))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = makeAABox((-1 + x_offset + bridge_x, -1 + y_offset + bridge_y, -3), (0 + x_offset, 0 + y_offset, -2))
    box.setColor(*color)
    box.reparentTo(blocknp)

    #bottom part
    box = makeAABox((-1 + x_offset, -1 + y_offset, -4), (0 + x_offset, 0 + y_offset, -3))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = makeAABox((0 + x_offset, -1 + y_offset, -4), (1 + x_offset, 0 + y_offset, -3))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = makeAABox((-1 + x_offset, 0 + y_offset, -4), (0 + x_offset, 1 + y_offset, -3))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = makeAABox((0 + x_offset, 0 + y_offset, -4), (1 + x_offset, 1 + y_offset, -3))
    box.setColor(*color)
    box.reparentTo(blocknp)

    block.collect()
    return blocknp

def moveCameraRight():
    global cam_alpha
    cam_alpha += turn_speed
    calcCameraPosition()
    startSequence()

def moveCameraLeft():
    global cam_alpha
    cam_alpha -= turn_speed
    calcCameraPosition()
    startSequence()

def moveCameraUp():
    global cam_beta
    cam_beta += turn_speed
    if cam_beta > PI/2:
        cam_beta = PI/2 - 0.05
    calcCameraPosition()
    startSequence()

def moveCameraDown():
    global cam_beta
    cam_beta -= turn_speed
    if cam_beta < -PI/2:
        cam_beta = -PI/2 + 0.05
    calcCameraPosition()
    startSequence()

def startSequence():
    global sequence_started
    if not sequence_started:
        cameraWarning.destroy()
        #Sequence(*piece_intervals).start()
        #Sequence.setPlayRate(0.2)
        sequence.start()
        sequence.setPlayRate(0.2)
        sequence_started = True

def calcCameraPosition():
    cam_x = cam_r * cos(cam_alpha) * cos(cam_beta)
    cam_y = cam_r * sin(cam_alpha) * cos(cam_beta)
    cam_z = cam_r * sin(cam_beta)
    base.camera.setPos(cam_x, cam_y, cam_z)
    base.camera.lookAt(0, 0, 0)

def importPieces():
    f = open('pieces.json')
    data = json.load(f)
    f.close()

    return data['pieces']

def createIntervalPositions(piece_sequence, piece_mapping):
    piece_intervals = []

    for piece in piece_sequence:
        piece_name = piece['name']
        piece_coords = piece['coordinates']
        match piece_name:
            case 'piece1':
                ip = piece_mapping[0].posInterval(1, (piece_coords['x'], piece_coords['y'], piece_coords['z']))
            case 'piece2':
                ip = piece_mapping[1].posInterval(1, (piece_coords['x'], piece_coords['y'], piece_coords['z']))
            case 'piece3':
                ip = piece_mapping[2].posInterval(1, (piece_coords['x'], piece_coords['y'], piece_coords['z']))
            case 'piece4':
                ip = piece_mapping[3].posInterval(1, (piece_coords['x'], piece_coords['y'], piece_coords['z']))

        piece_intervals.append(ip)

    return piece_intervals

def buildBarrierBox(color):
    for x in range(-2, 4):
        for z in range(-4, 0):
            y = -2
            box = makeAABox((x, y, z), (x + 1, y + 1, z + 1))
            box.setColor(*color)
            box = makeAABox((x, y + 5, z), (x + 1, y + 6, z + 1))
            box.setColor(*color)

    for y in range(-2, 2):
        for z in range(-4, 0):
            x = -2
            box = makeAABox((x, y + 1, z), (x + 1, y + 2, z + 1))
            box.setColor(*color)
            box = makeAABox((x + 5, y + 1, z), (x + 6, y + 2, z + 1))
            box.setColor(*color)

    for y in range(2):
        x = -1
        z = -3
        box = makeAABox((x, y, z), (x + 1, y + 1, z + 1))
        box.setColor(*color)
        box = makeAABox((x + 3, y, z), (x + 4, y + 1, z + 1))
        box.setColor(*color)

    box = makeAABox((-1, 0, -2), (0, 1, -1))
    box.setColor(*color)
    box = makeAABox((2, 1, -2), (3, 2, -1))
    box.setColor(*color)

if __name__ == '__main__':
    base = ShowBase()
    base.disableMouse()

    cam_alpha = 0
    cam_beta = 0
    cam_r = 10
    turn_speed = 0.07
    base.camLens.setFov(120) #wide angle view

    cameraWarning = OnscreenText(text="Please turn the camera!",
        style=1, fg=(1, 1, 1, 1), pos=(0, 0.8), scale=.12,
        align=TextNode.ACenter)

    nameText = OnscreenText(text="PocolocoSolver",
        style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
        parent=base.a2dBottomRight, align=TextNode.ARight)

    exitText = OnscreenText(text="Press ESC to exit",
        style=1, fg=(1, 1, 1, 1), pos=(0.1, 0.1), scale=.07,
        parent=base.a2dBottomLeft, align=TextNode.ALeft)

    addAmbientLight()
    addPointLight((-2, -4, 0))

    buildBarrierBox([0.5, 0.5, 0.5, 1])

    piece1 = buildPieces([0, 0], [0, 0], [1, 0, 0, 1]) #Rot
    piece2 = buildPieces([0, 2], [0, 2], [1, 1, 0, 1]) #Gelb
    piece3 = buildPieces([2, 0], [2, 0], [0, 1, 0, 1]) #Grün
    piece4 = buildPieces([2, 2], [2, 2], [0, 0, 1, 1]) #Blau

    piece_sequence = importPieces()
    piece_mapping = [piece1, piece2, piece3, piece4]
    piece_intervals = createIntervalPositions(piece_sequence, piece_mapping)

    sequence = Sequence(*piece_intervals)

    base.accept('arrow_right-repeat', moveCameraRight)
    base.accept('arrow_left-repeat', moveCameraLeft)
    base.accept('arrow_up-repeat', moveCameraUp)
    base.accept('arrow_down-repeat', moveCameraDown)
    base.accept('escape', sys.exit)

    base.run()