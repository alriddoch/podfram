#  class Object:
#    def draw(): draw it

from OpenGL.GL import *
from OpenGL.GLU import *

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
    glNormal3d(0,0,1)
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
