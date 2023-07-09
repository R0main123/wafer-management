import pytest

from filter import filter_by_meas, filter_by_temp
from getter import get_types, get_temps, get_compliance, get_VBDs
from manage_DB import register_compliance, register_VBD
from collections import Counter
def test_filter():
    assert Counter(filter_by_meas(["C"], "AL213656_D02")) == Counter(["CAP-BEOL10_23-50_50-BEOL10", "CAP-BEOL9_14-100_100-BEOL9",
                                                     "CAP-BEOL9_16-200_200-BEOL9", "CAP-BEOL9_21-700_700-BEOL9",
                                                     "CAP-BEOL11_19-1000_1000-BEOL11", "CAP-BEOL10_2-50_50-BEOL10",
                                                     "CAP-BEOL9_11-100_100-BEOL9", "CAP-BEOL9_9-200_200-BEOL9",
                                                     "CAP-BEOL9_4-700_700-BEOL9", "CAP-BEOL11_6-1000_1000-BEOL11",
                                                     "pad_start", "px24_short", "pad_CAP-BEOL9_7-pad-BEOL9",
                                                     "pad_CAP-BEOL9_18-pad-BEOL9"])

    assert Counter(filter_by_meas(["C", "I"], "AL213656_D02")) == Counter(["CAP-BEOL10_23-50_50-BEOL10", "CAP-BEOL9_14-100_100-BEOL9",
                                                     "CAP-BEOL9_16-200_200-BEOL9", "CAP-BEOL9_21-700_700-BEOL9",
                                                     "CAP-BEOL11_19-1000_1000-BEOL11", "CAP-BEOL10_2-50_50-BEOL10",
                                                     "CAP-BEOL9_11-100_100-BEOL9", "CAP-BEOL9_9-200_200-BEOL9",
                                                     "CAP-BEOL9_4-700_700-BEOL9", "CAP-BEOL11_6-1000_1000-BEOL11",
                                                     "pad_start", "px24_short", "pad_CAP-BEOL9_7-pad-BEOL9",
                                                     "pad_CAP-BEOL9_18-pad-BEOL9"])

    assert Counter(filter_by_meas(["I"], "AL213656_D02")) == Counter(["CAP-BEOL10_23-50_50-BEOL10", "CAP-BEOL9_14-100_100-BEOL9",
                                                          "CAP-BEOL9_16-200_200-BEOL9", "CAP-BEOL9_21-700_700-BEOL9",
                                                          "CAP-BEOL11_19-1000_1000-BEOL11", "CAP-BEOL10_2-50_50-BEOL10",
                                                          "CAP-BEOL9_11-100_100-BEOL9", "CAP-BEOL9_9-200_200-BEOL9",
                                                          "CAP-BEOL9_4-700_700-BEOL9", "CAP-BEOL11_6-1000_1000-BEOL11"])

    assert Counter(filter_by_meas(["C", "It"], "AL213656_D02")) == Counter(["CAP-BEOL10_23-50_50-BEOL10", "CAP-BEOL9_14-100_100-BEOL9",
                                                          "CAP-BEOL9_16-200_200-BEOL9", "CAP-BEOL9_21-700_700-BEOL9",
                                                          "CAP-BEOL11_19-1000_1000-BEOL11", "CAP-BEOL10_2-50_50-BEOL10",
                                                          "CAP-BEOL9_11-100_100-BEOL9", "CAP-BEOL9_9-200_200-BEOL9",
                                                          "CAP-BEOL9_4-700_700-BEOL9", "CAP-BEOL11_6-1000_1000-BEOL11",
                                                          "pad_start", "px24_short", "pad_CAP-BEOL9_7-pad-BEOL9",
                                                          "pad_CAP-BEOL9_18-pad-BEOL9"])

    assert filter_by_meas(["It"], "AL213656_D02") == []

    assert filter_by_meas([], "AL213656_D02") == []

    assert filter_by_meas(["C"], "AL213656") == []

    assert Counter(filter_by_temp("25", "AL213656_D02")) == Counter(["CAP-BEOL10_23-50_50-BEOL10", "CAP-BEOL9_14-100_100-BEOL9",
                                                     "CAP-BEOL9_16-200_200-BEOL9", "CAP-BEOL9_21-700_700-BEOL9",
                                                     "CAP-BEOL11_19-1000_1000-BEOL11", "CAP-BEOL10_2-50_50-BEOL10",
                                                     "CAP-BEOL9_11-100_100-BEOL9", "CAP-BEOL9_9-200_200-BEOL9",
                                                     "CAP-BEOL9_4-700_700-BEOL9", "CAP-BEOL11_6-1000_1000-BEOL11",
                                                     "pad_start", "px24_short", "pad_CAP-BEOL9_7-pad-BEOL9",
                                                     "pad_CAP-BEOL9_18-pad-BEOL9"])

    assert filter_by_temp("2,5", "AL213656_D02") == []

    assert filter_by_temp("25", "AL213656") == []

def test_getter():
    assert Counter(get_types("AL213656_D02")) == Counter(["I", "J", "C"])

    assert Counter(get_types("AL215095_D16")) == Counter(["I", "J"])

    assert "C" not in get_types("AL234567_D04")

    assert get_temps("AL234567_D04") == ["25"]

    assert get_compliance("AL215095_D07", "M2GAP-Cap-22_0_250_125_0-M2GC") is None

    register_compliance("AL213656_D02", "CAP-BEOL10_23-50_50-BEOL10", "0.01")

    assert get_compliance("AL213656_D02", "CAP-BEOL10_23-50_50-BEOL10") == "0.01"

    register_compliance("AL213656_D02", "CAP-BEOL10_23-50_50-BEOL10", "0.001")

    assert get_compliance("AL213656_D02", "CAP-BEOL10_23-50_50-BEOL10") == "0.001"


def test_VBD():
    assert get_VBDs("AL213656_D02", "CAP-BEOL10_23-50_50-BEOL10", "7", "-14") is not None

    register_VBD("AL213656_D02", "CAP-BEOL10_23-50_50-BEOL10", "7", "-14", "26")

    assert get_VBDs("AL213656_D02", "CAP-BEOL10_23-50_50-BEOL10", "7", "-14") == "26"


