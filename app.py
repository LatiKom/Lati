from tkinter import *
import tkinter as tk
from custom.widgets.text import *
from custom.widgets.linenumbers import *
from settings import *
from custom.widgets.terminal import *
from custom.widgets.minimap import *
from utils.utils import *
from custom.widgets.toolbar import *
from syntax.highlight import *
from custom.widgets.treeview import *
from custom.widgets.recentfiles import *
from custom.widgets.headers import *
from utils.package import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.editorTextarea = TextWidget(self, undo=True, autocomplete=self.getmatches)
        if theme['editor']['config']['custom-styles']:
            self.editorTextarea.style()
            
        self.editorMinimap = MinimapWidget(self.editorTextarea)
        if theme['editor']['config']['custom-styles']:
            self.editorMinimap.style()
            
        self.editorRecentFiles = RecentFileWidget(self)
        if theme['editor']['config']['custom-styles']:
            self.editorRecentFiles.style()
            
        self.editorTreeview = TreeManeger(self)
        if theme['editor']['config']['custom-styles']:
            self.editorTreeview.style()

        self.editorToolsFrame = ToolBar(self, background=theme['editor']['widgets']["background"])
        if theme['editor']['config']['custom-styles']:
            self.editorToolsFrame.style()
        self.editorToolsFrame._updateToolBar(self.editorTextarea)
        
        self.editorLinenumbers = TextLineNumbersWidget(self, width=theme['editor']['widgets-config']['linebar']['width'])
        if theme['editor']['config']['custom-styles']:
            self.editorLinenumbers.style()
        self.editorLinenumbers.attach(self.editorTextarea)

        
        self.editorTerminal = TerminalWidget(self)
        if theme['editor']['config']['custom-styles']:
            self.editorTerminal.style()

        # * Adding widgets to the screen
        if prefs['editor']['toolbar']:
            self.editorToolsFrame.pack(side=prefs['editor']['toolbar-widget']['side'], fill=prefs['editor']['toolbar-widget']['fill'], expand=prefs['editor']['toolbar-widget']['expand'])
        if prefs['editor']['terminal']:
            self.editorTerminal.pack(side=prefs['editor']['terminal-widget']['side'], fill=prefs['editor']['terminal-widget']['fill'], expand=prefs['editor']['terminal-widget']['expand'])
        if prefs['editor']['recentfile']:
            self.editorRecentFiles.pack(side=prefs['editor']['recentfile-widget']['side'], fill=prefs['editor']['recentfile-widget']['fill'], expand=prefs['editor']['recentfile-widget']['expand'])
        if prefs['editor']['treeview']:
            self.editorTreeview.pack(side=prefs['editor']['treeview-widget']['side'], fill=prefs['editor']['treeview-widget']['fill'], expand=prefs['editor']['treeview-widget']['expand'])
        if prefs['editor']['linebar']:
            self.editorLinenumbers.pack(side=prefs['editor']['linebar-widget']['side'], fill=prefs['editor']['linebar-widget']['fill'], expand=prefs['editor']['linebar-widget']['expand'])
        if prefs['editor']['textarea']:
            self.editorTextarea.pack(side=prefs['editor']['textarea-widget']['side'], fill=prefs['editor']['textarea-widget']['fill'], expand=prefs['editor']['textarea-widget']['expand'])
        if prefs['editor']['minimap']:
            self.editorMinimap.pack(side=prefs['editor']['minimap-widget']['side'], fill=prefs['editor']['minimap-widget']['fill'], expand=prefs['editor']['minimap-widget']['expand'])
        
        # * File Until Binds widgets
        self.fu = FilesUtil(self, self.editorTextarea, self.editorTerminal, self.editorTreeview)
        self.fu._start()
        self.drawMenuBar()

        # * Highlight syntax system
        SyntaxHighlightUtil(self.editorTextarea).highlight()
        
        # * Binds widgets
        self.editorTextarea.bind("<<Change>>", self._OnChanageEditorArea)
        self.editorTextarea.bind("<Configure>", self._OnChanageEditorArea)
        self.editorTreeview.bind("<<TreeviewSelect>>", lambda str: self.editorTreeview._onClickedNode(self.fu.openFilePath))
        self.editorTreeview.bind('<Double-1>', lambda str: self.editorTreeview._addNewRecent(self.editorRecentFiles.addNewRecent))
        self.editorRecentFiles.bind("<<TreeviewSelect>>", lambda str: self.editorRecentFiles._onClickedNode(self.fu.openFilePath))
        
        self.drawMenuBar()
        self.pkg = Packages(self.packgaes, self.fu)
        self.pkg.insertMenus()
        
    def _OnChanageEditorArea(self, event):
        self.editorLinenumbers.redraw()
        
    def getmatches(self, word):
        words = js['MATCHES']
        matches = [x for x in words if x.startswith(word)]
        return matches
    
    def drawMenuBar(self):
        self.fu._start()
        self.menuApplication = Menu(self)

        self.fileDropdown = Menu(self.menuApplication, tearoff=False)
        self.fileDropdown.add_command(
            label=lang["dropdown"]["new"],
            command=lambda: self.fu.newFile(),
            accelerator=keys["key.new-file"][0],
        )
        self.bind(keys["key.new-file"][1], lambda string: self.fu.newFile())
        self.fileDropdown.add_command(
            label=lang["dropdown"]["new-saved"],
            command=lambda: self.fu.newSavedFile(),
            accelerator=keys["key.new-saved-file"][0],
        )
        self.bind(
            keys["key.new-saved-file"][1],
            lambda string: self.fu.newSavedFile)
        self.fileDropdown.add_command(
            label=lang["dropdown"]["open"],
            command=lambda: self.fu.openFileDialog(),
            accelerator=keys["key.open-file"][0],
        )
        self.bind(keys["key.open-file"][1],
                  lambda string: self.fu.openFileDialog())
        self.fileDropdown.add_separator()
        self.fileDropdown.add_command(
            label=lang["dropdown"]["opendir"],
            command=lambda: self.fu.openDirectory(),
            accelerator=keys["key.open-dir"][0],
        )
        self.bind(keys["key.open-dir"][1], lambda: self.fu.openDirectory())
        self.fileDropdown.add_separator()
        self.fileDropdown.add_command(
            label=lang["dropdown"]["save"],
            command=lambda: self.fu.saveSaveAS(),
            accelerator=keys["key.save-file"][0],
        )
        self.bind(
            keys["key.save-file"][1],
            lambda string: self.fu.saveSaveAS())
        self.fileDropdown.add_command(
            label=lang["dropdown"]["saveas"],
            command=lambda: self.fu.saveSaveAS(),
            accelerator=keys["key.save-as-file"][0],
        )
        self.bind(
            keys["key.save-as-file"][1],
            lambda string: self.fu.saveSaveAS())
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["file-drop"], menu=self.fileDropdown
        )
        
        self.editMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.editMenu.add_command(
            label=lang["dropdown"]["undo"],
            command=lambda: self.editorTextarea.edit_undo(),
            accelerator=keys["key.undo"][0],
        )
        self.bind(
            keys["key.undo"][1],
            lambda string: self.editorTextarea.edit_undo())
        self.editMenu.add_command(
            label=lang["dropdown"]["redo"],
            command=lambda: self.editorTextarea.edit_redo(),
            accelerator=keys["key.redo"][0],
        )
        self.bind(
            keys["key.redo"][1],
            lambda string: self.editorTextarea.edit_redo())
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["edit-drop"], menu=self.editMenu
        )

        self.prefMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.prefMenu.add_command(
            label=lang["dropdown"]["settings"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/settings.json")
            ),
            accelerator=keys["key.settings"][0],
        )
        self.bind(
            keys["key.settings"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/settings.json")
            ),
        )
        self.prefMenu.add_separator()
        self.prefMenu.add_command(
            label=lang["dropdown"]["theme"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/themes/theme.json")
            ),
            accelerator=keys["key.theme"][0],
        )
        self.bind(
            keys["key.theme"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/themes/theme.json")
            ),
        )
        self.prefMenu.add_command(
            label=lang["dropdown"]["hotkeys"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/keys.json")
            ),
            accelerator=keys["key.hotkeys"][0],
        )
        self.bind(
            keys["key.hotkeys"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/keys.json")
            ),
        )
        self.prefMenu.add_command(
            label=lang["dropdown"]["lang"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/lang/lang.json")
            ),
            accelerator=keys["key.lang"][0],
        )
        self.bind(
            keys["key.lang"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/lang/lang.json")
            ),
        )
        self.packgaes = Menu(self.prefMenu)
        self.prefMenu.add_separator()
        self.prefMenu.add_cascade(
            label=lang["dropdown"]["packages"], menu=self.packgaes
        )
        self.prefMenu.add_separator()
        self.prefMenu.add_cascade(
            label=lang["dropdown"]["packages-import"],
            command=lambda: self.pkg.importPackage(),
        )
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["preferences"], menu=self.prefMenu
        )

        self.shellMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.shellMenu.add_command(
            label=lang["dropdown"]["run"],
            command=lambda: self.fu.runFile(),
            accelerator=keys["key.run-module"][0],
        )
        self.bind(keys["key.run-module"][1], lambda string: self.fu.runFile())
        self.shellMenu.add_command(
            label=lang["dropdown"]["configurerun"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/run.json")
            ),
            accelerator=keys["key.run-debug"][0],
        )
        self.bind(
            keys["key.run-debug"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/run.json")
            ),
        )
        self.shellMenu.add_separator()
        self.shellMenu.add_command(
            label=lang["dropdown"]["clear"],
            command=lambda: self.editorTerminal.run_command("clear"),
            accelerator=keys["key.run-clear"][0],
        )
        self.bind(
            keys["key.run-clear"][1],
            lambda string: self.editorTerminal.run_command("clear"),
        )
        self.shellMenu.add_separator()
        self.shellMenu.add_command(
            label=lang["dropdown"]["virtual"],
            command=lambda: None,
            state=DISABLED,
            accelerator=keys["key.virtual"][0],
        )
        self.bind(keys["key.virtual"][1], lambda string: None)
        self.shellMenu.add_command(
            label=lang["dropdown"]["pep"],
            command=lambda: self.fu.pep8format(),
            state=DISABLED,
            accelerator=keys["key.pep"][0],
        )
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["shell-drop"], menu=self.shellMenu
        )

        self.helpMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.helpMenu.add_command(
            label=lang["dropdown"]["about"],
            command=lambda: self.fu.about()
        )
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["help"], menu=self.helpMenu)

        self.config(menu=self.menuApplication)