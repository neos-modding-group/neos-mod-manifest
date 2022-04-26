#!/bin/sh
set -e

NEOS_PATH="$HOME/.local/share/Steam/steamapps/common/NeosVR"

MOD_GUID="$1"
MOD_VERSION="$2"

BASEDIR="$(dirname "$0")"
ARTIFACT_SELECTOR=".mods[\""$MOD_GUID"\"].versions[\""$MOD_VERSION"\"].artifacts[0]"
FILE_URL="$(jq -r "$ARTIFACT_SELECTOR.url" "$BASEDIR/manifest.json")"
FILE_FILENAME="$(jq -r "$ARTIFACT_SELECTOR.filename" "$BASEDIR/manifest.json")"
FILE_SHA256="$(jq -r "$ARTIFACT_SELECTOR.sha256" "$BASEDIR/manifest.json")"
FILE_BLAKE3="$(jq -r "$ARTIFACT_SELECTOR.blake3" "$BASEDIR/manifest.json")"


if [ "$FILE_URL" == "null" ]; then
	echo "Couldn't get artifact URL!"
	exit 1
fi

if [ "$FILE_FILENAME" == "null" ]; then
	FILE_FILENAME="$(basename "$FILE_URL")"
fi

if [[ "$FILE_FILENAME" != *.dll ]]; then
	echo "Couldn't get dll filename"
	exit 1
fi

MOD_VERSION_FOLDER="$BASEDIR/reviews/$MOD_GUID/$MOD_VERSION"
mkdir -p "$MOD_VERSION_FOLDER"
MOD_FILEPATH="$MOD_VERSION_FOLDER/$FILE_FILENAME"

if [ -f "$MOD_FILEPATH" ]; then
	echo "$FILE_FILENAME exists, skipping download."
else
	curl -L "$FILE_URL" > "$MOD_FILEPATH"
fi

if [ "$FILE_SHA256" == "null" ]; then
	echo "WARNING! SHA256 value wasn't found, so no check could be performed!" >&2
else
	FILE_SHA256="$(echo "$FILE_SHA256" | tr '[:upper:]' '[:lower:]')"
	ACTUAL_SHA256="$(sha256sum "$MOD_FILEPATH" | cut -d ' ' -f 1 | tr '[:upper:]' '[:lower:]')"
	if [ "$FILE_SHA256" != "$ACTUAL_SHA256" ]; then
		echo "SHA256 sums don't match!"
		echo "Expected: $FILE_SHA256"
		echo "Actual:   $ACTUAL_SHA256"
		exit 1
	fi
fi

if [ "$FILE_BLAKE3" != "null" ]; then
	FILE_BLAKE3="$(echo "$FILE_BLAKE3" | tr '[:upper:]' '[:lower:]')"
	ACTUAL_BLAKE3="$(b3sum "$MOD_FILEPATH" | cut -d ' ' -f 1 | tr '[:upper:]' '[:lower:]')"
	if [ "$FILE_BLAKE3" != "$ACTUAL_BLAKE3" ]; then
		echo "Blake3sums don't match!"
		echo "Expected: $FILE_BLAKE3"
		echo "Actual:   $ACTUAL_BLAKE3"
		exit 1
	fi
fi

ilspycmd -d --il-sequence-points -o "$MOD_VERSION_FOLDER" \
-r "$NEOS_PATH/" \
-r "$NEOS_PATH/Neos_Data/Managed" \
-r "$NEOS_PATH/Libraries" \
-r "$NEOS_PATH/nml_libs/" \
"$MOD_FILEPATH"

ilspycmd -d -p -o "$MOD_VERSION_FOLDER" \
-r "$NEOS_PATH/" \
-r "$NEOS_PATH/Neos_Data/Managed" \
-r "$NEOS_PATH/Libraries" \
-r "$NEOS_PATH/nml_libs/" \
"$MOD_FILEPATH"

echo "Done, output is at: $MOD_VERSION_FOLDER"
