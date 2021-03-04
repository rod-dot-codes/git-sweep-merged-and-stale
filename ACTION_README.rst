Git Sweep Merged and Stale
===========================
Delete merged and stale branches from a Github repository.

This deletes branches that fulfil either of these:
  - Merged into Master or Main (specified by ``which_master_main``) OR
  - Branches older than X days (specified by ``delete_stale_after_days``)

This by default does not actually delete until you set parameter action = ``cleanup``

The following branches are not deleted by default:
  - main
  - develop
  - master

::

    WARNING: When you delete branches with no active PR, you will lose access to the ability to restore the branch. Please back it up using Github Artifacts or
    a copy of the branch prior to running this.


`PyPi`_ version available for PIP. Based off `git-sweep`_ .


.. _PyPi: https://pypi.org/project/git-sweep-merged-and-stale/
.. _git-sweep: https://github.com/arc90/git-sweep