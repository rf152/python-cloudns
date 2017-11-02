import requests

class api:
	def __init__(self, username, password):
		self._user = username;
		self._pass = password;
		
		# Currently hard-coded, but could offer XML in the future
		self._type = 'json';
		
		self._urlbase = 'https://api.cloudns.net/{0}.{1}?auth-id={2}&auth-password={3}&{0}'.format('{}', self._type, self._user, self._pass);
	
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
		return self._do_request('dns/available-name-servers');
	
	def register(self, domain_name, zone_type, ns='', master_ip=''):
		params = 'domain-name={}&zone-type={}&ns={}&master-ip={}'.format(domain_name, zone_type, ns, master_ip);
		return self._do_request('dns/register', params);
	
	def delete(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/delete', params);
	
	def list_zones(self, page=1, rows_per_page=100, search=None):
		params = 'page={}&rows-per-page={}'.format(page, rows_per_page);
		if search is not None:
			params += '&search={}'.format(search);
		return self._do_request('dns/list-zones', params);
	
	def get_pages_count(self, rows_per_page=100, search=None):
		params = 'rows-per-page={}'.format(rows_per_page);
		if search is not None:
			params += '&search={}'.format(search);
		return self._do_request('dns/get-pages-count', params);
	
	def get_zone_stats(self):
		return self._do_request('dns/get-zone-stats');
	
	def get_mail_forwards_stats(self):
		return self._do_request('dns/get-mail-forwards-stats');
	
	def get_zone_info(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/get-zone-info', params);
	
	def update_zone(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/update-zone', params);
	
	def update_status(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/update-status', params);
	
	def is_updated(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/is-updated', params);
	
	def change_status(self, domain_name, status=None):
		params = 'domain-name={}'.format(domain_name);
		if status is not None:
			params += '&status={}'.format(status);
		return self._do_request('dns/change-status', params);
	
	def records(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/records', params);
	
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
		
		return self._do_request('dns/add-record', params);
	
	def delete_record(self, domain_name, record_id):
		params = 'domain-name={}&record-id={}'.format(domain_name, record_id);
		return self._do_request('dns/delete-record', params);
	
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
				params += '&{}={}'.format(k.replace('_', '-'), v);
		
		params = params[1:];
		return self._do_request('dns/mod-record', params);
	
	def copy_records(self, domain_name, from_domain, delete_current_records=0):
		params = 'domain-name={}&from-domain={}&delete_current_records={}'.format(domain_name, from_domain, delete_current_records);
		return self._do_request('dns/copy-records', params);
	
	def soa_details(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/soa-details', params);
	
	def modify_soa(self, domain_name, primary_ns, admin_mail, refresh, retry, expire, default_ttl):
		params = 'domain-name={}&primary-ns={}&admin-mail={}&refresh={}&retry={}&expire={}&default-ttl={}'.format(
					domain_name, primary_ns, admin_mail, refresh, retry, expire, default_ttl);
		return self._do_request('dns/modify-soa', params);
	
	def get_dynamic_url(self, domain_name, record_id):
		params = 'domain-name={}&record-id={}'.format(domain_name, record_id);
		return self._do_request('dns/get-dynamic-url', params);
	
	def axfr_import(self, domain_name, server):
		params = 'domain-name={}&server={}'.format(domain_name, server);
		return self._do_request('dns/axfr-import', params);
	
	def change_record_status(self, domain_name, record_id, status=None):
		params = 'domain-name={}&record-id={}'.format(domain_name, record_id);
		if status is not None:
			params += '&status={}'.format(status);
		return self._do_request('dns/change-record-status', params);

	def add_master_server(self, domain_name, master_ip):
		params = 'domain-name={}&master-ip={}'.format(domain_name, master_ip);
		return self._do_request('dns/add-master-server', params);

	def delete_master_server(self, domain_name, master_id):
		params = 'domain-name={}&master-id={}'.format(domain_name, master_id);
		return self._do_request('dns/delete-master-server', params);

	def master_servers(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/master-servers', params);

	def add_mail_forward(self, domain_name, box, host, destination):
		params = 'domain-name={}&box={}&host={}&destination={}'.format(domain_name, box, host, destination);
		return self._do_request('dns/add-mail-forward', params);

	def delete_mail_forward(self, domain_name, mail_forward_id):
		params = 'domain-name={}&mail-forward-id={}';
		return self._do_request('dns/delete-mail-forward', params);

	def modify_mail_forward(self, domain_name, box, host, destination, mail_forward_id):
		params = 'domain-name={}&box={}&host={}&destination={}&mail-forward-id={}'.format(domain_name, box, host, destination, mail_forward_id);
		return self._do_request('dns/modify-mail-forward', params);

	def mail_forwards(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/mail-forwards', params);

	def add_cloud_domain(self, domain_name, cloud_domain_name):
		params = 'domain-name={}&cloud-domain-name={}'.format(domain_name, cloud_domain_name);
		return self._do_request('dns/add-cloud-domain', params);

	def delete_cloud_domain(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/delete-cloud-domain', params);

	def set_master_cloud_domain(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/set-master-cloud-domain', params);

	def list_cloud_domains(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/list-cloud-domains', params);

	def axfr_add(self, domain_name, ip):
		params = 'domain-name={}&ip={}'.format(domain_name, ip);
		return self._do_request('dns/axfr-add', params);
	
	def axfr_remove(self, domain_name, axfr_id):
		params = 'domain-name={}&id={}'.format(domain_name, axfr_id);
		return self._do_request('dns/axfr-remove', params);

	def axfr_list(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/axfr-list', params);

	def statistics_hourly(self, domain_name, year, month, day):
		params = 'domain-name={}&year={}&month={}&day={}'.format(domain_name, year, month, day);
		return self._do_request('dns/statistics-hourly', params);

	def statistics_daily(self, domain_name, year, month):
		params = 'domain-name={}&year={}&month={}'.format(domain_name, year, month);
		return self._do_request('dns/statistics-daily', params);

	def statistics_monthly(self, domain_name, year):
		params = 'domain-name={}&year={}'.format(domain_name, year);
		return self._do_request('dns/statistics-daily', params);

	def statistics_yearly(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/statistics-daily', params);

	def statistics_last_30_days(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/statistics-last-30-days', params);

	def get_parked_templates(self):
		return self._do_request('dns/get-parked-templates');

	def get_parked_settings(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('dns/get-parked-settings');

	def set_parked_settings(self, domain_name, template, title=None, description=None, keywords=None, contact_form=0):
		args = locals();
		params = '';
		for k, v in args.items():
			if k == 'self':
				continue;
			if v is not None:
				params += '&{}={}'.format(k, v);

		params = params[1:];
		return self._do_request('dns/set-parked-settings', params);
