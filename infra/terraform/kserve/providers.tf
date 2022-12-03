terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.16.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "2.7.1"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = "1.14.0"
    }
  }
}

# https://registry.terraform.io/providers/hashicorp/helm
provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

# https://registry.terraform.io/providers/hashicorp/kubernetes/2.16.0
provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "kubectl" {
  config_path = "~/.kube/config"
}
