import modeled

import pytest


class TestStrict:

    def test_meta(self):
        assert modeled.strict.meta.__qualname__ == 'strict.meta'

    def test_class(self):
        assert type(modeled.strict) is modeled.strict.meta

    def test_class_getitem(self):
        wrapped = modeled.strict[str]

        assert issubclass(wrapped, str)
        assert issubclass(wrapped, modeled.strict)
        assert modeled.strict not in wrapped.mro()
        assert wrapped.__name__ == wrapped.__qualname__ == 'strict[str]'

        assert type(wrapped) is wrapped.meta
        assert type(wrapped).__name__ == type(wrapped).__qualname__ \
            == 'strict[str].meta'

    def test_class_getitem_with_class_with_metaclass(self):
        class Meta(type):
            pass

        class Class(metaclass=Meta):
            pass

        wrapped = modeled.strict[Class]

        assert issubclass(wrapped, Class)
        assert issubclass(wrapped, modeled.strict)
        assert modeled.strict not in wrapped.mro()
        assert wrapped.__name__ == wrapped.__qualname__ == 'strict[Class]'

        assert type(wrapped) is wrapped.meta
        assert issubclass(type(wrapped), Meta)
        assert type(wrapped).__name__ == type(wrapped).__qualname__ \
            == 'strict[Class].meta'

    def test_class_getitem_without_class(self):
        with pytest.raises(TypeError) as exc:
            modeled.strict[7]
        # should not be a derived exception here
        assert exc.type is TypeError
        assert 'MODELED data types must be classes' in str(exc.value)
