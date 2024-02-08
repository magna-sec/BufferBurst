from collections import namedtuple


# Stack based Overflow
dbg_cmds_bof = namedtuple("debugger_commands", ["name", "breakpoint", "bad_bytes", "jmpeax"])
windbg_bof = dbg_cmds_bof("WinDbg", "bp", "db esp - 10 L110", 
                          "lm \n \
                           Go Through Each Module with the following format:\n \
                           s -b <NUM1> <NUM2> 0xFF 0xE4 \n \
                           e.g: \n \
                           62500000 62508000   essfunc    (deferred)\n \
                           s -b 62500000 62508000 0xFF 0xE4"
                         )
