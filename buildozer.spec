[app]
title = Gudang Diskon
package.name = gudangdiskon
package.domain = org.gudangdiskon
source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,kivymd

orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 34
android.minapi = 24
android.build_tools = 34.0.0
android.sdk = 34
android.ndk = 25b
