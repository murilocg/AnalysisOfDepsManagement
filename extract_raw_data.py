
import json
import subprocess
import os
import pandas as pd
import query_lib

def load_package(path):
    package = {}
    if os.path.exists(path):
        with open(path) as d:
            package = json.load(d)
    return package

def add_field(dep, version, client, is_dev_dep):
    return {
        'client': client,
        'is_dev_dep': is_dev_dep,
        'lib': dep,
        'version': version
    }

def load_deps(client, field, package):
    is_dev_dep = field == "devDependencies"
    if package.get(field) is not None:
        deps = package[field]
        return [add_field(k, deps[k], client, is_dev_dep) for k in deps]
    return []
        
def write_data(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)

def start(url, name):
    path = "workdir/repositories/" + name
    subprocess.call(['git', 'clone', url + ".git", path])
    package = load_package(path + "/package.json")
    deps = load_deps(name, 'dependencies', package)
    deps = deps + load_deps(name, 'devDependencies', package)

    if not os.path.exists('workdir/raw_data'):
        os.mkdir('workdir/raw_data')
    if not os.path.exists('workdir/raw_data/clients'):
        os.mkdir('workdir/raw_data/clients')
    if not os.path.exists('workdir/raw_data/libs'):
        os.mkdir('workdir/raw_data/libs')

    write_data('workdir/raw_data/clients/dependencies.csv', deps)

    all_versions = []
    libs = []
    for d in deps:
        lib, versions = query_lib.get_info_lib(d['lib'])
        all_versions = all_versions + versions
        libs.append(lib)

    write_data('workdir/raw_data/libs/info.csv', libs)
    write_data('workdir/raw_data/libs/versions.csv', all_versions)



    

start("https://github.com/murilocg/pectometro", "pectometro")