# Ono - Universal AI-Powered Preprocessor

*"Oh no, this is complicated... let AI figure it out."*

Ono is a universal templating preprocessor that uses AI to solve those annoying cross-platform, language-specific problems you don't want to think about. Write once, deploy anywhere, in any language.

## Why Ono?

Ever tried to write a script that needs to safely kill a process on an unknown system? Or find what's listening on a port across different Unix variants? These "simple" tasks explode into platform-specific complexity:

```bash
#!/bin/bash
port_to_free=8080

# The traditional nightmare of cross-platform compatibility
if command -v lsof >/dev/null 2>&1; then
    pid=$(lsof -ti:$port_to_free)
elif command -v netstat >/dev/null 2>&1; then
    # Different netstat flags on different systems...
    if [[ "$OSTYPE" == "darwin"* ]]; then
        pid=$(netstat -anp tcp | grep ":$port_to_free " | awk '{print $9}' | cut -d. -f1)
    else
        pid=$(netstat -tlnp | grep ":$port_to_free " | awk '{print $7}' | cut -d/ -f1)
    fi
# ... 50 more lines of platform detection
```

With Ono:

```bash
#!/bin/bash
port_to_free=8080

cleanup_result="?ono find process on port $port_to_free, attempt graceful shutdown, verify port is freed, return 'SUCCESS' only if $check_port_free($port_to_free) confirms port is available ?"

if [ "$cleanup_result" != "SUCCESS" ]; then
    force_result="?ono force kill process on $port_to_free and verify $(netstat -tuln | grep -v ":$port_to_free") shows port is free ?"
fi
```

## Real-World Use Cases

**Cross-Platform Process Management:**
```bash
# Works on Linux, macOS, BSD variants
running_services="?ono list all processes listening on network ports with process names ?"
webapp_pid="?ono find PID of process matching 'webapp' pattern using $ps_command($grep_flags) ?"
safe_kill="?ono safely terminate $webapp_pid with proper cleanup and verification ?"
```

**Docker Intelligence:**
```dockerfile
# Analyzes your codebase to make smart decisions
FROM "?ono determine optimal base image for this python flask app with minimal attack surface ?"

WORKDIR "?ono get appropriate working directory for containerized python apps ?"

# Installs only what's needed, with proper security
RUN "?ono analyze requirements.txt and generate secure apt install with caching for $package_list ?"

# Smart port selection
EXPOSE "?ono determine best port for flask app avoiding common conflicts with $existing_services ?"

HEALTHCHECK "?ono create appropriate health check for flask app at $app_endpoint ?"
```

**Database Migration Scripts:**
```sql
-- Adapts to your specific database version and setup
"?ono create table for user sessions with appropriate column types for $database_version ?";

"?ono add index on sessions table optimized for $query_patterns with proper naming for $db_engine ?";

"?ono generate migration rollback script for the above changes compatible with $migration_system ?";
```

**Microservice Orchestration:**
```yaml
# Kubernetes manifest that adapts to your environment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: "?ono generate service name from $project_config ?"-service
spec:
  replicas: "?ono determine optimal replica count for $service_load_requirements ?"
  template:
    spec:
      containers:
      - name: app
        resources:
          limits:
            memory: "?ono calculate memory limit for $app_type with $expected_traffic ?"
            cpu: "?ono determine cpu limit based on $performance_profile ?"
```

**Install Scripts:**
```bash
#!/bin/bash
# Handles every possible system configuration
package_manager="?ono detect available package manager and return command syntax ?"
dependencies="?ono install python development dependencies using $package_manager with proper error handling ?"

# Smart Python setup
python_setup="?ono configure python environment with $python_version, create venv at $venv_path($project_name), handle $path_requirements ?"
```

## Variable Substitution

Ono supports intelligent variable substitution with universal syntax:

- **Variables**: `$variable_name` → platform-appropriate variable access
- **Function calls**: `$function_name($args)` → proper calling convention  
- **Expressions**: `$(expression)` → evaluated expressions

```python
# Universal template
config_path = "?ono get config directory and create $config_file($app_name.conf) with proper $permissions(644) ?"
db_connection = "?ono establish database connection to $db_host with timeout $timeout_calc($load_factor + 30) ?"
```

**Becomes Python:**
```python
config_path = get_config_dir() + "/" + create_config_file(f"{app_name}.conf", permissions=0o644)  
db_connection = create_db_connection(db_host, timeout=timeout_calc(load_factor + 30))
```

**Becomes Bash:**
```bash
config_path=$(get_config_dir && create_config_file "${app_name}.conf" 644)
db_connection=$(establish_db_connection "$db_host" $((load_factor + 30)))
```

## Quick Start

```bash
# Install
pip install ono-preprocessor

# Set your LLM endpoint  
export ONO_API_URL="http://localhost:8000/v1"

# Process templates
ono deploy.ono.sh > deploy.sh
ono docker-compose.ono.yml > docker-compose.yml
ono migration.ono.sql > migration.sql

# Try it instantly (no install)
echo 'cleanup="?ono safely kill process on port $target_port ?"' | nc demo.onolang.com 8080
```

## Context Intelligence

Build sophisticated workflows with automatic context management:

```bash
# Analyzes your system (creates "system" context)
system_info="?ono context=system analyze this server environment and identify key services ?"

# Uses system analysis for smart decisions  
monitoring_setup="?ono context=system setup appropriate monitoring for the identified services ?"

# Forks context for specific tasks
backup_strategy="?ono context=system/backup design backup strategy for $critical_services ?"
security_audit="?ono context=system/security audit the identified services for common vulnerabilities ?"
```

## File Convention

Use `.ono.ext` naming to keep syntax highlighting and tool compatibility:

```
deploy.ono.sh           # → deploy.sh
docker-compose.ono.yml  # → docker-compose.yml  
migrate.ono.sql         # → migrate.sql
k8s-config.ono.yaml     # → k8s-config.yaml
```

## Smart Metadata

Every generated file includes build info for reproducibility:

```bash
#!/bin/bash
# ?ono
# type=meta
# build_id=20250530-143022-abc123
# source=deploy.ono.sh
# ono_version=0.1.0
# ?

cleanup_result="SUCCESS"
```

## Why "Ono"?

The name comes from **p**hp → **o**no (removing the straight lines). Just like how ono takes PHP's templating concept and makes it fluid for the AI age.

Plus, it captures that "oh no, this is complicated" moment when you realize you need AI to figure it out instead of spending hours researching platform-specific edge cases.

---

**License:** MIT  
**Docs:** [onolang.com](https://onolang.com)  
**Demo:** `nc demo.onolang.com 8080`