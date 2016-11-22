from six.moves import builtins

from moretools import cached

import modeled
from modeled import typed

from .error import MemberError


class meta(typed.base.meta):
    """
    Metaclass for :class:`modeled.member`:

    * Provides modeled.member[<mtype>], ...[<choices>] (==> implicit mtype)
      and ...[<mtype>][<choices>] syntax.
    * Stores member (sub)class specific exception class.
    """
    __qualname__ = 'member.meta'

    # to make the member exception class overridable in derived classes
    error = MemberError

    def __getitem__(cls, mtype_or_choices, typedcls=None, choicecls=None):
        """Dynamically create a derived typed member class
           and optionally a further derived class with member value choices.

        - Member value type can be implicitly determined from choices.
        - Override __getitem__ methods in derived classes
          can optionally provide a precreated `typedcls` or `choicecls`.
        """
        if type(mtype_or_choices) is builtins.tuple:
            choices = mtype_or_choices
            try: # Is member cls already typed?
                cls.mtype
            except AttributeError:
                mtype = type(choices[0])
                cls = typed.base.type.__getitem__(cls, mtype, typedcls)

            if not choicecls:
                class choicecls(cls):
                    pass

            choicecls.choices = choices = builtins.list(choices)
            choicecls.__module__ = cls.__module__
            choicecls.__name__ = '%s%s' % (cls.__name__, choices)
            return choicecls

        mtype = mtype_or_choices
        return typed.base.meta.__getitem__(cls, mtype, typedcls)
