#!/bin/bash

# Параметры релиза
VERSION="1.0.0"
OUTPUT_DIR="dist"
SOURCE_FILE="getas/main.py"

# Очистка и подготовка
mkdir -p $OUTPUT_DIR
rm -f $OUTPUT_DIR/*.deb $OUTPUT_DIR/*.rpm

echo "--- Начинаю сборку версии $VERSION ---"

# 1. Сборка DEB (архитектура 'all' для Python-скрипта)
echo "[1/2] Сборка .deb пакета (Debian/Ubuntu/Astra)..."
fpm -s dir -t deb \
    -n getas \
    -v $VERSION \
    -a all \
    -d "python3" \
    --description "CLI tool to retrieve AS info and BGP routes" \
    --prefix /usr/bin \
    -f $SOURCE_FILE=getas

# 2. Сборка RPM (архитектура 'noarch' для ALT/Fedora/CentOS)
echo "[2/2] Сборка .rpm пакета (ALT Linux/RedHat)..."
fpm -s dir -t rpm \
    -n getas \
    -v $VERSION \
    -a noarch \
    -d "python3" \
    --description "CLI tool to retrieve AS info and BGP routes" \
    --prefix /usr/bin \
    -f $SOURCE_FILE=getas

# Перемещаем готовое в dist
mv *.deb *.rpm $OUTPUT_DIR/

echo "--- Сборка завершена! Файлы в папке $OUTPUT_DIR ---"
ls -lh $OUTPUT_DIR
