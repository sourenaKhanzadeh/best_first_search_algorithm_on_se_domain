import requests
import os
import sys
import zipfile


class GithubScraper:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.repos = []
    
    def scrape(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            print("Successfully scraped")
            self.repos = response.json()
        else:
            print("Failed to scrape")
    
    def print_repos(self):
        for repo in self.repos:
            print(repo['name'])
    
    def check_if_repo_language_is_java(self, repo):
        return repo['language'] == 'Java'
    
    def get_java_repos(self):
        java_repos = []
        for repo in self.repos:
            if self.check_if_repo_language_is_java(repo):
                java_repos.append(repo)
        return java_repos
    
    def download_java_repos(self):
        java_repos = self.get_java_repos()
        for repo in java_repos:
            print(f"Downloading {repo['name']}")
            response = requests.get(repo['clone_url'])
            if response.status_code == 200:
                # clone the repo in data folder
                # create a folder for the repo
                repo_folder = os.path.join('data', repo['name'])
                if not os.path.exists(repo_folder):
                    os.makedirs(repo_folder)
                
                # clone the repo
                os.system(f"git clone {repo['clone_url']} {repo_folder}")
                # move folder to data
                os.system(f"mv {repo['name']} {repo_folder}")

                           
                print(f"Successfully downloaded {repo['name']}")
            else:
                print(f"Failed to download {repo['name']}")



if __name__ == "__main__":
    scraper = GithubScraper("sourenakhanzadeh", "https://api.github.com/users/sourenakhanzadeh/repos")
    scraper.scrape()
    # scraper.print_repos()
    java_repos = scraper.get_java_repos()
    scraper.download_java_repos()