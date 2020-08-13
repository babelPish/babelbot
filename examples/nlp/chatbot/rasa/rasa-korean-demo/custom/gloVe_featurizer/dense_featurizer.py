from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.config import RasaNLUModelConfig
# from rasa.nlu.components import Component
from rasa.nlu.tokenizers.tokenizer import Token
from rasa.nlu.featurizers.featurizer import DenseFeaturizer
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.constants import (
    TEXT,
    TOKENS_NAMES,
    DENSE_FEATURE_NAMES,
    DENSE_FEATURIZABLE_ATTRIBUTES,
)

import os
import numpy as np
import time
import logging

logger = logging.getLogger(__name__)


class GloVeFeaturizer(DenseFeaturizer):

    # @classmethod
    # def required_packages(cls) -> List[Text]:
    #     '''
    #     이 컴포넌트를 사용하려면 필요한 라이브러리
    #     사전에 학습된 임베딩 텍스트 파일을 딕셔너리 형태로 가지고 있어서 Glove 라이브러리가 필요업삳.
    #     '''
    #     return []

    # 임베딩 파일은 "한국어 임베딩" 책의 github에서 다운로드 하였습니다.
    defaults = {
        'glove_path': 'custom/gloVe_featurizer/model/glove.txt'
    }

    def __init__(self,
                 component_config: Optional[Dict[Text, Any]] = None,
                 glove_dict=None
                 ):
        '''
        학습 시 초기에 들어오는 메서드
        '''
        super().__init__(component_config)
        logger.info('component_config : {}'.format(self.component_config))
        self.glove_dict = glove_dict
        if self.glove_dict is None:
            self.glove_dict = loadGloVe(self.component_config.get('glove_path'))

    def train(
            self,
            training_data: TrainingData,
            config: Optional[RasaNLUModelConfig] = None,
            **kwargs: Any,
    ) -> None:

        if self.glove_dict is None:
            logger.warning('model is None')
            raise ValueError('Model이 없다!!')

        '''
        training_data 에는 학습시 사용한 데이터(인텐트, 엔티티 등)가 모두 들어있다.
        라사에서 학습 문장의 경우 인텐트의 예시므로 아래와 같이 추출한다.
        다른 컴포넌트와 달리 featurizer의 train()은 실제 학습이 아니고 학습시에 사용하는 피쳐를 뽑아주는 역할을 한다.
        '''
        for example in training_data.intent_examples:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                # attribute : text or response
                #   text : intent examples
                #   response : system utter[action] examples
                # featurizing only text
                if attribute == 'text':
                    self._set_glove_features(example, attribute)

    def process(self, message: Message, **kwargs: Any) -> None:
        '''
        Rasa agent 를 구동할 때 입력 문장이 들어올 때 처리하는 메서드
        여기서는 입력 문장에 대해 dense feature를 뽑아주는 역할을 한다.
        :param message:
        :param kwargs:
        :return:
        '''
        self._set_glove_features(message)

    def _set_glove_features(self, message: Message, attribute: Text = TEXT):
        """Adds the word vectors to the messages features.
        feature를 뽑아서 message에 세팅함.
        """

        # get tokens from mecab tokenizer (in NLU pipeline)
        tokens = message.get(TOKENS_NAMES[attribute])

        # start_time = time.time()

        # convert tokens object to tokens text
        # for inputting to featurizer
        tokens_text = self._tokens_to_text(tokens)

        # 실제 dense feature 뽑는 메서드
        features = self.extract_features(tokens_text)

        # end_time = time.time()
        # 한 번 시간을 비교해보려고 작성했는데 dict 이기 때문에 완전 빠름.
        # logger.info('process time : {}'.format(end_time - start_time))

        features = self._combine_with_existing_dense_features(
            message, features, DENSE_FEATURE_NAMES[attribute]
        )

        message.set(DENSE_FEATURE_NAMES[attribute], features)

    def extract_features(self, tokens):
        '''
        딕셔너리 형태의 glove_dict으로부터 각 토큰의 임베딩 값을 쌓는다.
        '''
        res = []
        for tok in tokens:
            try:
                res.append(self.glove_dict[tok])
            except KeyError:
                res.append(self.glove_dict['<unk>'])
        embs = np.asarray(res)

        logger.debug('embs shape : {}'.format(embs.shape))
        logger.debug('embs : {}'.format(embs))

        return embs

    @staticmethod
    def _tokens_to_text(tokens: List[Token]) -> List[Text]:
        text = []
        for token in tokens:
            text.append(token.text)
        return text


    @classmethod
    def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional["Metadata"] = None,
            cached_component: Optional["GloVeFeaturizer"] = None,
            **kwargs: Any,
    ) -> "GloVeFeaturizer":
        """Load this component from file.
        agent 구동시 init() 안 거치고 load()만 거쳐서 바로 process()로 넘어간다.
        """
        logger.info('meta : {}'.format(meta))
        glove_dict = loadGloVe(meta['glove_path'])
        return cls(component_config=meta,
                   glove_dict=glove_dict)

def loadGloVe(glove_path):
    embedding_dict = dict()
    f = open(glove_path, encoding="utf8")

    for line in f:
        word_vector = line.split()
        word = word_vector[0]
        word_vector_arr = np.asarray(word_vector[1:], dtype='float32')  # 100개의 값을 가지는 array로 변환
        embedding_dict[word] = word_vector_arr
    f.close()
    logger.debug('%s개의 Embedding vector가 있습니다.' % len(embedding_dict))
    return embedding_dict