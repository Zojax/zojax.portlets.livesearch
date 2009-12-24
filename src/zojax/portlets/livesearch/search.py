##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from simplejson import JSONEncoder
from zope.component import queryUtility, queryMultiAdapter
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import ICMFDublinCore

from zojax.catalog.interfaces import ICatalog
from zojax.content.type.interfaces import IItem
from zojax.ownership.interfaces import IOwnership
from zojax.formatter.utils import getFormatter

from interfaces import _


encoder = JSONEncoder()


class Search(object):

    def __call__(self):
        request = self.request
        callback = request.get('callback', 'stcCallback1001') + '(%s)'

        try:
            start = int(request.form.get('start', 0))
            limit = int(request.form.get('limit', 10))
            query = request.form.get('query', u'')
        except:
            return callback%encoder.encode({'result': [], 'totalCount': 0})

        catalog = queryUtility(ICatalog)
        if catalog is not None:
            fti = catalog.getFTIndex()
            if fti is None:
                return callback%encoder.encode({'result': [], 'totalCount': 0})

            result = catalog.searchResults(
                **{'searchContext': (getSite(),),
                   str(fti):  {'any_of': (query,)}})
            formatter = getFormatter(request, 'fancyDatetime', 'medium')

            data = []
            for idx in range(start, start+limit):
                item = result.get(idx)
                if item is None:
                    break

                info = {'id': str(idx),
                        'url': '%s/'%absoluteURL(item, request)}

                it = IItem(item, None)
                if it is not None:
                    info['title'] = it.title
                    info['description'] = it.description
                else:
                    info['title'] = unicode(getattr(item, 'title', item.__name__))
                    info['description'] = u''

                if not info['description']:
                    info['description'] = _('empty description')

                icon = queryMultiAdapter((item, request), name='zmi_icon')
                if icon is not None:
                    info['icon'] = icon()
                else:
                    info['icon'] = ''

                dc = ICMFDublinCore(item)
                info['modified'] = formatter.format(dc.modified)

                owner = IOwnership(item).owner
                try:
                    info['owner'] = owner.title
                except:
                    info['owner'] = owner

                data.append(info)

            return callback%encoder.encode({'result': data, 'totalCount': len(result)})

        return callback%encoder.encode({'result': [], 'totalCount':0})
