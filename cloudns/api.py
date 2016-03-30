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
		response = self._do_request('available-name-servers');
		return response;
	
	def register(self, domain_name, zone_type, ns='', master_ip=''):
		params = 'domain-name={}&zone-type={}&ns={}&master-ip={}'.format(domain_name, zone_type, ns, master_ip);
		return self._do_request('register', params);
	
	def delete(self, domain_name):
		params = 'domain-name={}'.format(domain_name);
		return self._do_request('delete', params);
	