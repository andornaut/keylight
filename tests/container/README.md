# Container tooling

WORKAROUND: Scoped npm overrides keep Markdown lint dependencies patched for
[re2js](https://github.com/advisories/GHSA-gg6h-894w-4m9c) and
[KaTeX](https://github.com/advisories/GHSA-238p-pmpm-9mq7).
Remove the overrides when the upstream CLI dependency graph resolves patched
versions without them.
