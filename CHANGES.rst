Products.MeetingPROVHainaut Changelog
=====================================

4.2.0 (2023-04-11)
------------------

- Completed `test_FinancesAdvicesWorkflow` to check that finances adviser
  may take over item.
  [gbastien]
- Fixed `test_pm_WFA_availableWFAdaptations`, take into account new WFA `transfered`.
  [gbastien]
- Fixed `setuphandlers._addDemoData`.
  [gbastien]
- Removed `collegeMeeting.transitionsForPresentingAnItem` from `import_data` as
  field `MeetingConfig.transitionsForPresentingAnItem` was removed.
  [gbastien]
- Use the `waiting_advices_given_and_signed_advices_required_to_validate` WF adaptation
  and added `testCustomWorkflows.test_ItemNotValidableWhenFinancesAdviceWFIncomplete`.
  [gbastien]
- Advices is no more using Plone versioning, removed `repositorytool.xml`
  from `default` profile (migration is managed by `Products.PloneMeeting`).
  [gbastien]
- Adapted `meetingadvicefinances` and `meetingadvicefinancescec` portal_types
  to use the `PMRichTextWidget` for extra field `accounting_commitment`.
  [gbastien]
- Adapted translation of advice field title that must now start with `title_`
  so it is displayed correctly when historized.
  [gbastien]
- Adapted code now that we use `imio.helpers.cache.get_plone_groups_for_user`
  instead `ToolPloneMeeting.get_plone_groups_for_user`.
  [gbastien]
- Adapted code regarding removal of `MeetingConfig.useGroupsAsCategories`.
  [gbastien]

4.2b6 (2022-04-28)
------------------

- Adapted `events.onAdviceAfterTransition`, do no more call
  `MeetingItem.update_local_roles` as it is done in PloneMeeting in
  `events.onAdviceTransition` now, just after call to `AdviceAfterTransitionEvent`.
  [gbastien]
- Fixed `zprovhainaut import_data`, was failing with demo data.
  [gbastien]

4.2b5 (2022-01-07)
------------------

- Fixed call to `ToolPloneMeeting.isManager`, pass no context when `realManagers=True`.
  [gbastien]

4.2b4 (2021-07-19)
------------------

- Added `testVotes.py` as it is launched now by `Products.MeetingCommunes`.
  [gbastien]
- Added `test_CompletenessEvaluationAskedAgain` that shows that completeness
  evaluation is asked correctly (test fixes in
  `Products.MeetingCommunes.adapters._will_ask_completeness_eval_again` and
  `Products.MeetingCommunes.adapters._doWaitAdvices`).
  [gbastien]
- Adapted code regardind fact that Meeting was moved from AT to DX.
  [gbastien]
- Removed `MeetingItem.groupedItemsNum` functionnality.
  [gbastien]
- Fixed code and POD templates, use `updatePODTemplatesCode` helper in migration to 4203 to fix POD templates code.
  [gbastien]

4.2b3 (2020-10-14)
------------------

- Added upgrade step to 4202 that will update `advice_type` of every finances advices.
  [gbastien]

4.2b2 (2020-10-02)
------------------

- In `CustomMeetingItem.getCustomAdviceMessageFor`, take into account new key `displayAdviceReviewState`,
  set it to True so advice review_state is shown to users that may not view the advice.
- Fixed `config.EXTRA_GROUP_SUFFIXES` regarding new key `fct_management` in `collective.contact.plonegroup`.
- Enable `MeetingItemPROVHainautWorkflowConditions._get_waiting_advices_icon_advisers` for every finances advisers.
- Configure `waiting_advices` WFAdaptation regarding changes in `Products.PloneMeeting`.

4.2b1 (2020-08-24)
------------------

- Added upgrade step to 4201 to move MeetingItem.motivation to MeetingItem.description

4.2a4 (2020-06-24)
------------------

- Fixed demo data as now MeetingItem.groupsInCharge can not be empty

4.2a3 (2020-04-02)
------------------

- Display also 'Can not add advice before item is complete' for DF 2. advice

4.2a2 (2020-02-21)
------------------

- Added import_meetingsUsersAndRoles_from_csv in Extensions.utils
- Removed override of meetingitem_view for now as it was only done to display field MeetingItem.groupedItemsNum that is not really used...

4.2a1 (2020-02-06)
------------------

- Display item completeness not evaluated advice custom message also when advice is asked again
- Use profile post_handler attribute to manage postInstall handler, removed use of import_steps.xml for every profiles
- Define 3 types of finances advice with separated workflows
- Removed overrides of meetingitem_view.pt/meetingitem_edit.pt, it was to include no more used MeetingItem.groupedItemsNum field
- Change colors to match visual identity of Province of Hainaut
- Fixed _adviceIsEditableByCurrentUser, check if item is_complete AND if user is able to edit the advice or edit.png icon appear
  even when user can not really edit the advice
- Override translations for wait_advices_from, MeetingItem.manuallyLinkedItems description and MeetingItem.preferredMeeting description
- Added specific logo.png
- Configure local roles for state 'proposed_to_financial_reviewer' in workflows meetingadvicefinanceseditor_workflow and meetingadvicefinancesmanager_workflow

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
