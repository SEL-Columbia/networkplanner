"""
Define command-line wrappers
"""
# Import context modules
import os; basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys; sys.path.append(basePath)
# Import system modules
import optparse


def connect():
    'Connects the script to a database'
    # Import system modules
    import ConfigParser
    import sqlalchemy as sa
    # Import custom modules
    from np import model
    # Parse options and arguments
    optionParser = optparse.OptionParser()
    optionParser.add_option('-c', '--configurationPath', dest='configurationPath', 
        default=os.path.join(basePath, 'development.ini'), metavar='PATH', 
        help='use specified configuration file')
    options, arguments = optionParser.parse_args()
    # Load configuration
    configuration = ConfigParser.ConfigParser({'here': basePath})
    configuration.read(options.configurationPath)
    # Initialize model
    model.init_model(sa.create_engine(configuration.get('app:main', 'sqlalchemy.url')))
    # Return
    return configuration


def run(step, scriptPath, convertByName):
    'Runs the script on a configuration file'
    # Import custom modules
    from np.lib import store, folder_store
    # Parse options and arguments
    optionParser = optparse.OptionParser(usage='%prog QUEUE-PATH')
    optionParser.add_option('-t', '--test', dest='isTest', 
        default=False, action='store_true', 
        help='test your QUEUE-PATH')
    optionParser.add_option('-d', '--directory', dest='directory', 
        default='.', metavar='DIRECTORY', 
        help='save results in DIRECTORY')
    options, arguments = optionParser.parse_args()
    if len(arguments) != 1:
        return optionParser.print_help()
    filePath = arguments[0]
    # Go
    try: 
        # Load information
        parameterByNameByTask = store.loadQueue(filePath, convertByName)
        # Initialize
        if options.isTest: 
            options.directory = store.makeFolderSafely(os.path.join(options.directory, 'test'))
        folderStore = folder_store.Store(options.directory)
        # Step through each task
        for taskName, parameterByName in parameterByNameByTask.iteritems():
            step(taskName, parameterByName, folderStore, options.isTest)
    except (store.StoreError, folder_store.FolderError, ScriptError), error:
        print '%s %s\n%s' % (store.extractFileBaseName(scriptPath), filePath, error)


class ScriptError(Exception):
    'Generic exception for script-related errors'
    pass
