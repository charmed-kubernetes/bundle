#!/bin/bash

display_usage() {
    echo "This script should be run with the intended latest kubernetes release supported"
    echo "This aligns with the track/risk in charmhub as 1.XX/stable"
    echo -e "\n Usage: $0 [release] [cs:charmed-kubernetes-XXX|ch:charmed-kubernetes] \n"
}


RELEASE=$1
BUNDLE_REVISION=$2
if [[ $BUNDLE_REVISION = cs:* ]]; then
    wget "https://api.jujucharms.com/charmstore/v5/${BUNDLE_REVISION/cs:/}/archive" -O "/tmp/$RELEASE.zip"
    rm -f $BUNDLE_REVISION
    ln -s $RELEASE/ $BUNDLE_REVISION
else
    juju download charmed-kubernetes --channel $RELEASE/stable - > "/tmp/$RELEASE.zip"
fi
unzip -n "/tmp/$RELEASE.zip" -d $RELEASE/
