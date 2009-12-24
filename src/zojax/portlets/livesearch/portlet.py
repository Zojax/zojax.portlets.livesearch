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
from zope import interface
from zope.component import queryUtility
from zope.app.component.hooks import getSite
from zojax.catalog.interfaces import ICatalog
from zojax.resourcepackage.library import include

from interfaces import ILiveSearchPortlet


class LiveSearchPortlet(object):
    interface.implements(ILiveSearchPortlet)

    def update(self):
        self.catalog = queryUtility(ICatalog)

        if self.catalog is not None:
            self.fti = self.catalog.getFTIndex()
        else:
            self.fti = None

        self.value = self.request.get(self.fti)
        self.portal = getSite()

        if self.fti is not None:
            include('zojax.portlets.livesearch')

    def isAvailable(self):
        return self.fti is not None
