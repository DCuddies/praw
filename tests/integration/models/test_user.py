"""Test praw.models.user."""
from praw.models import Multireddit, Redditor, Subreddit

from .. import IntegrationTest


class TestUser(IntegrationTest):
    def test_blocked(self):
        self.reddit.read_only = False
        with self.recorder.use_cassette('TestUser.test_blocked'):
            blocked = self.reddit.user.blocked()
        assert len(blocked) > 0
        assert all(isinstance(user, Redditor) for user in blocked)

    def test_contributor_subreddits(self):
        self.reddit.read_only = False
        with self.recorder.use_cassette(
                'TestUser.test_contributor_subreddits'):
            count = 0
            for subreddit in self.reddit.user.contributor_subreddits():
                assert isinstance(subreddit, Subreddit)
                count += 1
            assert count > 0

    def test_friends(self):
        self.reddit.read_only = False
        with self.recorder.use_cassette('TestUser.test_friends'):
            friends = self.reddit.user.friends()
        assert len(friends) > 0
        assert all(isinstance(friend, Redditor) for friend in friends)

    def test_me(self):
        self.reddit.read_only = False
        with self.recorder.use_cassette('TestUser.test_me'):
            me = self.reddit.user.me()
        assert isinstance(me, Redditor)

    def test_moderator_subreddits(self):
        self.reddit.read_only = False
        with self.recorder.use_cassette('TestUser.test_moderator_subreddits'):
            count = 0
            for subreddit in self.reddit.user.moderator_subreddits():
                assert isinstance(subreddit, Subreddit)
                count += 1
            assert count > 0

    def test_multireddits(self):
        self.reddit.read_only = False
        with self.recorder.use_cassette('TestUser.test_multireddits'):
            multireddits = self.reddit.user.multireddits()
            assert isinstance(multireddits, list)
            assert multireddits
            assert all(isinstance(x, Multireddit) for x in multireddits)

    def test_subreddits(self):
        self.reddit.read_only = False
        with self.recorder.use_cassette('TestUser.test_subreddits'):
            count = 0
            for subreddit in self.reddit.user.subreddits():
                assert isinstance(subreddit, Subreddit)
                count += 1
            assert count > 0
