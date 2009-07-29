import os
import pdb

DATA_PATH = 'download'

class Repo(object):
    """Represent a repo and how many follows it has"""
    
    def __init__(self, id, name, date, forked=None):
        self.id = id
        self.name = name
        self.date = date
        self.forked = forked
        self.follows = 0

    def __cmp__(self, repo):
        if self.follows < repo.follows:
            return -1
        elif self.follows > repo.follows:
            return 1
        else:
            return 0


class User(object):
    """Represents one user"""

    def __init__(self, id):
        self.id = id
        self.repos = []

    def __str__(self):
        str = self.id + ':'
        for repo in self.repos:
            str = str + repo.id + ','
        return str[0:-1]


class JohnnyReco(object):
    """The recomendation engine"""
    
    def __init__(self, data_file, lang_file, repo_file, user_file, output_file):
        self.data_file = data_file
        self.lang_file = lang_file
        self.repo_file = repo_file
        self.user_file = user_file
        self.output_file = output_file

    def run(self):
        """Read the input files and create an output file called results.txt"""
        repos = self._parse_repos()
        users = self._parse_users()
        self._parse_follow_data(repos)
        top_ten_repos = self._find_top_repos(repos, 10)
        self._assign_repos_to_users(users, top_ten_repos)
        self._write_results_file(users)

    def _assign_repos_to_users(self, users, repos):
        """For now naively assign the repos passed in to the user"""
        for user in users:
            user.repos = repos

    def _write_results_file(self, users):
        f = open(self.output_file, 'w')
        for user in users:
            f.write(str(user) + '\n')
        f.close()

    def _parse_repos(self):
        """Parses a file listing repo data"""
        repos = {}
        f = open(self.repo_file, 'r')
        for line in f:
            id, name, date, fork = self._split_line(line.strip())
            repos[id] = Repo(id, name, date, fork)
        f.close()
        return repos

    def _split_line(self, line):
        """Splits a line of the format id:name, date, fork where fork is optional"""
        tokens = line.split(':')
        id = tokens[0]
        data = tokens[1].split(',')
        name, date = data[0], data[1]
        forks = None
        if len(data) == 3:
            forks = data[2]
        return id, name, date, forks        

    def _find_top_repos(self, repos, number):
        vals = repos.values()
        vals.sort(reverse=True)
        return vals[0:number]

    def _parse_users(self):
        users = []
        f = open(self.user_file)
        for id in f:
            users.append(User(id.strip()))
        f.close()
        return users

    def _parse_follow_data(self, repos):
        f = open(self.data_file)
        for line in f:
            tokens = line.strip().split(':')
            user, repo = tokens[0], tokens[1]
            repos[repo].follows += 1
        f.close()

def file_location(filename):
    """Return the path of the file passed in based on the DATA_PATH"""
    return os.path.join(DATA_PATH, filename)

def main():
    data_file = file_location('data.txt')
    lang_file = file_location('lang.txt')
    repo_file = file_location('repos.txt')
    user_file = file_location('test.txt')
    output_file = 'results.txt'

    recommender = JohnnyReco(data_file,
                             lang_file,
                             repo_file,
                             user_file,
                             output_file)
    recommender.run()

if __name__ == '__main__':
    main()
        
