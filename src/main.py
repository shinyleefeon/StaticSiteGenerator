



from functions import recursive_copy
from functions import generate_page


def main():
    

    recursive_copy("static", "public/")
    generate_page("content/index.md", "template.html", "public/")


main()
