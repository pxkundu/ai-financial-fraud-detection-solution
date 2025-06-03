output "vpc_id" {
  value = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "s3_bucket_name" {
  value = module.s3.bucket_name
}

output "eks_node_ips" {
  description = "IP addresses of EKS worker nodes"
  value       = module.eks.worker_node_private_ips
}

output "prometheus_endpoint" {
  description = "Prometheus endpoint for monitoring"
  value       = module.eks.prometheus_endpoint
}

output "grafana_endpoint" {
  description = "Grafana endpoint for visualization"
  value       = module.eks.grafana_endpoint
}

output "app_endpoint" {
  description = "Application endpoint"
  value       = "http://${module.eks.worker_node_private_ips[0]}:8080"
}

output "monitoring_endpoints" {
  description = "All monitoring endpoints"
  value = {
    prometheus = module.eks.prometheus_endpoint
    grafana    = module.eks.grafana_endpoint
    node_exporter = formatlist("http://%s:9100", module.eks.worker_node_private_ips)
  }
}
