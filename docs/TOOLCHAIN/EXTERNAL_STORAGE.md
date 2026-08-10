# External Storage for Heavy Operational Artifacts

JGA uses one operational setting for future heavy default writes:

```bash
export JGA_EXTERNAL_ROOT="/path/on/external-volume/JGA"
```

The configured root must already exist, be absolute and be writable. JGA does
not create the root itself. On first use it creates these standard directories:

```text
datasets/    recordings/  stems/       validation/  experiments/
renders/     reports/     temporary/   cache/
```

If the root is unset, missing or unavailable, heavy default writes stop with an
explicit diagnostic. JGA does not silently fall back to repository storage.
Explicit caller-supplied destinations continue to be honored.

Future WAV renders, separated stems, generated figures, experiment working
files, validation working artifacts, caches and temporary processing data
should use this storage. Lightweight canonical metadata and scientific records
remain in the repository.

Existing canonical assets are grandfathered. They must not be moved, deleted
or replaced with symlinks without separate scientific-authority approval.
