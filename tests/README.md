# Kubernetes Testplans

The organization of the test plan is as follows:

The yaml files in `tests/*.yaml` are test plans that control the behavior of
[bundletester](https://github.com/juju-solutions/bundletester). The different
tiers of tests are as follows:


- 10-*  Individual component class checks.
  - Anything the unit can verify as a stand-alone function


- 20-* Component Integration checks.
  - Multi-service connection
  - Connection strings
  - access controls
  - et-al


- 30-* Behavior Driven tests
  - client / consumer behavior tests
  - workload launch, cycle, upgrade tests
  - e2e style testing for binary release management


To execute one of the permutations of this test suite, examine the `tests/*.yaml`
testplans, and determine if your testing category fits within these tiers.

Note: Resource deployment is currently experimental. Its recommended to use the
charms from the charm store, and follow those deployment tests before diving into
hacking on the local deployment test suites


Additional Note:  The local deployment tests encapsulated in `tests/local.yaml`
are currently programmed for CharmBox deployment (:devel juju 2.0+ only) for
now.
