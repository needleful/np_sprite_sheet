from krita import *
import json
import math
import os.path

def generate_file(app):
	activeDoc = app.activeDocument()

	frame_width = activeDoc.width()
	frame_height = activeDoc.height()

	properties = {
		"framerate":activeDoc.framesPerSecond(),
	}
	anims = {}

	frames = []
	for layer in activeDoc.topLevelNodes():
		if layer.animated():
			anims[layer.name()] = {
				"offset":len(frames),
				"key_times":[]
			}
			last_frame = 0
			total_frames = 0
			for frame in range(activeDoc.animationLength()):
				if layer.hasKeyframeAtTime(frame):
					frames.append(layer.pixelDataAtTime(0, 0, frame_width, frame_height, frame))
					total_frames += 1
					if total_frames > 1:
						anims[layer.name()]["key_times"].append(frame - last_frame)
					last_frame = frame
			# By default, the last keyframe is held for 1 frame.
			# Use +[number] in the name of the layer to add a final keyframe time
			anims[layer.name()]["key_times"].append(1)

		else:
			anims[layer.name()] = {
				"offset":len(frames),
				"key_times":[1]
			}
			frames.append(layer.projectionPixelData(0, 0, frame_width, frame_height))

	for key in list(anims):
		values = key.split('+')
		if len(values) == 2:
			anim = values[0]
			anims[anim] = anims[key]
			del anims[key]
			added = int(values[1])
			key_times = anims[anim]["key_times"]
			key_times[len(key_times) - 1] += added

	properties['anims'] = anims
	
	columns = int(math.sqrt(len(frames)))
	rows = int(math.ceil(len(frames)/columns))

	properties['size'] = [rows, columns]

	exportDoc = app.createDocument(
		frame_width*columns, frame_height*rows,
		activeDoc.name() + ".sheet",
		activeDoc.colorModel(), activeDoc.colorDepth(), activeDoc.colorProfile(),
		300)
	 

	exportLayer = exportDoc.createNode("sprites", "paintlayer")
	exportDoc.rootNode().addChildNode(exportLayer, None)

	for col in range(columns):
		for r in range(rows):
			print("(%d, %d)" % (r, col))
			frame = col + r*columns
			if frame >= len(frames):
				print("(%d, %d) exceeds frames: %d" % (r, col, len(frames)))
				break
			frameData = frames[frame]
			x = frame_width*col
			y = frame_height*r

			res = exportLayer.setPixelData(frameData, x, y, frame_width, frame_height)
			if not res:
				print("Failed to paste at (%d, %d)" % (x, y))

	return exportDoc, properties


def export_spritesheet(output_path):
	app = Krita.instance()
	exportDoc, properties = generate_file(app)

	png = InfoObject()
	png.setProperty("alpha", True)
	png.setProperty("compression",9)
	png.setProperty("indexed", False)
	exportDoc.refreshProjection()
	exportDoc.exportImage(os.path.join(output_path), png)

	if properties != None:
		json_path = os.path.splitext(output_path)[0] + '.ss.json'
		with open(json_path, "w", encoding="utf-8") as json_out:
			json.dump(properties, json_out, sort_keys=True)



def preview_spritesheet():
	app = Krita.instance()
	exportDoc, properties = generate_file(app)

	app.activeWindow().addView(exportDoc)
	exportDoc.refreshProjection()