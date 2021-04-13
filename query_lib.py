import requests
import json
import urllib.parse


endpoint = "https://libraries.io/api/NPM/"

def get_info_lib(name):
  query = endpoint + urllib.parse.quote_plus(name) + "?api_key=<TOKEN>"
  request = requests.get(query, headers = {
      'Content-Type': 'application/json'
    })

  if  request.status_code == 200:
      return format_lib(request.json(), name)
  raise Exception("A query falhou: {}. {}".format(request.status_code, query))


def format_lib(data, name):
  lib =  {
    'dependent_repos_count': data['dependent_repos_count'],
    # 'dependents_count': data['dependents_counts'],
    'latest_release_number': data['latest_release_number'],
    'repository_url': data['repository_url'],
    'name': name
  }
  versions = [ format_version(x, name) for x in data['versions']]
  return lib, versions

def format_version(data, lib):
  return { 'number': data['number'], 'published_at': data['published_at'], 'lib': lib}