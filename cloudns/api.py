import requests;

class api:
	def __init__(self, username, password):
		self._user = username;
		self._pass = password;
		
		# Currently hard-coded, but could offer XML in the future
		self._type = 'json';
		
		self._urlbase = 'https://api.cloudns.net/dns/{0}.{1}?auth-id={2}&auth-password={3}&{0}'.format('{}', self._type, self._user, self._pass);
	
	def _do_request(self, function, params=''):
		response = self._do_raw_request(function, params);
		if (self._type == 'json'):
			return response.json();
	
	def _do_raw_request(self, function, params=''):
		return requests.get(self._urlbase.format(function, params));
	
	def test_login(self):
		response = self._do_raw_request('login');
		if response.status_code == 200:
			return True;
		else:
			return False;
	
	def available_name_servers(self):
		return self._do_request('available-name-servers');
	
	def register(self, domain_name, zone_type, ns='', master_ip=''):
		params = 'domain-name={}&zone-type={}&ns={}&master-ip={}'.format(domain_name, zone_type, ns, master_ip);
		return self._do_request('register', params);
	
	def delete(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('delete', params);
	
	def list_zones(self, page=1, rows_per_page=100, search=None):
		params = 'page={}&rows-per-page={}'.format(page, rows_per_page);
		if search is not None:
			params += '&search={}'.format(search);
		return self._do_request('list-zones', params);
	
	def get_pages_count(self, rows_per_page=100, search=None):
		params = 'rows-per-page={}'.format(rows_per_page);
		if search is not None:
			params += '&search={}'.format(search);
		return self._do_request('get-pages-count', params);
	
	def get_zone_stats(self):
		return self._do_request('get-zone-stats');
	
	def get_mail_forwards_stats(self):
		return self._do_request('get-mail-forwards-stats');
	
	def get_zone_info(self, domain_name):
		return self._do_request('get-zone-info', 'domain-name={}'.format(domain_name));
	
	def update_zone(self, domain_name):
		return self._do_request('update-zone', 'domain-name={}'.format(domain_name));
	
	def update_status(self, domain_name):
		return self._do_request('update-status', 'domain-name={}'.format(domain_name));
	
	def is_updated(self, domain_name):
		return self._do_request('is-updated', 'domain-name={}'.format(domain_name));
	
	def change_status(self, domain_name, status=None):
		params = 'domain-name={}'.format(domain_name);
		if status is not None:
			params += '&status={}'.format(status);
		return self._do_request('change-status', params);
	
	def records(self, domain_name):
		return self._do_request('records', 'domain-name={}'.format(domain_name));
	
	def add_record(self, domain_name, record_type, host, record, ttl=3600,
								 priority=10, weight=100, port=None, frame=0,
								 frame_title=None, frame_keywords=None, frame_description=None,
								 save_path=0, redirect_type=302, mail='', txt='',
								 algorithm=None, fptype=None, status=1
								):
		params = 'domain-name={}&record-type={}&host={}&record={}&ttl={}&status={}'.format(domain_name, record_type, host, record, ttl, status);
		if record_type == 'MX':
			params += '&priority={}'.format(priority);
		
		if record_type == 'SRV':
			if port is None:
				raise Exception('SRV record type defined, but no port supplied');
			params += '&priority={}&weight={}&port={}'.format(priority, weight, port);
		
		if record_type == 'WR':
			if frame == 1:
				if frame_title is None:
					raise Exception('Web Redirect with Frames defined, missing meta: title');
				if frame_keywords is None:
					raise Exception('Web Redirect with Frames defined, missing meta: keywords');
				if frame_description is None:
					raise Exception('Web Redirect with Frames defined, missing meta: description');
				params += '&frame-title={}&frame_keywords={}&frame-description={}'.format(
							frame_title, frame_keywords, frame_description);
			params += '&frame={}&save-path={}&redirect-type={}'.format(frame, save_path, redirect_type);
		
		if record_type == 'RP':
			params += '&mail={}&txt={}'.format(mail, txt);
		
		if record_type == 'SSHFP':
			if algorithm is None:
				raise Exception('SSHFP record with no algorithm');
			if fptype is None:
				raise Exception('SSHFP record with no fptype');
		
		return self._do_request('add-record', params);
	
	def delete_record(self, domain_name, record_id):
		params = 'domain-name={}&record-id={}'.format(domain_name, record_id);
		return self._do_request('delete-record', params);
	
	def mod_record(self, domain_name, record_id, host, record, ttl=3600,
								 priority=None, weight=None, port=None, frame=None,
								 frame_title=None, frame_keywords=None, frame_description=None,
								 save_path=None, redirect_type=None, mail=None, txt=None,
								 algorithm=None, fptype=None
								):
		args = locals();
		params = '';
		for k, v in args.items():
			if k == 'self':
				continue;
			if v is not None:
				params += '&{}={}'.format(k, v);
		
		params = params[1:];
		return self._do_request('mod-record', params);
	
	def copy_records(self, domain_name, from_domain, delete_current_records=0):
		params = 'domain-name={}&from-domain={}&delete_current_records={}'.format(domain_name, from_domain, delete_current_records);
		return self._do_request('copy-records', params);
	
	def soa_details(self, domain_name):
		return self._do_request('soa-details', 'domain-name={}'.format(domain_name));
	
	def modify_soa(self, domain_name, primary_ns, admin_mail, refresh, retry, expire, default_ttl):
		params = 'domain-name={}&primary-ns={}&admin-mail={}&refresh={}&retry={}&expire={}&default-ttl={}'.format(
					domain_name, primary_ns, admin_mail, refresh, retry, expire, default_ttl);
		return self._do_request('modify-soa', params);
	
	def get_dynamic_url(self, domain_name, record_id):
		params = 'domain-name={}&record-id={}'.format(domain_name, record_id);
		return self._do_request('get-dynamic-url', params);
	
	def axfr_import(self, domain_name, server):
		params = 'domain-name={}&server={}'.format(domain_name, server);
		return self._do_request('axfr-import', params);
	
	def change_record_status(self, domain_name, record_id, status=None):
		params = 'domain-name={}&record-id={}'.format(domain_name, record_id);
		if status is not None:
			params += '&status={}'.format(status);
		return self._do_request('change-record-status', params);
	
			