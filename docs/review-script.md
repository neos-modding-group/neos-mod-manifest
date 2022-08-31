# Review script

The [`review.sh`](../review.sh) script finds the first artifact from the [`manifest.json`](../manifest.json) file with a given GUID and version.
Meaning you'll need to checkout a PR for it to find the changed/new version.

It then downloads the file (if it doesn't exist already), checks the file's hashes and then generates a decompiled version.

Example usage:

```sh
review.sh "xyz.ljoonal.neos.latestlog" "0.2.0"
```

Please note that you'll still need to do the reviewing yourself, but the script helps with the tedious parts of downloading the file, checking the hashes and decompiling the .dll file.
