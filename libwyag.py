# we will use argparse to be able to pass our commands in terminal
import argparse
# We’ll need a few more container types than the base lib provides, most notably an OrderedDict
import collections

# Git uses a configuration file format that is basically Microsoft’s INI format. The configparser module can read and write these files
import configparser

# Git uses the SHA-1 function quite extensively. In Python, it’s in hashlib
import hashlib

# filesystem abstraction routines
import os

# regular expressions
import re

# sys to access the actual command-line arguments
import sys

# compresses everything using zlib
import zlib


argparser = argparse.ArgumentParser(description="Content tracker")
'''
    this ensures you just dont call git , we need to call git [argument] i.e git init 
'''
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

'''
    we  read this string and call the correct function accordingly
'''


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == 'add':
        cmd_add(args)
    elif args.command == "cat-file":
        cmd_cat_file(args)
    elif args.command == "checkout":
        cmd_checkout(args)
    elif args.command == "commit":
        cmd_commit(args)
    elif args.command == "hash-object":
        cmd_hash_object(args)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "log":
        cmd_log(args)
    elif args.command == "ls-tree":
        cmd_ls_tree(args)
    elif args.command == "merge":
        cmd_merge(args)
    elif args.command == "rebase":
        cmd_rebase(args)
    elif args.command == "rev-parse":
        cmd_rev_parse(args)
    elif args.command == "rm":
        cmd_rm(args)
    elif args.command == "show-ref":
        cmd_show_ref(args)
    elif args.command == "tag":
        cmd_tag(args)


class GitRepository(object):
    """
        A git repository
    """

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not(force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository %S" % path)

        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])

        else if not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(
                    "Unsupported repositoryformatversion %s" % vers)


def repo_path(repo, path):
    """ Compute path under repo gitdir """
    return os.path.join(repo.gitdir, *path)


def repo_file(repo, *path, mkdir=False):
    """ creates files like .git/refs/remotes/origin from  repo_file(r, \"refs\", \"remotes\", \"origin\", \"HEAD\")"""

    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)

def repo_dir(repo, *path, mkdir=False):
    """Same as repo_path, but mkdir *path if absent if mkdir."""
    path = repo_path(repo, *path)

    if os.path.exists(path):
        if (os.path.isdir(path)):
            return path
        else:
            raise Exception("Not a directory: %s" % path)

    if mkdir:
        os.makedirs(path)
        return path

    else:
        return None