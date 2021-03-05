Git Sweep Merged and Stale Github Action
========================================
Delete merged and stale branches from a Github repository.

See example `Preview`_ and `Cleanup`_ step.

You need to use Python 3.6+ and declare it before

::

    uses: actions/setup-python@v2
    with:
        python-version: '3.x'
        architecture: 'x64'


This deletes branches that fulfil either of these:
  - Merged into Master or Main (specified by ``which_master_main``) OR
  - Branches older than X days (specified by ``delete_stale_after_days``)

This by default does not actually delete until you set parameter action = ``cleanup``

The following branches are not deleted by default:
  - main
  - develop
  - master

::

    WARNING: When you delete branches with no active PR, 
    you will lose access to the ability to restore the branch.
    Please back it up using Github Artifacts or
    a copy of the branch prior to running this.

Read the Python `Readme`_ .
`PyPi`_ version available for PIP.

Based off `git-sweep`_ .

MIT License.

.. _Preview: https://github.com/rodvdka/git-sweep-merged-and-stale/blob/master/preview.yml
.. _Cleanup: https://github.com/rodvdka/git-sweep-merged-and-stale/blob/master/cleanup.yml
.. _PyPi: https://pypi.org/project/git-sweep-merged-and-stale/
.. _Readme: https://github.com/rodvdka/git-sweep-merged-and-stale/blob/master/PACKAGE_README.rst
.. _git-sweep: https://github.com/arc90/git-sweep