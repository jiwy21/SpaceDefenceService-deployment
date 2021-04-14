# -*- coding:utf-8 -*-


class IntermediateMeta(object):
    """
    """

    def __init__(self, id=None, count=None, packages=None, satellite=None, arrival_time=None,
                 duration=None, freq_down=None, freq_unit=None, iqlocation=None, iqlen=None,
                 bitrate=None, coderate=None, bandwidth=None, fs_rate=None, snr=None, freq_carrier=None, modulation_mode=None):

        """
        :param id:
        :param count:
        :param packages:
        :param satellite:
        :param arrival_time:
        :param duration:
        :param freq_down:
        :param freq_unit:
        :param iqlocation:
        :param iqlen:
        :param bitrate:
        :param coderate:
        :param bandwidth:
        :param modulation_mode:
        """

        self._id = id
        self._count = count
        self._packages = packages
        self._satellite = satellite
        self._arrival_time = str(arrival_time)
        self._duration = duration
        self._freq_down = freq_down
        self._freq_unit = freq_unit.strip()
        self._iqlocation = iqlocation.strip()
        self._iqlen = iqlen
        self._bitrate = bitrate
        self._coderate = coderate
        self._bandwidth = bandwidth
        self._fs_rate = fs_rate
        self._snr = snr
        self._freq_carrier = freq_carrier
        self._modulation_mode = modulation_mode.strip()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val

    @property
    def packages(self):
        return self._packages

    @packages.setter
    def packages(self, val):
        self._packages = val

    @property
    def satellite(self):
        return self._satellite

    @satellite.setter
    def satellite(self, val):
        self._satellite = val

    @property
    def arrival_time(self):
        return self._arrival_time

    @arrival_time.setter
    def arrival_time(self, val):
        self._arrival_time = val

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, val):
        self._duration = val

    @property
    def freq_down(self):
        return self._freq_down

    @freq_down.setter
    def freq_down(self, val):
        self._freq_down = val

    @property
    def freq_unit(self):
        return self._freq_unit

    @freq_unit.setter
    def freq_unit(self, val):
        self._freq_unit = val

    @property
    def iqlocation(self):
        return self._iqlocation

    @iqlocation.setter
    def iqlocation(self, val):
        self._iqlocation = val

    @property
    def iqlen(self):
        return self._iqlen

    @iqlen.setter
    def iqlen(self, val):
        self._iqlen = val

    @property
    def bitrate(self):
        return self._bitrate

    @bitrate.setter
    def bitrate(self, val):
        self._bitrate = val

    @property
    def coderate(self):
        return self._coderate

    @coderate.setter
    def coderate(self, val):
        self._coderate = val

    @property
    def bandwidth(self):
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, val):
        self._bandwidth = val

    @property
    def fs_rate(self):
        return self._fs_rate

    @fs_rate.setter
    def fs_rate(self, val):
        self._fs_rate = val
        
    @property
    def snr(self):
        return self._snr

    @snr.setter
    def snr(self, val):
        self._snr = val
        
    @property
    def freq_carrier(self):
        return self._freq_carrier

    @freq_carrier.setter
    def freq_carrier(self, val):
        self._freq_carrier = val

    @property
    def modulation_mode(self):
        return self._modulation_mode

    @modulation_mode.setter
    def modulation_mode(self, val):
        self._modulation_mode = val


class IQMeta(object):
    """
    """
    def __init__(self, i=None, q=None):
        """
        :param i: i路数据
        :param q: q路数据
        """
        self._i = i
        self._q = q

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, val):
        self._i = val

    @property
    def q(self):
        return self._q

    @q.setter
    def q(self, val):
        self._q = val


class SXDWMeta(object):
    """
    """
    def __init__(self, id=None, id_sxdw=None, arrival_time=None, freq_down=None, freq_down_unit=None,
                 batchnumber=None, true_value_lon=None, true_value_lat=None, true_value_error=None,
                 result_confidence=None, false_value_lon=None, false_value_lat=None, freq_up=None,
                 freq_up_unit=None, multi_access_mode=None, modulate_pattern=None, code_mode=None,
                 bandwidth=None, bandwidth_unit=None, sps=None, sps_unit=None, medial_sat_norad=None,
                 adjacent_sat_norad1=None, adjacent_sat_norad2=None):
        """
        :param id:
        :param id_sxdw:
        :param arrival_time:
        :param freq_down:
        :param freq_unit:
        :param batchnumber:
        :param true_value_lon:
        :param true_value_lat:
        :param true_value_error:
        :param result_confidence:
        :param false_value_lon:
        :param false_value_lat:
        :param freq_up:
        :param freq_up_unit:
        :param multi_access_mode:
        :param modulate_pattern:
        :param code_mode:
        :param bandwidth:
        :param bandwidth_unit:
        :param sps:
        :param sps_unit:
        :param medial_sat_norad:
        :param adjacent_sat_norad1:
        :param adjacent_sat_norad2:
        """
        self._id = id
        self._id_sxdw = id_sxdw
        self._arrival_time = str(arrival_time)
        self._freq_down = freq_down
        self._freq_down_unit = freq_down_unit.strip()
        self._batchnumber = batchnumber
        self._true_value_lon = true_value_lon
        self._true_value_lat = true_value_lat
        self._true_value_error = true_value_error
        self._result_confidence = result_confidence
        self._false_value_lon = false_value_lon
        self._false_value_lat = false_value_lat
        self._freq_up = freq_up
        self._freq_up_unit = freq_up_unit.strip()
        self._multi_access_mode = multi_access_mode.strip()
        self._modulate_pattern = modulate_pattern.strip()
        self._code_mode = code_mode.strip()
        self._bandwidth = bandwidth
        self._bandwidth_unit = bandwidth_unit.strip()
        self._sps = sps
        self._sps_unit = sps_unit.strip()
        self._medial_sat_norad = medial_sat_norad
        self._adjacent_sat_norad1 = adjacent_sat_norad1
        self._adjacent_sat_norad2 = adjacent_sat_norad2


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def id_sxdw(self):
        return self._id_sxdw

    @id_sxdw.setter
    def id_sxdw(self, val):
        self._id_sxdw = val

    @property
    def arrival_time(self):
        return self._arrival_time

    @arrival_time.setter
    def arrival_time(self, val):
        self._arrival_time = val

    @property
    def freq_down(self):
        return self._freq_down

    @freq_down.setter
    def freq_down(self, val):
        self._freq_down = val

    @property
    def freq_down_unit(self):
        return self._freq_down_unit

    @freq_down_unit.setter
    def freq_down_unit(self, val):
        self._freq_down_unit = val

    @property
    def batchnumber(self):
        return self._batchnumber

    @batchnumber.setter
    def batchnumber(self, val):
        self._batchnumber = val

    @property
    def true_value_lon(self):
        return self._true_value_lon

    @true_value_lon.setter
    def true_value_lon(self, val):
        self._true_value_lon = val

    @property
    def true_value_lat(self):
        return self._true_value_lat

    @true_value_lat.setter
    def true_value_lat(self, val):
        self._true_value_lat = val

    @property
    def true_value_error(self):
        return self._true_value_error

    @true_value_error.setter
    def true_value_error(self, val):
        self._true_value_error = val

    @property
    def result_confidence(self):
        return self._result_confidence

    @result_confidence.setter
    def result_confidence(self, val):
        self._result_confidence = val

    @property
    def false_value_lon(self):
        return self._false_value_lon

    @false_value_lon.setter
    def false_value_lon(self, val):
        self._false_value_lon = val

    @property
    def false_value_lat(self):
        return self._false_value_lat

    @false_value_lat.setter
    def false_value_lat(self, val):
        self._false_value_lat = val

    @property
    def freq_up(self):
        return self._freq_up

    @freq_up.setter
    def freq_up(self, val):
        self._freq_up = val

    @property
    def freq_up_unit(self):
        return self._freq_up_unit

    @freq_up_unit.setter
    def freq_up_unit(self, val):
        self._freq_up_unit = val

    @property
    def multi_access_mode(self):
        return self._multi_access_mode

    @multi_access_mode.setter
    def multi_access_mode(self, val):
        self._multi_access_mode = val

    @property
    def modulate_pattern(self):
        return self._modulate_pattern

    @modulate_pattern.setter
    def modulate_pattern(self, val):
        self._modulate_pattern = val

    @property
    def code_mode(self):
        return self._code_mode

    @code_mode.setter
    def code_mode(self, val):
        self._code_mode = val

    @property
    def bandwidth(self):
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, val):
        self._bandwidth = val

    @property
    def bandwidth_unit(self):
        return self._bandwidth_unit

    @bandwidth_unit.setter
    def bandwidth_unit(self, val):
        self._bandwidth_unit = val

    @property
    def sps(self):
        return self._sps

    @sps.setter
    def sps(self, val):
        self._sps = val

    @property
    def sps_unit(self):
        return self._sps_unit

    @sps_unit.setter
    def sps_unit(self, val):
        self._sps_unit = val

    @property
    def medial_sat_norad(self):
        return self._medial_sat_norad

    @medial_sat_norad.setter
    def medial_sat_norad(self, val):
        self._medial_sat_norad = val

    @property
    def adjacent_sat_norad1(self):
        return self._adjacent_sat_norad1

    @adjacent_sat_norad1.setter
    def adjacent_sat_norad1(self, val):
        self._adjacent_sat_norad1 = val

    @property
    def adjacent_sat_norad2(self):
        return self._adjacent_sat_norad2

    @adjacent_sat_norad2.setter
    def adjacent_sat_norad2(self, val):
        self._adjacent_sat_norad2 = val





















