import tkinter as tk
from tkinter import ttk
from src.sqlconnector import SQLConnector

from sortedcontainers import SortedSet

INTERFACE_TITLE = "Search For Available Movies"

ROWS, COLS = 2, 3


class GUI(tk.Frame):
    """Used to create a graphic user interface for searching through the database

    Components:
        :param self.root: Holds graphics root figure
        :param self.sc: SQL connector used to interact with MySQL database
        :param self.search_entry_var: Holds entry for entering search term
    """

    def __init__(self):
        """Initializes all necessary variables"""

        self.root = tk.Tk()

        # Initializes frame with root object for graphics . . .
        tk.Frame.__init__(self, self.root)
        self.root.wm_title(INTERFACE_TITLE)

        # Makes the window close button quit program . . .
        self.root.protocol("WM_DELETE_WINDOW", self.__quit_program)
        self.root['bg'] = 'white'

        self.root.resizable(True, True)     # Allows window to be resized . . .

        # Setting weights for each row . . .
        for i in range(ROWS):
            self.root.rowconfigure(i, weight=1)
        for i in range(COLS):
            self.root.columnconfigure(i, weight=1)

        # Setting ttk styling . . .
        style = ttk.Style()
        style.configure('W.TButton', background='white')
        style.configure('W.TLabelframe', background='white')

        # Variables used to keep track of options/entries in the GUI . . .
        self.search_entry_var = tk.StringVar()  # Used for keeping track of search string . . .

        # MySQL Connector used for interacting with database . . .
        self.sc = None

    # END def __init__() #

    def add_features(self):
        """Inserts every feature into the root's figure"""

        # Goes through and includes all features . . .
        self.__feature_search_tool()

        # Non-visible features here . . .
        self.sc = SQLConnector()

    # END def add_features() #

    def __feature_search_tool(self):
        """Adds components for search feature, including label, entry, and button"""

        # Title for search . . .
        search_label = ttk.Label(self.root, text="Find Movies Playing", justify='center', background='white')
        search_label.config(font=("Courier", 25))
        search_label.grid(row=0, column=0, columnspan=3)

        # Entry box for search . . .
        search_entry = ttk.Entry(self.root, textvariable=self.search_entry_var, validate="key")
        search_entry.bind("<Return>", self.__search_tool_entry)
        search_entry.config(width=40)
        search_entry.grid(row=1, column=0, columnspan=2, sticky='ew')

        # Button for search . . .
        search_button = ttk.Button(self.root, text="Search", command=self.__search_tool, style='W.TButton')
        search_button.config(width=20)
        search_button.grid(row=1, column=2, sticky='ew')

    # END def __feature_search_tool #

    def __search_tool(self):
        """Interfaces with MySQL connector to provide a search"""

        # Gathers string from entry box . . .
        search_term = self.search_entry_var.get()

        # Connects to the database to find all movies playing with search term . . .
        results = self.sc.find_movies_playing(search_term)

        # Creates pop up dialog box to display movie listings . . .
        PopupDialog(self.root, 'display_movie_listings', data=results, title="Results for \'%s\'" % search_term)

        # Clears string from entry box . . .
        self.search_entry_var.set("")

    # END def __search_tool

    def __search_tool_entry(self, event):
        """Callback function to the real search function (holds event)

        Keyword arguments:
            :param event: Holds event data (unused)
        """

        self.__search_tool()

    # END def __search_tool_entry #
    def __quit_program(self):
        """Closes current running tkinter window"""

        self.sc.close()     # Close connection to MySQL connector . . .
        self.quit()         # Quit and destroy tkinter graphics . . .
        self.destroy()

    # END def __quit_program() #


class PopupDialog(object):
    """Dialog used during execution of a tkinter window

    Components:
        :param: self.top: Figure used on top of a root figure
    """

    def __init__(self, parent, option, data=None, title=None):
        """Initializes all necessary variables

        Keyword arguments:
            :param parent: Tkinter root that will be referenced in this object
            :param option: Decides which type of popup this dialog is
            :param data: Data needed for popup (sometimes used)
            :param title: Title for popup (sometimes used)
        """

        self.top = tk.Toplevel(parent)
        self.top.protocol("WM_DELETE_WINDOW", self._on_close)   # Redirects the windows close button to function . . .
        self.top.resizable(False, False)                        # Prevents windows from being re-sized . . .

        # Finds which option of pop up was chosen . . .
        if option is 'display_movie_listings':
            self.top.title(title)
            self.display_movie_listings(data)

    # END def __init__() #

    def display_movie_listings(self, results):
        """Displays all available movie listings

        Keyword arguments:
            :param results: Returned tuples of movies playing with title, date, and time
        """

        T = tk.Text(self.top)
        T.pack()

        T.tag_configure('title', font=('Verdana', 25, 'bold'))
        T.tag_configure('showing', font=('Arial', 15, 'bold', 'italic'))

        # If there are no results . . .
        if not results:
            T.insert(tk.END, "Sorry! We couldn't find any movies", 'title')

        # If there are results . . .
        else:

            # Ordered set, so that it checks for unique showings and displays items in order . . .
            unique_showings = SortedSet()

            for showing in results:
                unique_showings.add(showing[0])

            T.insert(tk.END, "There are %d movie(s) showing!\n\n" % len(unique_showings), 'title')

            # Begins displaying both movie titles and show times . . .
            showtime = 0
            num_showtimes = len(results)
            for showing in unique_showings:
                T.insert(tk.END, showing + '\n\n', 'showing')
                while showtime < num_showtimes and showing == results[showtime][0]:
                    T.insert(tk.END, results[showtime][1] + " @ " + results[showtime][2] + '\n')
                    showtime += 1
                T.insert(tk.END, '\n')

    # END def display_movie_listings() #

    def _on_close(self):
        """Closes popup window"""

        self.top.destroy()

    # END def _on_close() #
