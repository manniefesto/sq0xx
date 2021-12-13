#!/usr/bin/env python3

# Generator for Alps/Matias(Alps equivalent) keyboard switches

import sys
import os

# sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "kicad-footprint-generator"))  # load parent path of KicadModTree

import argparse
import yaml
import math

from KicadModTree import *

base_name = "SW_Alps_Matias"
base_tags = "Alps Matias Keyboard Keyswitch Switch Plate"
base_description = "Alps/Matias keyswitch (Matias is Alps Compatible), https://github.com/keyboardio/keyswitch_documentation/blob/master/datasheets/ALPS/SKCL.pdf"

# location_3d = "${KISYS3DMOD}/Switch_Keyboard_Alps_Matias.3dshapes/" + base_name + ".wrl"
location_3d = "${KEYSWITCH_LIB_3D}/Switch_Keyboard_Alps_Matias.3dshapes/" + base_name + ".wrl"

unit_value = 19.05

def generate_switch(footprint_name, footprint_description, footprint_tags):
	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	kicad_mod.setDescription(footprint_description)
	kicad_mod.setTags(footprint_tags)

	# set general values
	kicad_mod.append(Text(type='reference', text='REF**', at=[0,-8], layer='F.SilkS'))
	kicad_mod.append(Text(type='value', text=footprint_name, at=[0,8], layer='F.Fab'))
	kicad_mod.append(Text(type='user', text='%R', at=[0,0], layer='F.Fab'))

	# create fab outline
	kicad_mod.append(RectLine(start=[-7.75,-6.4], end=[7.75,6.4], layer='F.Fab', width=0.1))

	# create silscreen
	kicad_mod.append(RectLine(start=[-7.75,-6.4], end=[7.75,6.4], layer='F.SilkS', width=0.12, offset=0.1))

	# create courtyard
	kicad_mod.append(RectLine(start=[-7.75,-6.4], end=[7.75,6.4], layer='F.CrtYd', width=0.05, offset=0.25))

	# create pads
	kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=[-2.5,-4], size=[2.5,2.5], drill=1.5, layers=['*.Cu', 'B.Mask']))
	kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=[2.5,-4.5], size=[2.5,2.5], drill=1.5, layers=['*.Cu', 'B.Mask']))

	# add model
	kicad_mod.append(Model(filename=location_3d ,at=[0,0,0] ,scale=[1,1,1] ,rotate=[0,0,0]))

	return kicad_mod

def generate_switch_footprint():
	kicad_mod = generate_switch(base_name, base_description, base_tags)
	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile("{}.kicad_mod".format(base_name))

def generate_isoenter_key_footprint(orientation):
	footprint_name = ""

	if orientation == 0:
		footprint_name = "{}_ISOEnter".format(base_name)
	elif orientation == 1:
		footprint_name = "{}_ISOEnter_Rotated90".format(base_name)
	elif orientation == 2:
		footprint_name = "{}_ISOEnter_Rotated180".format(base_name)
	elif orientation == 3:
		footprint_name = "{}_ISOEnter_Rotated270".format(base_name)

	footprint_description = base_description
	footprint_tags = base_tags + " ISOEnter"

	kicad_mod = generate_switch(footprint_name, footprint_description, footprint_tags)

	if orientation == 0: # normal orientation
		polygone_line = [[(unit_value*1.25)/2, unit_value],
					 	 [(unit_value*1.25)/2, -unit_value],
					 	 [-(unit_value*1.75)/2, -unit_value],
					 	 [-(unit_value*1.75)/2, 0],
					 	 [-(unit_value*1.25)/2, 0],
						 [-(unit_value*1.25)/2, unit_value],
						 [(unit_value*1.25)/2, unit_value]]
	elif orientation == 1: # rotated 90 deg
		polygone_line = [[unit_value, -(unit_value*1.25)/2],
					 	 [-unit_value, -(unit_value*1.25)/2],
					 	 [-unit_value, (unit_value*1.75)/2],
					 	 [0, (unit_value*1.75)/2],
					 	 [0, (unit_value*1.25)/2],
						 [unit_value, (unit_value*1.25)/2],
						 [unit_value, -(unit_value*1.25)/2]]
	elif orientation == 2: # rotated 180 deg
		polygone_line = [[-(unit_value*1.25)/2, -unit_value],
					 	 [-(unit_value*1.25)/2, unit_value],
					 	 [(unit_value*1.75)/2, unit_value],
					 	 [(unit_value*1.75)/2, 0],
					 	 [(unit_value*1.25)/2, 0],
						 [(unit_value*1.25)/2, -unit_value],
						 [-(unit_value*1.25)/2, -unit_value]]
	elif orientation == 3: # rotated 270 deg
		polygone_line = [[-unit_value, (unit_value*1.25)/2],
					 	 [unit_value, (unit_value*1.25)/2],
					 	 [unit_value, -(unit_value*1.75)/2],
					 	 [0, -(unit_value*1.75)/2],
					 	 [0, -(unit_value*1.25)/2],
						 [-unit_value, -(unit_value*1.25)/2],
						 [-unit_value, (unit_value*1.25)/2]]

	# Generate user layout guides
	kicad_mod.append(PolygoneLine(polygone=polygone_line, layer='Dwgs.User', width=0.1))

	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile("{}.kicad_mod".format(footprint_name))

def generate_standard_key_footprint(unit_size, rotated, offset):
	footprint_name = ""
	footprint_description = ""
	footprint_tags = ""

	if rotated:
		footprint_name = "{}_{:4.2f}u_Rotated".format(base_name, unit_size)
		footprint_description = base_description
		footprint_tags = base_tags + " {:4.2f}u".format(unit_size) + " Rotated"
	else:
		footprint_name = "{}_{:4.2f}u".format(base_name, unit_size)
		footprint_description = base_description
		footprint_tags = base_tags + " {:4.2f}u".format(unit_size)

	if offset != 0:
		footprint_name += "_Offset"
		footprint_tags += " Offset"

	kicad_mod = generate_switch(footprint_name, footprint_description, footprint_tags)

	# Generate user layout guides
	if rotated:
		kicad_mod.append(RectLine(start=[-unit_value / 2, (-(unit_size * unit_value) / 2) + offset], end=[unit_value / 2, ((unit_size * unit_value) / 2) + offset], layer='Dwgs.User', width=0.1))
	else:
		kicad_mod.append(RectLine(start=[(-(unit_size * unit_value) / 2) + offset, -unit_value / 2], end=[((unit_size * unit_value) / 2) + offset, unit_value / 2], layer='Dwgs.User', width=0.1))

	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile("{}.kicad_mod".format(footprint_name))


if __name__ == "__main__":

	generate_switch_footprint()

	generate_isoenter_key_footprint(0)

	for key in [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 4, 4.5, 5.5, 6, 6.25, 6.50, 7]:
		generate_standard_key_footprint(key, False, 0)