import os
import sys


def set_enter():

    fn = "docker_enter.sh"

    tag = "src"

    src = fn + "." + tag
    dst = fn
    if os.path.isfile(dst):
        os.remove(dst)

    os.symlink(src, dst)


def set_dc(tag):

    fn = "docker-compose.yml"

    src = fn + "." + tag
    latest = fn + "." + "latest"

    if os.path.isfile(latest):
        os.remove(latest)

    cmd = "cp %s %s" %(src, latest)
    os.system(cmd)

    dst = fn

    if os.path.isfile(dst):
        os.remove(dst)

    os.symlink(latest, dst)


def main():

    usage = "usage: {} tag"

    if len(sys.argv) != 2:
        print(usage.format(sys.argv[0]))
        sys.exit()
    else:
        tag = sys.argv[1]
        set_dc(tag)
        set_enter()


if __name__ == "__main__":

    main()

