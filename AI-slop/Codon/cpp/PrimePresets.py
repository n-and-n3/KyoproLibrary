# Lazy segment tree monoids collected in cpp/Prime.cpp.

@tuple
class RSQ_RUQ_S:
    _value: int
    length: int


@tuple
class RSQ_RUQ_F:
    num: int
    iswrited: bool


class RSQ_RUQ:

    @staticmethod
    def op(a: RSQ_RUQ_S, b: RSQ_RUQ_S) -> RSQ_RUQ_S:
        return RSQ_RUQ_S(a._value + b._value, a.length + b.length)

    @staticmethod
    def comp(f: RSQ_RUQ_F, g: RSQ_RUQ_F) -> RSQ_RUQ_F:
        return f if f.iswrited else g

    @staticmethod
    def mapping(f: RSQ_RUQ_F, x: RSQ_RUQ_S) -> RSQ_RUQ_S:
        return RSQ_RUQ_S(f.num * x.length, x.length) if f.iswrited else x

    @staticmethod
    def e() -> RSQ_RUQ_S:
        return RSQ_RUQ_S(0, 0)

    @staticmethod
    def id() -> RSQ_RUQ_F:
        return RSQ_RUQ_F(0, False)


@tuple
class Affinell_S:
    sum: int
    min: int
    max: int
    length: int


@tuple
class Affinell_F:
    a: int
    b: int


class Affinell:
    infinity = 1 << 51

    @staticmethod
    def op(x: Affinell_S, y: Affinell_S) -> Affinell_S:
        return Affinell_S(x.sum + y.sum, min(x.min, y.min), max(x.max, y.max), x.length + y.length)

    @staticmethod
    def mapping(f: Affinell_F, x: Affinell_S) -> Affinell_S:
        if f.a >= 0:
            return Affinell_S(f.a * x.sum + f.b * x.length, f.a * x.min + f.b, f.a * x.max + f.b, x.length)
        return Affinell_S(f.a * x.sum + f.b * x.length, f.a * x.max + f.b, f.a * x.min + f.b, x.length)

    @staticmethod
    def comp(f: Affinell_F, g: Affinell_F) -> Affinell_F:
        return Affinell_F(f.a * g.a, f.a * g.b + f.b)

    @staticmethod
    def e() -> Affinell_S:
        return Affinell_S(0, Affinell.infinity, -Affinell.infinity, 0)

    @staticmethod
    def id() -> Affinell_F:
        return Affinell_F(1, 0)


@tuple
class Affinemint_S:
    sum: int
    length: int


@tuple
class Affinemint_F:
    a: int
    b: int


class Affinemint:
    MOD = 998244353

    @staticmethod
    def op(x: Affinemint_S, y: Affinemint_S) -> Affinemint_S:
        return Affinemint_S((x.sum + y.sum) % Affinemint.MOD, x.length + y.length)

    @staticmethod
    def mapping(f: Affinemint_F, x: Affinemint_S) -> Affinemint_S:
        return Affinemint_S((f.a * x.sum + f.b * x.length) % Affinemint.MOD, x.length)

    @staticmethod
    def comp(f: Affinemint_F, g: Affinemint_F) -> Affinemint_F:
        return Affinemint_F(f.a * g.a % Affinemint.MOD, (f.a * g.b + f.b) % Affinemint.MOD)

    @staticmethod
    def e() -> Affinemint_S:
        return Affinemint_S(0, 0)

    @staticmethod
    def id() -> Affinemint_F:
        return Affinemint_F(1, 0)


@tuple
class ADD_DIV_MAX_RESTORE_S:
    max: int
    initial_max: int
    min: int
    initial_min: int


@tuple
class ADD_DIV_MAX_RESTORE_F:
    offset: int
    den: int
    add: int
    flag: bool


class ADD_DIV_MAX_RESTORE:

    @staticmethod
    def op(x: ADD_DIV_MAX_RESTORE_S, y: ADD_DIV_MAX_RESTORE_S) -> ADD_DIV_MAX_RESTORE_S:
        return ADD_DIV_MAX_RESTORE_S(max(x.max, y.max), max(x.initial_max, y.initial_max), min(x.min, y.min), min(x.initial_min, y.initial_min))

    @staticmethod
    def e() -> ADD_DIV_MAX_RESTORE_S:
        return ADD_DIV_MAX_RESTORE_S(0, 0, 0, 0)

    @staticmethod
    def mapping(f: ADD_DIV_MAX_RESTORE_F, x: ADD_DIV_MAX_RESTORE_S) -> ADD_DIV_MAX_RESTORE_S:
        if f.flag:
            return ADD_DIV_MAX_RESTORE_S((x.initial_max + f.offset) // f.den + f.add, x.initial_max, (x.initial_min + f.offset) // f.den + f.add, x.initial_min)
        return ADD_DIV_MAX_RESTORE_S((x.max + f.offset) // f.den + f.add, x.initial_max, (x.min + f.offset) // f.den + f.add, x.initial_min)

    @staticmethod
    def comp(g: ADD_DIV_MAX_RESTORE_F, f: ADD_DIV_MAX_RESTORE_F) -> ADD_DIV_MAX_RESTORE_F:
        if g.flag:
            return g
        a = f.offset + f.den * ((f.add + g.offset) % g.den)
        b = f.den * g.den
        c = g.add + (f.add + g.offset) // g.den
        if b > 1000000000:
            a = max(a - (b - 1000000000), 0)
            b = 1000000000
        return ADD_DIV_MAX_RESTORE_F(a, b, c, f.flag)

    @staticmethod
    def id() -> ADD_DIV_MAX_RESTORE_F:
        return ADD_DIV_MAX_RESTORE_F(0, 1, 0, False)

    @staticmethod
    def gen(a: int) -> ADD_DIV_MAX_RESTORE_S:
        return ADD_DIV_MAX_RESTORE_S(a, a, a, a)
