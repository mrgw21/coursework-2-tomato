#!/bin/bash

# Detect the operating system
OS=$(uname -s)
echo "Detected OS: $OS"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist InsideImmune.zip InsideImmune.app InsideImmune-MacOS.zip InsideImmune-Linux.zip

# Build the project
echo "Building the project..."
if [[ "$OS" == "Darwin" ]]; then
    # macOS build
    pyinstaller --noconsole --name InsideImmune --distpath . \
        --add-data "assets:assets" --add-data "data:data" --windowed main.py

    echo "Creating macOS .app bundle..."
    APP_NAME="InsideImmune.app"
    mkdir -p "$APP_NAME/Contents/MacOS"
    mkdir -p "$APP_NAME/Contents/Resources"

    # Copy the binary to the .app bundle
    mv InsideImmune "$APP_NAME/Contents/MacOS/InsideImmune"

    # Ensure executable permissions
    echo "Ensuring executable permissions for macOS binary..."
    chmod +x "$APP_NAME/Contents/MacOS/InsideImmune"

    # Create Info.plist
    cat > "$APP_NAME/Contents/Info.plist" <<EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>InsideImmune</string>
    <key>CFBundleDisplayName</key>
    <string>InsideImmune</string>
    <key>CFBundleExecutable</key>
    <string>InsideImmune</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.insideimmune</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
EOL

    # Package the .app into a zip
    echo "Packaging InsideImmune for macOS into InsideImmune-MacOS.zip..."
    zip -r InsideImmune-MacOS.zip "$APP_NAME" assets/ data/ README.md

elif [[ "$OS" == "Linux" ]]; then
    # Linux build
    pyinstaller --onefile --name InsideImmune --distpath . \
        --add-data "assets:assets" --add-data "data:data" main.py

    # Ensure executable permissions
    echo "Ensuring executable permissions for Linux binary..."
    chmod +x InsideImmune

    # Package the binary into a zip
    echo "Packaging InsideImmune for Linux into InsideImmune-Linux.zip..."
    zip -r InsideImmune-Linux.zip InsideImmune assets/ data/ README.md

else
    echo "Unsupported OS: $OS. This script supports macOS and Linux only."
    exit 1
fi

echo "Build and packaging complete!"