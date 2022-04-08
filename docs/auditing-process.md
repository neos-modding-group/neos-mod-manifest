# Mod Auditing Process
This is the process mod auditors follow when reviewing a new addition to the manifest.

## Pull Requests
- Submissions are [pull requests] on this repository that add a new mod or mod version
- Reviewers must download the linked artifact and perform a binary inspection
- At least one (preferably more) approval from a reviewer is mandatory before merging
- Mod authors cannot approve their own mods

## Binary Inspection
The mod binary must be inspected in a decompiler for [malicious] code and other disallowed behavior.

### Hash
Ensure the provided SHA256 matches the artifact.

### Obfuscation
Ensure that the mod is not using any form of obfuscation.

### Network usage
Network usage should be examined closely. Examine worst-case scenarios assuming servers are untrustworthy. Make sure remote users can't force the mod user to hit arbitrary endpoints.

**Relevant imports:**
- System.Net

### Filesystem usage
Ensure the mod isn't reading or writing to files it shouldn't. Watch out for [path traversal] vulnerabilities. Make sure remote users can't force the mod user to read/write arbitrary files. Make sure the mod isn't downloading executable code, including LogiX and/or components (from a non-neosdb source).

**Relevant imports:**
- System.IO

### Process usage
Examine process invocation extremely closely. Why is this needed? Can it be abused to invoke arbitrary processes? Can remote users trigger this behavior?

**Relevant imports:**
- System.Diagnostics.Process

### Dynamic code execution
Ensure the mod can't execute arbitrary code, *especially* remotely. Ensure reflection can't be abused to leak sensitive internal Neos state, such as the Neos authorization token.

**Relevant imports:**
- System.Reflection
- System.Runtime.CompilerServices

### Denial of Service
While not a strict auditing requirement, keep an eye open for expensive operations a remote user could trigger. Vanilla Neos has plenty of ways to perform DoS attacks already, but if a mod is particularly easy to DoS it's worth mentioning.

### Performance
While not a strict auditing requirement, consider pointing out inefficiencies to the mod author.

### Third Party Libraries
Well-known and widely-used third-party libraries can be assumed to be trustworthy and do not need auditing.

Poorly-known third-party libraries from unknown authors need auditing.

### If You Are Uncertain
If you see something in a mod you're uncertain about, please don't hesitate to ask for a second opinion. Don't approve a submission unless you're 100% certain it's safe.

<!-- Links -->
[malicious]: mod-guidelines.md#not-malicious
[path traversal]: https://owasp.org/www-community/attacks/Path_Traversal
[pull requests]: https://github.com/neos-modding-group/neos-mod-manifest/pulls
