# Versioning

Unlike Friendly data, the registry follows calendar versioning.  The
rationale is, this repo will be see more frequent updates, and it is
more important to know how old a version is.  Also, there is no real
notion of stable/unstable, so calendar dates suit well as a versioning
scheme.

## Package version vs Git tag

The package version is a number, possibly followed by a single digit
patch version number: `20211120.[n]`; whereas the git tag separates
year, month, and day with a hyphen for readability: `2021-11-20.[n]`.
The package version needs to be a number for realiable sorting.

# Releasing a new version

    $ ./dev/tag_release.bash [patch-version]

The [tag_release.bash](./tag_release.bash) script in this directory
- generates a calendar version number,
- updates the appropriate package files with the new version number,
- creates a new commit, and
- tags the commit with the version number.

Note, that the script can also generate a patch release in case there
are multiple releases in one day. This is done by passing a patch
argument to the script, which is appended to the calendar version like
this: `2021-11-20` → `2021-11-20.1`.  The expected convention is that
the patch version is a single digit number (assuming there can only be
a handful of patch releases in a day).

The maintainer then has to push the tags to GitHub, and mark the tag
as a release from the web interface.  GitHub actions take care of the
rest.
