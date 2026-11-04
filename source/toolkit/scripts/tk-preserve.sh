n=${1:-evidence}
tar cf "/tmp/$n.tar" -C "$HOME" case
ls -l "/tmp/$n.tar"
sha256sum "/tmp/$n.tar"
