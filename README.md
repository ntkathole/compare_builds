# compare_builds
This is the script to compare packages in two different release engineering builds

### This script will perform 

1. <b>RPMs Signature Check</b>: Assure all packages are signed and check signed with particulat signature.
2. <b>Compare package versions</b>: Compare package versions between builds. This is probably close to being as simple as a diff on the filenames.

### Running script

<i> export SATELLITE_SNAP_URL = http://url/ </i>

<i> export RCM_COMPOSE_URL = http://url/ </i>

<i> export SIGNATURE = signature </i>

<i> python compare_versions.py </i>
