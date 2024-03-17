import contextvars

root_path_var = contextvars.ContextVar('root_path')
swarm_id_var = contextvars.ContextVar('swarm_id')
