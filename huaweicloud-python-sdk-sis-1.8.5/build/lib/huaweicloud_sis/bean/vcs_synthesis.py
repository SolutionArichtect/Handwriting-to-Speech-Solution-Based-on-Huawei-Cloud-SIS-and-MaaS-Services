# -*- coding: utf-8 -*-


class VcsSynthesisRequest :
    """ 声音复刻合成请求，除了初始化必选参数外，其他参数均可不配置使用默认 """
    def __init__(self, text, voice_name):
        """
            声音复刻合成请求初始化
        :param text: 需要合成的文本
        """
        self._text = text
        self._voice_name = voice_name
        self._audio_format = 'wav'
        self._sample_rate = '16000'
        self._saved = False
        self._saved_path = ''

    def set_audio_format(self, audio_format):
        self._audio_format = audio_format

    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate

    def set_saved(self, saved):
        self._saved = saved

    def set_saved_path(self, saved_path):
        self._saved_path = saved_path

    def get_saved(self):
        return self._saved

    def get_saved_path(self):
        return self._saved_path

    def construct_params(self):
        config = dict()
        config['audio_format'] = self._audio_format
        config['sample_rate'] = self._sample_rate
        config['voice_name'] = self._voice_name

        params = dict()
        params['text'] = self._text
        params['config'] = config
        return params
