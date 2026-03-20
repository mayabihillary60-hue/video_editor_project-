
[app]
title = Video Editor
package.name = videoeditor
package.domain = org.yourname

source.dir = src
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy,moviepy,opencv,numpy,Pillow

orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0

[buildozer]
log_level = 2
warn_on_root = 1
EOF

# Build APK (requires Android SDK/NDK)
buildozer android debug