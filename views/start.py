import tkinter as tk
from login import LoginApplication
import sys
from config import PROJECT_DIRECTORY
sys.path.append(str(PROJECT_DIRECTORY))

from views.login import LoginApplication 

def main():
    app = LoginApplication()
    app.mainloop()

if __name__ == "__main__":
    main()
