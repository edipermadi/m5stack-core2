# m5stack-core2
M5 Stack Core2 Micropython BSP

board = GENERIC_SPIRAM

comment out `GENERIC_SPIRAM` from sdkconfig.base add `CONFIG_ESPTOOLPY_FLASHSIZE_16MB=y`
replace the content of `partitions.csv` with `partitions-16MiB.csv`
