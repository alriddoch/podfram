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
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._renderer.add_object(
                        scene.sphere(self, [uniform(-25,25),
                                            uniform(-15,15),
                                            20], 1))
                    print pygame.mouse.get_pos()
                    # pygame.mouse.set_visible(False)
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.last_mouse_pos = None
                    # pygame.mouse.set_visible(True)
            if event.type == MOUSEMOTION: pass
                # if self.last_mouse_pos is not None: self.handle_mouse()
  def handle_keys(self, keys): pass
  def collide(self, args, geom1, geom2):
    contacts = ode.collide(geom1, geom2)
    # print type(geom1), type(geom2)
    if type(geom2) == ode.GeomPlane and type(geom1) == ode.GeomSphere:
      print "BOOOM"
      self.detonations.append(geom1.getBody().getPosition())
    for c in contacts:
      c.setBounce(0.9)
      c.setMu(5000)
      j = ode.ContactJoint(self.world, self.contact_group, c)
      j.attach(geom1.getBody(), geom2.getBody())
    
  def handle_world(self):
    self.space.collide((self.world,self.contact_group), self.collide)
    self.world.step(1/60.)
    self.contact_group.empty()
    for d in self.detonations:
      self._renderer.add_object(scene.explosion(self, d))
    self.detonations = []
  def run(self):
    #self._renderer.add_object(scene.sphere(self, [0,0,0], 10000))
    self._renderer.add_object(scene.floor(self, 25, 15))
    self._renderer.add_drop(hud.backdrop("worldphoto.jpg"))
    while self.running:
      self.handle_events(pygame.event.get())
      self.handle_keys(pygame.key.get_pressed())
      self.handle_world()
      self.clock.tick()
      self._renderer.update()
    print self.clock.get_fps()
