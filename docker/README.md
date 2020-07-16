# tools
git과 docker 관련 스크립트 파일들.

## git 관련 

* 최초 한번. 원격 저장소를 등록한다.
```shell
$ python git_remote.py  
```
* 이후 원격 저장소의 변경을 현재 로컬 develop 브랜치에 반영하려면
```shell
$ python git_pull.py  
```

## docker 관련 

* 사용하고자 하는 target_tag의 docker-compose 파일을 생성한다
```shell
$ python docker_build.py target_tag

# 실행하면 다음 3 개의 파일이 생긴다. 
#  docker-compose.yml , docker-compose.yml.latest docker_enter.sh
```

* 도커 컨테이너 활성화
```shell
$ docker-compose up  
```

* 활성화된 도커 컨테이너로 진입하는 스크립트
```shell
$ sh docker_enter.sh  
```

* 도커 컨테이너 변경을 특정 target_tag의 도커 이미지에 반영
```shell
$ python docker_commit.py target_tag  
```

* 특정 target_tag의 도커 이미지를 원격 도커 저장소에 반영
```shell
$ python docker_push.py target_tag  
```

