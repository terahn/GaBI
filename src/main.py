#!/usr/bin/env python3

import pygame
import math, random, sys
from pygame.locals import *
#from socket import *
import sys
from audio_input import *
from app_constants import *
from tkinter import *
from tkinter import filedialog as fd
from engine import gabi_run

root = Tk()
root.withdraw()

pygame.mixer.pre_init(22050, -16, 2, 1024) #
pygame.init()
pygame.mixer.set_num_channels(10)

# ----- pygame-loaded constants ------
# visuals
BACKGROUND = pygame.image.load("images/app_background.png")
ICONIMAGES = pygame.image.load("images/iconimages.png")

# sound
SFX1 = pygame.mixer.Sound("audio_out/kill.ogg")
SFX2 = pygame.mixer.Sound("audio_out/deeo.ogg")
SFX3 = pygame.mixer.Sound("audio_out/dadi.ogg")

class ToggleButton(pygame.sprite.Sprite):  
  def __init__(self, width, height, x, y):
    self.sheet = ICONIMAGES
    self.image = pygame.Surface( (width, height), pygame.SRCALPHA )
    self.rect = self.image.get_rect()
    self.image.blit(self.sheet, (0, 0))
    self.rect.x = x
    self.rect.y = y
    self.on = False

# circular button/sprite?
class PressButton(pygame.sprite.Sprite):
  def __init__(self, width, height, x, y, offset_x, offset_y):
    self.sheet = ICONIMAGES
    self.image = pygame.Surface( (width, height), pygame.SRCALPHA )
    self.rect = self.image.get_rect()
    self.image.blit(self.sheet, (offset_x, offset_y))
    self.rect.x = x
    self.rect.y = y
    self.pressed = False
  
    
class Interface:
  def __init__(self):
    global root
    self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption(TITLE)
    self.CLOCK = pygame.time.Clock()
    self.running = True
    self.framecount = 0
    self.background = BACKGROUND
    self.image = pygame.Surface( (790, 512), pygame.SRCALPHA )
    self.image.blit(self.background, ( 0,0 ) )

    # placeholders
    self.input_sample_name = '../samples/140_lofi_rhodes.wav'
    self.kick_sample_name = '../samples/drums/kicks/kick1.wav'
    self.snare_sample_name = '../samples/drums/snares/snare1.wav'
    self.hat_sample_name = '../samples/drums/hats/hat1.wav'
    self.output_name = '../output/frontend-output.wav'

    self.output_loaded = False
    self.playing_output = False
    
    self.doubleClickCount = 0
    self.setDoubleClick = False
    
    self.drum_seq_buttons = []
    for b in range(16):
      hihat_button = ToggleButton(DPAT_B_WIDTH, DPAT_B_HEIGHT, 380+(b*(DPAT_B_WIDTH+5)), 80)
      self.drum_seq_buttons.append(hihat_button)
    for b in range(16):
      snare_button = ToggleButton(DPAT_B_WIDTH, DPAT_B_HEIGHT, 380+(b*(DPAT_B_WIDTH+5)), 150)
      self.drum_seq_buttons.append(snare_button)
    for b in range(16):
      kick_button = ToggleButton(DPAT_B_WIDTH, DPAT_B_HEIGHT, 380+(b*(DPAT_B_WIDTH+5)), 220)
      self.drum_seq_buttons.append(kick_button)
    
    self.load_snare_button = PressButton(80, 95, 110, 350, 0-90, 0-65)
    self.load_kick_button = PressButton(80, 95, 5, 350, 0-90, 0-65)
    self.load_hat_button = PressButton(80, 95, 217, 350, 0-90, 0-65)
    self.load_sample_button = PressButton(80, 95, 20, 70, 0-90, 0-65)
    self.generate_button = PressButton(80, 95, 350, 370, 0, 0-162)
    self.playback_button = PressButton(80, 95, 460, 370, 0-180, 0-162)
    
    # ------- audio stuff ------
    # output
    
    self.short_noise = SFX1
    self.short_throw = SFX2
    self.short_blip = SFX3
    
    # input
    #self.audio_thing = audio_input()
    self.output_freq = 0
    # ------- Tkinter?
    
    
  def OpenFile(self):
    name = ""
    try:
      name = fd.askopenfilename(
        initialdir=".",
        filetypes =(("Audio Sample", "*.wav"),("All Files","*.*")),
        title = "Choose an audio file."
      )
    except:
      pass
    return name
    
    
    
    
  def input(self):
    x, y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        print("quitting")
        pygame.quit()
      
      # keyboard events
      elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          print("quitting")
          pygame.quit()
        elif event.key == K_LEFT:
          pass # rewind
      elif event.type == KEYUP:
        if event.key == K_LEFT:
          pass # stop rewinding
      
      # mouse events
      elif event.type == CLICK_HOLD:
        
        for (index, dsb) in enumerate(self.drum_seq_buttons):
          if dsb.rect.collidepoint((x,y)):
            print("button toggled")
            if not dsb.on:
              try:
                if index < 16:
                  self.hat_sound.play()
                elif index >= 16 and index < 32:
                  self.snare_sound.play()
                else:
                  self.kick_sound.play()
              except:
                print('Sample not loaded yet')
              dsb.image.blit(dsb.sheet, ( 0 - 1*DPAT_B_WIDTH - 20, 0 - 0*DPAT_B_HEIGHT ) )
              dsb.on = True
            else:
              dsb.image.blit(dsb.sheet, ( 0 - 0*DPAT_B_WIDTH, 0 - 0*DPAT_B_HEIGHT ) )
              dsb.on = False
        if self.load_sample_button.rect.collidepoint((x,y)):
          #self.load_sample_button.blit
          self.input_sample_name = self.OpenFile()
          self.load_sample_button.image.blit(self.load_sample_button.sheet, (0, 0-65))
          print(self.input_sample_name)
        if self.load_kick_button.rect.collidepoint((x,y)):
          #self.load_kick_button.blit
          self.kick_sample_name = self.OpenFile()
          try:
            self.kick_sound = pygame.mixer.Sound(self.kick_sample_name)
          except:
            print('file cannot be 32 bits per sample')
          self.load_kick_button.image.blit(self.load_kick_button.sheet, (0, 0-65))
          print(self.kick_sample_name)
        if self.load_snare_button.rect.collidepoint((x,y)):
          #self.load_snare_button.blit
          self.snare_sample_name = self.OpenFile()
          try:
            self.snare_sound = pygame.mixer.Sound(self.snare_sample_name)
          except:
            print('file cannot be 32 bits per sample')
          self.load_snare_button.image.blit(self.load_snare_button.sheet, (0, 0-65))
          print(self.snare_sample_name)
        if self.load_hat_button.rect.collidepoint((x,y)):
          #self.load_hat_button.blit
          self.hat_sample_name = self.OpenFile()
          try:
            self.hat_sound = pygame.mixer.Sound(self.hat_sample_name)
          except:
            print('file cannot be 32 bits per sample')
          self.load_hat_button.image.blit(self.load_hat_button.sheet, (0, 0-65))
          print(self.hat_sample_name)

        # generate button clicked
        if self.generate_button.rect.collidepoint((x,y)):
          self.playback_button.image.blit(self.playback_button.sheet, (0-180, 0-162))
          self.generate()
        
        # play button clicked
        if self.playback_button.rect.collidepoint((x,y)) and self.output_loaded:
          if self.playing_output == False:
            print('Play')
            self.playback_button.image.blit(self.playback_button.sheet, (0-90, 0-162))
            self.output_file.play()
            self.playing_output = True
          else:
            print('Stop')
            self.playback_button.image.blit(self.playback_button.sheet, (0-180, 0-65))
            self.output_file.stop()
            self.playing_output = False
        
        if not self.setDoubleClick:
          self.setDoubleClick = True
          
        else:
          self.setDoubleClick = False
          self.doubleClickCount = 0
          
      
      elif event.type == UNCLICK_RELEASE:
        pass
     
  def audio_input(self, play_freq=4):
    sa, sf, amp, rms, fre, mfccs, note = self.audio_thing.stream_capture()
    
    if fre < 30000:
      if rms > 30 and fre < 30000:
        #print(fre, rms, sa+sf, note)
        print(sa+sf, note)
      else:
        print(".")
      
    self.playing_sound()
      
  def reset_sound(self, play_freq):
    self.output_freq = play_freq
   
  def playing_sound(self):
    self.output_freq -= 1
    if self.output_freq <= 0:
      self.output_freq = 0
       
  def update(self):
    self.framecount += 1
    if self.setDoubleClick:
      self.doubleClickCount += 1
      if self.doubleClickCount >= 10:
        self.doubleClickCount = 0
        self.setDoubleClick = False
        print("double click reset")

  def draw(self):
    self.image.blit(self.background, (0,0))
    self.screen.blit(self.image, (0,0))
    for dsb in self.drum_seq_buttons:
      self.screen.blit(dsb.image, (dsb.rect.x, dsb.rect.y))
    self.screen.blit(self.load_sample_button.image, (self.load_sample_button.rect.x, self.load_sample_button.rect.y))
    self.screen.blit(self.generate_button.image, (self.generate_button.rect.x, self.generate_button.rect.y))
    self.screen.blit(self.load_kick_button.image, (self.load_kick_button.rect.x, self.load_kick_button.rect.y))
    self.screen.blit(self.load_snare_button.image, (self.load_snare_button.rect.x, self.load_snare_button.rect.y))
    self.screen.blit(self.load_hat_button.image, (self.load_hat_button.rect.x, self.load_hat_button.rect.y))
    self.screen.blit(self.playback_button.image, (self.playback_button.rect.x, self.playback_button.rect.y))

    pygame.display.flip()

  def generate(self):
    print('run beat generation with the following:')
    print(self.input_sample_name)
    print(self.kick_sample_name)
    print(self.snare_sample_name)
    print(self.hat_sample_name)
    print([dsb.on for dsb in self.drum_seq_buttons])
    drum_sequence = [dsb.on for dsb in self.drum_seq_buttons]
    gabi_run(self.input_sample_name, self.kick_sample_name, self.snare_sample_name, self.hat_sample_name, drum_sequence)
    self.output_file = pygame.mixer.Sound(self.output_name)
    self.playback_button.image.blit(self.playback_button.sheet, (0-180, 0-65))
    self.output_loaded = True

  
  # 'main' loop:
  def run(self):
    self.playing = True
    while self.playing:
      self.CLOCK.tick(FPS)
      self.input()
      self.update()
      self.draw()
      #self.audio_input()
      

 
if __name__ == '__main__':
  I = Interface()
  I.run()

pygame.quit()