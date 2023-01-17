from settings import *
from app import *

if __name__ == "__main__":
    window = App()
    window.geometry(prefs['editor']['window']['geometry'])
    window.title(prefs['editor']['window']['title'])
    window.resizable(prefs['editor']['window']['resizable'], prefs['editor']['window']['resizable'])
    window.minsize(prefs['editor']['window']['minimizable'][0], prefs['editor']['window']['minimizable'][1])
    window.mainloop()
