resource "stratus_bucket" "customer_exports" {
  name       = "customer-exports"
  acl        = "public-read"
  versioning = false
}

resource "stratus_security_group" "staging" {
  name = "staging-api"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "stratus_database" "staging" {
  name                = "staging-db"
  publicly_accessible = true
  storage_encrypted   = false
  password            = "staging-db-2026"
}
