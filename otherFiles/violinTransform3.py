# Jesse's notes:
    # this script oscillates the violin 
    # by putting a transform filter on the violin and then 
    # changing the transform position in a loop (at the end)

# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
import math
import time
import msvcrt

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'STL Reader'
myViolinstl = STLReader(registrationName='myViolin.stl', FileNames=['C:\\Users\\jesse\\Downloads\\myViolin.stl'])

# set active source
SetActiveSource(myViolinstl)

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
myViolinstlDisplay.ScaleFactor = 56.60140075683594
myViolinstlDisplay.SelectScaleArray = 'STLSolidLabeling'
myViolinstlDisplay.GlyphType = 'Arrow'
myViolinstlDisplay.GlyphTableIndexArray = 'STLSolidLabeling'
myViolinstlDisplay.GaussianRadius = 2.830070037841797
myViolinstlDisplay.SetScaleArray = [None, '']
myViolinstlDisplay.ScaleTransferFunction = 'PiecewiseFunction'
myViolinstlDisplay.OpacityArray = [None, '']
myViolinstlDisplay.OpacityTransferFunction = 'PiecewiseFunction'
myViolinstlDisplay.DataAxesGrid = 'GridAxesRepresentation'
myViolinstlDisplay.PolarAxes = 'PolarAxesRepresentation'

# show color bar/color legend
myViolinstlDisplay.SetScalarBarVisibility(renderView1, True)

# reset view to fit data
renderView1.ResetCamera()

# get opacity transfer function/opacity map for 'STLSolidLabeling'
sTLSolidLabelingPWF = GetOpacityTransferFunction('STLSolidLabeling')

# show data in view
myViolinstlDisplay = Show(myViolinstl, renderView1, 'GeometryRepresentation')

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show color bar/color legend
myViolinstlDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Transform'
transform1 = Transform(registrationName='Transform1', Input=myViolinstl)
transform1.Transform = 'Transform'

# Properties modified on transform1.Transform
transform1.Transform.Translate = [0.0, 11.0, 0.0]

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
transform1Display.ScaleFactor = 56.60140075683594
transform1Display.SelectScaleArray = 'None'
transform1Display.GlyphType = 'Arrow'
transform1Display.GlyphTableIndexArray = 'None'
transform1Display.GaussianRadius = 2.830070037841797
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

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

# get layout
layout1 = GetLayout()

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1944, 1002)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
# renderView1.CameraPosition = [-47.399749755859375, 109.30000305175781, 1164.6169570699203]
# renderView1.CameraFocalPoint = [-47.399749755859375, 109.30000305175781, -6.726900100708008]
# renderView1.CameraParallelScale = 303.16609859960545

totalSeconds = 5
sleepSeconds = .01
freq = .3
x = 0
for x in range(int(totalSeconds/sleepSeconds/3)):

    # while True:
    # to enter changes through command line to oscillating freq during animation (doesn't work)

    # done = False
    # string = ""
    # if msvcrt.kbhit():
    #     currChar = msvcrt.getch().decode("utf-8")
    #     print(currChar)
    #     if currChar == '\r' or currChar == '\n':
    #         print(string)
    #         done = True
    #         # freq = float(string)
    #         string = ""
    #     string += currChar

    y = math.sin(x * freq) * 10
    x+=1
    # Properties modified on transform2.Transform
    transform1.Transform.Translate = [0.0, y, 0.0]
    # show data in view
    transform1Display = Show(transform1, renderView1, 'GeometryRepresentation')
    # show color bar/color legend
    transform1Display.SetScalarBarVisibility(renderView1, True)
    renderView1.Update()

    Render()
    # RenderAllViews()
    # interact()
    time.sleep(sleepSeconds)



#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# Interact()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
