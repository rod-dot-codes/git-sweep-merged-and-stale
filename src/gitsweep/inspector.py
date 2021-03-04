from git import Git, Repo

from datetime import datetime

from .base import BaseOperation


class Inspector(BaseOperation):

    """
    Used to introspect a Git repository.

    """

    def merged_refs(self, skip=[]):
        """
        Returns a list of remote refs that have been merged into the master
        branch.

        The "master" branch may have a different name than master. The value of
        ``self.master_name`` is used to determine what this name is.
        """
        origin = self._origin

        master = self._master_ref(origin)
        refs = self._filtered_remotes(origin, skip=["HEAD", self.master_branch] + skip)
        merged = []

        for ref in refs:
            upstream = "{origin}/{master}".format(
                origin=origin.name, master=master.remote_head
            )
            head = "{origin}/{branch}".format(
                origin=origin.name, branch=ref.remote_head
            )
            cmd = Git(self.repo.working_dir)
            # Drop to the git binary to do this, it's just easier to work with
            # at this level.
            (retcode, stdout, stderr) = cmd.execute(
                ["git", "cherry", upstream, head],
                with_extended_output=True,
                with_exceptions=False,
            )
            if retcode == 0 and not stdout:
                # This means there are no commits in the branch that are not
                # also in the master branch. This is ready to be deleted.
                merged.append(ref)

        return merged

    def stale_branches(self, datetime_older_than, skip=[]):
        """
        Returns a list of remote refs that are stale,
        which is set to the timedelta.
        """
        origin = self._origin

        self._master_ref(origin)
        refs = self._filtered_remotes(origin, skip=["HEAD", self.master_branch] + skip)

        repo = Repo(self.repo.working_dir)

        commits = {}

        for ref in refs:
            commits[ref] = []
            for commit in list(repo.iter_commits(ref)):
                date_committed = datetime.utcfromtimestamp(commit.committed_date)
                if ref in commits:
                    commits[ref] += [date_committed]

        result = []
        for key in commits.keys():
            if commits[key]:
                youngest_commit = max(commits[key])
                if youngest_commit < datetime_older_than:
                    diff = abs(youngest_commit - datetime_older_than).days
                    result.append((key, youngest_commit, diff))

        return result
