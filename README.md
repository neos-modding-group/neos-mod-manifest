# Neos Mod Manifest

This is a community-managed listing of [NeosModLoader] mods. If you have more items for the list, please [open a PR][submission tutorial]. If you want to get update notifications join [our Discord][discord].

The [list][mod list] is automatically generated from a machine-readable [manifest] with github actions. The [schema documentation][schema] explains what the fields in the manifest mean. Having a machine-readable manifest is an important step towards our planned mod manager and auto-updater software.

## Review script

The `review.sh` script finds the first artifact from the `manifest.json` file with a given GUID&version.
Meaning you'll need to checkout a PR for it to find the changed/new version.

It then downloads the file (if it doesn't exist already), checks the file's hashes and then generates a decompiled version.

Example usage:

```sh
review.sh "xyz.ljoonal.neos.latestlog" "0.2.0"
```

Please note that you'll still need to do the reviewing yourself, but the script helps with the tedious parts of downloading the file, checking the hashes and decompiling the .dll file.

<!-- Links -->
[discord]: https://discord.gg/vCDJK9xyvm
[manifest]: manifest.json
[mod list]: https://www.neosmodloader.com/mods
[NeosModLoader]: https://github.com/neos-modding-group/NeosModLoader
[schema]: https://www.neosmodloader.com/schema
[submission tutorial]: https://www.neosmodloader.com/submission-tutorial
