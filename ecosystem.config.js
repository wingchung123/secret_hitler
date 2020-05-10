module.exports = {
  apps : [{
    name: 'secret-hitler',
    script: './bin/www',
    instances: 1,
    autorestart: true,
    max_memory_restart: '500M',
    error_file: 'err.log',
	out_file: 'out.log',
	log_file: 'combined.log',
	time: true
  }]
};
