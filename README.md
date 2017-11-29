###############################################################################################################################
#### First time Installation ####
#Copy small_install to desired directory

#From the small_install directory:
    small_install.py small_install  # This will do the first small_install installation

#   if the .paths.json file is wrong, edit the file and re-run (see sample.paths.json)

###############################################################################################################################
#### Stand-alone script ####
#If you have a stand-alone script to small_install, go to the appropriate directory (e.g. "stand-alone-script") and type
    small_install stand-alone-script

# This will generate a bash version executed as 'stand-alone-script' (unless you use -i for a different name) and copy it to the small_install bin

###############################################################################################################################
#### python import ####
# If you want to have code accessible to ipython, go to the appropriate directory (e.g. "ipython-code") and type
    small_install ipython-code.py

#This will copy it to the small_install python bin (e.g. miniconda2/bin).

#If it needs to import from the "home" path, add the name to ~/.paths.json and at the top of the module (e.g. "ipython-code") include

    import code_path
    code_path.set("whatever-name-you-gave-it-in-.paths.json; e.g. ipython-code")
