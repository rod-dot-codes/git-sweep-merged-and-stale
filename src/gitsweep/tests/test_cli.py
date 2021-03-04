from mock import patch

from string import Template

from freezegun import freeze_time
from datetime import timedelta, datetime

from gitsweep.tests.testcases import CommandTestCase


class TestHelpMenu(CommandTestCase):

    """
    Command-line tool can show the help menu.

    """

    def test_help(self):
        """
        If no arguments are given the help menu is displayed.
        """
        (retcode, stdout, stderr) = self.gscommand("git-sweep -h")

        self.assertResults(
            """
            usage: git-sweep <action> [-h]

            Clean up your Git remote branches.

            optional arguments:
              -h, --help         show this help message and exit

            action:
              Preview changes or perform clean up

              {preview,cleanup}
                preview          Preview the branches that will be deleted
                cleanup          Delete merged branches from the remote
            """,
            stdout,
        )

    def test_fetch(self):
        """
        Will fetch if told not to.
        """
        (retcode, stdout, stderr) = self.gscommand("git-sweep preview")

        self.assertResults(
            """
            Fetching from the remote
            No remote branches are available for cleaning up
            """,
            stdout,
        )

    def test_no_fetch(self):
        """
        Will not fetch if told not to.
        """
        (retcode, stdout, stderr) = self.gscommand("git-sweep preview --nofetch")

        self.assertResults(
            """
            No remote branches are available for cleaning up
            """,
            stdout,
        )

    def test_will_preview(self):
        """
        Will preview the proposed deletes.
        """
        for i in range(1, 6):
            self.command("git checkout -b branch{0}".format(i))
            self.make_commit()
            self.command("git checkout master")
            self.make_commit()
            self.command("git merge branch{0}".format(i))

        (retcode, stdout, stderr) = self.gscommand("git-sweep preview")

        self.assertResults(
            """
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

            To delete them, run again with `git-sweep cleanup`
            """,
            stdout,
        )

    def test_will_preserve_arguments(self):
        """
        The recommended cleanup command contains the same arguments given.
        """
        for i in range(1, 6):
            self.command("git checkout -b branch{0}".format(i))
            self.make_commit()
            self.command("git checkout master")
            self.make_commit()
            self.command("git merge branch{0}".format(i))

        preview = "git-sweep preview --master=master --origin=origin"
        cleanup = "git-sweep cleanup --master=master --origin=origin"

        (retcode, stdout, stderr) = self.gscommand(preview)

        self.assertResults(
            """
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

            To delete them, run again with `{0}`
            """.format(
                cleanup
            ),
            stdout,
        )

    def test_will_preview_none_found(self):
        """
        Will preview the proposed deletes.
        """
        for i in range(1, 6):
            self.command("git checkout -b branch{0}".format(i))
            self.make_commit()
            self.command("git checkout master")

        (retcode, stdout, stderr) = self.gscommand("git-sweep preview")
        self.assertResults(
            """
            Fetching from the remote
            No remote branches are available for cleaning up
            """,
            stdout,
        )

    def test_will_cleanup(self):
        """
        Will preview the proposed deletes.
        """
        for i in range(1, 6):
            self.command("git checkout -b branch{0}".format(i))
            self.make_commit()
            self.command("git checkout master")
            self.make_commit()
            self.command("git merge branch{0}".format(i))

        with patch("gitsweep.cli.raw_input", create=True) as ri:
            ri.return_value = "y"
            (retcode, stdout, stderr) = self.gscommand("git-sweep cleanup")

        self.assertResults(
            """
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

            Delete these branches? (y/n) 
              deleting branch1 (done)
              deleting branch2 (done)
              deleting branch3 (done)
              deleting branch4 (done)
              deleting branch5 (done)

            All done!

            Tell everyone to run `git fetch --prune` to sync with this remote.
            (you don't have to, yours is synced)
            """,
            stdout,
        )

    def test_will_abort_cleanup(self):
        """
        Will preview the proposed deletes.
        """
        for i in range(1, 6):
            self.command("git checkout -b branch{0}".format(i))
            self.make_commit()
            self.command("git checkout master")
            self.make_commit()
            self.command("git merge branch{0}".format(i))

        with patch("gitsweep.cli.raw_input", create=True) as ri:
            ri.return_value = "n"
            (retcode, stdout, stderr) = self.gscommand("git-sweep cleanup")

        self.assertResults(
            """
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

            Delete these branches? (y/n) 
            OK, aborting.
            """,
            stdout,
        )

    def test_will_skip_certain_branches(self):
        """
        Can be forced to skip certain branches.
        """
        for i in range(1, 6):
            self.command("git checkout -b branch{0}".format(i))
            self.make_commit()
            self.command("git checkout master")
            self.make_commit()
            self.command("git merge branch{0}".format(i))

        (retcode, stdout, stderr) = self.gscommand(
            "git-sweep preview --skip=branch1,branch2"
        )

        cleanup = "git-sweep cleanup --skip=branch1,branch2"

        self.assertResults(
            """
            Fetching from the remote
            These branches have been merged into master:

              branch3
              branch4
              branch5

            To delete them, run again with `{0}`
            """.format(
                cleanup
            ),
            stdout,
        )

    def test_will_force_clean(self):
        """
        Will cleanup immediately if forced.
        """
        for i in range(1, 6):
            self.command("git checkout -b branch{0}".format(i))
            self.make_commit()
            self.command("git checkout master")
            self.make_commit()
            self.command("git merge branch{0}".format(i))

        (retcode, stdout, stderr) = self.gscommand("git-sweep cleanup --force")

        self.assertResults(
            """
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

              deleting branch1 (done)
              deleting branch2 (done)
              deleting branch3 (done)
              deleting branch4 (done)
              deleting branch5 (done)

            All done!

            Tell everyone to run `git fetch --prune` to sync with this remote.
            (you don't have to, yours is synced)
            """,
            stdout,
        )

    def test_will_force_clean_mixed_with_dates(self):
        """
        Will cleanup immediately if forced.
        """
        valid_deletes = [101, 300, 31, 900]
        invalid_deletes = [29, 30, 14, 0, 1, -100]
        valid_dates = [datetime.now() - timedelta(days=i) for i in valid_deletes]
        invalid_dates = [datetime.now() - timedelta(days=i) for i in invalid_deletes]
        all_deletes = valid_deletes + invalid_deletes
        all_dates = valid_dates + invalid_dates
        for i, date in zip(all_deletes, all_dates):
            self.command("git checkout master")
            time_in_past = freeze_time(date.strftime("%Y-%m-%dT%H:%M"))
            self.command("git checkout -b branch-stale-{0}".format(i))
            self.make_commit(time_in_past)
            self.command("git checkout master")

        for i in range(1, 6):
            self.command("git checkout -b branch{0}".format(i))
            self.make_commit()
            self.command("git checkout master")
            self.make_commit()
            self.command("git merge branch{0}".format(i))

        (retcode, stdout, stderr) = self.gscommand(
            "git-sweep cleanup --force --delete_stale_after_days 30"
        )
        date_replace = {}
        for i, d in enumerate(valid_dates):
            date_replace["date%s" % i] = d.strftime("%Y-%m-%d")

        comparision = Template(
            """
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5
              branch-stale-101 is stale ($date0)
              branch-stale-300 is stale ($date1)
              branch-stale-31 is stale ($date2)
              branch-stale-900 is stale ($date3)

              deleting branch1 (done)
              deleting branch2 (done)
              deleting branch3 (done)
              deleting branch4 (done)
              deleting branch5 (done)
              deleting branch-stale-101 (done)
              deleting branch-stale-300 (done)
              deleting branch-stale-31 (done)
              deleting branch-stale-900 (done)

            All done!

            Tell everyone to run `git fetch --prune` to sync with this remote.
            (you don't have to, yours is synced)
            """
        ).substitute(date_replace)
        self.assertResults(comparision, stdout)

    def test_preview_clean_mixed(self):
        """
        Will cleanup immediately if forced.
        """
        valid_deletes = [101, 300, 31, 900]
        invalid_deletes = [29, 30, 14, 0, 1, -100]
        valid_dates = [datetime.now() - timedelta(days=i) for i in valid_deletes]
        invalid_dates = [datetime.now() - timedelta(days=i) for i in invalid_deletes]
        all_deletes = valid_deletes + invalid_deletes
        all_dates = valid_dates + invalid_dates
        for i, date in zip(all_deletes, all_dates):
            self.command("git checkout master")
            time_in_past = freeze_time(date.strftime("%Y-%m-%dT%H:%M"))
            self.command("git checkout -b branch-stale-{0}".format(i))
            self.make_commit(time_in_past)
            self.command("git checkout master")

        for i in range(1, 6):
            self.command("git checkout -b branch{0}".format(i))
            self.make_commit()
            self.command("git checkout master")
            self.make_commit()
            self.command("git merge branch{0}".format(i))

        (retcode, stdout, stderr) = self.gscommand(
            "git-sweep preview --delete_stale_after_days=30 --force"
        )
        date_replace = {}
        for i, d in enumerate(valid_dates):
            date_replace["date%s" % i] = d.strftime("%Y-%m-%d")

        comparision = Template(
            """
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5
              branch-stale-101 is stale (2020-11-23)
              branch-stale-300 is stale (2020-05-08)
              branch-stale-31 is stale (2021-02-01)
              branch-stale-900 is stale (2018-09-16)

            To delete them, run again with `git-sweep cleanup --delete_stale_after_days=30 --force`
            """
        ).substitute(date_replace)
        print(comparision)
        print(stdout)
        self.assertResults(comparision, stdout)
