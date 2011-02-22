'Generate documentation'
# Import system modules
import os
import re
import inspect
import collections
# Import custom modules
import script_process
from np.lib import metric, network, variable_store


# Set constants

pattern_uppercase = re.compile(r'([A-Z])')

def formatModuleName(moduleName):
    moduleName = moduleName.replace(metricModelName, '')
    return moduleName[1:] if moduleName.startswith('.') else moduleName

def formatHeader(text, separator, link=''):
    parts = []
    if link:
        parts.append('.. _%s:\n' % link)
    parts.append(text)
    parts.append(separator * len(text))
    return '\n'.join(parts) + '\n'

def formatTable(columns, rows):
    # Prepare boundary
    columnLengths = [max(len(x[columnIndex]) for x in [columns] + rows) for columnIndex in xrange(len(columns))]
    boundary = ' '.join('=' * x for x in columnLengths)
    # Build
    parts = []
    parts.append(boundary)
    parts.append(' '.join(('%%-%ss' % columnLength) % column for column, columnLength in zip(columns, columnLengths)))
    parts.append(boundary)
    for row in rows:
        parts.append(' '.join(('%%-%ss' % columnLength) % column for column, columnLength in zip(row, columnLengths)))
    parts.append(boundary)
    # Return
    return '\n'.join(parts)

def unCamel(x):
    return pattern_uppercase.sub(r' \1', x).strip()

def generateDocumentation(modelModule):
    # Initialize
    lines, rows = [], []
    # Extract
    sectionPacks, derivativesByVariable, roots = variable_store.buildSectionPacks(modelModule)
    # For each section in order,
    for section, variables in sectionPacks:
        # Prepare header for module 
        lines.append(formatHeader(section.capitalize(), '-'))
        # For each variable sorted by name,
        for variable in sorted(variables, key=lambda x: x.__name__):
            # Write header for variable
            lines.append(formatHeader(unCamel(variable.__name__).capitalize(), '^', variable_store.formatLabel(variable)))
            # Write dependencies
            if variable.dependencies:
                lines.append('Dependencies\n')
                lines.extend('- :ref:`%s > %s <%s>`\n' % (x.section, x.option, variable_store.formatLabel(x)) for x in variable.dependencies)
            # Write derivatives
            if variable in derivativesByVariable:
                lines.append('Derivatives\n')
                lines.extend('- :ref:`%s > %s <%s>`\n' % (x.section, x.option, variable_store.formatLabel(x)) for x in derivativesByVariable[variable])
            # Output code
            lines.append('\n::\n\n%s\n\n\n' % '\n'.join('    ' + x for x in inspect.getsource(variable).splitlines()))
        # For each variable sorted by option,
        for variable in sorted(variables, key=lambda x: x.option):
            # Append long alias, short alias, units
            rows.append((':ref:`%s > %s <%s>`' % (variable.section, variable.option, variable_store.formatLabel(variable)), ' '.join(variable.aliases or []), variable.units))
    # Return
    return roots, lines, rows


# If we are running the script from the command-line,
if __name__ == '__main__':
    # For each metric model,
    for metricModelName in metric.getModelNames():
        # Load metric model
        metricModel = metric.getModel(metricModelName)
        metricRoots, metricLines, metricRows = generateDocumentation(metricModel)
        # Save and close
        referenceFile = open(os.path.join(script_process.basePath, 'docs/metric-%s.rst' % metricModelName), 'wt')
        referenceFile.write(formatHeader('Metric Model %s' % metricModelName, '='))
        for root in sorted(metricRoots, key=lambda x: metricModel.roots.index(x)):
            referenceFile.write('- :ref:`%s`\n' % variable_store.formatLabel(root))
        referenceFile.write('\n\n' + 'You can override the value of any variable in the model on a node-by-node basis.  To perform a node-level override, use the aliases in the following table as additional columns in your spreadsheet or fields in your shapefile.  Both long and short aliases are recognized.')
        referenceFile.write('\n\n' + formatTable(['Long alias', 'Short alias', 'Units'], metricRows))
        referenceFile.write('\n\n' + '\n'.join(metricLines))
        referenceFile.close()
    # For each network model,
    for networkModelName in network.getModelNames():
        # Load network model
        networkModel = network.getModel(networkModelName)
        networkRoots, networkLines, networkRows = generateDocumentation(networkModel)
        # Save and close
        referenceFile = open(os.path.join(script_process.basePath, 'docs/network-%s.rst' % networkModelName), 'wt')
        referenceFile.write(formatHeader('Network Model %s' % networkModelName, '='))
        for root in sorted(networkRoots, key=lambda x: networkModel.roots.index(x)):
            referenceFile.write('- :ref:`%s`\n' % variable_store.formatLabel(root))
        referenceFile.write('\n\n' + '\n'.join(networkLines))
        referenceFile.close()
