data "kubectl_file_documents" "kserve" {
  content = file("kserve-v0.9.0.yaml")
}

data "kubectl_file_documents" "kserveruntimes" {
  content = file("kserve-runtimes-v0.9.0.yaml")
}

resource "kubectl_manifest" "kserve" {
  for_each  = data.kubectl_file_documents.kserve.manifests
  yaml_body = each.value
  wait      = true

  depends_on = [kubectl_manifest.certmanager]
}

resource "kubectl_manifest" "kserveruntimes" {
  for_each  = data.kubectl_file_documents.kserveruntimes.manifests
  yaml_body = each.value
  wait      = true

  depends_on = [kubectl_manifest.kserve]
}
