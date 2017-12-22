# aotd

`aotd` is sample code that helps put Azure Advisor recommendations in your `/etc/motd` via `update-motd`.

## Requirements

* Python
* python-requests
* Azure CLI 2.0
* An `update-motd` compatible distribution (we used Ubuntu 14.04)

Note that `aotd` assumes that `root` can run `az advisor recommendation list`. That means, that the `root` user has `az login`'d.

## Configuration

Other than a working Azure CLI 2.0, there's no other configuration needed.

By default, `aotd` will only display high impact recommendations for the VM based on the hostname, as reported by Azure's Instance Metadata Service.

If you want to see all the recommendations, change the `highImpactOnly` setting in `/usr/bin/aotd`.
