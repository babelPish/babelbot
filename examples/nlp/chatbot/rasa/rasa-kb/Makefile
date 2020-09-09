
help:
	@echo "make"
	@echo "    ready"
	@echo "        Ready."
	@echo "    start_grakn"
	@echo "        grakn server start"
	@echo "    stop_grakn"
	@echo "        grakn server stop"
	@echo "    status_grakn"
	@echo "        grakn server status"


ready:
	cp create_schema.sh tutorial-knowledge-base
	cp load_data.sh tutorial-knowledge-base
	cp graph_database_patch.py tutorial-knowledge-base
	cp run_action_srv.sh tutorial-knowledge-base
	cp schema_new.gql tutorial-knowledge-base/knowledge_base
	cp migrate_new.py tutorial-knowledge-base/knowledge_base
	make start_grakn
	make status_grakn

start_grakn:
	grakn server start

stop_grakn:
	grakn server stop

status_grakn:
	grakn server status
