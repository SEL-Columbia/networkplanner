"""
Classes for caching variables

!!! Add support for html_input property
!!! Add support for html_output property
"""
# Import system modules
import collections


# VariableStore

class VariableStore(object):
    'Hierarchical cache for variables'

    variableModules = None
    variableClasses = None
    aggregateClasses = None
    summaryClasses = None

    def __init__(self, valueByOptionBySection=None, variableStore=None, state=None):
        'Prepare cache and remember parent'
        # Initialize
        if not self.variableModules: 
            self.variableModules = []
        if not self.variableClasses: 
            self.variableClasses = []
        if not self.aggregateClasses: 
            self.aggregateClasses = []
        if not self.summaryClasses: 
            self.summaryClasses = []
        if not valueByOptionBySection: 
            valueByOptionBySection = {}
        self.variableStore = variableStore
        self.variableByClass = {}
        self.state = state
        # Populate variableClasses using variableModules
        for variableModule in self.variableModules:
            # For each class name in the module,
            for variableClassName in dir(variableModule):
                # Convert the class name into a class
                variableClass = getattr(variableModule, variableClassName)
                # If the class is a new variable,
                if isinstance(variableClass, type) and issubclass(variableClass, Variable) and variableClass != Variable and variableClass not in self.variableClasses:
                    # Append class
                    self.variableClasses.append(variableClass)
        # Make sure there are no name or alias overlaps
        validateVariableClasses(self.variableClasses + self.aggregateClasses + self.summaryClasses)
        # Prepare cache
        for variableClass in self.variableClasses:
            # Extract
            storeInCache, value = extractVariableValue(valueByOptionBySection, variableClass, variableStore)
            # If we need to store the variable in the cache,
            if storeInCache:
                # Store the variable by class in the cache
                self.set(variableClass, value)

    def set(self, variableClass, value=None):
        'Set the value of the variable corresponding to the given class'
        # Store the variable by class in the cache
        self.variableByClass[variableClass] = variableClass(self, value)

    def get(self, variableClass):
        return self.getVariable(variableClass).value

    def getVariable(self, variableClass):
        'Get the instance of the variable corresponding to the given class'
        # If the variable is in the cache,
        if variableClass in self.variableByClass:
            # Return the variable from the cache
            return self.variableByClass[variableClass]
        # If the variable has dependencies and any of the variable's 
        # dependencies are in the cache,
        if variableClass.dependencies and self.has(variableClass.dependencies):
            # Recompute the variable
            variable = variableClass(self)
        # If a parent is defined,
        elif self.variableStore:
            # Get the variable from the parent
            variable = self.variableStore.getVariable(variableClass)
        # Otherwise,
        else:
            raise VariableError('Unable to get ' + variableClass.__name__)
        # Store the variable in the cache
        self.variableByClass[variableClass] = variable
        # Return the variable
        return variable

    def getVariableByOptionBySection(self):
        'Return variables arranged by section'
        # Initialize
        variableByOptionBySection = {} 
        if self.variableStore:
            variableByOptionBySection = \
                self.variableStore.getVariableByOptionBySection()

        # For each variable in the cache,
        for x in self.variableByClass.values():
            # Update
            if x.section not in variableByOptionBySection:
                variableByOptionBySection[x.section] = {}
            variableByOptionBySection[x.section][x.option] = x
        # Return
        return variableByOptionBySection

    def getValueByOptionBySection(self):
        'Return variable values arranged by section'
        # Initialize
        valueByOptionBySection = {}
        # For each section,
        for section, variableByOption in self.getVariableByOptionBySection().iteritems():
            # For each option,
            for option, variable in variableByOption.iteritems():
                # Load methods
                format = variable.c['format'] if 'format' in variable.c else str
                # Update
                if section not in valueByOptionBySection:
                    valueByOptionBySection[section] = {}
                valueByOptionBySection[section][option] = format(variable.value)
        # Return
        return valueByOptionBySection

    def has(self, variableClasses):
        'Return true if any of the variables are in the cache'
        # For each variableClass,
        for variableClass in variableClasses:
            # If the variableClass is in the cache or any of its dependencies is in the cache,
            if variableClass in self.variableByClass or (variableClass.dependencies and self.has(variableClass.dependencies)):
                # Return true
                return True
        # Return false
        return False

    def initializeAggregates(self):
        # For each aggregateClass,
        for aggregateClass in self.aggregateClasses:
            # Set
            self.set(aggregateClass)

    def updateAggregates(self, childVS):
        # For each aggregateClass,
        for aggregateClass in self.aggregateClasses:
            # Aggregate
            self.getVariable(aggregateClass).aggregate(childVS)

    def processAggregates(self):
        # For each summaryClass,
        for summaryClass in self.summaryClasses:
            # Compute
            self.get(summaryClass)


# Variable

class Variable(object):
    'Encapsulated variable'

    section = ''
    option = ''
    aliases = None
    c = None
    default = None # Leave default=None if you want the value to be computed
    dependencies = None
    units = ''

    def __init__(self, variableStore, value=None):
        # Initialize
        if not self.aliases:
            self.aliases = []
        if not self.dependencies:
            self.dependencies = []
        if not self.c:
            self.c = {}
        if 'input' not in self.c:
            self.c['input'] = inputText
        if 'validate' not in self.c:
            self.c['validate'] = 'validateNumber'
        if 'parse' not in self.c:
            self.c['parse'] = float
        if 'format' not in self.c:
            self.c['format'] = str
        # Set aliases
        self.aliases = [x.lower() for x in self.aliases]
        # Store variableStore for future computation
        self.variableStore = variableStore
        self.state = variableStore.state
        # If we do not have a value,
        if value == None or value == '':
            # Compute the value if we do not have a default
            if self.default == None:
                self.value = self.compute()
            else:
                self.value = self.c['parse'](self.default)

        # If we have a value,
        else:
            # Parse the value
            self.value = self.c['parse'](value)
        # If a validation method exists,
        if 'check' in self.c:
            try:
                # Validate
                self.c['check'](self.value)
            # If the value does not validate,
            except AssertionError, error:
                # Raise error
                raise VariableError('"%s > %s" ' % (self.section, self.option) + str(error))

    def __str__(self):
        return '<Variable(section=%s, option=%s, value=%s)>' % (self.section, self.option, self.value)

    def get(self, variableClass):
        return self.variableStore.get(variableClass)

    def compute(self):
        'Compute the value of the variable; note that to have the value computed, you must leave default=None'
        return self.default


# Helpers

def buildSectionPacks(model):
    'Gather each section and its variables in order'
    # Grok model
    variables, roots = gatherVariables(model.VariableStore)
    variablesBySection = collections.defaultdict(list)
    derivativesByVariable = collections.defaultdict(list)
    for variable in sorted(variables, key=lambda x: x.__name__):
        variablesBySection[variable.section].append(variable)
        for dependency in variable.dependencies or []:
            derivativesByVariable[dependency].append(variable)
    # Make sure that all sections are represented
    assert set(variablesBySection) == set(model.sections)
    # Return
    return [(x, variablesBySection[x]) for x in model.sections], derivativesByVariable, roots

def gatherVariables(modelClass):
    """
    Gather variables from the model
    NOTE:  This depends on all variable's dependencies list being 
           accurate...otherwise, it will miss variables
    An alternative method to get all variables in a model is to
    get them via the __subclasses__ method of the Variable class, 
    though this may include classes not intended to be included in 
    the model.
    """
    # Initialize
    variableClasses = set()
    nextClasses = []
    if modelClass.variableClasses:
        nextClasses.extend(modelClass.variableClasses)
    if modelClass.aggregateClasses:
        nextClasses.extend(modelClass.aggregateClasses)
    if modelClass.summaryClasses:
        nextClasses.extend(modelClass.summaryClasses)
    rootClasses = set(nextClasses)
    # While there are more,
    while nextClasses:
        # Initialize
        variableClass = nextClasses.pop()
        variableClasses.add(variableClass)
        # If the variableClass has dependencies,
        if variableClass.dependencies:
            # Remove all dependencies from rootClasses
            rootClasses = rootClasses.difference(variableClass.dependencies)
            # Add dependencies
            variableClasses.update(variableClass.dependencies)
            # Append classes
            nextClasses.extend(variableClass.dependencies)
    # Return
    return variableClasses, rootClasses

def validateVariableClasses(variableClasses):
    'Make sure there are no name or alias overlaps'
    # Initialize
    variableClassByName = {}
    variableClassByAlias = {}
    # For each variableClass,
    for variableClass in variableClasses:
        # If section and option are not defined,
        if not variableClass.section or not variableClass.option:
            raise Exception('Empty variable name for class: %s' % variableClass)
        # Prepare variable name
        variableName = '%s > %s' % (variableClass.section, variableClass.option)
        if variableName in variableClassByName:
            raise Exception('Please fix duplicate variable name %s: %s %s' % (variableName, variableClassByName[variableName], variableClass))
        variableClassByName[variableName] = variableClass
        # For each variableAlias,
        for variableAlias in variableClass.aliases or []:
            if variableAlias in variableClassByAlias:
                raise Exception('Please fix duplicate variable alias: %s: %s %s' % (variableAlias, variableClassByAlias[variableAlias], variableClass))
            variableClassByAlias[variableAlias] = variableClass


def extractVariableValue(valueByOptionBySection, variableClass, variableStore):
    """
    Extract value corresponding to variableClass
    This is where the 'override' functionality is implemented...i.e.
    for each Variable, if the valueByOptionBySection (a dict) has a value
    either for the Variable's aliases OR the Variable's section/option, then
    use this for that Variable's value.
    """
    # For each alias,
    for variableAlias in variableClass.aliases or []:
        # If we find a matching alias,
        if variableAlias in valueByOptionBySection:
            # Get the associated value
            return True, valueByOptionBySection[variableAlias]
    # If we find a matching section and option,
    if variableClass.section in valueByOptionBySection and variableClass.option in valueByOptionBySection[variableClass.section]:
            # Get the associated value
        return True, valueByOptionBySection[variableClass.section][variableClass.option]
    # If we have a parent or a default value is not defined,
    if variableStore or variableClass.default == None:
        # Do not store the variable in the cache
        return False, None
    # If we cannot find a matching value, signal variableClass to use default value
    return True, None

#TODO:  Put this in a better spot?  
BASE_PATH = "np.lib.metric"

def getAlias(varClass):
    """
    Get alias as first item in list of aliases if there
    else just use option
    """
    if varClass.aliases != None and len(varClass.aliases) > 0:
        return varClass.aliases[0]
    else:
        return varClass.option.capitalize()

def getClassname(varClass):
    """
    Outputs classname minus BASE_PATH
    """
    moduleName = varClass.__module__.replace(BASE_PATH + ".", "")
    return "%s.%s" % (moduleName, varClass.__name__)
 
def getClassnameForId(varClass):
    """
    Outputs classname minus BASE_PATH with underscores over dots
    (since pydot does funky escaping of dots)
    """
    return getClassname(varClass).replace(".", "_") 

def getOption(varClass):
    return "%s\n%s" % (varClass.section, varClass.option)

def buildOrderedDependencies(varClass):
    """
    Output graph of dependencies in Breadth-First order
    Graph is represented as 
      [(Variable, [dependency,...]),...] 
    """

    classDependencies = []

    dependencyQueue = [varClass]
    visited = set()
    visited.add(varClass) #add root to visited set
    while len(dependencyQueue) > 0:
        vCls = dependencyQueue.pop()
        depList = [] #collect the dependencies
        # check if dependencies is None
        if vCls.dependencies != None:
            for cls in (dep for dep in vCls.dependencies if dep not in visited):
                # insert in front so list acts as queue
                dependencyQueue.insert(0, cls)
                visited.add(cls)
            depList = [dep for dep in vCls.dependencies if vCls.dependencies]

        classDependencies.append((vCls, depList))
    return classDependencies

def getRelatedVariables(varClass):
    """
    Get unique set of classes related to varClass through the dependency graph
    """

    variableGraph = buildOrderedDependencies(varClass)
    # use a list rep to maintain order
    variableSet = [varTuple[0] for varTuple in variableGraph]
    return variableSet

def getBaseVariables(modelModule): 
    """
    Get all variables depended on by the top-level variables referenced
    in the models variableClasses element.  This should restrict the
    set of vars to those NOT in the summary/aggregate category.
    """
    varSets = [set(getRelatedVariables(var)) for var in 
               modelModule.VariableStore.variableClasses]
    return reduce(lambda s1, s2: s1.union(s2), varSets)


#TODO:  Put these somewhere else?
HEADER_TYPE_SECTION_OPTION = 'section_option' # i.e. 'Finance > Time Horizon'
HEADER_TYPE_ALIAS          = 'alias' # The *first* item in the list of aliases for the variable

def getFieldNamesForHeaderPacks(modelClass, headerPacks, headerFieldNameType=HEADER_TYPE_SECTION_OPTION):
    """
    Given a list of section, option tuples (headerPacks), return a map of 
    section, option to corresponding name in the format specified by 
    headerFieldNameType.

    NOTE:  "headerPacks" (i.e. a list of section, option tuples) seem to be 
    the standard identification mechanism for metric model variables at this point.  
    This is why we use the section, option tuple to look up the variable class 
    definition in order to display via it's member variables.

    This function is not really required for HEADER_TYPE_SECTION_OPTION
    but, it keeps the header creation def in a single place.  
    """
    
    variableSet, roots = gatherVariables(modelClass.VariableStore)
    section_option_to_var = {(var.section, var.option): var for var in variableSet}


    # inner function for naming
    def get_field_name(section, option, headerFieldNameType):
        if section_option_to_var.get((section, option)):
            var = section_option_to_var[(section, option)]
            # handle short_name and alias options
            if (headerFieldNameType==HEADER_TYPE_ALIAS and 
                 var.aliases and len(var.aliases) > 0):
                return var.aliases[0] # simply the first alias of the variable

        # Handle the HEADER_TYPE_SECTION_OPTION case
        # This is the fallback case for any fieldName type
        if section: 
            return "%s > %s" % (section.capitalize(), option.capitalize())
        else:
            return option.capitalize()

    section_option_to_name = {}

    for section, option in headerPacks:
        section_option_to_name[(section, option)] = \
          get_field_name(section, option, headerFieldNameType)
            
    return section_option_to_name


# Key

separator = '00'

def formatKey(modelType, variable):
    'Return jQuery-compatible key'
    return ('%(modelType)s%(separator)s%(section)s%(separator)s%(option)s' % dict(modelType=modelType, section=variable.section, option=variable.option, separator=separator)).replace(' ', '11').replace('(', '22').replace(')', '33')

def parseKey(key):
    'Parse jQuery-compatible key'
    return [x.strip() for x in key.replace('11', ' ').replace('22', '(').replace('33', ')').split(separator)]



# Label

def formatLabel(x):
    'Return label whether we have an object or a class'
    return '%s-%s' % (x.__module__.lower().replace('.', '-'), getattr(x, '__name__', x.__class__.__name__).lower())


# Input

inputText = '<input id="${key}" name="${key}" class="value ${validate}" value="${value}">'
inputFile = """\
<input id="${key}_h" name="${key}_h" type=hidden value=${scenario.id if scenario else 0}>
<span id="${key}_on" style="color: gray" class=override>${scenario.name if scenario else ''}</span>
<input id="${key}" name="${key}" class="value upload" type=file>"""


# Error

class VariableError(Exception):
    pass
