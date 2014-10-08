"""An enhanced enum option, with built in iterability.
(From http://code.activestate.com/recipes/413486-first-class-enums-in-python/)
Usage:
print '\n*** Enum Demo ***'
print '--- Days of week ---'
Days = Enum('Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su')
print Days
print Days.Mo
print Days.Fr
print Days.Mo < Days.Fr
print list(Days)
for each in Days:
  print 'Day:', each
print '--- Yes/No ---'
Confirmation = Enum('No', 'Yes')
answer = Confirmation.No
print 'Your answer is not', ~answer
"""


def Enum(*names):
    """A further-enhanced enum option, with built in iterability.
    (From http://code.activestate.com/recipes/413486-first-class-enums-in-python/)
    Usage:
    print '\n*** Enum Demo ***'
    print '--- Days of week ---'
    Days = Enum('Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su')
    print Days
    print Days.Mo
    print Days.Fr
    print Days.Mo < Days.Fr
    print list(Days)
    for each in Days:
      print 'Day:', each
    print '--- Yes/No ---'
    Confirmation = Enum('No', 'Yes')
    answer = Confirmation.No
    print 'Your answer is not', ~answer
    """
    class EnumClass(object):
        __slots__ = names

        def __iter__(self):
            return iter(constants)

        def __len__(self):
            return len(constants)

        def __getitem__(self, i):
            return constants[i]

        def __repr__(self):
            return 'Enum' + str(names)

        def __str__(self):
            return 'enum ' + str(constants)

    class EnumValue(object):
        __slots__ = ('__value')

        def __init__(self, value):
            self.__value = value

        Value = property(lambda self: self.__value)
        EnumType = property(lambda self: EnumType)

        def __hash__(self):
            return hash(self.__value)

        def __cmp__(self, other):
            # C fans might want to remove the following assertion
            # to make all enums comparable by ordinal value {;))
            assert self.EnumType is other.EnumType, "Only values from the same enum are comparable"
            return cmp(self.__value, other.__value)

        def __invert__(self):
            return constants[maximum - self.__value]

        def __nonzero__(self):
            return bool(self.__value)

        def __repr__(self):
            return str(names[self.__value])

    maximum = len(names) - 1
    constants = [None] * len(names)
    for i, each in enumerate(names):
        val = EnumValue(i)
        setattr(EnumClass, each, val)
        constants[i] = val
    constants = tuple(constants)
    EnumType = EnumClass()
    return EnumType


def valid_enum_val(val, enum_class):
    """Is val a valid member of enum"""
    if val not in list(enum_class) and val not in [str(e) for e in enum_class]:
        return False
    else:
        return True


def get_enum_choices(enum_class):
    """get django model style choices...tup of tups... ((, ), )"""
    tup_list = []
    for v in list(enum_class):
        tup_list.append(tuple([v, v]))
    return tuple(tup_list)
