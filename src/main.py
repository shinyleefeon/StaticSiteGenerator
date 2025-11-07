



from functions import recursive_copy
from functions import generate_pages_recursive


def main():
    

    recursive_copy("static", "public/")
    generate_pages_recursive("content/", "template.html", "public/")


main()
