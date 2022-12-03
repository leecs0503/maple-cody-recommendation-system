terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "0.0.16"
    }
  }
}

# https://registry.terraform.io/providers/tehcyx/kind/latest/docs
provider "kind" {
  # Configuration options
}
