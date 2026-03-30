# Maintainer: Mikhail Barinov <dev@mbarinov.ru>
pkgname=getas
pkgver=1.1.1
pkgrel=1
pkgdesc="A CLI tool to retrieve AS information and BGP routes from WHOIS"
arch=('any')
url="https://github.com/mnbarinov/getas"
license=('MIT')
depends=('python')
source=("getas::https://raw.githubusercontent.com/mnbarinov/getas/refs/heads/master/getas/main.py")
sha256sums=('1d22c082e8b85271dee6d1de3085a003b2a53ead3db25c48473485c6274260b7')

package() {
    # Создаем директорию для исполняемых файлов
    install -Dm755 "${srcdir}/getas" "${pkgdir}/usr/bin/getas"
}
