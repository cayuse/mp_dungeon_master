#  using this tutorial http://www.mygamefast.com/category/volume1/
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import matplotlib as mpl
import png
from PIL import Image
import IPython
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from IPython import embed


WORLD_HEIGHT = 257  # does have to be square
WORLD_WIDTH = WORLD_HEIGHT  # should be 2 ** x + 1 (x > 0)
BUF = 4  # minimum number of pixels between any two rooms we place
HIGH = 65535
LOW = 0

np.random.seed(12345)

# we are still using globals.. get over it.. we are  fiddling
canvas = np.zeros((WORLD_WIDTH,WORLD_HEIGHT), dtype=np.float) # Canvas of pixels hopefully all "black"
ai_canvas = np.zeros((WORLD_WIDTH,WORLD_HEIGHT), dtype=np.float) # Canvas of pixels hopefully all "black"

for x in range(0,WORLD_WIDTH):
    for y in range(0,WORLD_HEIGHT):
        canvas[x][y] = HIGH
        ai_canvas[x][y] = 65535
# here we make a certain number of room "widths" (second arg) with a poisson distribution around the first arg

# if all is right, we should have a nice 2d array, and we should be able to create a png out of it.
f = open('terrains/blankHM.png', 'wb')      # binary mode is important
w = png.Writer(WORLD_HEIGHT, WORLD_WIDTH, bitdepth=16, greyscale=True)
w.write(f, canvas)
f.close()

widths = np.random.poisson(25, 400)

# we have considered a special room that acts as a 'front door' but haven't implemented it
# problem: not all levels will have a front door on the same edge, only level 1, consider for later
def frontDoor():
    None

# this function takes a width (previously generated as a random distribution) and assigns a height for it
# so far we are getting very square rooms, and may want to tweak these values, but this is not a pressing issue
def getHeight(width):
    aspect = 0.8 + (np.random.rand() *0.4)
    return int(np.round(width * aspect, 0))

# this function takes a 4-element list of the format [x1,y1,x2,y2] plus a buffer argument for minimum spacing
# it returns true if the rectangles would overlap (or encroach on buffer space) false if not
# false is "useable" in this case
def overlaps(a,b, buff):
    if (a[0] - buff > b[2]):
        return False
    if (a[2] + buff < b[0]):
        return False
    if (a[1] - buff > b[3]):
        return False
    if (a[3] + buff < b[1]):
        return False
    return True

# this function takes 3 tuples start(x,y,z), end(x,y,z), cur(x,y) and returns the 'z' that cur should use
def getCurZ(start, stop, cur):
    totDist = np.sqrt( (start[0] - stop[0]) ** 2 + (start[1] - stop[1]) ** 2 )
    curDist = np.sqrt( (start[0] - cur[0])  ** 2 + (start[1] - cur[1])  ** 2 )
    heightrange = abs(start[2] - stop[2])
    return min(start[2], stop[2]) + heightrange * curDist / totDist

# this function takes a 6-element list of the format [x1,y1,x2,y2] and returns the 'Manhattan distance' between them
def dist(a,b):
    return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1]) #+ np.abs(a[2] - b[2])

dungeon_graph = nx.Graph()
a = 0
for ww in widths:
    hh = getHeight(ww)
    # the next two lines of code will pick a random place on the map
    # they should guarantee that the selected location won't go outside the map, given the room to be placed
    xx = np.random.randint(BUF, WORLD_WIDTH  - ww - BUF)
    yy = np.random.randint(BUF, WORLD_HEIGHT - hh - BUF)

    #the following loop compares against all previous rooms and checks for collisions
    add = True
    for node in dungeon_graph.nodes(data=True):
        origx = node[1]['x']
        maxx = origx + node[1]['w']
        origy = node[1]['y']
        maxy = origy + node[1]['h']
        if overlaps([origx, origy, maxx, maxy], [xx,yy, xx+ww, yy+hh], BUF):
            add = False
    # if there were no collisions, go through the process of adding the room
    if add:
        cx = xx + (ww / 2.0)
        cy = yy + (hh / 2.0)
        icy = WORLD_HEIGHT - cy
        iy  = WORLD_HEIGHT - yy
        print(cx)
        print(", ")
        print("( ")
        print(cy)
        print(" ),")
        zz = np.random.randint(5000) + 20000
        zz = LOW
        dungeon_graph.add_node(a,x = xx, y = yy, z = zz, w = ww, h = hh, cx = cx, cy = cy, iy = iy, icy = icy)
        # next add an edge to all existing rooms
        for let in range(0, a-1):
            distance = dist([cx,cy,zz],[dungeon_graph.node[let]['cx'], dungeon_graph.node[let]['cy'], dungeon_graph.node[let]['z']])
            dungeon_graph.add_edge(a,let, weight = distance )
        a = a + 1

# print the rooms to the canvas
for node in dungeon_graph.nodes(data=True):
    origx = node[1]['x']
    origy = node[1]['y']
    origz = node[1]['z']
    for doty in range(origy, origy + node[1]['h']):
        for dotx in range(origx, origx + node[1]['w']):
            canvas[dotx][doty] = origz
            ai_canvas[dotx][doty] = 0
## get a MST from the original graph, call it mst_dungeon
mst_dungeon = nx.minimum_spanning_tree(dungeon_graph)

## now lets fiddle with adding some of the edges back in.. in this case, we want to find leaf nodes
## and maybe add some connections back in.
## not implemented
leaf_nodes = [node for node in mst_dungeon.nodes() if mst_dungeon.degree(node)==1]
for edge in mst_dungeon.edges_iter():
  dungeon_graph.remove_edge(edge[0],edge[1])
a = nx.minimum_spanning_tree(dungeon_graph)
for edge in a.edges_iter():
  None
  #mst_dungeon.add_edge(edge[0],edge[1])

  for node in leaf_nodes:
    #mynode = dungeon_graph.node[node].nlist()
    #print mynode
    None
print("leaf nodes")
print(leaf_nodes)
keys = []
#embed()
keyKinds = ("e", "w", "f")
for i in range(3):
    x = int(mst_dungeon.node[leaf_nodes[i]]['cx'])
    y = int(mst_dungeon.node[leaf_nodes[i]]['icy'])
    keys.append( (x, y, keyKinds[i]) )
output = dump(keys, Dumper=Dumper)
stream = file('models/keys.yaml', 'w')
dump(keys, stream)
stream.close()

startLoc = ( int(mst_dungeon.node[leaf_nodes[4]]['cx']), int(mst_dungeon.node[leaf_nodes[4]]['icy']), 0)
stream = file('models/start.yaml', 'w')
dump(startLoc, stream)
stream.close()

#print "end leaf nodes"

"""
# this code was here to draw direct lines between the room centers where there are edges
# its commented out, we don't have an easy way to draw a straight line like this, so for now its jsut historical
# but may come in useful later, so i'll leave it
for edge in mst_dungeon.edges(data=True):
    node_a = mst_dungeon.node[edge[0]]
    node_b = mst_dungeon.node[edge[1]]
    #print node_a
    #print node_b
    #print edge
    # this shows the node links, turned off for the moment
    #plt.plot([node_a['cy'], node_b['cy']], [node_a['cx'], node_b['cx']], 'r-')

    if edge[2]['weight'] < 35:
        plt.plot([node_a['cy'], node_b['cy']], [node_a['cx'], node_b['cx']], 'r-')
    else:
        dungeon_graph.remove_edge(edge[0], edge[1])
"""




'''
#attemp to perterb the data a little
#for times in range(0,10):
for x in range(0,WORLD_WIDTH-5): #step by fives
    for y in range(0,WORLD_HEIGHT-5): #step by fives
        canvas[x][y] = canvas[x][y] + np.random.randint(4) - 2

for x in range(0,WORLD_WIDTH): #step by fives
    for y in range(0,WORLD_HEIGHT): #step by fives
        if canvas[x][y] > 255:
            canvas[x][y] = 255
        if canvas[x][y] < 0:
            canvas[x][y] = 0
'''
#after we fuzz the rooms, we  will bore the tunnels

# this is a version of the 'drunkards walk' to connect the rooms that have joining edges
for edge in mst_dungeon.edges(data=True):
    not_there = True
    node_a = mst_dungeon.node[edge[0]]
    node_b = mst_dungeon.node[edge[1]]
    start = (int(node_a['cx']), int(node_a['cy']), int(node_a['z']))
    stop  = (int(node_b['cx']), int(node_b['cy']), int(node_b['z']))
    cur   =  (int(node_a['cx']), int(node_a['cy']))
    #print "trying new path"
    while not_there:
      #if canvas[cur[0]][cur[1]] != start[2] and canvas[cur[0]][cur[1]] != stop[2]:
      #this_step = getCurZ(start, stop, cur)
      canvas[cur[0]][cur[1]]   = LOW
      canvas[cur[0]-1][cur[1]] = LOW
      canvas[cur[0]+1][cur[1]] = LOW
      canvas[cur[0]][cur[1]-1] = LOW
      canvas[cur[0]][cur[1]+1] = LOW
      canvas[cur[0]-2][cur[1]] = LOW
      canvas[cur[0]+2][cur[1]] = LOW
      canvas[cur[0]][cur[1]-2] = LOW
      canvas[cur[0]][cur[1]+2] = LOW
      ai_canvas[cur[0]][cur[1]]   = 0
      ai_canvas[cur[0]-1][cur[1]] = 0
      ai_canvas[cur[0]+1][cur[1]] = 0
      ai_canvas[cur[0]][cur[1]-1] = 0
      ai_canvas[cur[0]][cur[1]+1] = 0
      ai_canvas[cur[0]-2][cur[1]] = 0
      ai_canvas[cur[0]+2][cur[1]] = 0
      ai_canvas[cur[0]][cur[1]-2] = 0
      ai_canvas[cur[0]][cur[1]+2] = 0

      #plt.plot( start[1],start[0], 'or')
      #roll to see if we are going to go in the right direction
      lr = cur[0] - stop[0]
      ud = cur[1] - stop[1]
      good = []
      bad = []
      if lr > 0:
        good.append ((-1,0))
        bad.append ((1,0))
      if lr < 0:
        good.append ((1,0))
        bad.append ((-1,0))
      if lr == 0:
        bad.append ((-1,0))
        bad.append ((1,0))
      if ud < 0:
        good.append ((0,1))
        bad.append ((0,-1))
      if ud > 0:
        good.append ((0,-1))
        bad.append ((0,1))
      if ud == 0:
        bad.append ((0,-1))
        bad.append ((0,1))
      if np.random.rand() <= 1.0:
        #first 80% going in the "good" direction
        si = np.random.randint(len(good))
        step = good[si]
        cur = tuple(map(sum,zip(cur,step)))
      else:
        #rest goes in a "bad" direction
        si = np.random.randint(len(bad))
        step = bad[si]
        cur = tuple(map(sum,zip(cur,step)))
      if cur[0] == stop[0] and cur[1] == stop[1]:
        not_there = False
      #print start, stop

# attemp to perterb the data a little
# for times in range(0,10):
#for x in range(0, WORLD_WIDTH ):  # step by fives
#    for y in range(0, WORLD_HEIGHT ):  # step by fives
#        canvas[x][y] = canvas[x][y] + np.random.randint(200) - 100

#canvas[256][0] = 65535
#canvas[255][255] = 65535

torches = []
for node in dungeon_graph.nodes(data=True):
    print(node)
    x = int(node[1]['cx'])
    y = int(node[1]['y'])
    #check pixel above north
    if canvas[x][y-1] == HIGH:
        direction = 0 # north
    else: #east
        x = int(node[1]['x']) + int(node[1]['w'])
        y = int(node[1]['cy'])
        #check pixel right of east
        if canvas[x+1][5] == HIGH:
            direction = 1 #east
        else: #south
            x = int(node[1]['cx'])
            y = int(node[1]['cy']) + int(node[1]['h'])
            #check below south
            if canvas[x][y+1]:
                direction = 2 #south
            else:
                x = int(node[1]['x'])
                y = int(node[1]['cy'])
                #check left of west
                if canvas[x-1][y] == HIGH:
                    direction = 3
                else: #corner
                    x = int(node[1]['x'])
                    y = int(node[1]['y'])
                    direction = 4
    torches.append((x,y,direction))
output = dump(torches, Dumper=Dumper)
stream = file('models/torches.yaml', 'w')
dump(torches, stream)
stream.close()

# this gets used a bunch later
norm = mpl.colors.Normalize(np.min(canvas), np.max(canvas))


# if all is right, we should have a nice 2d array, and we should be able to create a png out of it.
f = open('terrains/ramp_HM.png', 'wb')      # binary mode is important
w = png.Writer(WORLD_HEIGHT, WORLD_WIDTH, bitdepth=16, greyscale=True)
w.write(f, canvas)
f.close()

#f = open('nav1.png', 'wb')      # binary mode is important
#w = png.Writer(WORLD_HEIGHT, WORLD_WIDTH, bitdepth=16, greyscale=True)
#w.write(f, ai_canvas)
#f.close()
cmap = plt.cm.RdGy_r
image = cmap(norm(canvas))
plt.imsave('../server/terrains/nav1.png', image)
#test = np.flipud(canvas)
#image = cmap(norm(test))
#plt.imsave('nav2.png', image)

# if all is right, we should have a nice 2d array, and we should be able to create a png out of it.
#f = open('ramp_HM.png', 'wb')  # binary mode is important
#w = png.Writer(WORLD_HEIGHT, WORLD_WIDTH, bitdepth=16, greyscale=True)
##w = png.Writer(WORLD_HEIGHT, WORLD_WIDTH, greyscale=True)
#w.write(f, canvas.tolist())
#f.close()

'''     
cmap = plt.cm.gist_earth
image = cmap(norm(canvas))
plt.imsave('terrains/ramp_TM.png', image)

swapped = np.flipud(canvas)
image = cmap(norm(swapped))
plt.imsave('ramp_TM.png', image)
'''
## next we are going to dump a Yaml description of the dungeon
