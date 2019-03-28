I created a script implementing the Jacobi Iterative Method of the Finite Difference Expression of the Laplace Equation 
during my Master's program for the Florida Atlantic University class LiDAR Remote Sensing Applications (GIS6032C) on 12/4/2015. 
This is the original script I created without significant updates (troubleshooted to make sure it works properly, only tested on ArcMap).

Included:
Groundwater_ApproxOfTopography_
TestData.rar					> Archive (.rar) containing sample test data and ArcMap project, as well as toolbox containing the python tool.
	\dem_l					> Sample DEM raster for testing.
	\wtrfeat_l				> Sample groundwater boundary conditions raster for testing
	\wtrtable_l				> Output water table elevation model (WTEM) from running above two datasets through geoprocessing tool.
	\Groundwater.tbx			> Toolbox containing the ApproxGroundwaterFromTopo, which references Groundwater_ApproxOfTopography.py
					  	  Tool description available when running tool from ArcMap. 
	\Groundwater_ApproxOfTopography
	 _TestDoc.mxd				> Map document used for testing.
Groundwater_ApproxOfTopography.py		> Python script.
GroundwaterAsASubduedReplicaOf
Topography_GIS6032C_FinalProject_
HannesZiegler.pdf				> Project report PDF detailing the research that went into creating the tool and how the tool was used.

The default values convergence tolerance and iterations should suffice to yield a decent result on the sample data I provided.
