#  class Object:
#    def draw(): draw it

from OpenGL.GL import *
from OpenGL.GLU import *

import Image
import Numeric
import ode
import random

class floor:
  "A class that uses a physcical box to model a floor of limted size"
  def __init__(self, game, width, height):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    glColor3f(1,.9,.5)
    glBegin(GL_QUADS)
    glNormal3d(0,0,1)
    glVertex3f(-width,-height,0)
    glVertex3f(-width,height,0)
    glVertex3f(width,height,0)
    glVertex3f(width,-height,0)
    glEnd()
    glEndList()

    self.body = ode.Body(game.world)
    self.body.setKinematic()
    self.body.setPosition((0,0,0))
    self.geom = ode.GeomBox(game.space, (width*2, height*2, 0.1))
    self.geom.setBody(self.body)
  def draw(self):
    glPushMatrix()
    pos = self.body.getPosition()
    glTranslated(pos[0], pos[1], pos[2])
    glCallList(self.display_list)
    glPopMatrix()
  def obsolete(self):
    return False

class sphere:
  "A physical sphere, acting under gravity"
  def __init__(self, game, pos, radius):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricDrawStyle(quadric, GLU_FILL)
    glColor3f(1,0,0)
    gluSphere(quadric, radius, 16, 16)
    glEndList()

    self.body = ode.Body(game.world)
    self.body.setGravityMode(True)
    self.body.setPosition(pos)
    self.body.kind = sphere
    self.mass = ode.Mass()
    self.mass.setSphere(0.0001, radius)
    self.body.setMass(self.mass)
    self.geom = ode.GeomSphere(game.space,radius)
    self.geom.setBody(self.body)
  def draw(self):
    glPushMatrix()
    pos = self.body.getPosition()
    glTranslated(pos[0], pos[1], pos[2])
    glCallList(self.display_list)
    glPopMatrix()
  def obsolete(self):
    return False

class avatar:
  "A class the represents a cylindricall pseudo-humanoid avatar"
  def __init__(self, game, pos, radius):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricDrawStyle(quadric, GLU_FILL)
    glColor3f(0,0,1)
    glTranslated(0, 0, -1)
    gluCylinder(quadric, radius, radius, 2, 16, 16)
    glEndList()

    self.body = ode.Body(game.world)
    self.body.setGravityMode(True)
    self.body.setPosition(pos)
    self.body.kind = avatar
    self.mass = ode.Mass()
    self.mass.setCylinder(100, 3, radius, 2)
    self.body.setMass(self.mass)
    self.geom = ode.GeomCylinder(game.space, radius, 2)
    self.geom.setBody(self.body)
  def draw(self):
    glPushMatrix()
    pos = self.body.getPosition()
    glTranslated(pos[0], pos[1], pos[2])
    glCallList(self.display_list)
    glPopMatrix()
  def obsolete(self):
    return False

class portal:
  "An obsolete class for punching holes in other things"
  def __init__(self, game, pos, radius):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, radius+1, 16, 16)
    glEndList()

    self.body = ode.Body(game.world)
    self.body.setKinematic()
    self.body.setPosition(pos)
    self.body.kind = portal
    self.geom = ode.GeomSphere(game.space,radius)
    self.geom.setBody(self.body)
    self.pos = pos
    self.age = 0
    self.game = game
  def draw(self):
    pos = self.pos
    glPushMatrix()
    glTranslated(pos[0], pos[1], pos[2])
    glCallList(self.display_list)
    glPopMatrix()
    self.age += 1
  def obsolete(self):
    if self.age > 300:
      print "suicide"
      self.game.space.remove(self.geom)
      return True
    return False

class explosion:
  "An obsolete class which renders an expanding sphere to model a large bomb"
  def __init__(self, game, pos):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 100000, 16, 16)
    glEndList()

    self.size = 0
    self.pos = pos

  def draw(self):
    factor = self.size / 100.0
    glColor3f(1,min(factor/10,0.5),0)
    self.size += 1
    glPushMatrix()
    pos = self.pos
    glTranslated(pos[0], pos[1], pos[2])
    glScalef(factor, factor, factor)
    glCallList(self.display_list)
    glPopMatrix()
  def obsolete(self):
    return self.size > 200

class voxel:
  "This physics compenent of a voxel field"
  def __init__(self, game, pos):
    print pos
    self.body = ode.Body(game.world)
    self.body.setKinematic()
    self.body.setPosition(pos)
    self.body.kind = voxel
    self.geom = ode.GeomBox(game.space, (1,1,1))
    self.geom.setBody(self.body)

class voxels:
  "A 3D vosel field"
  def __init__(self, game):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    glBegin(GL_QUADS)
    # top
    glNormal3d(0,0,1)
    glVertex3f(-0.5,-0.5,0.5)
    glVertex3f(-0.5,0.5,0.5)
    glVertex3f(0.5,0.5,0.5)
    glVertex3f(0.5,-0.5,0.5)
    # bottom
    glNormal3d(0,0,-1)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,0.5,-0.5)
    glVertex3f(0.5,0.5,-0.5)
    glVertex3f(0.5,-0.5,-0.5)
    # back
    glNormal3d(0,-1,0)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(0.5,-0.5,-0.5)
    glVertex3f(0.5,-0.5,0.5)
    glVertex3f(-0.5,-0.5,0.5)
    # front
    glNormal3d(0,1,0)
    glVertex3f(-0.5,0.5,-0.5)
    glVertex3f(0.5,0.5,-0.5)
    glVertex3f(0.5,0.5,0.5)
    glVertex3f(-0.5,0.5,0.5)
    # left
    glNormal3d(-1,0,0)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,0.5,-0.5)
    glVertex3f(-0.5,0.5,0.5)
    glVertex3f(-0.5,-0.5,0.5)
    # right
    glNormal3d(1,0,0)
    glVertex3f(0.5,-0.5,-0.5)
    glVertex3f(0.5,0.5,-0.5)
    glVertex3f(0.5,0.5,0.5)
    glVertex3f(0.5,-0.5,0.5)
    glEnd()
    glEndList()

    self.game = game
    self.voxels = { }

    for x in range(-15, 15):
      for y in range(-10, 10):
        z = random.randint(-2, 2)
        self.add_voxel(x, y, z, 1)
  def add_voxel(self, x, y, z, val):
    "Add a vocel to the field"
    if not self.voxels.has_key(x):
      self.voxels[x] = {}
    row = self.voxels[x]
    if not row.has_key(y):
      row[y] = {}
    pillar = row[y]
    pillar[z] = voxel(self.game, (x,y,z))
  def draw(self):
    glColor3f(0.6,.9,.6)
    for x in self.voxels.keys():
      row = self.voxels[x]
      for y in row.keys():
        pillar = row[y]
        for z in pillar.keys():
          # print x, y, z
          glPushMatrix()
          glTranslated(x, y, z)
          glCallList(self.display_list)
          glPopMatrix()
  def obsolete(self):
    return False

class heightfield:
  def __init__(self, filename):
    image = Image.open(filename)
    raw = image.tostring("raw", "RGBX", 0, -1)
    print image.size, len(raw)
    width = image.size[0]
    height = image.size[1]
    vertex_count = width * height
    vertices = Numeric.zeros((vertex_count, 3), Numeric.Float32)
    sea_vertices = Numeric.zeros((vertex_count, 3), Numeric.Float32)
    for y in range(0, height):
      for x in range(0, width):
        index = x + y * width
        vertices[index, 0] = x - (width / 2)
        vertices[index, 1] = y - (height / 2)
        vertices[index, 2] = (float(ord(raw[(index) * 4]))  - 128.0) / 4.0
        sea_vertices[index, 0] = x - (width / 2)
        sea_vertices[index, 1] = y - (height / 2)
        sea_vertices[index, 2] = 0.0
    normals = Numeric.zeros((vertex_count, 3), Numeric.Float32)
    colors = Numeric.zeros((vertex_count, 3), Numeric.Float32)
    for y in range(1, height - 1):
      for x in range(1, width - 1):
        index = x + y * width
        h1 = vertices[(x - 1) + y * width, 2]
        h2 = vertices[x +       ((y + 1) * width), 2]
        h3 = vertices[x + 1 +   y * width, 2]
        h4 = vertices[x +       (y - 1) * width, 2]
        
        normals[index, 0] = (h1 - h3) / 2.0
        normals[index, 1] = (h4 - h2) / 2.0
        normals[index, 2] = 1.0
        steepness = abs(h1 - h3) + abs(h3 - h2)
        z = vertices[index, 2]
        if z < -1.0:
          grey = 0.6 * (32.0 + z) / 32.0
          colors[index, 0] = grey
          colors[index, 1] = grey
          colors[index, 2] = grey
        elif steepness < 4.0:
          if z < 1.0:
            colors[index, 0] = 1.0
            colors[index, 1] = 1.0
            colors[index, 2] = 0.0
          else:
            colors[index, 0] = 0.0
            colors[index, 1] = 1.0
            colors[index, 2] = 0.0
        else:
          colors[index, 0] = 0.4
          colors[index, 1] = 0.4
          colors[index, 2] = 0.4
          
    print len(vertices), len(vertices.tostring())
    #self.vertices = vertices.tostring()
    #self.colors = colors.tostring()
    #self.normals = normals.tostring()
    #self.vertex_count = vertex_count

    index_count = width * height * 2
    indices = Numeric.zeros((index_count), Numeric.Int32)
    idx = 0
    x = 0
    while x < (width - 1):
      # std::cout << "G: " << i << ":" << (i&2) << std::endl << std::flush;
      if x & 1:
        y = height - 1
        while y >= 0:
          indices[idx] = y * width + x + 1
          idx += 1
          indices[idx] = y * width + x
          idx += 1
          y -= 1
      else:
        y = 0
        while y < height:
          indices[idx] = y * width + x
          idx += 1
          indices[idx] = y * width + x + 1
          idx += 1
          y += 1
      x += 1
    print index_count, idx
    self.indices = indices.tostring()
    self.index_count = idx

    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

    # Draw the land
    glVertexPointer(3, GL_FLOAT, 0, vertices.tostring())
    glColorPointer(3, GL_FLOAT, 0, colors.tostring())
    glNormalPointer(GL_FLOAT, 0, normals.tostring())
    glDrawElements(GL_TRIANGLE_STRIP, self.index_count,
                   GL_UNSIGNED_INT, self.indices)

    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)

    # Draw the sea
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glColor4f(0, 0.4, 0.9, 0.4)
    glNormal3d(0,0,1)
    glVertexPointer(3, GL_FLOAT, 0, sea_vertices.tostring())
    glDrawElements(GL_TRIANGLE_STRIP, self.index_count,
                   GL_UNSIGNED_INT, self.indices)
    glDisable(GL_BLEND)

    glDisableClientState(GL_VERTEX_ARRAY)

    glEndList()
  def draw(self):
    glCallList(self.display_list)
  def obsolete(self):
    return False
