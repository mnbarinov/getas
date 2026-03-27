# Maintainer: Your Name <your@email.com>
pkgname=getas-tool
pkgver=1.0.0
pkgrel=1
pkgdesc="A CLI tool to retrieve AS information and BGP routes from WHOIS"
arch=('any')
url="https://github.com/mnbarinov/getas"
license=('MIT')
depends=('python')
source=("getas::https://raw.githubusercontent.com/mnbqrinov/getas/master/getas.py")
sha256sums=('117d500608cfdf0fc155d6504a279058220b3721ff2172c402b5dd512ad65968')

package() {
    # Создаем директорию для исполняемых файлов
    install -Dm755 "${srcdir}/getas" "${pkgdir}/usr/bin/getas"
}
