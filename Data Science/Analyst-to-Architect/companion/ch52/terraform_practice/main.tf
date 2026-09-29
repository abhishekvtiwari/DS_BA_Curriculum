# Practice for reading a plan (Chapter 52, section 52.4). terraform_data is built into Terraform,
# so this needs no provider download and no cloud account. Each resource stands in for a firewall rule.
# Run terraform init, then terraform apply; then delete the second block and run terraform plan.
# Riverstone Supplies is fictional; every name and number is invented.

resource "terraform_data" "rule_https_from_internet" {
  input = "allow 443 from 0.0.0.0/0 to the load balancer"
}

resource "terraform_data" "rule_pipeline_to_database" {
  input = "allow 5432 from the pipeline to the database"
}
