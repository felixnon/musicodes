
import sys, getopt

def show_help():
    print ("Usage: python musicodes.py <options> <spotify_uri>")
    print("Options:")
    print("-s\t--split \tCreate seperate model for base and code.")
    print("-p\t--preview \tShow preview of the 3D model.")
    print("-h\t--help \t\tShows this help page.")


def parse_args(argv):
    uri = ""
    split = False
    preview = False

    try:
        opts, args = getopt.getopt(argv,"hsp",["help","split","preview"])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, _ in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-s", "--split"):
            split = True
        elif opt in ("-p", "--preview"):
            preview = True

    if len(args) == 1:
        uri = args[0]
    else:
        show_help()
        sys.exit(2)

    return uri, split, preview
