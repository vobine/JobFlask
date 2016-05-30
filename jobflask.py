from jobflask import app
import argparse

def run (debug):
    app.run (debug=debug)

def main (argv):
    run (True)

if __name__ == '__main__':
    from sys import argv
    main (argv[1:])
