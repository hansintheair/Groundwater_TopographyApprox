###############################
###### Jacobi Iteration #######
## Simple Groundwater Model  ##
###############################
## Hannes Ziegler            ##
## v 2.05                    ##
## 10/28/2015                ##
###############################

### Import Modules and Data, set Environments ###
import arcpy, numpy, sys
inrast = arcpy.Raster(arcpy.GetParameterAsText(0)) ## Input raster of initial guesses
inboun = arcpy.Raster(arcpy.GetParameterAsText(1)) ## input raster of internal boundary conditions
outrasterloc = arcpy.GetParameterAsText(2) ## Output raster filepath
convtolerance = float(arcpy.GetParameterAsText(3)) ## Convergence tolerance for iteration exit condition
maxiterations = int(arcpy.GetParameterAsText(4)) ## Maximum iterations for iteration exit condition
rastarray = arcpy.RasterToNumPyArray(inrast) ## Convert inrast to numpy array for operations
bounarray = arcpy.RasterToNumPyArray(inboun) ## Convert inboun to numpy array for operations
arcpy.env.overwriteOutput = True ## Allow overwriting of files
arcpy.SetProgressor("step", "Executing Jacobi Iteration...", 0, maxiterations, 1) ## Initial Progress Bar Object

### Determine Raster Shape ###
rowrange = rastarray.shape[0]
colrange = rastarray.shape[1]
#print "Raster Extent ( Rows: {}, Cols: {} )".format(rowrange, colrange) ##DEBUG##
#print "Model Max Bounds ( Rows: {0}, Cols: {1} )".format(rowrange-2, colrange-2) ##DEBUG##

### Copy Water Feature Heads Into Iteration Raster ###
i = 0
while i < rowrange:
    j = 0
    while j < colrange:
        if bounarray[i][j] != -340282346638528859811704183484516925440.0000000000:
            rastarray[i][j] = bounarray[i][j]
        j += 1
    i += 1
del i, j
### Jacobi Iteration Procedure ###
"""
Access data in the array with the five-point star operator using while loop structure
Indices i,j are accessed. i is for rows, j is for columns. Starting position of center (wt)
of five-point star operator is at i+1, j+1
"""
conv = convtolerance+1
iterations = 0
while conv > convtolerance and iterations < maxiterations: ## Exit condition
    conv = 0
    temparray = numpy.array(rastarray)
    iterations += 1
    i = 0
    while i < (rowrange-2): ## Ensures center (wt) does not reach last row
        j = 0
        while j < (colrange-2): ## Ensures center (wt) does not reach last column
            ## If current cell is not a boundary condition, calculate the cell (-34X10^-38 is the NULL value)
            if bounarray[i+1][j+1] == -340282346638528859811704183484516925440.0000000000:
                #print "Iteration: {}, Row: {}, Col: {}, Val: {:07.3f}".format(iterations, i, j, rastarray[i+1][j+1]) ##DEBUG##
                """ Five-Point Moving Average moves accross the raster as shown in the diagram
                       a
                    d  wt b
                       c
                """
                a = rastarray[i][j+1]
                b = rastarray[i+1][j+2]
                c = rastarray[i+2][j+1]
                d = rastarray[i+1][j]
                wt = (a+b+c+d)/4
                ##Calculate convergence value, a list holds all convergence values for current iteration level
                convcur = abs(wt-rastarray[i+1][j+1])
                if convcur > conv:
                    conv = convcur
                temparray[i+1][j+1] = wt ## write new values to temporary array
                #print "\t{:07.3f}\n{:07.3f}\t\t{:07.3f}\n\t{:07.3f}".format(a, d, b, c) ##DEBUG##
            j += 1
        i += 1
    del rastarray #removes from memory
    rastarray = numpy.array(temparray) #copy rastarray for next iteration
    del temparray
    """ Peripheral No-Flow boundary condition updated (mirror)
        The outside boundaries take on the same values as the
        adjacent cells.
    """
    rastarray[0][1:-1] = rastarray[1][1:-1]
    rastarray[-1][1:-1] = rastarray[-2][1:-1]
    rastarray[1:-1:,0] = rastarray[1:-1:,1]
    rastarray[1:-1:,-1] = rastarray[1:-1:,-2]
    #arcpy.AddMessage("maxconv: {}".format(conv))
    arcpy.SetProgressorPosition() ## Update Progress Bar
    arcpy.SetProgressorLabel("Iteration step {} of {}; Convergence: {}".format(iterations, maxiterations, conv)) ## Update Progress Bar Message
    #arcpy.AddMessage("Iterations: {}, Convergence: {}".format(iterations, conv)) ##DEBUG##

### Check whether exit conditions supply accurate surface
if iterations == maxiterations:
    arcpy.AddWarning("Iteration thershold of {} was met, data has not converged. Increase your threshold.".format(maxiterations))
    arcpy.AddWarning("Convergence value is at {}.".format(conv))
else:
    arcpy.AddMessage("Convergence tolerance of {} has been met.n\Iterations: {}\nConvergence: {}".format(convtolerance, iterations, conv))

### Export Data ###
## Extract projection information from inrast (the raster of initial guesses)
desc = arcpy.Describe(inrast)
spatialref = desc.spatialReference ## extract spatial reference from inrast
## Create point object of bottom left coordinates, move over and up by one cell to account for excluded peripheral cells
extent = desc.Extent
origin = arcpy.Point(extent.XMin + desc.meanCellWidth, extent.YMin + desc.meanCellHeight)
## Create out raster using extracted spatial information
## *Outermost rows and columns of cells "peripheral cells" are excluded from being copied. These are the no-flow boundaries and are trash.
outraster = arcpy.NumPyArrayToRaster(rastarray[1:-1:,1:-1], origin, desc.meanCellWidth, desc.meanCellHeight)
outraster.save(outrasterloc) ## Save the outraster
## Define projection of newly created raster
arcpy.management.DefineProjection(outraster, spatialref)

