# Reader Release Bundle

Every tagged companion-laboratory release includes a ZIP archive containing the
complete reader curriculum, templates, schemas, examples, tests, and licenses.
It excludes Git metadata, GitHub administration files, caches, databases, and
build output.

Build locally:

```bash
python3 scripts/build_reader_bundle.py
```

The command writes the archive, a manifest, and SHA-256 checksums under
`dist/`. The directory is generated and is not committed. Release assets are
available from the repository's
[latest release](https://github.com/bmozi/accountable-ai-software-factory-companion/releases/latest).
