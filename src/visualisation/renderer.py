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
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectSlider


from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task


loadPrcFileData("", "fullscreen true")
loadPrcFileData("", "win-origin 0 0")
loadPrcFileData("", "undecorated true")
loadPrcFileData("", "win-size 1920 1080")

sequence_started = False
sequence_paused = False


def toggleSequence():
    global sequence_paused
    if sequence_paused:
        sequence.resume()
    else:
        sequence.pause()
    sequence_paused = not sequence_paused


def resetSequence():
    global sequence_paused
    sequence.finish()
    sequence.pause()
    sequence.setT(0)
    sequence_paused = True


def stepForward():
    current_time = sequence.getT()
    new_time = min(sequence.getDuration(), current_time + 1)
    sequence.setT(new_time)
    sequence.pause()


def stepBackward():
    current_time = sequence.getT()
    new_time = max(0, current_time - 1)
    sequence.setT(new_time)
    sequence.pause()


def zoomIn():
    global cam_r
    cam_r = max(2, cam_r - 1)
    calc_camera_position()


def zoomOut():
    global cam_r
    cam_r += 1
    calc_camera_position()


def adjustSpeed():
    speed = speedSlider['value']
    sequence.setPlayRate(speed)


speedSlider = DirectSlider(
    range=(0.1, 2.0),
    value=1.0,
    pageSize=0.1,
    scale=0.4,
    pos=(0, 0, -0.8),
    command=adjustSpeed
)


cam_alpha = 0
cam_beta = 0.5
cam_r = 15
turn_speed = 1.5

key_states = {
    "lookLeft": False,
    "lookRight": False,
    "lookUp": False,
    "lookDown": False
}

def normalized(*args):
    vec = LVector3(*args)
    vec.normalize()
    return vec

def create_geometry():
    format = GeomVertexFormat.getV3n3()
    vdata = GeomVertexData('piece', format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    scene = Geom(vdata)

    return scene, (vertex, normal)


def create_geom_node(geom):
    node = GeomNode('scene')
    scene,_ = geom
    node.addGeom(scene)
    return render.attachNewNode(node)

def make_box(pMin, pMax):
    geom = create_geometry()
    addAABox(pMin, pMax, geom)
    return create_geom_node(geom)

# Extends an existing geometry with an axex aligned box
# corner1 and corner 2 must be opposite corners
def addAABox(corner1, corner2, geom):
    # get corners with minimal and maximal coordinates, resp.
    pMin,pMax = zip(*[(min(c1,c2),max(c1,c2)) for c1,c2 in zip(corner1,corner2)])
    # Unpack the geometry tuple into scene and the vertex/normal writers
    scene, (vertex, normal) = geom
    tris = GeomTriangles(Geom.UHStatic)

    # Calculate the midpoint, coordinate ranges and side lengths of the bounding box
    ranges = tuple(zip(pMin, pMax))
    pMid = [0.5 * sum(range) for range in ranges]
    lengths = [cMax - cMin for cMin,cMax in ranges]

    # Add vertices and normals to create the 6 faces of the bounding box
    for axis_idx in range(3): # x,y,z
        for axis_orient in (-1, 1):
            face_normal = [0, 0, 0]
            face_normal[axis_idx] = axis_orient
            vec_normal_2 = face_normal[-axis_orient:] + face_normal[:-axis_orient]
            vec_normal_3 = face_normal[axis_orient:] + face_normal[:axis_orient]
            face_center = [cMid + c_normal * lengths[axis_idx]/2 for cMid, c_normal in zip(pMid, face_normal)]
            # first corner of face
            face_start = [face_center[i] - vec_normal_2[i] * lengths[(axis_idx+1)%3] / 2 - vec_normal_3[i] * lengths[(axis_idx+2)%3] / 2
                          for i in range(3)]
            # Get number of vertices in the existing geometry
            vertCnt = vertex.getVertexData().get_num_rows()
            # add 4 corners of the face
            for corner_idx in range(4):
                corner = [face_start[i] +
                          ((corner_idx+1)%4//2) * vec_normal_2[i] * lengths[(axis_idx+1)%3] +
                          (corner_idx//2)       * vec_normal_3[i] * lengths[(axis_idx+2)%3] for i in range(3)]
                vertex.addData3(*corner)
                normal.addData3(*face_normal)
            # add two triangles for this face
            tris.addVertices(vertCnt, vertCnt + 1, vertCnt + 2)
            tris.addVertices(vertCnt, vertCnt + 2, vertCnt + 3)

    # Add all (12) triangles of the box to the existing geometry
    scene.addPrimitive(tris)


def add_ambient_light(intensity=0.5):
    light = AmbientLight('ambientLight')
    light_color = tuple(3 * [intensity] + [1])
    light.setColor(light_color)
    light_np = render.attachNewNode(light)
    render.setLight(light_np)


def add_point_light(pos, intensity=1):
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
    box = make_box((-1 + x_offset, -1 + y_offset, -1), (0 + x_offset, 0 + y_offset, 0))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = make_box((0 + x_offset, -1 + y_offset, -1), (1 + x_offset, 0 + y_offset, 0))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = make_box((-1 + x_offset, 0 + y_offset, -1), (0 + x_offset, 1 + y_offset, 0))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = make_box((0 + x_offset, 0 + y_offset, -1), (1 + x_offset, 1 + y_offset, 0))
    box.setColor(*color)
    box.reparentTo(blocknp)

    #bridge part
    box = make_box((-1 + x_offset + bridge_x, -1 + y_offset + bridge_y, -2), (0 + x_offset, 0 + y_offset, -1))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = make_box((-1 + x_offset + bridge_x, -1 + y_offset + bridge_y, -3), (0 + x_offset, 0 + y_offset, -2))
    box.setColor(*color)
    box.reparentTo(blocknp)

    #bottom part
    box = make_box((-1 + x_offset, -1 + y_offset, -4), (0 + x_offset, 0 + y_offset, -3))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = make_box((0 + x_offset, -1 + y_offset, -4), (1 + x_offset, 0 + y_offset, -3))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = make_box((-1 + x_offset, 0 + y_offset, -4), (0 + x_offset, 1 + y_offset, -3))
    box.setColor(*color)
    box.reparentTo(blocknp)
    box = make_box((0 + x_offset, 0 + y_offset, -4), (1 + x_offset, 1 + y_offset, -3))
    box.setColor(*color)
    box.reparentTo(blocknp)

    block.collect()
    return blocknp

def createIntervalPositions(piece_sequence, piece_mapping):
    piece_intervals = []
    piece_positions = [mapping.get_pos() for mapping in piece_mapping]

    for piece in reversed(piece_sequence):
        piece_name = piece['name']
        piece_coords = piece['coordinates']

        coords = (piece_coords['dx'], piece_coords['dy'], piece_coords['dz'])
        #coords = (piece_coords['x'], piece_coords['y'], piece_coords['z'])

        piece_index = int(piece_name[-1]) - 1
        piece_positions[piece_index] += coords
        ip = piece_mapping[piece_index].posInterval(1, piece_positions[piece_index])

        piece_intervals.append(ip)

    return piece_intervals

def buildBarrierBox(color):
    for x in range(-2, 4):
        for z in range(-4, 0):
            y = -2
            box = make_box((x, y, z), (x + 1, y + 1, z + 1))
            box.setColor(*color)
            box = make_box((x, y + 5, z), (x + 1, y + 6, z + 1))
            box.setColor(*color)

    for y in range(-2, 2):
        for z in range(-4, 0):
            x = -2
            box = make_box((x, y + 1, z), (x + 1, y + 2, z + 1))
            box.setColor(*color)
            box = make_box((x + 5, y + 1, z), (x + 6, y + 2, z + 1))
            box.setColor(*color)

    for x in range(2):
        y = -1
        z = -3
        box = make_box((x, y, z), (x + 1, y + 1, z + 1))
        box.setColor(*color)
        box = make_box((x, y + 3, z), (x + 1, y + 4, z + 1))
        box.setColor(*color)

    box = make_box((0, -1, -2), (1, 0, -1))
    box.setColor(*color)
    box = make_box((1, 2, -2), (2, 3, -1))
    box.setColor(*color)

def start_sequence():
    global sequence_started
    if not sequence_started:
        cameraWarning.destroy()
        sequence.start()
        sequence.setPlayRate(0.5)
        sequence_started = True

def calc_camera_position():
    cam_x = cam_r * cos(cam_alpha) * cos(cam_beta)
    cam_y = cam_r * sin(cam_alpha) * cos(cam_beta)
    cam_z = cam_r * sin(cam_beta)
    base.camera.setPos(cam_x, cam_y, cam_z)
    base.camera.lookAt(0, 0, 0)

def update_camera(task):
    global cam_alpha, cam_beta
    dt = globalClock.getDt()

    moved = False

    if key_states["lookLeft"]:
        cam_alpha -= turn_speed * dt
        calc_camera_position()
        moved = True
    if key_states["lookRight"]:
        cam_alpha += turn_speed * dt
        calc_camera_position()
        moved = True
    if key_states["lookUp"]:
        cam_beta += turn_speed * dt
        if cam_beta > PI / 2:
            cam_beta = PI / 2 - 0.05
        calc_camera_position()
        moved = True
    if key_states["lookDown"]:
        cam_beta -= turn_speed * dt
        if cam_beta < -PI / 2:
            cam_beta = -PI / 2 + 0.05
        calc_camera_position()
        moved = True

    if moved:
        start_sequence()

    return Task.cont

def press_key(key):
    key_states[key] = True

def release_key(key):
    key_states[key] = False

def import_pieces():
    f = open('pieces.json')
    data = json.load(f)
    f.close()

    return data['pieces']

if __name__ == '__main__':
    base = ShowBase()
    base.disableMouse()

    base.camLens.setFov(100) #wide angle view (usually 120 for debugging)

    cameraWarning = OnscreenText(text="Please turn the camera! Hold arrows",
                                 style=1, fg=(1, 1, 1, 1), pos=(0, 0.8), scale=.12,
                                 align=TextNode.ACenter)

    nameText = OnscreenText(text="PocolocoSolver",
        style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
        parent=base.a2dBottomRight, align=TextNode.ARight)

    exitText = OnscreenText(text="Press ESC to exit",
        style=1, fg=(1, 1, 1, 1), pos=(0.1, 0.1), scale=.07,
        parent=base.a2dBottomLeft, align=TextNode.ALeft)

    add_ambient_light()
    add_point_light((-3, -4, 2))
    calc_camera_position()

    buildBarrierBox([0.5, 0.5, 0.5, 1])

    piece1 = buildPieces([0, 0], [0, 0], [1, 0, 0, 1])  # Rot
    piece2 = buildPieces([0, 2], [0, 2], [1, 1, 0, 1])  # Gelb
    piece3 = buildPieces([2, 0], [2, 0], [0, 1, 0, 1])  # Grün
    piece4 = buildPieces([2, 2], [2, 2], [0, 0, 1, 1])  # Blau

    piece_sequence = import_pieces()
    piece_mapping = [piece4, piece2, piece3, piece1]
    piece_intervals = createIntervalPositions(piece_sequence, piece_mapping)

    sequence = Sequence(*piece_intervals)

    base.accept('arrow_left', press_key, ["lookLeft"])
    base.accept('arrow_left-up', release_key, ["lookLeft"])
    base.accept('arrow_right', press_key, ["lookRight"])
    base.accept('arrow_right-up', release_key, ["lookRight"])
    base.accept('arrow_up', press_key, ["lookUp"])
    base.accept('arrow_up-up', release_key, ["lookUp"])
    base.accept('arrow_down', press_key, ["lookDown"])
    base.accept('arrow_down-up', release_key, ["lookDown"])
    base.accept('escape', sys.exit)

    pauseButton = DirectButton(
        text="Pause/Play", scale=0.07, pos=(-0.5, 0.5, -0.4),
        command=toggleSequence, parent=base.a2dTopRight
    )

    resetButton = DirectButton(
        text="Reset", scale=0.07, pos=(-0.5, 0.5, -0.3),
        command=resetSequence, parent=base.a2dTopRight
    )

    forwardButton = DirectButton(
        text=">>", scale=0.1, pos=(-0.4, 0, -0.5),
        command=stepForward, parent=base.a2dTopRight
    )

    backwardButton = DirectButton(
        text="<<", scale=0.1, pos=(-0.6, 0, -0.5),
        command=stepBackward, parent=base.a2dTopRight
    )

    zoomInButton = DirectButton(
        text="Zoom In", scale=0.07, pos=(-0.5, 0.5, -0.1),
        command=zoomIn, parent=base.a2dTopRight
    )

    zoomOutButton = DirectButton(
        text="Zoom Out", scale=0.07, pos=(-0.5, 0.5, -0.2),
        command=zoomOut, parent=base.a2dTopRight
    )

    speedLabel = OnscreenText(
        text="Sequence Speed", pos=(0, 0.1), scale=0.07, fg=(1, 1, 1, 1),
        align=TextNode.ACenter, parent=base.a2dBottomCenter
    )

    taskMgr.add(update_camera, "update_camera_task")
    base.run()