name: Build Android APK

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install --upgrade "cython<3.0.0" buildozer
        sudo apt-get update
        sudo apt-get install -y build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev libffi-dev uuid-dev libncurses5-dev libncursesw5-dev xz-utils libtool autoconf automake cmake gettext pkg-config

    - name: Build with Buildozer
      run: |
        buildozer init
        sed -i 's/android.api = 33/android.api = 31/' buildozer.spec
        sed -i 's/requirements = python3,kivy/requirements = python3==3.10.12,kivy==2.3.0,requests/' buildozer.spec
        yes y | buildozer -v android debug

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: Sweety-APK
        path: bin/*.apk
