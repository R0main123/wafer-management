from getter import get_wafer


def setCompliance(waferId, session, compliance):
    wafer = get_wafer(waferId)
    wafer[session]['Compliance'] = compliance



