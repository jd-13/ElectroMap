set SCRIPT_DIR=%~dp0

ECHO "=== Downloading JUCE ==="
set JUCE_VERSION=8.0.7
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest https://github.com/juce-framework/JUCE/releases/download/%JUCE_VERSION%/juce-%JUCE_VERSION%-windows.zip -OutFile %SCRIPT_DIR%..\..\juce-%JUCE_VERSION%-windows.zip}"
powershell -Command "& {Expand-Archive -LiteralPath %SCRIPT_DIR%..\..\juce-%JUCE_VERSION%-windows.zip -DestinationPath %SCRIPT_DIR%..\..}"

ECHO "=== Generating project ==="
set JUCE_HOME=%SCRIPT_DIR%..\..\JUCE
set PROJECT_DIR=%SCRIPT_DIR%..\..\Projects
%JUCE_HOME%\Projucer --set-global-search-path windows defaultJuceModulePath %JUCE_HOME%\modules
%JUCE_HOME%\Projucer --resave %PROJECT_DIR%\ElectroMap\ElectroMap.jucer

ECHO "=== Starting ElectroMap build ==="
msbuild -version
cd %PROJECT_DIR%\ElectroMap\Builds\VisualStudio2019
msbuild ElectroMap.sln /p:Configuration=Release /p:Platform=x64 || exit /b

ECHO "=== Collecting artefacts ==="
cd %PROJECT_DIR%\ElectroMap\Builds\VisualStudio2019\x64\Release
dir
cd %SCRIPT_DIR%
mkdir -p dist
cd dist
copy %PROJECT_DIR%\ElectroMap\Builds\VisualStudio2019\x64\Release\ElectroMap\ElectroMap.exe || exit /b
