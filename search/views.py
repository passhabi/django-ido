from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ido.helpers.filterhelper import FilterHelper


@login_required
def search(request, title_quest=None):
    if not title_quest:
        return redirect("homepage")

    filter_hlp = FilterHelper(request.user, title_quest)
    config_dict = request.GET

    if config_dict:  # if it is not the first time asked for the query:
        filter_hlp.set_filters(config_dict)

    # print('\33[32m', hex(id(filter_hlp)), '\33[0m')
    return render(request, 'search.html',
                  context={'searched_query': filter_hlp.title_quest,
                           'query_result': filter_hlp.get_queryset(),
                           'filter_config': filter_hlp.get_filter_config()})
