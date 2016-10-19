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
        cmd.Cmd.__init__(self, *args, **kwargs)
        self.status = 'status'

        path = [os.path.expanduser('~'), self.status,
                '%s.yml' % self._get_next_monday().strftime("%B-%m-%d").lower()]
        self.file = '/'.join(path)

        if not os.path.exists(self.file):
            file(self.file, 'w').close()

        content = ''
        with open(self.file, 'r') as fobj:
            content = fobj.read()

        self._d = yaml.load(content) or []

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
        """
        Changes to the given project

        Usage: p <project_name> -- Sets context to the project, creates if not present
               p list -- Returns the list of project
        """
        if arg == 'list':
            if self.projects:
                for cnt, project in enumerate(self.projects):
                    print '{}. {}'.format(cnt, project)
            else:
                print 'No project yet'

            return

        if arg not in self.projects:
            self.projects.add(arg)
            self._cp = {
                'date': datetime.datetime.now().date(),
                'tasks': [],
                'project': arg
            }
            self._d.append(self._cp)
            self._save()
            return

        for item in self._d:
            if item['project'] == arg:
                self._cp = item
                self.task = self._cp['tasks']
                return

    def do_n(self, arg):
        if not arg and not len(self._cp['tasks']):
            print('No tasks yet. Create one using `n <task>`')
            return

        if arg == 'list':
            if not len(self._cp['tasks']):
                print('No tasks yet. Create one using `n <task>`')
                return
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
        self._save()

    def do_a(self, arg):
        self.task['annotations'].append(arg)
        self._save()

    def do_s(self, arg):
        self._save()

    def do_q(self, arg):
        self._save()
        sys.exit()

    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            self._save()
            self.cmdloop()

if __name__ == '__main__':
    TahShell().cmdloop()
