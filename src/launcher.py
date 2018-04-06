'''
Created on Feb 12, 2018

Initial class that runs the show.

@author: Philip Deck
'''
import window

if __name__ == '__main__':
    
    app = window.Window()
    app.mainloop()
    
    print("Program created by Philip Deck")
    print(" Ran for {0:.2f} seconds.".format(app.get_uptime()))