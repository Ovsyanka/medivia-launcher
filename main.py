import os
import platform
import shutil
import subprocess
from distutils.dir_util import copy_tree

import click
from pygit2 import Repository

import gitOperations

# TODO: make config sets for different platforms.

homePathEnvironName = getHomePathEnvironName()
homePath = os.environ[homePathEnvironName]

# settings
gameConfigPath = os.path.join(homePath, getGameConfigFolderName())
configsRootPath = os.path.join(homePath, '.medivia-launcher')
# override for development
# configsRootPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.medivia-launcher')
originConfigPath = os.path.join(configsRootPath, 'originConfig')
instanciesConfigPath = os.path.join(configsRootPath, 'instancies')
# configRepoSkeletonPath =

# TODO: make the command to print it
def version():
    print("0.0.2")

@click.command()
@click.option('--instance', default='instance1', help='Instance name.')
@click.option('--executable', default='medivia', help='Full path for medivia executable ("medivia" by default).')
# @click.argument('executable')
def launchMedivia(executable='medivia', instance=None):
    print(executable)
    print(instance)

    # if var1 is None:
    # var1 = 4
    # instance = 'test'
    currentHomePath = os.path.join(instanciesConfigPath, instance)
    pidFilePath = os.path.join(currentHomePath, 'pid')

    # ensure origin configs exists
    if not os.path.isdir(originConfigPath):
        createOrigin(gameConfigPath, originConfigPath)

    # ensure instance path exists
    if not os.path.isdir(currentHomePath):
        # os.mkdir(currentHomePath)
        createInstance(path=currentHomePath, originPath=originConfigPath)

    # TODO: create commit if any changes in the instance after the last commit

    # TODO: return error
    if os.path.isfile(pidFilePath):
        exit

    env = os.environ.copy()
    env[homePathEnvironName] = currentHomePath
    process = subprocess.Popen([executable], env=env)

    pid = process.pid

    pidFile = open(pidFilePath, "w")
    pidFile.write(str(pid))
    pidFile.close()

    process.communicate()

    os.remove(pidFilePath)

    print('commiting changes')

    # commiting any changes made
    instanceRepo = gitOperations.getRepo(currentHomePath)
    gitOperations.commitAll(instanceRepo)

    print('end')

def getHomePathEnvironName() -> str:
    """
    Returning crossplatform user home path environment variable name.
    
    Returns:
        str -- crossplatform user home path environment variable name.
    """
    
    # if HOMEPATH defined considering this is the Windows system
    if os.environ.get('HOMEPATH') is not None:
        return 'HOMEPATH'
    # else it is the linux or Mac
    else:
        return 'HOME'

def getGameConfigFolderName():
    if platform.system() is 'Windows':
        return 'medivia'
    else:
        return '.medivia'
    return 

# def onStart():
#     pass


def createInstance(path: str, originPath: str) -> None:
    """
    Creates new instance. Path should't be existed.

    originPath should be the path to the origin repository. It will be cloned to the path and saved as `origin` remote repo.
    The current commit will be `master` and the new local branch will be created: `instance/<name>`

    TODO: replace the `path` to the `name` or add the `name` parameter
    TODO: implement and return the Instance class?

    Arguments:
        path {str} -- instance path
        originPath {str} -- path to the origin repo
    """

    # можно перехватывать FileExistsError и выводить норм сообщение
    # if os.path.isdir(currentHomePath):
    # os.mkdir(path)

    instanceName = os.path.basename(os.path.normpath(path))

    # TODO: test if remote added
    print("cloning from " + originPath + " to " + path)
    repo = gitOperations.cloneOrigin(originPath, path)
    gitOperations.makeInstanceBranch(repo, instanceName)


def createOrigin(gameConfigsPath, targetPath):
    # copying all from configs from original game configs folder
    # shutil.copytree(gameConfigsPath, targetPath)
    # targetPath = os.path.relpath(targetPath)
    print("creating " + targetPath)
    os.makedirs(targetPath)
    
    copy_tree(gameConfigsPath, os.path.join(
        targetPath, getGameConfigFolderName()))

    gitignoreFile = open(os.path.join(targetPath, ".gitignore"), "w")
    gitignoreFile.write(".nv\n")
    gitignoreFile.write("pid\n")
    gitignoreFile.close()

    repo = gitOperations.initRepository(targetPath)
    gitOperations.commitAll(repo, 'initial copy of the settings directory')


if __name__ == '__main__':
    launchMedivia()
    # createOrigin(gameConfigPath, './tmpTest')
