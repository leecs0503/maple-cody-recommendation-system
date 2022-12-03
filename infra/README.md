# infra 관련 디렉토리

## infra 구축 순서
0. docker login (~/.docker/config.json 생성)
1. kind
2. kserve


## istio helm repo 추가
> helm repo add istio https://istio-release.storage.googleapis.com/charts
> helm repo update
## dependency
terraform 1.3.5

## terraform install
https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

## helm install
> curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
> chmod 700 get_helm.sh
> ./get_helm.sh
> rm ./get_helm.sh

## dns 문제시 해결법
/etc/resolv.conf에 `nameserver 8.8.8.8`이 있는지 확인