from todos.views import *
from django.urls import path

urlpatterns = ([
    path('list/', list_todos, name='list_todos'),
    path('item/', detailed_todo, name='item'),
    path('item/<int:id>', detailed_todo, name='item'),
    path('delete/', delete_todo, name='delete'),
    path('delete/<int:id>', delete_todo, name='delete'),
    path('markascompleted/', make_as_completed, name='mark_as_complete'),
    path('markascompleted/<int:id>', make_as_completed, name='mark_as_complete'),
    path('completed/', list_completed_todos, name='completed'),
    # path('completed/<int:id>', completed_todos, name='completed'),
    path('uncompleted/', un_complete_todos, name='un_complete'),
    path('uncompleted/<int:id>', un_complete_todos, name='un_complete'),
    path('add/', add_todo, name='add'),

    path('ordering/', order_it_by, name='order_it_by'),
    path('reverse_order/', reverse_the_order, name='reverse_the_order'),
])
