from krita import *
import math

#TODO: JSON export

def export_spritesheet():
	print("NP Spritesheet")

	app = Krita.instance()
	activeDoc = app.activeDocument()

	frame_width = activeDoc.width()
	frame_height = activeDoc.height()

	frames = []
	for layer in activeDoc.topLevelNodes():
		if layer.animated():
			for frame in range(activeDoc.animationLength()):
				if layer.hasKeyframeAtTime(frame):
					frames.append(layer.pixelDataAtTime(0, 0, frame_width, frame_height, frame))
		else:
			frames.append(layer.projectionPixelData(0, 0, frame_width, frame_height))

	columns = int(math.sqrt(len(frames)))
	rows = int(math.ceil(len(frames)/columns))

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

	app.activeWindow().addView(exportDoc)
	exportDoc.refreshProjection()