# Contributor Guide

This Juju bundle and associated code is open source ([Apache License 2.0](./LICENSE)) and we actively seek any
community contibutions for code, suggestions and documentation.
Most of the code contributions for Charmed Kubernetes are likely to relate to the charms themselves, rather than
this bundle which is mainly unchanged from release to release.

The [README.md](./README.md) file details how to use this bundle and the bundle commands to compile the bundle.yaml
files for the current Charmed Kubernetes and derived bundles. 

## Licensing

This charm has been created under the [Apache License 2.0](./LICENSE), which will cover any contributions you may
make to this project. Please familiarise yourself with the terms of the license.

Additionally, this charm uses the Harmony CLA agreement.  It’s the easiest way for you to give us permission to
use your contributions.
In effect, you’re giving us a license, but you still own the copyright — so you retain the right to modify your
code and use it in other projects. Please [sign the CLA here](https://ubuntu.com/legal/contributors/agreement) before
making any contributions.

## Code of conduct

We have adopted the Ubuntu code of Conduct. You can read this in full [here](https://ubuntu.com/community/code-of-conduct).

## Contributing code

To contribute code to this project, please use the following workflow:

1. [Submit a bug](https://bugs.launchpad.net/charmed-kubernetes/+filebug) to explain the need for and track the change.
2. Create a branch on your fork of the repo with your changes, including a unit test covering the new or modified code.
3. Submit a PR. The PR description should include a link to the bug on Launchpad.
4. Update the Launchpad bug to include a link to the PR and the `review-needed` tag.
5. Once reviewed and merged, the change will become available on the edge channel and assigned to an appropriate milestone
   for further release according to priority.

## Documentation

Documentation for Charmed Kubernetes docs is currently located at 
[this repository](https://github.com/charmed-kubernetes/kubernetes-docs/).
