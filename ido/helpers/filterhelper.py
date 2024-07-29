from todos.models import Todolist


class FilterHelper:

    def __init__(self, user, title_quest):

        self._title_quest = title_quest
        self._user = user
        self.query_set: Todolist

        #  resetting the search page:
        self.set_filters(config_dict={
            # html request.GET:
            'completed': True,
            'un_completed': True,
            'p1': True,
            'p2': True,
            'p3': True,
            'p4': True,
        })

        self.completed = True
        self.un_completed = True
        self.priority1 = True
        self.priority2 = True
        self.priority3 = True
        self.priority4 = True

    def get_queryset(self):
        return list(self.query_set)

    @property
    def title_quest(self):
        return self._title_quest

    def get_filter_config(self):
        return {
            'completed': self.completed and 'checked',
            'un_completed': self.un_completed and 'checked',
            'priority1': self.priority1 and 'checked',
            'priority2': self.priority2 and 'checked',
            'priority3': self.priority3 and 'checked',
            'priority4': self.priority4 and 'checked',
        }

    def set_complete_and_un_completed(self, completed, un_completed):
        if completed and un_completed:
            self.completed = True
            self.un_completed = True

        if not completed and not un_completed:
            self.completed = False
            self.un_completed = False
            self.query_set = self.query_set.filter(completion_time__isnull=False).filter(completion_time__isnull=True)
            # returns none

        if completed and not un_completed:
            self.completed = True
            self.un_completed = False
            self.query_set = self.query_set.filter(completion_time__isnull=False)  # show completed todos

        if not completed and un_completed:
            self.completed = False
            self.un_completed = True
            self.query_set = self.query_set.filter(completion_time__isnull=True)  # show un_completed todos

    def set_priorities(self, p1, p2, p3, p4):
        # set priorities with True and False of the template:
        self.priority1 = bool(p1)
        self.priority2 = bool(p2)
        self.priority3 = bool(p3)
        self.priority4 = bool(p4)

        # list priorites that should been in the query:
        enum_priorities = zip(range(1, 5), [p1, p2, p3, p4])

        priorities = [i for i, p in enum_priorities if p]  # [1, 2, 3, 4]

        self.query_set = self.query_set.filter(priority__in=priorities)

    def set_filters(self, config_dict):

        # reset the query_set:
        self.query_set = Todolist.objects.filter(title__icontains=self._title_quest, user=self._user)

        # status:
        self.set_complete_and_un_completed(config_dict.get('completed'), config_dict.get('un_completed'))

        # priority:
        self.set_priorities(
            config_dict.get('p1'),
            config_dict.get('p2'),
            config_dict.get('p3'),
            config_dict.get('p4')
        )

        # date:
