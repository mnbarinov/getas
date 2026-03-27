#!/bin/bash
VERSION="1.0.0"
OUTPUT_DIR="dist"

mkdir -p $OUTPUT_DIR

echo "Building DEB..."
fpm -s dir -t deb -n getas -v $VERSION -a amd64 --prefix /usr/bin -f getas/main.py=getas
mv *.deb $OUTPUT_DIR/

echo "Building RPM..."
fpm -s dir -t rpm -n getas -v $VERSION -a all -d "python3" --prefix /usr/bin -f getas/main.py=getas
mv *.rpm $OUTPUT_DIR/

echo "Done! Check the $OUTPUT_DIR directory."
