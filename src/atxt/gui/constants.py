from atxt.__main__ import __version__
from atxt.check import check_os

windows = check_os() == 'Windows'


BTN_BROWSER = "Browser"
BTN_SAVE_LOG = "Save Log"
LABEL_BOX_ACTIONS = "Actions"
LABEL_BOX_DIRECTORY = "From:" + \
    (' [directory]' if windows else ' [directory or file]')
LABEL_BOX_FORMATS = "Extensions"
LABEL_BOX_LAYOUT1 = "Settings"
LABEL_BOX_LAYOUT2 = ""
LABEL_BOX_SAVE_IN = "To:[directory]"
LABEL_DEPTH = "Depth:"
LABEL_OVERWRITE = "Overwrite Files"
LABEL_USE_TEMP = "Use Temp Files"
MSG_SAVE_IN = "Save In"
MSG_TEXT_BROWSER = "First Step: Please set a source for data"
NAME_FOLDER_TXT = "TXT"
SELECT_DIRECTORY = "select a folder to perform the search"
TITLE_WINDOW = "aTXT v%s" % __version__
TOOLTIP_BOX_SAVEIN = "select a folder destination [default: 'TXT' folder for each depth level)"
TOOLTIP_DEPTH = "level for a depth search trasversing the directory"
TOOLTIP_OVERWRITE = "Dont process file if txt version exists"
TOOLTIP_SAVEIN = "aTXT creates new folder for each one that contains files of the search."
TOOLTIP_SCAN = "Warning: scan a folder can take long time if is a big one"
TOOLTIP_USE_TEMP = "[slow process] To enforce a safe conversion, with temporary file version for each file."
WARNING_LONG_PROCESS = "This process could be take few minutes, do you want to continue?"
NONE_EXT_CHOOSED = "Please choose at least one extension of file to search"
TOOLTIP_OCR_NECESSARY = 'Check the document. If is necessary to perform a OCR recognition process. It will run it. Even if OCR option is turn off'
