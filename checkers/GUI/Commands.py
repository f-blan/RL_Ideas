from enum import Enum

#list of commands sent between CPU and GUI

#CPU Receives
class Commands(Enum):
    QUIT_GAME =             0x00000002
    START_PVP_MODE =        0x00000003
    START_CVC_MODE =        0x00000004
    START_PVC_MODE =        0x00000005

    EXIT_APP =              0x00000006
    PROCESS_ACQUIRED_MOVE =          0x00000030


    #GUI Receives
    MENU_SCREEN =           0x00000007
    GAME_SCREEN =           0x00000008
    SELECTION_SCREEN =      0x00000010
    GUI_TERMINATE =         0x00000020

    ACQUIRE_HUMAN_INPUT =   0x00000000
    PROCESS_CPU_INPUT =     0x00000001
