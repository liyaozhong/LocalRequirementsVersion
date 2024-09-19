import os
import sys
import platform
import argparse
from pathlib import Path
import pkg_resources
from pkg_resources import get_distribution, DistributionNotFound
from packaging import requirements, version

try:
    from packaging.requirements import InvalidRequirement
except ImportError:
    from pkg_resources._vendor.packaging.requirements import InvalidRequirement

def print_environment_info():
    print(f"Python version: {platform.python_version()}")
    print(f"Python executable: {sys.executable}")
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Platform: {platform.platform()}")
    print(f"Working directory: {os.getcwd()}")
    print("\n")

def parse_requirement(req_str):
    # Split the requirement string into the package specification and any additional flags
    parts = req_str.split()
    package_spec = parts[0]
    flags = ' '.join(parts[1:]) if len(parts) > 1 else ''
    
    # Parse the package specification
    req = requirements.Requirement(package_spec)
    
    return req, flags

def check_compatibility(requirements_list):
    incompatibilities = []
    installed_packages = {pkg.key: pkg for pkg in pkg_resources.working_set}

    for req_str in requirements_list:
        try:
            req, flags = parse_requirement(req_str)
            if req.name in installed_packages:
                installed_version = installed_packages[req.name].version
                if not req.specifier.contains(installed_version):
                    incompatibilities.append(f"{req.name} {installed_version} does not satisfy {req}")
        except Exception as e:
            print(f"Error processing requirement {req_str}: {str(e)}")

    return incompatibilities

def update_requirements(project_path):
    req_file = Path(project_path) / 'requirements.txt'
    
    if not req_file.exists():
        print(f"requirements.txt file not found in {project_path}")
        return
    
    with open(req_file, 'r') as f:
        requirements = f.readlines()
    
    updated_requirements = []
    for req in requirements:
        req = req.strip()
        if req and not req.startswith('#'):
            try:
                package_spec, flags = parse_requirement(req)
                package = package_spec.name
                try:
                    version = get_distribution(package).version
                    updated_req = f"{package}=={version}"
                    if flags:
                        updated_req += ' ' + flags
                    updated_requirements.append(updated_req + '\n')
                except DistributionNotFound:
                    print(f"Package {package} not found, keeping as is")
                    updated_requirements.append(req + '\n')
            except Exception as e:
                print(f"Error processing {req}: {str(e)}")
                updated_requirements.append(req + '\n')
        else:
            updated_requirements.append(req + '\n')
    
    # Sort the requirements alphabetically
    sorted_requirements = sorted(updated_requirements, key=lambda x: x.lower())

    with open(req_file, 'w') as f:
        f.writelines(sorted_requirements)
    
    print(f"Updated and sorted {req_file}")
    
    # Check compatibility
    incompatibilities = check_compatibility([req.strip() for req in updated_requirements if req.strip() and not req.startswith('#')])
    if incompatibilities:
        print("\nWarning: The following incompatibilities were found:")
        for incompatibility in incompatibilities:
            print(f"  - {incompatibility}")
    else:
        print("\nAll dependencies are compatible.")

def main():
    parser = argparse.ArgumentParser(description="Update requirements.txt with installed package versions.")
    parser.add_argument('project_path', nargs='?', default=os.getcwd(),
                        help="Path to the project directory containing requirements.txt (default: current directory)")
    args = parser.parse_args()
    
    print_environment_info()
    update_requirements(args.project_path)

if __name__ == "__main__":
    sys.exit(main())