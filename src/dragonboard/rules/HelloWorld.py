from durable.lang import *

with ruleset('test'):
    # antecedent
    @when_all(m.subject == 'World')
    def say_hello(c):
        # consequent
        print('Hello {0}'.format(c.m.subject))

    # on ruleset start
    @when_start
    def start(host):    
        host.post('test', { 'subject': 'World' })

run_all()