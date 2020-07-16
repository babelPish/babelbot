import os
import sys


D_INAME = "babelpish/babelbot"


def push_image(tag):
    
    cmd = "docker push {image_name}:{tag}".format(image_name=D_INAME,
                                                  tag=tag)
    print(cmd)
    os.system(cmd)

 
def main():

    usage = "usage: {} tag"

    if len(sys.argv) != 2:
        print(usage.format(sys.argv[0]))
        sys.exit()
    else:
        tag = sys.argv[1]
        push_image(tag)


if __name__ == "__main__":

    main()
