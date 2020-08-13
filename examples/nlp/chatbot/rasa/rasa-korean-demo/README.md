# Rasa 한글 처리를 위한 custom component 개발 튜토리얼

## 사전 작업

### GloVe Featurizer의 사전 임베딩 다운받기

아래 경로에서 다운 받았고 시간이 급하여 따로 이 glove.txt 파일만 다운로드하는 방법을 준비하지 못했습니다.
아래 방법으로 다운 받을 수 있습니다. 후에 업데이트 하도록 하겠습니다.

```shell script
git clone https://github.com/ratsgo/embedding.git
```

아래 방법으로 도커 컨테이너 설치
```shell script
https://ratsgo.github.io/embedding/environment.html
```

워드 임베딩 파일들 다운로드하는 명령어
```shell script
bash preprocess.sh dump-word-embeddings
```

디렉토리 내에서 glove.txt 파일을 아래 경로에 둔다.
>./custom/gloVe_featurizer/model/glove.txt


