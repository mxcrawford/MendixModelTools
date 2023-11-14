import subprocess, random, os, shutil, urllib.request, os.path, tarfile, argparse, platform, glob

## Setup all input arguments 
parser = argparse.ArgumentParser(description='Automatically export the latest revision and build an .mda  using mxbuild.' ) 
parser.add_argument('-java', action="store", dest="java", help='the Java home directory: \r\n   (Usually \'/usr/lib/jvm/java-8-oracle\' or \'C:\Program Files\Java\jdk1.8.0_144\')')
parser.add_argument('-revision','-r', action="store", dest="svnRevision", type=int, default=-1, help='The revision you want to build, defaults to the latest revision ')
parser.add_argument('-mprName','-m', action="store", dest="mpr", help='Optionally specify the file name of the mpr file, if you have multiple mpr files this argument is mandarory')
parser.add_argument('-outputFile','-o', action="store", dest="output", help='The path, including the filename where the .mda should be exported')
parser.add_argument('-mxversion','-v', action="store", dest="mxVersion", help='Mendix Version e.g. 9.8.1.32679')
parser.add_argument('-debug', '-d', action="store", dest="debug", default=False, help='Enable debug logging')
parser.add_argument('-folder', '-f', action="store", dest="folder", default=False, help='Folder containing project')

args = parser.parse_args()

_exportDirectory = os.getcwd() + "/exports/"
_mxLibraryDirectory = os.getcwd() + "/mxLib/"
_buildOutputDirectory =  os.getcwd() + "/builds/"

#exportFolder = "{}{}/".format( _exportDirectory, random.randint(100000000,1000000000) )
exportFolder = args.folder
while( exportFolder == None or exportFolder.isspace() or not exportFolder.strip()):
	exportFolder = input("Please specify the Project directory")

####
# 		Validate all input arguments, and make sure the user either used an argument or enters it through the CL
####

javaLocation = args.java
#If Java isn't part of the args, ask the user for the Java home directory
while( javaLocation == None or javaLocation.isspace() or not javaLocation.strip()):
	javaLocation = input("Please specify the Java home directory: \r\n   (Usually '/usr/lib/jvm/java-8-oracle' or 'C:\Program Files\Java\jdk1.8.0_144') \n > ")

svnRev = args.svnRevision
# If Revision isn't part of the arguments, ask the user to enter 
while( svnRev == None or isinstance(svnRev,str)):
	svnRev = input("Please provide your build revision:\n > ")

mprFileName = args.mpr
outputFile = args.output
mxVersion = args.mxVersion
while( mxVersion == None or mxVersion.isspace() or not mxVersion.strip()):
	mxVersion = input("Please specify Mendix Version, usually 9.8.1.32679")

debugEnabled = args.debug

def debug( msg ):
    if (debugEnabled):
	    print( "  *  " +  msg )

## Review te MxVersion number, and  download the MxBuild files if they don't exist yet
def getMxBuildFiles( mxVersion , _mxLibraryDirectory):
	## Check if we need the tar.gz build package.   
	## If we don't have that on disk yet, download the tar file and extract it
	targetMxBuild = _mxLibraryDirectory + mxVersion
	if not os.path.exists( targetMxBuild ): 
		targetMxBuildZip =  "win-mxbuild-{}.tar.gz".format(mxVersion)
		
		if not os.path.exists( _mxLibraryDirectory + targetMxBuildZip ): 
			debug("Start downloading: " + targetMxBuildZip)
			urllib.request.urlretrieve("https://cdn.mendix.com/runtime/" + targetMxBuildZip, _mxLibraryDirectory + targetMxBuildZip )

			debug("Download finished, extracting ...")
		else:
			debug("MxBuild .tar.gz file found, extracting ..." + targetMxBuild)
		
		tar = tarfile.open( _mxLibraryDirectory + targetMxBuildZip )
		tar.extractall( targetMxBuild )
		tar.close()
		os.unlink( _mxLibraryDirectory + targetMxBuildZip )
		debug("MxBuild extracted to " + targetMxBuild )
		
	# We already have the MxBuild files, so nothing to do here
	else:
		debug("Mx Build : {} already downloaded".format( targetMxBuild ) )

	return targetMxBuild
### End getMxBuildFiles()

## Build the MxBuild comand line operation and run the build script
def buildMendixDeploymentArchive(  mxBuildFolder, javaLocation, mprFile, outputFile, version ):
	javaExeLocation = javaLocation
	if not javaExeLocation.endswith("\\") and not javaExeLocation.endswith("/") :  	javaLocation += "/"
	
	# Windows and linux require a different Java.exe reference
	if platform.system() == "Windows":		javaExeLocation = javaLocation + "bin/java.exe"
	else : 		javaExeLocation = javaLocation + "bin/java"
	
	# If our java path ends with a \ make sure we escape it
	if javaLocation.endswith("\\") :  	javaLocation += "\\"
	
	## Build the OutputFile location if this wasn't specified through the arguments
	# Default to builds/[mprName][-version].mda
	if outputFile is None: 
		idx = mprFile.rfind("/")
		idx2 = mprFile.rfind("\\")
		idx = max( idx, idx2 )
		
		if( not version is None ):		
			outputFile = _buildOutputDirectory + "{}-{}.mda".format( mprFile[idx:len(mprFile)-4], version )
			version_tag = " --model-version=\"{}\" ".format( version )
		else:
			outputFile = _buildOutputDirectory + "{}.mda".format( mprFile[idx:len(mprFile)-4] )
			version_tag = ""
	
	elif ( not "/" in outputFile and not "\\" in outputFile ):
		outputFile = _buildOutputDirectory + outputFile
		version_tag = ""
	
	buildCL = "{}/modeler/mxbuild.exe \"{}\" --java-home=\"{}\" --java-exe-path=\"{}\" {} --output=\"{}\" ".format( mxBuildFolder, mprFile, javaLocation, javaExeLocation, version_tag, outputFile )
	debug( "Running script : " + buildCL )
	
	p = subprocess.Popen( buildCL,  shell=True)
	(output, err) = p.communicate()

### End runMxBuild()

##
##	Main execution 
##

def main():

    mxBuildFolder = getMxBuildFiles( mxVersion, _mxLibraryDirectory )
    print( "* Located MxBuild files, start building using: {} ", mxBuildFolder)


    ## Attempt to locate the mpr file
    mprFiles = glob.glob(exportFolder + "/*.mpr")
    print( exportFolder )
    if len(mprFiles) == 1:
        print( "* Starting build process" )
        buildMendixDeploymentArchive( mxBuildFolder, javaLocation, mprFiles[0], outputFile, mxVersion )
        #tagRevision( svnRepo, svnRev, svnUser, svnPass, version )
        
    ## If we've found more than 1 mpr file, lookup the target file either in the arguments or ask the user for input
    elif len(mprFiles) > 1:
        while( mprFileName is None or mprFileName.isspace() or not mprFileName.strip() or not mprFileName.endswith(".mpr") or ( "/" in mprFileName) or ("\\" in mprFileName) ):
            mprFileName = input("The following .mpr files are found, which one would you like to use in the build?\n" + "\n".join(mprFiles) +"\nOnly enter the mpr name without path\n > " )
        
        print( "* Starting build process" )
        buildMendixDeploymentArchive( mxBuildFolder, javaLocation, exportFolder + "/" + mprFileName, outputFile, mxVersion )
        #tagRevision( svnRepo, svnRev, svnUser, svnPass, version )
        
    elif len(mprFiles) < 1:
        print( "No mpr files were found in the exported svn folder, aborting build. " + exportFolder)
        
    try: 
        print( "* Process Completed, start removing svn folder: ", exportFolder)
        #shutil.rmtree( exportFolder )
        print( "Process successfully completed ")
        
    except e: 
        print( "Unable to remove folder: {} because of error: {}".format( exportFolder, e ) )
        

if __name__ == "__main__":
    main()
