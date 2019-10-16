TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = Conv
# Conv.dbd will be created and installed
DBD += Conv.dbd

# Conv.dbd will be made up from these files:
Conv_DBD += base.dbd
Conv_DBD += calcSupport.dbd

# Include dbd files from all support applications:
Conv_LIBS += calc

# Conv_registerRecordDeviceDriver.cpp derives from Conv.dbd
Conv_SRCS += Conv_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
Conv_SRCS_DEFAULT += ConvMain.cpp
Conv_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#Conv_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
Conv_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

