import time
import json
import os
import re
from typing import Any, List, Optional, Text, Dict

from rasa.nlu.constants import ENTITIES
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData
from rasa.utils.common import raise_warning

import logging
logger = logging.getLogger(__name__)


class RegexExtractor(EntityExtractor):

    defaults = {
        'output_dir': os.path.join('custom', 'regexExtractor'),
        'entity_filename': 'patterns.dic'
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        dic: dict = None
    ) -> None:

        super().__init__(component_config)
        self.patterns = dic


    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        """
        여기서는 학습이라기 보다는 ExactMatch 를 쉽게 하기 위한 딕셔너리 파일을 만드는
        작업을 한다.
        
        엔티티로 추출될 수 있는 것은 다음과 같다.

        * training_data 하부에는  
        1 training_examples : nlu 학습 예시 문장에 등록되어 있는 엔티티
        2 entity_synonyms : synonyms
        3 regex_features : 정규식
        4 lookup_tables : lookup table 에 등록된 엔티티

        DIET에서는 정규식을 뽑아주지는 않는다. 후처리가 필요하다는게 라사 공식문서 내용
        그래서 여기서 뽑아주는 역할을 한다.
        """

        patterns = {}
        
        logger.debug('regex_features : {}'.format(training_data.regex_features))
        for item in training_data.regex_features:
            if '\\b' not in item['pattern']: # regex
                patterns[item['pattern']] = {
                    'entity': item['name'],
                    'value': item['pattern']
                }
        # write
        output_dir = self.component_config.get('output_dir')
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        file_path = os.path.join(output_dir, self.component_config.get('entity_filename'))
        with open(file_path, 'w') as json_file:
            json.dump(patterns, json_file)

        # printEntity = json.dumps(patterns, indent=4, ensure_ascii=False)
        # logger.debug('final dumps : \n{}'.format(printEntity))
        logger.debug('regex extractor training finished..')
        return

    def process(self, message: Message, **kwargs: Any) -> None:
        # 익스트렉터가 있는지
        if self.patterns is None:
            logger.warning('There is no dictionary for user regex patterns.')
            return

        extracted = self.exact_match(message.text)
        em_list = self.add_extractor_name(extracted)
        
        # 앞선 파이프라인 컴포턴트에서 뽑힌 엔티티 목록
        diet_list = message.get(ENTITIES,[])
        logger.debug('em_list : {}'.format(em_list))
        logger.debug('diet_list : {}'.format(diet_list))

        # 1. DIET 추출X, EM 추출O
        if diet_list == [] and em_list != []:
            message.set(
                ENTITIES, em_list, add_to_output=True
            )

        # 2. DIET O, EM O
        elif diet_list != [] and em_list != []:
            add_entity = []
            for em in em_list:
                for diet in diet_list:
                    if em['value'] in diet['value']:
                        pass
                    else:
                        add_entity.append(em)
            message.set(
                ENTITIES, diet_list + add_entity, add_to_output=True
            )
        # 3. EM X
        else:
            pass        

    def exact_match(self, text: str):

        # patterns의 key값만 리스트로 담아두기
        ue_pattern_list = list(self.patterns.keys())
        
        entities = []

        for pattern in ue_pattern_list:
            for item in re.finditer(pattern, text):
                entities.append({
                    'entity': self.patterns[pattern]['entity'],
                    'value': text[item.start(): item.end()],
                    'start': item.start(),
                    'end': item.end(),
                    'confidence': 1.0 # exact match 라서 100%
                })

        outputs = json.dumps(entities, ensure_ascii=False)
        logger.debug('entities from regex extractor : {}'.format(outputs))

        return entities

    @classmethod
    def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional["Metadata"] = None,
            cached_component: Optional["RegexExtractor"] = None,
            **kwargs: Any,
    ) -> "RegexExtractor":
        """Load this component from file."""
        logger.info('meta : {}'.format(meta))
        logger.info('cached_component : {}'.format(cached_component))

        try:
            file_path = os.path.join(meta['output_dir'], meta['entity_filename'])
            with open(file_path, 'r') as json_file:
                patterns = json.load(json_file)
            logger.info('The dictionary for regex extractor is loaded.')
        except:
            patterns = None

        return cls(component_config=meta,
                   dic=patterns)
