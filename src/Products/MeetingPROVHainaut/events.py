# -*- coding: utf-8 -*-

from Products.MeetingPROVHainaut.utils import finance_group_uid


def onAdviceAfterTransition(advice, event):
    '''Called whenever a transition has been fired on an advice.'''
    # pass if we are pasting items as advices are not kept
    if advice != event.object or advice.REQUEST.get('currentlyPastingItems', False):
        return

    # manage finance workflow, just consider relevant transitions
    # if it is not a finance wf transition, return
    finance_group = finance_group_uid()
    if advice.advice_group != finance_group:
        return

    item = advice.getParentNode()
    oldStateId = event.old_state.id
    newStateId = event.new_state.id

    # initial_state or going back from 'advice_given', we set automatically
    # advice_hide_during_redaction to True
    if not event.transition or \
       (newStateId == 'advicecreated' and oldStateId == 'advice_given'):
        advice.advice_hide_during_redaction = True

    if newStateId == 'financial_advice_signed':
        # final state of the wf, make sure advice is no more hidden during redaction
        advice.advice_hide_during_redaction = False

    # in some corner case, we could be here and we are actually already updating advices,
    # this is the case if we validate an item and it triggers the fact that advice delay is exceeded
    # this should never be the case as advice delay should have been updated during nightly cron...
    # but if we are in a '_updateAdvices', do not _updateAdvices again...
    # also bypass if we are creating the advice as onAdviceAdded is called after onAdviceTransition
    if event.transition and not item.REQUEST.get('currentlyUpdatingAdvice', False):
        item.updateLocalRoles()


def onItemLocalRolesUpdated(item, event):
    """Called after localRoles have been updated on the item.
       Update local_roles regarding :
       - finances adviser able to change item's state."""
    pass
