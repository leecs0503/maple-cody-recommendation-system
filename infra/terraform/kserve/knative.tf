# https://knative.dev/docs/install/yaml-install/serving/install-serving-with-yaml/#prerequisites
# kubectl_manifest가 yaml에 정의된 configmap을 먼저 apply하지 않아서 파일을 분리

data "kubectl_file_documents" "knativeservingcrdinstall" {
  content = file("knative-serving-crd-v1.4.0.yaml")
}

data "kubectl_file_documents" "knativeservingcoreconfigmapinstall" {
  content = file("knative-serving-core-configmap-v1.4.0.yaml")
}

data "kubectl_file_documents" "knativeservingcoreinstall" {
  content = file("knative-serving-core-v1.4.0.yaml")
}

data "kubectl_file_documents" "knativeservingreleaseinstall" {
  content = file("knative-serving-release-v1.4.0.yaml")
}

resource "kubernetes_namespace" "knativeserving" {
  depends_on = [kubectl_manifest.istioingressinstall]
  metadata {
    annotations = {
      name = "knative-serving"
    }

    labels = {
      "app.kubernetes.io/name": "knative-serving"
      "app.kubernetes.io/version": "1.4.0"
    }

    name = "knative-serving"
  }
}


resource "kubectl_manifest" "knativeservingcrdinstall" {
  for_each  = data.kubectl_file_documents.knativeservingcrdinstall.manifests
  yaml_body = each.value

  depends_on = [kubernetes_namespace.knativeserving]
}

resource "kubectl_manifest" "knativeservingcoreconfigmapinstall" {
  for_each  = data.kubectl_file_documents.knativeservingcoreconfigmapinstall.manifests
  yaml_body = each.value

  depends_on = [kubectl_manifest.knativeservingcrdinstall]
}

resource "kubectl_manifest" "knativeservingcoreinstall" {
  for_each  = data.kubectl_file_documents.knativeservingcoreinstall.manifests
  yaml_body = each.value

  depends_on = [kubectl_manifest.knativeservingcoreconfigmapinstall]
}

resource "kubectl_manifest" "knativeservingreleaseinstall" {
  for_each  = data.kubectl_file_documents.knativeservingreleaseinstall.manifests
  yaml_body = each.value

  depends_on = [kubectl_manifest.knativeservingcoreinstall]
}
