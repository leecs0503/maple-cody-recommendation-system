# https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/namespace
resource "kubernetes_namespace" "istio-system" {
  depends_on = [kubernetes_default_service_account.defaultsa]
  metadata {
    annotations = {
      name = "istio-system"
    }

    labels = {
      istio-injection = "enabled"
    }

    name = "istio-system"
  }
}

# https://registry.terraform.io/providers/hashicorp/helm/latest/docs/resources/release
# https://istio.io/latest/docs/setup/install/helm/
resource "helm_release" "istio-base" {
  depends_on = [kubernetes_namespace.istio-system]

  name      = "istio-base"
  namespace = "istio-system"
  chart     = "istio/base"
}

# https://registry.terraform.io/providers/hashicorp/helm/latest/docs/resources/release
# https://istio.io/latest/docs/setup/install/helm/
resource "helm_release" "istiod" {
  depends_on = [helm_release.istio-base]

  name      = "istiod"
  namespace = "istio-system"
  chart     = "istio/istiod"
  wait      = true
}

# https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/namespace
# https://istio.io/latest/docs/setup/install/helm/
resource "kubernetes_namespace" "istio-ingress" {
  depends_on = [helm_release.istiod]
  metadata {
    annotations = {
      name = "istio-ingress"
    }

    labels = {
      istio-injection = "enabled"
    }

    name = "istio-ingress"
  }
}

data "kubectl_file_documents" "istioingressinstall" {
  content = file("istio-ingress.yaml")
}

resource "kubectl_manifest" "istioingressinstall" {
  for_each  = data.kubectl_file_documents.istioingressinstall.manifests
  yaml_body = each.value

  depends_on = [kubernetes_namespace.istio-ingress]
}
