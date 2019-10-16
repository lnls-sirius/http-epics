#!../../bin/linux-x86_64/Conv

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/Conv.dbd"
Conv_registerRecordDeviceDriver pdbbase

dbLoadRecords("db/DCCT.db")
dbLoadRecords("db/PS.db")

cd "${TOP}/iocBoot/${IOC}"
iocInit
