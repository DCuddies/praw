"""Provide the Reddit class."""
import os

from update_checker import update_check
from prawcore import Authenticator, ReadOnlyAuthorizer, Requestor, session

from .errors import RequiredConfig
from .config import Config
from .const import __version__, USER_AGENT_FORMAT
from .models import Front, Redditor, Subreddit


class Reddit(object):
    """Provide convenient access to reddit's API."""

    update_checked = False

    def __enter__(self):
        """Handle the context manager open."""
        return self

    def __exit__(self, *_args):
        """Handle the context manager close."""
        pass

    def __init__(self, site_name=None, **config_settings):
        """Initialize a Reddit instance.

        :param site_name: The name of a section in your ``praw.ini`` file from
            which to load settings from. This parameter in tandem with an
            appropriately configured ``praw.ini`` file is useful if you wish to
            easily save credentials for different applications, or communicate
            with other servers running reddit. If ``site_name`` is ``None``,
            then the site name will be looked for in the environment variable
            PRAW_SITE. If it is not found there, the default site name
            ``reddit`` will be used.

        Additional keyword arguments will be used to initialize the ``Config``
        object. This can be used to specify configuration settings during
        instantiation of the ``Reddit`` instance. For more details please see:
        https://praw.readthedocs.org/en/stable/pages/configuration_files.html

        Required settings are:

        * client_id
        * client_secret
        * user_agent

        """
        self.config = Config(site_name or os.getenv('PRAW_SITE') or 'reddit',
                             **config_settings)

        for attr in ['client_id', 'client_secret', 'user_agent']:
            if not getattr(self.config, attr):
                raise RequiredConfig(attr)

        self._check_for_update()

        self._prepare_prawcore()
        self.front = Front(self)

    def _check_for_update(self):
        if not Reddit.update_checked and self.config.check_for_updates:
            update_check(__package__, __version__)
            Reddit.update_checked = True

    def _prepare_prawcore(self):
        requestor = Requestor(USER_AGENT_FORMAT.format(self.config.user_agent),
                              self.config.oauth_url, self.config.reddit_url)
        authenticator = Authenticator(requestor, self.config.client_id,
                                      self.config.client_secret)
        authorizer = ReadOnlyAuthorizer(authenticator)
        self._core = session(authorizer)

    def redditor(self, name):
        """Lazily return an instance of :class:`~.Redditor` for ``name``.

        :param name: The name of the redditor.

        """
        return Redditor(self, name)

    def request(self, path, params):
        """Return the parsed JSON data returned from a GET request to URL.

        :param path: The path to fetch.
        :param params: The query parameters to add to the request.

        """
        if not self._core._authorizer.is_valid():
            self._core._authorizer.refresh()
        return self._core.request('GET', path, params=params)

    def subreddit(self, name):
        """Lazily return an instance of :class:`~.Subreddit` for ``name``.

        :param name: The name of the subreddit.

        """
        lower_name = name.lower()
        if lower_name == 'random':
            return self.random_subreddit()
        elif lower_name == 'randnsfw':
            return self.random_subreddit(nsfw=True)
        return Subreddit(self, name)