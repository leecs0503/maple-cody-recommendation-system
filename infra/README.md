# infra 관련 디렉토리

## infra 구축 순서
0. docker login (~/.docker/config.json 생성)
1. kind
2. kserve


## dependency
terraform 1.3.5

## terraform install
https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

## dns 문제시 해결법
/etc/resolv.conf에 `nameserver 8.8.8.8`이 있는지 확인