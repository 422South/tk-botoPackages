# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.



THIS_MODULE_NAME = "python"

# first import our alternative API
import six
if six.PY3:
    import python3
    ALT_API_NAME = "python3"
else:
    import python27
    ALT_API_NAME = "python27"


# now go through and duplicate all entries in sys.modules
import sys

# Generate a list of keys to iterate over,
# since we'll be mutating the dict as we iterate.
for x in list(sys.modules.keys()):

    if x.startswith("%s." % ALT_API_NAME):
        # this is a submodule inside the alternative API
        # create a copy in sys.modules with our own name
        new_name = "%s.%s" % (THIS_MODULE_NAME, x[len(ALT_API_NAME) + 1 :])
        sys.modules[new_name] = sys.modules[x]

    elif x == ALT_API_NAME:
        # this is the actual alternative module
        # remap that too - this means we are remapping ourselves...
        sys.modules[THIS_MODULE_NAME] = sys.modules[x]
        # now ensure that the other module has sys imported,
        # otherwise we can no longer access sys or any of the predefined variables
        # beyond this point.
        if six.PY3:
            ALT_API_NAME = "python3"
        else:
            ALT_API_NAME = "python27"

        THIS_MODULE_NAME = "python"
        import sys

# lastly, remap the globals accessor to point at our new module
globals()[THIS_MODULE_NAME] = sys.modules[THIS_MODULE_NAME]
