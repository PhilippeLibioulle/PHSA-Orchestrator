from durable.lang import *

with ruleset('flow'):
    # state condition uses 's'
    @when_all(s.status == 'start')
    def start(c):
        # state update on 's'
        c.s.status = 'next' 
        print('start')

    @when_all(s.status == 'next')
    def next(c):
        c.s.status = 'last' 
        print('next')

    @when_all(s.status == 'last')
    def last(c):
        c.s.status = 'end' 
        print('last')
        # deletes state at the end
        c.delete_state()

    @when_start
    def on_start(host):
        # modifies context state
        host.patch_state('flow', { 'status': 'start' })

run_all()
