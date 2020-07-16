#!/usr/bin/env bash

# Set mecab related variable(s)
mecab_dicdir="/usr/local/lib/mecab/dic/mecab-ko-dic"

# Exit as soon as we fail
set -e

# Determine sudo
if hash "sudo" &>/dev/null; then
    sudo="sudo"
else
    sudo=""
fi

# Determine python
python="python3"

install_mecab_ko(){
    cd /tmp
    curl -LO https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz
    tar zxfv mecab-0.996-ko-0.9.2.tar.gz
    cd mecab-0.996-ko-0.9.2
    ./configure
    make
    make check
    $sudo make install
}

install_automake(){
    ## install requirement automake1.11
    # TODO: if not [automake --version]
    $sudo apt-get update && $sudo apt-get install -y automake-1.15
}

install_mecab_ko_dic(){
    echo "Install mecab-ko-dic"
    cd /tmp
    curl -LO https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz
    tar -zxvf mecab-ko-dic-2.1.1-20180720.tar.gz
    cd mecab-ko-dic-2.1.1-20180720
    ./autogen.sh
    ./configure
    mecab-config --libs-only-L | $sudo tee /etc/ld.so.conf.d/mecab.conf  # XXX: Resolve #271, #182, #133
    $sudo ldconfig

    make
    $sudo sh -c 'echo "dicdir=/usr/local/lib/mecab/dic/mecab-ko-dic" > /usr/local/etc/mecabrc'
    $sudo make install
}

echo "Installing automake (A dependency for mecab-ko)"
install_automake

echo "Install mecab-ko-dic"
install_mecab_ko


echo "Install mecab-ko-dic"
install_mecab_ko_dic

echo "Done."
