resource "kubernetes_secret" "dockercfg" {
  metadata {
    name = "docker-cfg"
  }

  data = {
    ".dockerconfigjson" = "${file("~/.docker/config.json")}"
  }

  type = "kubernetes.io/dockerconfigjson"
}

resource "kubernetes_default_service_account" "defaultsa" {
  depends_on = [kubernetes_secret.dockercfg]
  metadata {
    namespace = "default"
  }
  image_pull_secret {
    name = kubernetes_secret.dockercfg.metadata.0.name
  }
}

resource "kubernetes_namespace" "kserve-inference" {
  metadata {
    annotations = {
      name = "kserve-inference"
    }

    labels = {
      istio-injection = "enabled"
    }

    name = "kserve-inference"
  }
}
