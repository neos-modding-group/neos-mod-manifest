# Mod Submission Guidelines

These guidelines explain what is expected when submitting a new mod version to the manifest.

## Submissions

New submissions **must** be submitted as a [new pull request] to the [manifest] in this repository. Be sure to follow the [schema], and to include a correct SHA256 hash of your artifacts. If you need help with your submission, read the [submission tutorial].

## Obfuscation

Mods **must not** be obfuscated. We audit mods by inspecting their binaries, which is not feasible for obfuscated mods.

## Transparency

Mods **should** be up-front about what they do. Accurate descriptions, screenshots, etc, are all good to have.

Mods **should** be open-source. While this is not a hard requirement, having up-to-date source code available is helpful for the auditing process.

## Remote Code

Mods **must not** download or execute remote code. This means the following are forbidden:

- auto updaters
- fetching Neos json/7zbson/etc from a non-neos server (neosdb urls are okay)

## Not Malicious

Mods **must not** violate the [Neos guidelines] or the [mod and plugin policy].

- Do not bypass protections and controls within Neos, for example SimpleAvatarProtection, permissions, and bans.
- Do not enable asset theft
- Do not enable harassment

## Telemetry

Mods **must not** track users, as defined in the *User Data Tracking* section of the [Neos guidelines].

## Performance

Mods **should** avoid performance hits to Neos where possible. While performance is not the primary goal of the audit, if we notice code that is extremely inefficient we may ask you to improve it.

## Libraries

Mods **should** avoid repackaging third party libraries into their DLL. Consider adding third-party libraries as an external dependency in the manifest. This allows auditors to review your mod and libraries separately and makes the auditing process much faster.

<!-- Links -->
[manifest]: ../manifest.json
[mod and plugin policy]: https://wiki.neos.com/Mod_%26_Plugin_Policy
[Neos guidelines]: https://docs.google.com/document/d/1G_-PaxSp8rGYeHUIXK-19b2VqOLlpOZ18e7DrOwNjG4/edit
[new pull request]: https://github.com/neos-modding-group/neos-mod-manifest/compare
[schema]: schema.md
[submission tutorial]: submission-tutorial.md
