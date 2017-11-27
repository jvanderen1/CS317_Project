from src.gui import GUI


def main():
    """Generates UI for the user"""

    gui = GUI()         # Creates graphics object . . .
    gui.add_features()  # Adds search bar, etc . . .
    gui.mainloop()      # Starts GUI . . .


# Program begins execution here . . .
if __name__ == "__main__":
    main()
