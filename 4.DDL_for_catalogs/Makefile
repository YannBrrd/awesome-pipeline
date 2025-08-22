# Makefile for DDL generation across multiple platforms
# Usage: make <target>

.PHONY: help install all bigquery databricks snowflake postgres duckdb clean

# Default contract and output paths
CONTRACT ?= ../1.Data_contract/contract.yaml
OUTPUT_DIR ?= ./output

# Colors for output
GREEN = \033[0;32m
BLUE = \033[0;34m
YELLOW = \033[1;33m
NC = \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)DDL Generation Makefile$(NC)"
	@echo ""
	@echo "$(YELLOW)Usage:$(NC)"
	@echo "  make <target> [CONTRACT=path] [OUTPUT_DIR=path]"
	@echo ""
	@echo "$(YELLOW)Targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-12s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make all                                    # Generate DDL for all platforms"
	@echo "  make bigquery                               # Generate BigQuery DDL only"
	@echo "  make all CONTRACT=../1.Data_contract/my.yaml # Use specific contract"
	@echo "  make databricks OUTPUT_DIR=./my-output      # Use specific output directory"

install: ## Install datacontract CLI
	@echo "$(BLUE)Installing datacontract CLI...$(NC)"
	pip install datacontract-cli
	@echo "$(GREEN)Installation complete!$(NC)"

check-deps: ## Check if dependencies are installed
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@which datacontract > /dev/null || (echo "$(YELLOW)datacontract CLI not found. Run 'make install' first.$(NC)" && exit 1)
	@echo "$(GREEN)Dependencies OK!$(NC)"

check-contract: ## Check if contract file exists
	@echo "$(BLUE)Checking contract file: $(CONTRACT)$(NC)"
	@test -f "$(CONTRACT)" || (echo "$(YELLOW)Contract file not found: $(CONTRACT)$(NC)" && exit 1)
	@echo "$(GREEN)Contract file found!$(NC)"

all: check-deps check-contract ## Generate DDL for all platforms
	@echo "$(BLUE)Generating DDL for all platforms...$(NC)"
	@chmod +x ./generate-all-ddl.sh
	./generate-all-ddl.sh "$(CONTRACT)" "$(OUTPUT_DIR)"

bigquery: check-deps check-contract ## Generate BigQuery DDL
	@echo "$(BLUE)Generating BigQuery DDL...$(NC)"
	@chmod +x ./generate-ddl.sh
	./generate-ddl.sh bigquery "$(CONTRACT)" "$(OUTPUT_DIR)/bigquery"

databricks: check-deps check-contract ## Generate Databricks Unity Catalog DDL
	@echo "$(BLUE)Generating Databricks DDL...$(NC)"
	@chmod +x ./generate-ddl.sh
	./generate-ddl.sh databricks "$(CONTRACT)" "$(OUTPUT_DIR)/databricks"

snowflake: check-deps check-contract ## Generate Snowflake DDL
	@echo "$(BLUE)Generating Snowflake DDL...$(NC)"
	@chmod +x ./generate-ddl.sh
	./generate-ddl.sh snowflake "$(CONTRACT)" "$(OUTPUT_DIR)/snowflake"

postgres: check-deps check-contract ## Generate PostgreSQL DDL
	@echo "$(BLUE)Generating PostgreSQL DDL...$(NC)"
	@chmod +x ./generate-ddl.sh
	./generate-ddl.sh postgres "$(CONTRACT)" "$(OUTPUT_DIR)/postgres"

duckdb: check-deps check-contract ## Generate DuckDB DDL
	@echo "$(BLUE)Generating DuckDB DDL...$(NC)"
	@chmod +x ./generate-ddl.sh
	./generate-ddl.sh duckdb "$(CONTRACT)" "$(OUTPUT_DIR)/duckdb"

clean: ## Clean generated DDL files
	@echo "$(BLUE)Cleaning generated DDL files...$(NC)"
	rm -rf ./output/
	@echo "$(GREEN)Clean complete!$(NC)"

validate: check-deps check-contract ## Validate the data contract
	@echo "$(BLUE)Validating contract: $(CONTRACT)$(NC)"
	datacontract lint "$(CONTRACT)"
	@echo "$(GREEN)Contract validation complete!$(NC)"

demo: ## Run demo with example contract
	@echo "$(BLUE)Running demo with example contract...$(NC)"
	$(MAKE) all CONTRACT=../1.Data_contract/contract.yaml OUTPUT_DIR=./demo-output
	@echo "$(GREEN)Demo complete! Check ./demo-output/$(NC)"

.DEFAULT_GOAL := help
