# Jesse's notes:
	 # uses the built in animation feature of paraview.
	 # have to manually add keyframes
# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'STL Reader'
myViolinstl = STLReader(registrationName='myViolin.stl', FileNames=['C:\\Users\\jesse\\Downloads\\myViolin.stl'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
myViolinstlDisplay = Show(myViolinstl, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'STLSolidLabeling'
sTLSolidLabelingLUT = GetColorTransferFunction('STLSolidLabeling')

# trace defaults for the display properties.
myViolinstlDisplay.Representation = 'Surface'
myViolinstlDisplay.ColorArrayName = ['CELLS', 'STLSolidLabeling']
myViolinstlDisplay.LookupTable = sTLSolidLabelingLUT
myViolinstlDisplay.SelectTCoordArray = 'None'
myViolinstlDisplay.SelectNormalArray = 'None'
myViolinstlDisplay.SelectTangentArray = 'None'
myViolinstlDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
myViolinstlDisplay.SelectOrientationVectors = 'None'
myViolinstlDisplay.ScaleFactor = 60.863598632812504
myViolinstlDisplay.SelectScaleArray = 'STLSolidLabeling'
myViolinstlDisplay.GlyphType = 'Arrow'
myViolinstlDisplay.GlyphTableIndexArray = 'STLSolidLabeling'
myViolinstlDisplay.GaussianRadius = 3.043179931640625
myViolinstlDisplay.SetScaleArray = [None, '']
myViolinstlDisplay.ScaleTransferFunction = 'PiecewiseFunction'
myViolinstlDisplay.OpacityArray = [None, '']
myViolinstlDisplay.OpacityTransferFunction = 'PiecewiseFunction'
myViolinstlDisplay.DataAxesGrid = 'GridAxesRepresentation'
myViolinstlDisplay.PolarAxes = 'PolarAxesRepresentation'

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show color bar/color legend
myViolinstlDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get opacity transfer function/opacity map for 'STLSolidLabeling'
sTLSolidLabelingPWF = GetOpacityTransferFunction('STLSolidLabeling')

# get animation scene
animationScene1 = GetAnimationScene()

# Properties modified on animationScene1
animationScene1.EndTime = 10.0
animationScene1.NumberOfFrames = 300

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# create a new 'Transform'
transform1 = Transform(registrationName='Transform1', Input=myViolinstl)
transform1.Transform = 'Transform'

# show data in view
transform1Display = Show(transform1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
transform1Display.Representation = 'Surface'
transform1Display.ColorArrayName = ['CELLS', 'STLSolidLabeling']
transform1Display.LookupTable = sTLSolidLabelingLUT
transform1Display.SelectTCoordArray = 'None'
transform1Display.SelectNormalArray = 'None'
transform1Display.SelectTangentArray = 'None'
transform1Display.OSPRayScaleFunction = 'PiecewiseFunction'
transform1Display.SelectOrientationVectors = 'None'
transform1Display.ScaleFactor = 60.863598632812504
transform1Display.SelectScaleArray = 'None'
transform1Display.GlyphType = 'Arrow'
transform1Display.GlyphTableIndexArray = 'None'
transform1Display.GaussianRadius = 3.043179931640625
transform1Display.SetScaleArray = [None, '']
transform1Display.ScaleTransferFunction = 'PiecewiseFunction'
transform1Display.OpacityArray = [None, '']
transform1Display.OpacityTransferFunction = 'PiecewiseFunction'
transform1Display.DataAxesGrid = 'GridAxesRepresentation'
transform1Display.PolarAxes = 'PolarAxesRepresentation'

# hide data in view
Hide(myViolinstl, renderView1)

# show color bar/color legend
transform1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get animation track
transform1TransformPositionTrack = GetAnimationTrack('Position', index=1, proxy=transform1.Transform)

keyf0 = CompositeKeyFrame()
keyf0.Interpolation = 'Sinusoid'
# At time = 0, value = 0

keyf0.KeyTime = 0
keyf0.KeyValues= [30]

keyf1 = CompositeKeyFrame()
# At time = 1.0, value = 200
keyf1.KeyTime =.5
keyf1.KeyValues = [0]

# Add keyframes.
transform1TransformPositionTrack.KeyFrames = [keyf0, keyf1]

print("starting	")
animationScene1.Play()
print("finished")

Render()