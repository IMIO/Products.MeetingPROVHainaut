# -*- coding: utf-8 -*-
from imio.history.interfaces import IImioHistory
from plone import api
from zope.component import getAdapter
from zope.i18n import translate

from Products.MeetingCommunes.browser.overrides import MCFolderDocumentGenerationHelperView


class MPHFolderDocumentGenerationHelperView(MCFolderDocumentGenerationHelperView):

    def _get_given_advice_histories(self, advice):
        """Get the given advice histories of an item."""
        if not advice:
            return []
        histories = list(getAdapter(advice, IImioHistory, "advice_given").getHistory())
        # older histories first
        histories.reverse()
        return histories

    def _format_date(self, dt, fmt="%d/%m/%Y %H:%M"):
        """Format a datetime object, return empty string if None."""
        return dt.strftime(fmt) if dt else ""

    def _format_history_entries(self, entries, domain="PloneMeeting"):
        """Format history entries."""
        return u"".join(
            u"{0}: {1} - {2}\n".format(
                translate(entry["action"], domain=domain, context=self.context.REQUEST).replace("None", u"En création"),
                entry["actor"],
                self._format_date(entry["time"]),
            )
            for entry in entries
        )

    def get_finance_advices_stats(self, brains, finance_advice_ids=[]):
        """
        Print a list of all the items with a finance advice asked on it
        with additional information related to the advice, like completeness history, wf history, etc.
        """
        results = []
        tool = api.portal.get_tool("portal_plonemeeting")
        cfg = tool.getMeetingConfig(self.context)
        if not finance_advice_ids:
            finance_advice_ids = cfg.adapted().getUsedFinanceGroupIds()
        for brain in brains:
            item = brain.getObject()
            advices = item.getAdviceDataFor(item)
            fin_advice_ids = set(finance_advice_ids).intersection(set(advices.keys()))
            if not fin_advice_ids:
                continue
            fin_advice_id = next(iter(fin_advice_ids))
            advice_infos = advices[fin_advice_id]
            given_advice = advice_infos["given_advice"]
            item_wf_history = getAdapter(item, IImioHistory, "workflow").getHistory()
            advice_histories = self._get_given_advice_histories(given_advice)
            # Get filtered waiting_advices_* item workflow history
            filtered_item_history = list(
                filter(lambda x: x["action"] and "wait_advices_" in x["action"], item_wf_history)
            )
            filtered_item_history.sort(key=lambda x: x["time"], reverse=True)
            completeness = translate(item.getCompleteness(), domain="PloneMeeting", context=self.context.REQUEST)
            completeness_history = None
            completeness_first_date = ""
            completeness_last_date = ""
            formatted_completeness_history = ""
            incompleteness_count = 0
            formatted_workflow_history = ""
            if given_advice:
                completeness_history = item.completeness_changes_history
                formatted_completeness_history = self._format_history_entries(completeness_history)
                complete_times = sorted([c["time"] for c in completeness_history if c["action"] == "completeness_complete"])
                if complete_times:
                    completeness_first_date = self._format_date(complete_times[0])
                    completeness_last_date = self._format_date(complete_times[-1])
                incompleteness_count = len(
                    list(filter(lambda x: x["action"] and "incomplete" in x["action"], item.completeness_changes_history))
                )

                advice_wf_history = getAdapter(given_advice, IImioHistory, "workflow").getHistory()
                formatted_workflow_history = self._format_history_entries(advice_wf_history, domain="plone")

            base_row = {
                "item": item,
                "given_advice": given_advice,
                "title": item.Title(),
                "group": item.getProposingGroup(theObject=True).Title(),
                "meeting_date": self._format_date(item.getMeeting().date) if item.hasMeeting() else "",
                "adviser": advice_infos["name"],
                "completeness": completeness,
                "completeness_history": completeness_history,
                "completeness_first_date": completeness_first_date,
                "completeness_last_date": completeness_last_date,
                "formatted_completeness_history": formatted_completeness_history,
                "incompleteness_count": incompleteness_count,
                "formatted_workflow_history": formatted_workflow_history,
            }
            results.append(dict(base_row, **{
                "reception_date": self._format_date(item_wf_history[0]["time"]) if item_wf_history else "",
                "advice_date": self._format_date(advice_infos.get("advice_given_on")),
                "end_advice": "OUI" if advice_infos.get("advice_given_on") else "-",
                "advice_type": advice_infos["type_translated"],
                "comments": advice_infos["comment"],
            }))
            if not advice_histories or len(advice_histories) == 1:
                continue
            for i, advice_history in enumerate(advice_histories[1:], start=1):  # skip the first one as it was added previously.
                # We need to do it this way to handle cases when advice is not yet given and there is no advice history.
                advice_data = {d["field_name"]: d["field_content"] for d in advice_history["advice_data"]}
                results.append(dict(base_row, **{
                    "reception_date": self._format_date(item_wf_history[i]["time"]) if i < len(item_wf_history) else "",
                    "advice_date": self._format_date(advice_history["time"]),
                    "end_advice": "NON",
                    "advice_type": advice_data.get("advice_type"),
                    "comments": advice_data.get("advice_comments"),
                }))

        return results
