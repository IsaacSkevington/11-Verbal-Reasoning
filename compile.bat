

@echo on
@echo ###########################################################################################################
@echo ##################### This will build the verbal question setter into an executable #######################
@echo #### Python, pyinstaller and the requirements specified in requirements.txt are required for the build ####
@echo ###########################################################################################################

pyinstaller verbalquestionsetter.spec

@echo #####################################################################################################
@echo ######################################  BUILD COMPLETE  #############################################
@echo #####################################################################################################

pause
