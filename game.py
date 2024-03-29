import ode
from pygame.locals import *
import pygame
from random import uniform

import hud
import scene

class podflaps:
  _GRAVITY = 9.81
  def __init__(self):
    pygame.init()

    self.running = True
    self.clock = pygame.time.Clock()
    self.world = ode.World()
    self.world.setGravity((0,0,-self._GRAVITY))
    self.world.setERP(0.8)
    self.world.setCFM(1E-5)
    self.space = ode.Space()
    self.contact_group = ode.JointGroup()
    #self.floor = ode.GeomPlane(self.space, (0,0,1), -50)
    #self.walls = [ode.GeomPlane(self.space, (1,0,0), -500000),
                  #ode.GeomPlane(self.space, (-1,0,0), -500000),
                  #ode.GeomPlane(self.space, (0,1,0), -500000),
                  #ode.GeomPlane(self.space, (0,-1,0), -500000)]

    self.detonations = []
  def add_renderer(self, r):
    self._renderer = r
  def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_UP:
                  print "1"
                  self.character.body.setForce((0,10000,0))
                if event.key == K_DOWN:
                  self.character.body.setForce((0,-10000,0))
                if event.key == K_LEFT:
                  self.character.body.setForce((-10000,0,0))
                if event.key == K_RIGHT:
                  self.character.body.setForce((10000,0,0))
                if event.key == K_SPACE:
                  self.character.body.setForce((0,0,10000))
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    print pygame.mouse.get_pos()
                    pos = self._renderer.click(pygame.mouse.get_pos())
                    print pos
                    self._renderer.add_object(
                        scene.sphere(self, pos, 2))
                    # pygame.mouse.set_visible(False)
                elif event.button == 4:
                    self._renderer.scale /= 1.2
                elif event.button == 5:
                    self._renderer.scale *= 1.2
                  
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.last_mouse_pos = None
                    # pygame.mouse.set_visible(True)
            if event.type == MOUSEMOTION: pass
                # if self.last_mouse_pos is not None: self.handle_mouse()
  def handle_keys(self, keys): pass
  def detect_interaction(self, platform, other):
    body = other.getBody()
    if body is not None and hasattr(body, 'kind'):
      if body.kind == scene.sphere:
        print "BOOOM"
        self.detonations.append((other, body.getPosition()))
  def detect_death(self, one, two):
    body_one = one.getBody()
    body_two = two.getBody()
    if body_one is None or body_two is None:
      return
    if not hasattr(body_one, 'kind') or not hasattr(body_two, 'kind'):
      return
    if body_one.kind == scene.avatar and body_two.kind == scene.portal or \
       body_two.kind == scene.avatar and body_one.kind == scene.portal:
      print "ARRRG"
      self.character.geom.disable()

  def collide(self, args, geom1, geom2):
    contacts = ode.collide(geom1, geom2)
    # print type(geom1), type(geom2)
    if type(geom1) == ode.GeomBox:
      self.detect_interaction(geom1, geom2)
    elif type(geom2) == ode.GeomBox:
      self.detect_interaction(geom2, geom1)
    else:
      self.detect_death(geom1, geom2)
    for c in contacts:
      c.setBounce(0.2)
      c.setMu(5000)
      j = ode.ContactJoint(self.world, self.contact_group, c)
      j.attach(geom1.getBody(), geom2.getBody())
    
  def handle_world(self):
    self.space.collide((self.world,self.contact_group), self.collide)
    self.world.step(1/60.)
    self.contact_group.empty()
    for d in self.detonations:
      geom = d[0]
      pos = d[1]
      self._renderer.add_pre_object(scene.portal(self, (pos[0], pos[1], 0), 1))
      self.space.remove(geom)
      self._renderer.remove_object_by_geom(geom)
    self.detonations = []
  def run(self):
    #self._renderer.add_object(scene.sphere(self, [0,0,0], 10000))
    #self._renderer.add_object(scene.floor(self, 25, 15))
    #self._renderer.add_object(scene.voxels(self))
    #self._renderer.add_drop(hud.sky())
    self._renderer.add_object(scene.heightfield("diplomacy_heightfield.jpg"))

    self.character = scene.avatar(self, (0, 0, 5), 0.3)
    self._renderer.add_object(self.character)
    while self.running:
      self.handle_events(pygame.event.get())
      self.handle_keys(pygame.key.get_pressed())
      self.handle_world()
      self.clock.tick()
      #self._renderer.set_camera_focus(self.character.body.getPosition())
      self._renderer.update()
    print self.clock.get_fps()
