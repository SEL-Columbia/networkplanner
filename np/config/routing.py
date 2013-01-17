'URL configuration'
# Import pylons modules
from routes import Mapper

def make_map(config):
    'Create, configure and return the routes mapper'
    # Initialize map
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.minimization = False
    map.explicit = False
    # Remove trailing slash
    map.redirect('/{controller}/', '/{controller}')
    # Map errors
    map.connect('/errors/{action}', controller='errors')
    map.connect('/errors/{action}/{id}', controller='errors')
    # Map landing
    map.connect('landing_index', '/', controller='landing', action='index')
    # Map people
    map.connect('person_index', '/people', controller='people', action='index')
    map.connect('person_register', '/people/register', controller='people', action='register')
    map.connect('person_register_', '/people/register_', controller='people', action='register_')
    map.connect('person_confirm', '/people/confirm/{ticket}', controller='people', action='confirm')
    map.connect('person_login', '/people/login/{targetURL}', controller='people', action='login')
    map.connect('person_login_plain', '/people/login', controller='people', action='login')
    map.connect('person_login_', '/people/login_', controller='people', action='login_')
    map.connect('person_update', '/people/update', controller='people', action='update')
    map.connect('person_update_', '/people/update_', controller='people', action='update_')
    map.connect('person_logout_plain', '/people/logout', controller='people', action='logout') 
    map.connect('person_logout', '/people/logout/{targetURL}', controller='people', action='logout')
    map.connect('person_reset', '/people/reset', controller='people', action='reset')
    # Map scenarios
    map.connect('scenario_index', '/scenarios', controller='scenarios', action='index', 
            conditions=dict(method=['GET']))
    map.connect('scenario_create', '/scenarios', controller='scenarios', action='create', 
            conditions=dict(method=['POST']))
    map.connect('scenario_feedback', '/feedback', controller='scenarios', action='feedback')
    map.connect('scenario_check', '/scenarios/{scenarioID}/check', controller='scenarios', action='check')
    map.connect('scenario_clone', '/scenarios/{scenarioID}/clone', controller='scenarios', action='clone')
    map.resource('scenario', 'scenarios')
    # Map processors
    map.connect('processor_index', '/processors', controller='processors', action='index')
    map.connect('processor_update', '/processors/update', controller='processors', action='update')
    # Map jobs
    map.connect('job_index', '/jobs', controller='jobs', action='index')
    map.connect('job_log', '/jobs/{jobID}_{host}/log', controller='jobs', action='log')
    map.connect('job_show', '/jobs/{jobID}_{host}', controller='jobs', action='show')
    map.connect('job_kill', '/jobs/{jobID}_{host}/kill', controller='jobs', action='kill')
    # Return
    return map
