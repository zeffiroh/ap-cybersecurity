resource "stratus_bucket" "invoices" {
  name       = "monsoon-invoices"
  acl        = "public-read"
  versioning = false
}

resource "stratus_security_group" "bastion" {
  name = "bastion-ssh"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "stratus_db_instance" "orders" {
  identifier          = "orders-db"
  engine              = "postgres"
  publicly_accessible = true
  storage_encrypted   = false
  username            = "orders_admin"
  password            = var.db_password
}
