Products.MeetingPROVHainaut Changelog
=====================================

4.1rc2 (2019-07-02)
-------------------

- Use already existing Products.MeetingCommunes.config.FINANCE_WAITING_ADVICES_STATES constant to manage item states
  in which the finances advice may be given instead new constant FINANCE_GIVEABLE_ADVICE_STATES
- Override adaptable method MeetingItem._adviceIsAddable to only return True if item _is_complete, this way the
  'searchitemstocontrolcompletenessof' faceted search is working
- Only set completeness to 'completeness_evaluation_asked_again' when advice coming from 'advice_given' to 'advicecreated'
- Fix meetingitem_view when displaying MeetingItem.category
- Set meetingadvicefinances.advice_accounting_commitment to required=False
- Import FINANCE_WAITING_ADVICES_STATES only when about to use it, as it is monkeypatched from Products.MeetingCommunes.config

4.1rc1 (2019-06-28)
-------------------
- Manage zprovhainaut install profile
- Create and configure finances and compta advices
- Adapt comptabilite Workflow to remove relevant states
- Override MeetingItem.mayEvaluateCompleteness as only finances/comptabilite precontrollers may evaluate it
- Added new field for grouped items on a slip number
- When item sent to finances again, set completeness to 'completeness_evaluation_asked_again' automatically
- Adapted profile to have sample associatedGroups and groupsInCharge

4.0 (2018-10-25)
----------------
- Create Addon for Province of Hainaut
- New translations
