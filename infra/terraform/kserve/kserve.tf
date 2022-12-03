data "kubectl_file_documents" "kserve" {
  content = file("kserve-v0.9.0.yaml")
}

data "kubectl_file_documents" "kserveruntimes" {
  content = file("kserve-runtimes-v0.9.0.yaml")
}

resource "kubernetes_namespace" "kserve" {
  depends_on = [kubectl_manifest.certmanager]
  metadata {
    annotations = {
      name = "kserve"
    }

    labels = {
      "control-plane": "kserve-controller-manager"
      "controller-tools.k8s.io": "1.0"
      "istio-injection": "enabled"
    }

    name = "kserve"
  }
}


resource "kubectl_manifest" "kserve" {
  for_each  = data.kubectl_file_documents.kserve.manifests
  yaml_body = each.value
  wait      = true

  depends_on = [kubernetes_namespace.kserve]
}

resource "kubectl_manifest" "kserveruntimes" {
  for_each  = data.kubectl_file_documents.kserveruntimes.manifests
  yaml_body = each.value
  wait      = true

  depends_on = [kubectl_manifest.kserve]
}
