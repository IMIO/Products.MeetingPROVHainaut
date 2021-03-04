# encoding: utf-8

from Products.MeetingPROVHainaut.config import ADVICE_CATEGORIES
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class AdviceCategoriesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ """
        res = []
        for category_id, category_title in ADVICE_CATEGORIES:
            res.append(SimpleTerm(category_id,
                                  category_id,
                                  category_title))
        return SimpleVocabulary(res)

AdviceCategoriesVocabularyFactory = AdviceCategoriesVocabulary()
