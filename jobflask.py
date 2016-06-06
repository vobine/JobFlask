from jobflask import app
import argparse

def run (debug):
    app.run (debug=debug)

def main (argv):
    """CLI."""
    parser = argparse.ArgumentParser (
        'JobFlask: an implementation of JobJar using Flask.')
    parser.add_argument ('--debug', '-d',
                         action='store_true',
                         help='Run server in debug mode')

    args = parser.parse_args (argv)
    run (args.debug)

if __name__ == '__main__':
    from sys import argv
    main (argv[1:])
