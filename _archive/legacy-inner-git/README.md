# Legacy inner-git histories

These two zip files are the `.git/` directories that existed inside
`reporting-site/` and `luminosity-gap/` when the lab's main repo was
initialized on 2026-05-07. Both subfolders were originally scaffolded
as standalone git repositories (one was a Vite Create app; the other
was a Create Next App). When the lab repo did `git init` at the
parent level, git treated them as submodule references rather than
regular folders.

To make the lab a single coherent repository — one history, one
`git push`, no submodule complexity — the inner `.git/` directories
were removed from `reporting-site/` and `luminosity-gap/`, and their
contents were re-staged as regular folders under the lab repo.

These archives preserve the inner histories in case they are ever
needed for reference. To restore one:

```powershell
Expand-Archive -Path reporting-site-git.zip -DestinationPath some-temp-folder/reporting-site-restored
cd some-temp-folder/reporting-site-restored
git log
```

Neither archive is part of the lab's reproducibility chain. They are
preserved purely for audit-trail courtesy. The active lab repository
is the one at the parent of this `_archive/` folder.
