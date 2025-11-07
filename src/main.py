

import sys

from functions import recursive_copy
from functions import generate_pages_recursive


def main():
    
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    

    recursive_copy("static/", "docs/")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


main()
