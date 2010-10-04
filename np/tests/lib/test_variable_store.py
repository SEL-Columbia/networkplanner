'Make sure that we can cache variables properly'
# Import system modules
import unittest
# Import custom modules
from np.lib import variable_store


class TestVariableStore(unittest.TestCase):

    def testInitializingWithoutArgumentsShouldLoadDefaults(self):
        variableStore = VariableStore()
        self.assertEqual(variableStore.get(SimpleVariable), SimpleVariable.default)
        self.assertEqual(variableStore.get(ComplexVariable), SimpleVariable.default * 2)

    def testInitializingWithValueByOptionBySectionShouldLoadDefaultsForOtherValues(self):
        variableStore = VariableStore({'complex': {'variable': '5'}})
        self.assertEqual(variableStore.get(SimpleVariable), SimpleVariable.default)
        self.assertEqual(variableStore.get(ComplexVariable), 5)

    def testInitializingWithParentShouldEnableChildLevelOverrides(self):
        parentStore = VariableStore({'simple': {'variable': '10'}})
        childStore = VariableStore({'simple': {'variable': '3'}}, parentStore)
        self.assertEqual(parentStore.get(SimpleVariable), 10)
        self.assertEqual(parentStore.get(ComplexVariable), 20)
        self.assertEqual(childStore.get(SimpleVariable), 3)
        self.assertEqual(childStore.get(ComplexVariable), 6)

    def testOverridingDependenciesTriggersRecomputation(self):
        parentStore = VariableStore({'complex': {'variable': '20'}})
        childStore = VariableStore({'simple': {'variable': '4'}}, parentStore)
        self.assertEqual(parentStore.get(SimpleVariable), SimpleVariable.default)
        self.assertEqual(parentStore.get(ComplexVariable), 20)
        self.assertEqual(parentStore.get(NestedVariable), 400)
        self.assertEqual(childStore.get(SimpleVariable), 4)
        self.assertEqual(childStore.get(ComplexVariable), 8)
        self.assertEqual(childStore.get(NestedVariable), 64)

    def testGettingVariableTwiceReturnsSameObject(self):
        parentStore = VariableStore()
        c1 = id(parentStore.get(ComplexVariable))
        c2 = id(parentStore.get(ComplexVariable))
        self.assertEqual(c1, c2)

    def testGettingVariableFromChildWithoutOverrideReturnsSameObject(self):
        parentStore = VariableStore()
        c1 = id(parentStore.get(ComplexVariable))
        childStore = VariableStore(variableStore=parentStore)
        c3 = id(childStore.get(ComplexVariable))
        self.assertEqual(c1, c3)

    def testGettingVariableFromChildWithOverrideReturnsDifferentObject(self):
        parentStore = VariableStore()
        c1 = id(parentStore.get(ComplexVariable))
        childStore = VariableStore({'simple': {'variable': '4'}}, parentStore)
        c4 = id(childStore.get(ComplexVariable))
        self.assertNotEqual(c1, c4)


class SimpleVariable(variable_store.Variable):

    section = 'simple'
    option = 'variable'
    c = dict(parse=int)
    default = 2


class ComplexVariable(variable_store.Variable):

    section = 'complex'
    option = 'variable'
    c = dict(parse=int)
    dependencies = [
        SimpleVariable,
    ]

    def compute(self):
        return self.get(SimpleVariable) * 2


class NestedVariable(variable_store.Variable):

    section = 'nested'
    option = 'variable'
    c = dict(parse=int)
    dependencies = [
        ComplexVariable,
    ]

    def compute(self):
        return self.get(ComplexVariable) ** 2


class VariableStore(variable_store.VariableStore):
    
    variableClasses = [
        SimpleVariable,
        ComplexVariable,
        NestedVariable,
    ]
