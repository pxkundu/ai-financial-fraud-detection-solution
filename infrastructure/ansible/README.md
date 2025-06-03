# Ansible Configuration for Fraud Detection Solution

This directory contains Ansible playbooks and roles for configuring and managing the infrastructure components of the fraud detection solution. The configuration integrates with Terraform for infrastructure provisioning and includes monitoring, security, and application deployment capabilities.

## Directory Structure

```
ansible/
├── playbooks/          # Ansible playbooks
│   ├── configure_nodes.yml    # Basic node configuration
│   └── deploy_app.yml         # Application deployment with Terraform integration
├── roles/             # Ansible roles
│   ├── app_deploy/    # Application deployment role
│   └── monitoring/    # Monitoring setup role
├── inventory/         # Inventory files
│   └── hosts.yml      # Dynamic inventory configuration
├── group_vars/        # Group variables
│   └── all.yml        # Common variables
└── ansible.cfg        # Ansible configuration
```

## Features Implemented

### 1. Application Deployment
- Automated application deployment with systemd service management
- Python virtual environment setup
- Health check verification
- Configurable application parameters

### 2. Monitoring Setup
- Prometheus Node Exporter installation and configuration
- Telegraf metrics collection
- Log rotation for monitoring services
- Integration with Grafana visualization

### 3. Terraform Integration
- Dynamic inventory management using Terraform outputs
- Automatic node discovery
- Endpoint configuration for monitoring services
- Seamless infrastructure-provisioning integration

## Prerequisites

1. Ansible 2.9 or later
2. SSH access to target nodes
3. AWS CLI configured with appropriate credentials
4. Python 3.x installed on target nodes
5. Terraform installed and configured

## Configuration Steps

### 1. Initial Setup

1. Install Ansible:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install ansible

   # CentOS/RHEL
   sudo yum install ansible
   ```

2. Configure SSH access:
   ```bash
   # Generate SSH key if not exists
   ssh-keygen -t rsa -b 4096

   # Copy SSH key to nodes (after Terraform deployment)
   ssh-copy-id ubuntu@<node-ip>
   ```

### 2. Terraform Integration

1. Apply Terraform configuration:
   ```bash
   cd infrastructure
   terraform init
   terraform apply
   ```

2. Export Terraform outputs:
   ```bash
   # The deploy_app.yml playbook will automatically use these outputs
   terraform output -json > terraform_output.json
   ```

### 3. Ansible Configuration

1. Set up environment variables:
   ```bash
   # These will be used by the inventory
   export EKS_NODE_1_IP=<node1_ip>
   export EKS_NODE_2_IP=<node2_ip>
   ```

2. Verify Ansible configuration:
   ```bash
   ansible all -m ping
   ```

### 4. Deployment

1. Run node configuration:
   ```bash
   ansible-playbook playbooks/configure_nodes.yml
   ```

2. Deploy application:
   ```bash
   ansible-playbook playbooks/deploy_app.yml
   ```

## Available Playbooks

### configure_nodes.yml
- Basic system configuration
- Docker setup
- Security hardening
- System package installation

### deploy_app.yml
- Application deployment
- Monitoring setup
- Health check verification
- Terraform output integration

## Role Details

### app_deploy
- Creates application directory structure
- Sets up Python virtual environment
- Configures systemd service
- Manages application files

### monitoring
- Installs monitoring agents
- Configures Prometheus Node Exporter
- Sets up Telegraf
- Manages log rotation

## Security Notes

- All sensitive variables should be stored in Ansible Vault
- SSH keys should be properly secured
- Follow the principle of least privilege when configuring services
- Regular security updates are configured
- Firewall rules are managed through group variables

## Monitoring

The solution includes:
- Prometheus Node Exporter for system metrics
- Telegraf for application metrics
- Grafana for visualization
- Log rotation for monitoring services

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Connection Issues

1. SSH Connection Failures:
   ```bash
   # Check SSH connectivity
   ssh -v ubuntu@<node-ip>
   
   # Verify SSH key permissions
   chmod 600 ~/.ssh/id_rsa
   chmod 644 ~/.ssh/id_rsa.pub
   
   # Test Ansible connectivity
   ansible all -m ping -vvv
   ```

2. Permission Denied:
   ```bash
   # Check sudo access
   ansible all -m shell -a "sudo -l" -vvv
   
   # Verify ansible_user in inventory
   ansible-inventory --list
   ```

#### 2. Application Deployment Issues

1. Service Not Starting:
   ```bash
   # Check service status
   ansible all -m shell -a "systemctl status {{ app_name }}"
   
   # View service logs
   ansible all -m shell -a "journalctl -u {{ app_name }} -n 50"
   
   # Verify Python environment
   ansible all -m shell -a "{{ app_venv_dir }}/bin/python --version"
   ```

2. Health Check Failures:
   ```bash
   # Check application logs
   ansible all -m shell -a "tail -n 100 {{ app_install_dir }}/app.log"
   
   # Verify port availability
   ansible all -m shell -a "netstat -tulpn | grep {{ app_port }}"
   
   # Test endpoint manually
   ansible all -m uri -a "url=http://localhost:{{ app_port }}/health"
   ```

#### 3. Monitoring Issues

1. Prometheus Node Exporter:
   ```bash
   # Check service status
   ansible all -m shell -a "systemctl status prometheus-node-exporter"
   
   # Verify metrics endpoint
   ansible all -m uri -a "url=http://localhost:9100/metrics"
   
   # Check configuration
   ansible all -m shell -a "cat /etc/prometheus/node_exporter.yml"
   ```

2. Telegraf Issues:
   ```bash
   # Check service status
   ansible all -m shell -a "systemctl status telegraf"
   
   # View Telegraf logs
   ansible all -m shell -a "tail -n 100 /var/log/telegraf/telegraf.log"
   
   # Verify configuration
   ansible all -m shell -a "telegraf --test"
   ```

#### 4. Terraform Integration Issues

1. Output Parsing Errors:
   ```bash
   # Verify Terraform outputs
   cd {{ terraform_dir }} && terraform output -json
   
   # Check output format
   cat terraform_output.json | jq '.'
   
   # Debug inventory generation
   ansible-inventory --list -vvv
   ```

2. Dynamic Inventory Issues:
   ```bash
   # Regenerate inventory
   ansible-playbook playbooks/deploy_app.yml --tags inventory
   
   # Verify host variables
   ansible-inventory --host <hostname> -vvv
   ```

### Specific Scenarios

#### Scenario 1: Application Deployment Failure

Symptoms:
- Service fails to start
- Health check returns 500 error
- Python dependencies missing

Resolution Steps:
1. Check application logs:
   ```bash
   ansible all -m shell -a "journalctl -u {{ app_name }} -n 100"
   ```

2. Verify Python environment:
   ```bash
   ansible all -m shell -a "{{ app_venv_dir }}/bin/pip list"
   ```

3. Reinstall dependencies:
   ```bash
   ansible-playbook playbooks/deploy_app.yml --tags dependencies
   ```

#### Scenario 2: Monitoring Data Not Showing in Grafana

Symptoms:
- Grafana dashboards empty
- Prometheus targets down
- Telegraf metrics missing

Resolution Steps:
1. Check Prometheus targets:
   ```bash
   ansible all -m uri -a "url=http://localhost:9090/api/v1/targets"
   ```

2. Verify Telegraf configuration:
   ```bash
   ansible all -m shell -a "telegraf --test --config /etc/telegraf/telegraf.conf"
   ```

3. Restart monitoring stack:
   ```bash
   ansible-playbook playbooks/deploy_app.yml --tags monitoring
   ```

#### Scenario 3: High Resource Usage

Symptoms:
- Slow application response
- High CPU/Memory usage
- Monitoring alerts

Resolution Steps:
1. Check resource usage:
   ```bash
   ansible all -m shell -a "top -b -n 1 | head -n 20"
   ```

2. Analyze application logs:
   ```bash
   ansible all -m shell -a "tail -n 1000 {{ app_install_dir }}/app.log | grep ERROR"
   ```

3. Verify monitoring metrics:
   ```bash
   ansible all -m uri -a "url=http://localhost:9100/metrics | grep process_cpu"
   ```

### General Troubleshooting Commands

1. System Health Check:
   ```bash
   # Check system resources
   ansible all -m shell -a "df -h && free -m && uptime"
   
   # Check running processes
   ansible all -m shell -a "ps aux | grep -E '{{ app_name }}|prometheus|telegraf'"
   
   # Check open ports
   ansible all -m shell -a "netstat -tulpn | grep -E '{{ app_port }}|9100|8125'"
   ```

2. Log Analysis:
   ```bash
   # Check system logs
   ansible all -m shell -a "tail -n 100 /var/log/syslog"
   
   # Check application logs
   ansible all -m shell -a "tail -n 100 {{ app_install_dir }}/app.log"
   
   # Check monitoring logs
   ansible all -m shell -a "tail -n 100 /var/log/telegraf/telegraf.log"
   ```

3. Service Management:
   ```bash
   # Restart all services
   ansible-playbook playbooks/deploy_app.yml --tags restart
   
   # Check service status
   ansible all -m shell -a "systemctl status {{ app_name }} prometheus-node-exporter telegraf"
   
   # Verify service dependencies
   ansible all -m shell -a "systemctl list-dependencies {{ app_name }}"
   ```

### Debugging Tips

1. Enable Verbose Output:
   ```bash
   # Run playbook with verbose output
   ansible-playbook playbooks/deploy_app.yml -vvv
   
   # Check specific task
   ansible-playbook playbooks/deploy_app.yml --tags <tag> -vvv
   ```

2. Test Mode:
   ```bash
   # Run in check mode
   ansible-playbook playbooks/deploy_app.yml --check
   
   # Dry run with diff
   ansible-playbook playbooks/deploy_app.yml --check --diff
   ```

3. Step-by-Step Execution:
   ```bash
   # Run with step-by-step confirmation
   ansible-playbook playbooks/deploy_app.yml --step
   ```

## Maintenance

1. Update application:
   ```bash
   ansible-playbook playbooks/deploy_app.yml --tags update
   ```

2. Update monitoring:
   ```bash
   ansible-playbook playbooks/deploy_app.yml --tags monitoring
   ```

3. Security updates:
   ```bash
   ansible-playbook playbooks/configure_nodes.yml --tags security
   ```

### Security-Related Issues

#### 1. Authentication Failures

Symptoms:
- SSH connection refused
- Permission denied errors
- Service authentication failures

Resolution Steps:
1. Check SSH Configuration:
   ```bash
   # Verify SSH daemon status
   ansible all -m shell -a "systemctl status sshd"
   
   # Check SSH configuration
   ansible all -m shell -a "cat /etc/ssh/sshd_config | grep -v '^#'"
   
   # Verify SSH key permissions
   ansible all -m shell -a "ls -la ~/.ssh/"
   ```

2. Debug Authentication:
   ```bash
   # Test SSH with verbose output
   ansible all -m shell -a "ssh -vvv localhost"
   
   # Check authentication logs
   ansible all -m shell -a "tail -n 100 /var/log/auth.log"
   
   # Verify sudo access
   ansible all -m shell -a "sudo -l -U {{ ansible_user }}"
   ```

#### 2. Security Policy Violations

Symptoms:
- SELinux/AppArmor denials
- Firewall blocking connections
- Service access restrictions

Resolution Steps:
1. Check Security Policies:
   ```bash
   # Check SELinux status
   ansible all -m shell -a "getenforce && sestatus"
   
   # Check AppArmor status
   ansible all -m shell -a "aa-status"
   
   # Verify firewall rules
   ansible all -m shell -a "iptables -L -n -v"
   ```

2. Analyze Security Logs:
   ```bash
   # Check audit logs
   ansible all -m shell -a "ausearch -m avc -ts today"
   
   # Check system logs for security events
   ansible all -m shell -a "journalctl | grep -i 'security\|permission\|denied'"
   ```

### Network Connectivity Issues

#### 1. DNS Resolution Problems

Symptoms:
- Hostname resolution failures
- Service discovery issues
- API endpoint connection failures

Resolution Steps:
1. Check DNS Configuration:
   ```bash
   # Verify DNS settings
   ansible all -m shell -a "cat /etc/resolv.conf"
   
   # Test DNS resolution
   ansible all -m shell -a "nslookup {{ app_name }}.local"
   
   # Check DNS cache
   ansible all -m shell -a "systemd-resolve --status"
   ```

2. Network Connectivity Tests:
   ```bash
   # Test basic connectivity
   ansible all -m shell -a "ping -c 4 8.8.8.8"
   
   # Check routing
   ansible all -m shell -a "traceroute {{ app_name }}.local"
   
   # Verify network interfaces
   ansible all -m shell -a "ip addr show"
   ```

#### 2. Service Connectivity

Symptoms:
- Inter-service communication failures
- Load balancer issues
- Port conflicts

Resolution Steps:
1. Check Service Connectivity:
   ```bash
   # Verify port availability
   ansible all -m shell -a "netstat -tulpn | grep -E '{{ app_port }}|9100|8125'"
   
   # Test service endpoints
   ansible all -m uri -a "url=http://localhost:{{ app_port }}/health validate_certs=no"
   
   # Check load balancer health
   ansible all -m shell -a "curl -s localhost:8080/health"
   ```

2. Network Policy Verification:
   ```bash
   # Check network policies
   ansible all -m shell -a "kubectl get networkpolicy"
   
   # Verify service mesh configuration
   ansible all -m shell -a "istioctl analyze"
   ```

### Monitoring Stack Debugging

#### 1. Prometheus Issues

Symptoms:
- Missing metrics
- Scrape failures
- High resource usage

Resolution Steps:
1. Check Prometheus Status:
   ```bash
   # Verify Prometheus service
   ansible all -m shell -a "systemctl status prometheus"
   
   # Check Prometheus targets
   ansible all -m uri -a "url=http://localhost:9090/api/v1/targets"
   
   # Analyze Prometheus logs
   ansible all -m shell -a "tail -n 100 /var/log/prometheus/prometheus.log"
   ```

2. Debug Scrape Issues:
   ```bash
   # Check scrape configuration
   ansible all -m shell -a "cat /etc/prometheus/prometheus.yml"
   
   # Test scrape endpoints
   ansible all -m uri -a "url=http://localhost:9100/metrics"
   
   # Verify scrape intervals
   ansible all -m shell -a "curl -s localhost:9090/api/v1/status/config | jq"
   ```

#### 2. Grafana Problems

Symptoms:
- Dashboard loading failures
- Data source connection issues
- Visualization errors

Resolution Steps:
1. Check Grafana Status:
   ```bash
   # Verify Grafana service
   ansible all -m shell -a "systemctl status grafana-server"
   
   # Check Grafana logs
   ansible all -m shell -a "tail -n 100 /var/log/grafana/grafana.log"
   
   # Test Grafana API
   ansible all -m uri -a "url=http://localhost:3000/api/health"
   ```

2. Debug Data Sources:
   ```bash
   # List configured data sources
   ansible all -m shell -a "curl -s -u admin:admin http://localhost:3000/api/datasources"
   
   # Test data source connections
   ansible all -m shell -a "curl -s -u admin:admin http://localhost:3000/api/datasources/proxy/1/api/v1/query?query=up"
   ```

#### 3. Telegraf Configuration

Symptoms:
- Missing metrics
- High resource usage
- Configuration errors

Resolution Steps:
1. Check Telegraf Status:
   ```bash
   # Verify Telegraf service
   ansible all -m shell -a "systemctl status telegraf"
   
   # Check Telegraf configuration
   ansible all -m shell -a "telegraf --test --config /etc/telegraf/telegraf.conf"
   
   # Analyze Telegraf logs
   ansible all -m shell -a "tail -n 100 /var/log/telegraf/telegraf.log"
   ```

2. Debug Metric Collection:
   ```bash
   # List enabled plugins
   ansible all -m shell -a "telegraf --config /etc/telegraf/telegraf.conf --input-filter cpu --test"
   
   # Check metric output
   ansible all -m shell -a "telegraf --config /etc/telegraf/telegraf.conf --test --quiet"
   
   # Verify plugin configurations
   ansible all -m shell -a "cat /etc/telegraf/telegraf.d/*.conf"
   ```

### Advanced Debugging Techniques

#### 1. Performance Profiling

1. CPU Profiling:
   ```bash
   # Check CPU usage by process
   ansible all -m shell -a "top -b -n 1 | grep -E '{{ app_name }}|prometheus|telegraf'"
   
   # Analyze CPU bottlenecks
   ansible all -m shell -a "perf top -p $(pgrep -f {{ app_name }})"
   ```

2. Memory Analysis:
   ```bash
   # Check memory usage
   ansible all -m shell -a "free -m && vmstat 1 5"
   
   # Analyze memory leaks
   ansible all -m shell -a "pmap -x $(pgrep -f {{ app_name }})"
   ```

#### 2. Log Analysis

1. Centralized Log Analysis:
   ```bash
   # Search across all logs
   ansible all -m shell -a "find /var/log -type f -exec grep -l 'ERROR' {} \\;"
   
   # Analyze log patterns
   ansible all -m shell -a "journalctl -u {{ app_name }} | grep -i error | sort | uniq -c | sort -nr"
   ```

2. Real-time Log Monitoring:
   ```bash
   # Monitor application logs
   ansible all -m shell -a "tail -f {{ app_install_dir }}/app.log | grep -i error"
   
   # Watch system logs
   ansible all -m shell -a "journalctl -f | grep -i '{{ app_name }}'"
   ``` 