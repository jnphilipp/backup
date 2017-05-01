BIN_DIR=/usr/bin/
SHARE_DIR=/usr/share/psync/
BASH_COMPLETION_DIR=/etc/bash_completion.d/


install: psync psync.xsd psync.bash-completion
	apt-get install python3-gi rsync tar
	@install psync $(BIN_DIR)
	@install psync.xsd $(SHARE_DIR)
	@install psync.bash-completion $(BASH_COMPLETION_DIR)
	@echo "psync install completed."
