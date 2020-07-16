import os
import sys

D_CNAME = "docker_babelbot_1"
D_INAME = "babelpish/babelbot"


def commit_container_changes(tag):
    
    cmd = "docker commit -m \"{cmsg}\" {contanier_name} {image_name}:{tag}".format(cmsg="update",
                                                                                   contanier_name=D_CNAME,
                                                                                   image_name=D_INAME,
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
        commit_container_changes(tag)


if __name__ == "__main__":

    main()
