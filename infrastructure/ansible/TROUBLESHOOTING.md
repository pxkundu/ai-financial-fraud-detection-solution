# Advanced Troubleshooting Guide

This guide provides detailed troubleshooting steps for advanced scenarios, cloud-specific issues, and performance optimization in the fraud detection solution.

## Table of Contents
1. [Cloud-Specific Issues](#cloud-specific-issues)
2. [Database Connectivity](#database-connectivity)
3. [Performance Optimization](#performance-optimization)
4. [Advanced Monitoring](#advanced-monitoring)
5. [Security Hardening](#security-hardening)

## Cloud-Specific Issues

### AWS/EKS Issues

#### 1. EKS Cluster Problems

Symptoms:
- Node group scaling issues
- Pod scheduling failures
- Network policy conflicts

Resolution Steps:
1. Check Cluster Health:
   ```bash
   # Verify cluster status
   aws eks describe-cluster --name {{ cluster_name }} --query "cluster.status"
   
   # Check node group health
   aws eks describe-nodegroup --cluster-name {{ cluster_name }} --nodegroup-name {{ nodegroup_name }}
   
   # Verify cluster endpoint
   aws eks describe-cluster --name {{ cluster_name }} --query "cluster.endpoint"
   ```

2. Debug Node Issues:
   ```bash
   # Check node status
   kubectl get nodes -o wide
   
   # Verify node conditions
   kubectl describe node {{ node_name }}
   
   # Check node logs
   kubectl logs -n kube-system {{ node_name }}
   ```

#### 2. AWS Service Integration

Symptoms:
- S3 access failures
- IAM role issues
- Service endpoint connectivity

Resolution Steps:
1. Verify AWS Configuration:
   ```bash
   # Check AWS credentials
   aws sts get-caller-identity
   
   # Verify IAM roles
   aws iam get-role --role-name {{ role_name }}
   
   # Test S3 access
   aws s3 ls s3://{{ bucket_name }}/
   ```

2. Debug Service Connectivity:
   ```bash
   # Check VPC endpoints
   aws ec2 describe-vpc-endpoints --vpc-id {{ vpc_id }}
   
   # Verify security groups
   aws ec2 describe-security-groups --group-ids {{ sg_id }}
   
   # Test service endpoints
   aws ec2 describe-vpc-endpoint-services
   ```

## Database Connectivity

### 1. Connection Issues

Symptoms:
- Database connection timeouts
- Authentication failures
- Query performance issues

Resolution Steps:
1. Check Database Connectivity:
   ```bash
   # Test database connection
   ansible all -m shell -a "nc -zv {{ db_host }} {{ db_port }}"
   
   # Verify database credentials
   ansible all -m shell -a "psql -h {{ db_host }} -U {{ db_user }} -d {{ db_name }} -c '\l'"
   
   # Check connection pool
   ansible all -m shell -a "netstat -an | grep {{ db_port }}"
   ```

2. Debug Query Performance:
   ```bash
   # Check slow queries
   ansible all -m shell -a "psql -h {{ db_host }} -U {{ db_user }} -d {{ db_name }} -c 'SELECT * FROM pg_stat_activity WHERE state = ''active'';'"
   
   # Analyze table statistics
   ansible all -m shell -a "psql -h {{ db_host }} -U {{ db_user }} -d {{ db_name }} -c 'ANALYZE VERBOSE;'"
   ```

### 2. Database Maintenance

Symptoms:
- High disk usage
- Slow query performance
- Connection pool exhaustion

Resolution Steps:
1. Database Health Check:
   ```bash
   # Check disk usage
   ansible all -m shell -a "df -h /var/lib/postgresql"
   
   # Verify connection limits
   ansible all -m shell -a "psql -h {{ db_host }} -U {{ db_user }} -d {{ db_name }} -c 'SHOW max_connections;'"
   
   # Check table sizes
   ansible all -m shell -a "psql -h {{ db_host }} -U {{ db_user }} -d {{ db_name }} -c '\dt+'"
   ```

## Performance Optimization

### 1. Application Performance

Symptoms:
- High response times
- Memory leaks
- CPU bottlenecks

Resolution Steps:
1. Profile Application:
   ```bash
   # Check process stats
   ansible all -m shell -a "ps aux | grep {{ app_name }}"
   
   # Monitor memory usage
   ansible all -m shell -a "pmap -x $(pgrep -f {{ app_name }})"
   
   # Analyze thread usage
   ansible all -m shell -a "pstree -p $(pgrep -f {{ app_name }})"
   ```

2. Optimize Configuration:
   ```bash
   # Check application config
   ansible all -m shell -a "cat {{ app_install_dir }}/config.yml"
   
   # Verify resource limits
   ansible all -m shell -a "systemctl show {{ app_name }} | grep -i limit"
   
   # Analyze system calls
   ansible all -m shell -a "strace -p $(pgrep -f {{ app_name }})"
   ```

### 2. System Optimization

Symptoms:
- System resource exhaustion
- I/O bottlenecks
- Network latency

Resolution Steps:
1. System Analysis:
   ```bash
   # Check system resources
   ansible all -m shell -a "vmstat 1 5 && iostat -x 1 5"
   
   # Monitor network usage
   ansible all -m shell -a "iftop -i eth0"
   
   # Analyze disk I/O
   ansible all -m shell -a "iotop -b -n 5"
   ```

2. Kernel Tuning:
   ```bash
   # Check kernel parameters
   ansible all -m shell -a "sysctl -a | grep -E 'net.core|vm.'"
   
   # Verify file descriptors
   ansible all -m shell -a "lsof -n | wc -l"
   
   # Check system limits
   ansible all -m shell -a "ulimit -a"
   ```

## Advanced Monitoring

### 1. Custom Metrics

Symptoms:
- Missing business metrics
- Incomplete monitoring coverage
- Alert configuration issues

Resolution Steps:
1. Configure Custom Metrics:
   ```bash
   # Add custom metrics to Prometheus
   ansible all -m shell -a "cat /etc/prometheus/rules/custom_metrics.yml"
   
   # Verify metric collection
   ansible all -m uri -a "url=http://localhost:9090/api/v1/query?query=up"
   
   # Check alert rules
   ansible all -m shell -a "cat /etc/prometheus/rules/alerts.yml"
   ```

2. Debug Alerting:
   ```bash
   # Check alert manager
   ansible all -m shell -a "systemctl status alertmanager"
   
   # Verify alert rules
   ansible all -m shell -a "curl -s localhost:9090/api/v1/rules"
   
   # Test alert notifications
   ansible all -m shell -a "curl -X POST http://localhost:9093/api/v1/alerts"
   ```

## Security Hardening

### 1. Compliance Checks

Symptoms:
- Security policy violations
- Compliance failures
- Audit issues

Resolution Steps:
1. Security Audit:
   ```bash
   # Run security scan
   ansible all -m shell -a "lynis audit system"
   
   # Check open ports
   ansible all -m shell -a "nmap -sT -O localhost"
   
   # Verify file permissions
   ansible all -m shell -a "find {{ app_install_dir }} -type f -ls"
   ```

2. Compliance Verification:
   ```bash
   # Check security policies
   ansible all -m shell -a "auditctl -l"
   
   # Verify system hardening
   ansible all -m shell -a "cat /etc/security/limits.conf"
   
   # Check SSL/TLS configuration
   ansible all -m shell -a "openssl s_client -connect localhost:{{ app_port }}"
   ```

### 2. Access Control

Symptoms:
- Unauthorized access attempts
- Permission issues
- Authentication failures

Resolution Steps:
1. Access Verification:
   ```bash
   # Check user permissions
   ansible all -m shell -a "getfacl -R {{ app_install_dir }}"
   
   # Verify sudo access
   ansible all -m shell -a "sudo -l -U {{ ansible_user }}"
   
   # Check authentication logs
   ansible all -m shell -a "tail -n 100 /var/log/auth.log"
   ```

2. Security Configuration:
   ```bash
   # Verify SSH configuration
   ansible all -m shell -a "sshd -T"
   
   # Check firewall rules
   ansible all -m shell -a "iptables -L -n -v"
   
   # Verify security groups
   ansible all -m shell -a "aws ec2 describe-security-groups"
   ```

## Best Practices

1. Regular Maintenance:
   - Schedule regular security updates
   - Monitor system resources
   - Review and update configurations

2. Documentation:
   - Keep troubleshooting steps updated
   - Document custom configurations
   - Maintain change logs

3. Monitoring:
   - Set up comprehensive alerts
   - Regular log analysis
   - Performance benchmarking

## Additional Resources

1. AWS Documentation:
   - [EKS Troubleshooting](https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html)
   - [CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)

2. Kubernetes Resources:
   - [Kubernetes Debugging](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-application/)
   - [EKS Best Practices](https://aws.github.io/aws-eks-best-practices/)

3. Monitoring Tools:
   - [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
   - [Grafana Guides](https://grafana.com/docs/) 