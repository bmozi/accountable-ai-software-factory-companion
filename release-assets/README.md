# Reader Release Bundle

Every tagged companion-laboratory release includes a ZIP archive containing the
complete reader curriculum, templates, schemas, examples, tests, build and
validation scripts, public support templates, and licenses. Shell entry points
retain executable permissions in the archive. It excludes Git metadata,
caches, databases, and build output.

Build locally:

```bash
python3 scripts/build_reader_bundle.py
```

The command writes the archive, a manifest, and SHA-256 checksums under
`dist/`. The directory is generated and is not committed. Release assets are
available from the repository's
[latest release](https://github.com/bmozi/accountable-ai-software-factory-companion/releases/latest).

CI unpacks the release ZIP into a clean directory, verifies the shell entry
point is executable, runs the documented reader journey, and revalidates the
unpacked repository. The same code and journey also run on Windows through
native Python commands.
