import datetime

import modeled


class TestDateTime:
    def test_meta(self):
        assert issubclass(modeled.datetime.meta, modeled.base.meta)
        # and explcitly make sure datetime has its own derived meta
        assert modeled.datetime.meta is not modeled.base.meta
        assert modeled.datetime.meta.__qualname__ \
            == modeled.datetime.__qualname__ + '.meta'

    def test_class(self):
        assert type(modeled.datetime) is modeled.datetime.meta
        assert issubclass(modeled.datetime, datetime.datetime)
        assert issubclass(modeled.datetime, modeled.datetime.base)

    def test_new(self, args):
        std_dt = datetime.datetime(*args)
        assert modeled.datetime(*args) == std_dt
        assert modeled.datetime(str(std_dt)) == std_dt

    def test_subclass_meta(self, format):
        subclass = modeled.datetime[format]
        # no modeled.datetime as base anymore, only modeled.datetime.base
        subclass.meta is modeled.base.meta

    def test_subclass(self, args, format):
        subclass = modeled.datetime[format]

        # after creating subclass with format, the modeled.datetime is
        # not kept as actual base anymore
        assert type(subclass) is not modeled.datetime.meta
        assert modeled.datetime not in subclass.mro()

        # but still appears as subclass by meta.__subclasscheck__
        assert issubclass(subclass, modeled.datetime)
        # it's only really based on modeled.datetime.base
        assert issubclass(subclass, modeled.datetime.base)
        # and standard datetime class of course
        assert issubclass(subclass, datetime.datetime)

    def test_subclass_new(self, args, format):
        subclass = modeled.datetime[format]
        std_dt = modeled.datetime(*args)

        assert subclass(*args) == std_dt
        assert subclass(std_dt.strftime(format)) == std_dt
