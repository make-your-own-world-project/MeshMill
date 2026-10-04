# Releasing MeshMill

The release pipeline builds Windows artifacts on GitHub-hosted Windows runners. End users receive
a self-contained installer or portable ZIP and do not install Python, Node.js, or dependencies.

Before building, refresh and validate the localization source catalogs:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Before the first public release

1. Finish and validate the planned application and documentation translations.
2. Review the GPL and third-party notices.
3. Test installation, launch, STL loading, optimization, export, and uninstallation on a clean
   Windows account or virtual machine.
4. Run CI against `samples/sample-scan.stl`. Inspect every documentation screenshot and crop out
   the taskbar, window chrome that is not part of MeshMill, notifications, private paths, account
   details, and unrelated desktop content before publishing.
5. Configure the repository-local Git author with the account's GitHub no-reply address before the
   first commit. Confirm it with `git config --local --get user.email`.
6. Configure optional Authenticode signing secrets:
   - `WINDOWS_CERTIFICATE_BASE64`: Base64-encoded PFX certificate.
   - `WINDOWS_CERTIFICATE_PASSWORD`: PFX password.

Without a signing certificate, the generated files still work, but Windows SmartScreen may show
an unrecognized-publisher warning. Do not describe unsigned builds as signed or trusted.

## Original scan and Git LFS

`samples/original-scan.stl` is tracked through Git LFS because it exceeds GitHub's normal 100 MiB
file limit. Before the first commit, verify:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

The filter must be `lfs`, and the pointer object ID must match `samples/SHA256SUMS.txt`. The release
workflow checks out LFS content and publishes the original STL as a separate release asset. CI uses
the smaller normal-Git sample and does not download the LFS object.

## Test a release build without publishing

Open **Actions**, select **Release**, choose **Run workflow**, and enter a numeric version such as
`0.1.0`. A manual run uploads workflow artifacts for testing but does not create a public GitHub
Release.

## Publish a release

From a clean, reviewed `main` branch:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

The tag starts the release workflow. It:

1. installs the pinned build dependencies;
2. generates matching Windows version metadata;
3. builds the self-contained GUI and CLI executables;
4. signs the executables when signing secrets are configured;
5. builds the per-user Inno Setup installer;
6. signs the installer when configured;
7. creates the portable ZIP and SHA-256 checksum file;
8. uploads workflow artifacts;
9. creates the GitHub Release for the pushed tag.

Verify the installer and portable archive on a clean Windows system before announcing the release.
Keep the source corresponding to every distributed binary available under the same release tag.
Confirm that the GitHub button points to the final public repository URL before tagging the first
release.
