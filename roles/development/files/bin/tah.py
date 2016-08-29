#!/usr/bin/env python3.4

import cmd
import datetime
import os
import sys

import yaml


class TahShell(cmd.Cmd):
    intro = "Welcome to the TahShell. Type help or ? to list commands.\n"
    prompt = "(duh) "

    def __init__(self, *args, **kwargs):
        super(TahShell, self).__init__(*args, **kwargs)
        self.status = 'status'

        path = [os.path.expanduser('~'), self.status,
                '%s.yml' % self._get_next_monday().strftime("%B-%m-%d").lower()]
        self.file = '/'.join(path)

        content = ''
        with open(self.file, 'r') as fobj:
            content = fobj.read()

        self._d = yaml.load(content)

        self.projects = self._get_projects()

    def _get_next_monday(self, *args, **kwargs):
        today = datetime.date.today()
        return today + datetime.timedelta(days=-today.weekday(), weeks=1)

    def _get_projects(self):
        tdate = datetime.datetime.now().date()
        projects = set([])

        for item in self._d:
            if item['date'] == tdate:
                projects.add(item['project'])

        return projects

    def _save(self):
        content = yaml.dump(self._d)
        with open(self.file, 'w') as fobj:
            fobj.write(content)

    def do_p(self, arg):
        if arg not in self.projects:
            self.projects.add(arg)
            self._cp = {
                'date': datetime.datetime.now().date(),
                'tasks': [],
                'project': arg
            }

        for item in self._d:
            if item['project'] == arg:
                self._cp = item
                self.task = self._cp['tasks'][0]
                return


    def do_n(self, arg):
        if not arg:
            for count, item in enumerate(self._cp['tasks']):
                print(count, item['task'])
            ip = int(input('Select task: '))
            self.task = self._cp['tasks'][ip-1]
            return

        for item in self._cp['tasks']:
            if item['task'] == arg:
                self.task = item
                return

        self.task = [{
            'task': arg,
            'annotations': []
        }]
        self._cp['tasks'].extend(self.task)

    def do_a(self, arg):
        self.task[0]['annotations'].append(arg)

    def do_s(self, arg):
        self._save()

    def do_q(self, arg):
        self._save()
        sys.exit()

    def do_ipdb(self, arg):
        from ipdb import set_trace;set_trace()

    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt as e:
            self._save()
            self.cmdloop()

if __name__ == '__main__':
    TahShell().cmdloop()
