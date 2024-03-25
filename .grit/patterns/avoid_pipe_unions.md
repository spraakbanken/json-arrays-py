---
title: Avoid pipe unions in python 3.9
tag: [refactor]
---

Example

```grit
language python

`$type | None` => `Optional[$type]`
```
