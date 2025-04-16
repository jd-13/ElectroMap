#!/bin/bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null 2>&1 && pwd )"

echo "=== Downloading JUCE ==="
JUCE_VERSION=8.0.7
wget https://github.com/juce-framework/JUCE/releases/download/$JUCE_VERSION/juce-$JUCE_VERSION-osx.zip \
     -P $SCRIPT_DIR/../..
unzip $SCRIPT_DIR/../../juce-$JUCE_VERSION-osx.zip

echo "=== Generating project ==="
PROJECT_DIR=$SCRIPT_DIR/../../Projects
JUCE_HOME=$SCRIPT_DIR/../../JUCE
$JUCE_HOME/Projucer.app/Contents/MacOS/Projucer --set-global-search-path osx defaultJuceModulePath $JUCE_HOME/modules
$JUCE_HOME/Projucer.app/Contents/MacOS/Projucer --resave $PROJECT_DIR/ElectroMap/ElectroMap.jucer

echo "=== Starting ElectroMap build ==="
cd $PROJECT_DIR/ElectroMap/Builds/MacOSX
xcodebuild -version
xcodebuild -project ElectroMap.xcodeproj -scheme "ElectroMap - App" -configuration Release ONLY_ACTIVE_ARCH=NO

echo "=== Collecting artefacts ==="
mkdir -p $SCRIPT_DIR/dist
cp -r $PROJECT_DIR/ElectroMap/Builds/MacOSX/build/Release/ElectroMap.app $SCRIPT_DIR/dist
