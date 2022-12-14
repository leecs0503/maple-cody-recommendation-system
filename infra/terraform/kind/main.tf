resource "kind_cluster" "default" {
  name           = "mcrs-cluster"
  node_image     = "kindest/node:v1.23.4"
  wait_for_ready = true
  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"

      kubeadm_config_patches = [
        "kind: InitConfiguration\nnodeRegistration:\n  kubeletExtraArgs:\n    node-labels: \"ingress-ready=true\"\n"
      ]

      extra_mounts {
        host_path      = "/etc/resolv.conf"
        container_path = "/etc/resolv.conf"
      }
      extra_mounts {
        host_path      = "/etc/docker/daemon.json"
        container_path = "/etc/docker/daemon.json"
      }
      extra_port_mappings {
        container_port = 80
        host_port      = 80
      }
      extra_port_mappings {
        container_port = 443
        host_port      = 443
      }
    }

    node {
      role = "worker"
    }
  }
}
