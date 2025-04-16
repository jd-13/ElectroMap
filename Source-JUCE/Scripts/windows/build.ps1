$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

Write-Output "=== Downloading JUCE ==="
$JUCE_VERSION = "8.0.7"
$JUCE_ZIP = Join-Path -Path $SCRIPT_DIR -ChildPath "..\..\juce-$JUCE_VERSION-windows.zip"
$JUCE_URL = "https://github.com/juce-framework/JUCE/releases/download/$JUCE_VERSION/juce-$JUCE_VERSION-windows.zip"
Invoke-WebRequest -Uri $JUCE_URL -OutFile $JUCE_ZIP -UseBasicParsing

Expand-Archive -LiteralPath $JUCE_ZIP -DestinationPath (Join-Path -Path $SCRIPT_DIR -ChildPath "..\..")

Write-Output "=== Generating project ==="
$PROJECT_DIR = Join-Path -Path $SCRIPT_DIR -ChildPath "..\..\Projects"
$JUCE_HOME = Join-Path -Path $SCRIPT_DIR -ChildPath "..\..\JUCE"


& "$JUCE_HOME\Projucer.exe" --set-global-search-path windows defaultJuceModulePath "$JUCE_HOME\modules"
& "$JUCE_HOME\Projucer.exe" --status "$PROJECT_DIR\ElectroMap\ElectroMap.jucer"
& "$JUCE_HOME\Projucer.exe" --resave "$PROJECT_DIR\ElectroMap\ElectroMap.jucer"

Write-Output "=== Starting ElectroMap build ==="
msbuild -version

cd "$PROJECT_DIR\ElectroMap\Builds\VisualStudio2019"
msbuild "ElectroMap.sln" /p:Configuration=Release /p:Platform=x64

Write-Output "=== Collecting artefacts ==="
cd "$PROJECT_DIR"
New-Item -ItemType Directory -Force -Path "$SCRIPT_DIR/dist"
Copy-Item "$PROJECT_DIR\ElectroMap\Builds\VisualStudio2019\x64\Release\ElectroMap.exe" "$SCRIPT_DIR\dist\ElectroMap.exe"
