data "kubectl_file_documents" "certmanager" {
  content = file("cert-manager-v1.3.0.yaml")
}

resource "kubernetes_namespace" "certmanager" {
  depends_on = [kubectl_manifest.knativeservingreleaseinstall]
  metadata {
    annotations = {
      name = "cert-manager"
    }

    name = "cert-manager"
  }
}


resource "kubectl_manifest" "certmanager" {
  for_each  = data.kubectl_file_documents.certmanager.manifests
  yaml_body = each.value
  wait      = true

  depends_on = [kubernetes_namespace.certmanager]
}
