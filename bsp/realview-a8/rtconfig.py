import os

# toolchains options
ARCH='arm'
CPU='realview-a8-vmm'
CROSS_TOOL='gcc'

if os.getenv('RTT_CC'):
	CROSS_TOOL = os.getenv('RTT_CC')

if  CROSS_TOOL == 'gcc':
	PLATFORM 	= 'gcc'
	EXEC_PATH       = ''
elif CROSS_TOOL == 'keil':
	PLATFORM 	= 'armcc'
	EXEC_PATH 	= 'C:/Keil'

if os.getenv('RTT_EXEC_PATH'):
	EXEC_PATH = os.getenv('RTT_EXEC_PATH')

BUILD = 'debug'
VMM = True

if PLATFORM == 'gcc':
    # toolchains
    PREFIX = 'arm-none-eabi-'
    CC = PREFIX + 'gcc'
    CXX = PREFIX + 'g++'
    AS = PREFIX + 'gcc'
    AR = PREFIX + 'ar'
    LINK = PREFIX + 'gcc'
    TARGET_EXT = 'elf'
    SIZE = PREFIX + 'size'
    OBJDUMP = PREFIX + 'objdump'
    OBJCPY = PREFIX + 'objcopy'

    DEVICE = ' -march=armv7-a -mtune=cortex-a8 -mfpu=vfpv3-d16 -ftree-vectorize -ffast-math -mfloat-abi=softfp'
    CFLAGS = DEVICE + ' -Wall'
    AFLAGS = ' -c' + DEVICE + ' -x assembler-with-cpp -D__ASSEMBLY__'
    if VMM:
        LINK_SCRIPT = 'realview_vmm.lds'
    else:
        LINK_SCRIPT = 'realview.lds'
    LFLAGS = DEVICE + ' -Wl,--gc-sections,-Map=realview.map,-cref,-u,system_vectors'+\
                      ' -T %s' % LINK_SCRIPT

    CPATH = ''
    LPATH = ''

    # generate debug info in all cases
    AFLAGS += ' -gdwarf-2'
    CFLAGS += ' -g -gdwarf-2'

    if BUILD == 'debug':
        CFLAGS += ' -O0'
    else:
        CFLAGS += ' -O2'

    POST_ACTION = OBJCPY + ' -O binary $TARGET rtthread.bin\n' +\
                  SIZE + ' $TARGET \n' +\
                  OBJDUMP + ' -S $TARGET > rtt.S\n'

elif PLATFORM == 'armcc':
    # toolchains
    CC = 'armcc'
    CXX = 'armcc'
    AS = 'armasm'
    AR = 'armar'
    LINK = 'armlink'
    TARGET_EXT = 'axf'

    DEVICE = ' --device DARMP'
    CFLAGS = DEVICE + ' --apcs=interwork'
    AFLAGS = DEVICE
    LFLAGS = DEVICE + ' --info sizes --info totals --info unused --info veneers --list rtthread-realview.map --scatter realview.sct'

    CFLAGS += ' -I' + EXEC_PATH + '/ARM/RV31/INC'
    LFLAGS += ' --libpath ' + EXEC_PATH + '/ARM/RV31/LIB'

    EXEC_PATH += '/arm/bin40/'

    if BUILD == 'debug':
        CFLAGS += ' -g -O0'
        AFLAGS += ' -g'
    else:
        CFLAGS += ' -O2'

    POST_ACTION = 'fromelf --bin $TARGET --output rtthread.bin \nfromelf -z $TARGET'

elif PLATFORM == 'iar':
    # toolchains
    CC = 'iccarm'
    AS = 'iasmarm'
    AR = 'iarchive'
    LINK = 'ilinkarm'
    TARGET_EXT = 'out'

    DEVICE = ' --cpu DARMP'

    CFLAGS = ''
    AFLAGS = ''
    LFLAGS = ' --config realview.icf'

    EXEC_PATH += '/arm/bin/'
    RT_USING_MINILIBC = False
    POST_ACTION = ''
